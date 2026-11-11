# Đánh giá đầu vào: 120 phút

Mục đích: phân bổ 112 giờ học theo [kế hoạch](vinfast-8-week-plan.md), không đánh
đồng số năm kinh nghiệm với mức thành thạo từng công nghệ. Chưa có điểm cho đến
khi có bài làm. Không cần cài cả stack để làm assessment.

## Cách làm

105 phút đầu tự làm, không dùng AI; được tra tài liệu chính thức nhưng ghi nguồn.
Có thể dùng editor, SQL dialect quen thuộc, Python standard library; ghi rõ phần
chưa chạy. Không trừ điểm chỉ vì chưa nhớ cú pháp ClickHouse nếu lập luận đúng.
15 phút cuối dùng tutor/reviewer hoặc tự review, ghi riêng sửa đổi sau hỗ trợ.
Điểm baseline lấy từ bài độc lập; ghi điểm sau hỗ trợ ở cột riêng.

Lưu bài làm tại `docs/learning/evidence/baseline.md`, code nếu có tại thư mục bài
tập tương ứng. Các đường dẫn này là đầu ra sẽ tạo khi học, chưa có sẵn. Không
commit thông tin công ty hoặc dữ liệu thật. Trả lời ngắn nhưng có ví dụ/test.

## A. SQL và grain — 20 phút

Fixture telemetry (tất cả timestamp UTC, cùng ngày):

| event_id | vehicle_id | event_time | ingested_at | version | distance_delta_km |
|---|---|---|---|---:|---:|
| e1 | v1 | 10:00 | 10:01 | 1 | 10 |
| e1 | v1 | 10:00 | 10:01 | 1 | 10 |
| e1 | v1 | 10:00 | 10:07 | 2 | 12 |
| e2 | v1 | 09:55 | 10:08 | 1 | 3 |
| e3 | v2 | 10:00 | 10:02 | 1 | 4 |

1. Viết SQL lấy một version hợp lệ mới nhất mỗi event rồi tính quãng đường theo
   xe/ngày. Nêu grain đầu vào/đầu ra và kết quả dự kiến trên fixture.
2. Nếu lần trước đã xử lý đến `event_time=10:00`, incremental lần sau cần làm gì
   để không bỏ e2 và bản cập nhật e1? Nêu một test đối chiếu với full rebuild.
3. Bổ sung SCD2 cho dealer của xe: v1 thuộc A trước 10:00, thuộc B từ 10:00.
   Join event đúng lịch sử thế nào? Nếu hai khoảng SCD chồng nhau thì bắt lỗi ở đâu?

## B. Python engineering — 20 phút

Viết hàm có type hints `normalize_events(lines)` nhận một iterable các chuỗi JSON
và trả về bản ghi hợp lệ cùng bản ghi bị quarantine. Mỗi event phải có `event_id`,
`vehicle_id`, timestamp ISO-8601 có timezone, integer version dương và distance
không âm. Thử thêm JSON hỏng, thiếu key và timestamp thiếu timezone.

Tự chọn interface, giải thích trade-off; viết ít nhất hai test meaningful. Nêu
cách tránh giữ toàn bộ file lớn trong RAM, tách I/O khỏi transform và đóng gói
để Airflow/Spark tái sử dụng. Không cần hoàn thành package trong 20 phút; phần
chưa triển khai ghi rõ thay vì coi pseudo-code đã chạy.

## C. ClickHouse và dbt — 20 phút

Telemetry có bản ghi cập nhật, truy vấn chủ yếu theo khoảng ngày và xe. Hệ thống
có hai shard, producer có thể gửi lại cùng event.

1. Đề xuất table engine, sorting key, partition key, shard key và lý do. Khi
   version mới tới, field nào của khóa bắt buộc ổn định?
2. Nếu hai version của cùng event rơi vào hai shard, query nào có thể trả sai?
   Background merge và `FINAL` giải quyết được gì, không giải quyết được gì?
3. Thiết kế dbt incremental + tests. Điều gì cần xác minh ở adapter/version
   trước khi chọn strategy? Làm sao chứng minh rerun không nhân đôi metric?

## D. Airflow và Spark — 15 phút

DAG đọc S3, Spark transform, load ClickHouse, chạy dbt. Task bị kill sau khi đã
ghi nửa batch nhưng chưa lưu checkpoint; scheduler retry. Một số object đến muộn.

Vẽ hoặc mô tả ranh giới task và protocol commit/checkpoint. Chỉ ra idempotency key,
cách chọn input theo data interval, backfill không trùng và xử lý partial write.
Nêu việc không được làm ở parse time. Nếu một dealer chiếm 60% dữ liệu join,
chẩn đoán Spark skew bằng evidence nào và chọn cách xử lý ra sao?

## E. Unstructured — 15 phút

Bucket chứa log, PDF, ảnh, audio và video; một số file hỏng, một số được thay nội
dung ở cùng object key. Thiết kế metadata contract và đường đi từ object tới
bảng query được: định danh/version/checksum, extractor version, attributes,
quarantine, retry và lineage. Phân biệt metadata extraction với content extraction.

Đưa một ví dụ query nghiệp vụ trên kết quả trích xuất. Nêu cách tránh đọc file
không giới hạn kích thước, tái xử lý khi parser đổi và tránh đưa dữ liệu cá nhân
vào log. Nếu chưa có kinh nghiệm một modality, ghi rõ mức độ đã làm.

## F. Platform, privacy và giao tiếp — 15 phút

Một yêu cầu xóa dữ liệu của khách hàng giả lập phải đi qua S3 versioned objects,
ClickHouse raw/staging/mart, extracted text và backup. Đề xuất inventory, quyền
truy cập, trình tự xóa, bằng chứng hoàn tất và cách tránh hồi sinh dữ liệu khi restore.

Tiếp theo, mart chậm 45 phút trong khi yêu cầu freshness là 30 phút: mô tả triage,
owner, kiểm tra upstream, khôi phục và rollback an toàn. Kết thúc bằng 5–7 câu
tiếng Anh: impact, evidence, mitigation, unknowns và follow-up.

## Review — 15 phút

Chọn hai giả định dễ sai nhất, tự tìm counterexample hoặc nhờ Codex phản biện.
Ghi câu trả lời ban đầu và phần thay đổi. Không sửa lại baseline để che việc có
hỗ trợ. Không cần hỏi tutor thêm một bộ câu hỏi khác trước khi bắt đầu học.

## Rubric

Chấm từng nhóm A–F từ 0 đến 4, tối đa 24. Chỉ dùng evidence đã viết/chạy, không
chấm dựa trên sự tự tin. Nếu không đủ evidence, đánh dấu “chưa đánh giá” và dành
tối đa 30 phút trong phần review tuần 1 để hoàn tất.

| Điểm | Evidence |
|---:|---|
| 0 | Chưa đưa được hướng xử lý hoặc có lỗi nền tảng chưa nhận ra |
| 1 | Nhận diện khái niệm nhưng chưa giải được tình huống/counterexample |
| 2 | Giải đúng happy path và nêu được ít nhất một rủi ro; còn thiếu cách kiểm chứng/recovery |
| 3 | Xử lý được edge cases, đưa test hoặc protocol kiểm chứng cụ thể và trade-off hợp lý |
| 4 | Đạt mức 3, có evidence chạy thử hoặc trace từng bước chứng minh tình huống hỏng; giải thích giới hạn và phương án thay thế |

| Nhóm | Điểm độc lập | Sau hỗ trợ | Evidence / lỗ hổng | Điều chỉnh giờ |
|---|---|---|---|---|
| A — SQL/grain | Chưa đánh giá | — | — | — |
| B — Python | Chưa đánh giá | — | — | — |
| C — ClickHouse/dbt | Chưa đánh giá | — | — | — |
| D — Airflow/Spark | Chưa đánh giá | — | — | — |
| E — Unstructured | Chưa đánh giá | — | — | — |
| F — Platform/privacy/English | Chưa đánh giá | — | — | — |

0–1: ưu tiên thời gian sửa nền; 2: làm lab có hướng dẫn rồi thử độc lập; 3–4:
giữ cửa kiểm tra, chuyển bớt giờ lý thuyết sang phần yếu. Không dùng tổng điểm
để che một nhóm yếu. Tuần 8 dùng fixture/tình huống mới cùng rubric, kèm demo
capstone; ghi riêng chất lượng English thay vì để nó che lỗi kỹ thuật.
