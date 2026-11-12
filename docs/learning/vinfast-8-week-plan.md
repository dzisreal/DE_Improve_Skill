# Lộ trình 8 tuần theo JD Data Engineer VinFast

## Mục tiêu và giới hạn

Kế hoạch được chốt cho **8 tuần × 7 ngày × 2 giờ = 112 giờ**, chưa có lịch phỏng
vấn. Mục tiêu là tạo bằng chứng thực hành đủ sát JD để ứng tuyển, đồng thời luyện
cách ra quyết định của Senior DE và Data Architect. Hoàn thành lộ trình không tự
động chứng minh seniority hoặc kinh nghiệm production ở một stack mới.

Đầu vào: khoảng 4 năm DE, kinh nghiệm Spark/SQL và AWS, phụ trách vận hành toàn bộ
IBM Cloud Pak for Data. Máy học chính: Mac mini M1, RAM 16 GB, SSD 256 GB; cloud
tối đa 30 USD/tháng, AI tính riêng. Chỉ sử dụng dữ liệu giả lập, không đưa CV,
dữ liệu ngân hàng, thông tin nội bộ hoặc credential vào repo.

**Một dự án xuyên suốt:** nền tảng telemetry và after-sales giả lập, từ object
storage qua raw → staging → mart, có nhánh dữ liệu phi cấu trúc. Các tính năng
được thêm mỗi tuần, không đợi tuần cuối mới tích hợp.

## Ưu tiên sau bài đánh giá

Lộ trình đã điều chỉnh theo câu trả lời đầu vào. Bài trả lời mới thể hiện lập
luận, chưa có code hoặc kết quả thực thi để xác nhận năng lực hands-on. Không
cần làm lại assessment trước khi học; 112 giờ dưới đây là thời gian học tiếp
theo. Không suy điểm từ CV hay số năm kinh nghiệm.

Ba vấn đề cần sửa trước khi tăng độ phức tạp: event time khác ingestion time;
job báo failed không bảo đảm mọi sink đã rollback; soft delete không đồng nghĩa
với erasure. Tuần 1 dùng bài nhỏ để hiểu cơ chế, tuần 2 trở đi kiểm chứng trên
stack mục tiêu. [Hướng dẫn tuần 1](week-01-foundations.md) có từng buổi và fixture.

| Năng lực | Evidence đầu vào | Ưu tiên và bằng chứng cần bổ sung |
|---|---|---|
| SQL/modelling | Nhận diện version/SCD; còn nhầm lựa chọn version, watermark và biên thời gian | P0: grain, window, late corrections và SCD2 non-overlap |
| Python engineering | Biết JSON/exception; chưa có evidence streaming, packaging và tests | P0: validation/quarantine, generators, tách I/O, type hints, tests |
| Spark | Chưa phân biệt job status với dữ liệu đã commit ở sink; skew chưa có evidence | P0: write semantics theo sink, retry/replay, partial write và shuffle/skew |
| ClickHouse nhiều shard | Chưa từng thiết kế/tối ưu storage; chưa đánh giá thực hành | P0: học từ một node, rồi engines, ORDER BY, partition/shard key và distributed joins |
| dbt | Chưa được kiểm chứng thực hành | P0: models, adapter/version, incremental, tests và artifacts |
| Airflow | Mức độ tự thiết kế/vận hành cần kiểm chứng | P1: parse time, data interval, retries, idempotency, backfill |
| Unstructured | Đã nghĩ đến text cleaning và lưu object path; thiếu extraction contracts | P0: extraction, quarantine, source/extractor version và lineage |
| Privacy/erasure | Nhận diện batch propagation; còn nhầm soft delete và S3 versioning | P0: access filtering, xóa xuyên các lớp, retention và restore safeguards |
| Platform reliability | Phụ trách vận hành toàn bộ CP4D | P1: chuyển thành SLO, incident evidence, runbooks và recovery của stack mới |
| AWS S3/IAM | Có kinh nghiệm AWS | P1: xác minh least privilege, versioned objects, secrets và chi phí |
| Architecture/English/AI review | Cần bài làm và tình huống cụ thể | Xuyên suốt: ADR, PR và giải thích trade-off bằng evidence |

P0 = phải luyện và demo; P1 = kiểm chứng rồi bổ sung. Không bỏ phần SQL/Python/
Spark chỉ vì đã dùng trong công việc. Kubernetes/EKS, GitOps, OCR/ASR nâng cao,
embeddings/vector search và replication 2×2 là mở rộng sau các cửa bắt buộc.

## Cách học và cách điều chỉnh

- Giữ [assessment và rubric](vinfast-baseline-assessment.md) làm mốc so sánh.
  Ngày 1 bắt đầu thực hành SQL. Phần ClickHouse chưa trả lời được giữ trạng thái
  chưa đánh giá, không tự đổi thành điểm 0.
- Một buổi 120 phút: 20 phút đọc/ôn, 70 phút tự làm, 20 phút kiểm chứng/giải
  thích, 10 phút learning log tiếng Anh. Ngày review có lịch riêng ở tuần 1.
- Mỗi tuần 12 giờ nội dung và 2 giờ review/bù lỗi. Không cộng thêm thời gian
  ngoài lịch để hoàn tất bài mở rộng; mỗi tuần chọn một ADR ngắn và một PR có
  evidence. Nội dung PR nhỏ có thể chia tiếp, không ép một tuần đúng một PR.
- Dùng Codex sau khi tự thử: yêu cầu gợi ý từng tầng, counterexample hoặc review
  diff. Không lấy code AI đã chạy thay cho khả năng tự giải thích/sửa lỗi.
- Chỉ chuyển giờ từ phần đã vững khi có demo độc lập đạt rubric 3–4/4; chuyển tối
  đa 4 giờ giữa các nhóm, giữ cửa nghiệm thu và tổng 112 giờ.

## Lịch theo tuần

| Tuần | Nội dung, phân bổ đúng 14 giờ | Đầu ra và cửa kiểm tra |
|---|---|---|
| 1 — SQL/Python và correctness | Grain/version 2h; incremental/late data 2h; SCD2 2h; Python validation 2h; streaming/I/O 2h; write/retry simulation 2h; review 2h | SQLite/Python local: đúng version, incremental khớp full rebuild, SCD đúng boundary; parser có quarantine; giải thích tác động còn lại sau failed write. Xem từng buổi trong tài liệu tuần 1. |
| 2 — Ingestion và ClickHouse một node | Object storage/contracts 2h; typed Python package + tests 4h; ClickHouse một node + raw/staging/mart 4h; config/CI cơ bản 2h; review 2h | Một batch chạy hết luồng; raw có provenance, manifest và replay test. Pin versions, tách config khỏi code, CI chạy test nhỏ; có hướng dẫn Linux/macOS. |
| 3 — ClickHouse nhiều shard | Engines/keys/EXPLAIN 3h; lab 2 shard 1 replica 4h; duplicates/late versions/distributed joins 3h; benchmark + ADR 2h; review 2h | Fixture đúng trên 1 và 2 shard; retry không làm KPI tăng; merge local không dedup toàn cụm. Thử mất shard, ghi hành vi thiếu/lỗi và cách phục hồi; đo read rows/query plan. |
| 4 — dbt và modelling | Chuyển staging/marts sang dbt 3h; facts + SCD2 + incremental 5h; tests/docs/reconciliation 3h; review SQL do AI viết 1h; review 2h | Fact grain rõ, SCD2 không overlap; full rebuild khớp incremental/replay/backfill. dbt build/docs chạy với adapter đã pin; lưu artifacts cho catalog. |
| 5 — Airflow + Spark | DAG/retry/data interval 3h; Spark dedup/window/joins 4h; tích hợp ingestion → Spark → dbt 3h; failure/replay drill 2h; review 2h | DAG không làm việc nặng lúc parse; kill sau partial write ở sink thực rồi retry vẫn đúng. Spark UI/plan chỉ ra skew; backfill không phá partition khác. |
| 6 — Unstructured | Contract + manifest + versioning 2h; parse logs/text/PDF 4h; image/audio/video metadata 2h; quarantine/reprocess/tests 2h; mart + lineage mapping 2h; review 2h | Text/PDF thành nội dung query được, media có metadata thật; mỗi modality có valid/corrupt fixtures. Source/extractor version truy vết được; rerun không tạo duplicate logical output. |
| 7 — Governance và vận hành | OpenMetadata ingestion + lineage 4h; classification/IAM/secrets 2h; erasure/restore drill 3h; DQ/SLO/runbooks 3h; review 2h | Catalog có owner và lineage từ artifacts trước; analyst bị deny dữ liệu restricted. Kiểm chứng soft delete, erasure và restore safeguard khác nhau; bad data kích hoạt check/alert. |
| 8 — Promotion, demo và đánh giá cuối | Promotion/schema rollback 3h; nghiệm thu/fresh checkout 3h; demo + architecture review 2h; mock SQL/Python/system design 3h; portfolio/English 1h; tổng kết 2h | Dùng config/CI từ tuần 2 để promote có approval và rollback. Demo 15 phút, rubric cuối với bài mới, evidence matrix và giới hạn kiểm chứng; ghi rõ mục chưa đạt. |

### Mốc ra quyết định

- Cuối tuần 1: tự giải thích/sửa ba lỗi SQL về version/watermark/SCD; parser
  phân biệt lỗi JSON với lỗi contract. Dùng buổi review sửa phần chưa đạt.
- Cuối tuần 2: cùng batch chạy lại không làm tăng metric sai. Nếu chưa đạt,
  dùng buổi review đầu tuần 3 cho replay trước khi thêm shard.
- Cuối tuần 4: có đối chiếu full/incremental/backfill và tests SCD2; sửa lỗi
  correctness trước khi orchestration tự động hóa chúng.
- Cuối tuần 8: đánh dấu từng AC trong capstone bằng link evidence. Nếu còn thiếu
  cửa bắt buộc sau khi dùng dự phòng, ghi chưa đạt và bổ sung vòng học 2–4 tuần
  theo nhóm yếu; không nới giờ/ngày hoặc tự hạ tiêu chí để coi là hoàn thành.

Từ tuần 2: ngày 1–2 hiểu vấn đề/thiết kế, ngày 3–4 xây luồng chính, ngày 5 tạo
lỗi/đối chiếu, ngày 6 tài liệu/PR/demo, ngày 7 review. Đây là nhịp tham khảo;
bảng giờ của từng tuần là ngân sách chính, không cộng thêm một lịch học thứ hai.

## Môi trường và ngân sách

Thiết kế lab local-first; đây là kế hoạch setup, **chưa có Compose stack hoặc
lab stack trong PR tài liệu này**. Tuần 1 chỉ cần Python/SQLite theo bài học;
tuần 2 bắt đầu object storage/ClickHouse và hướng dẫn setup Linux/macOS.
Hướng dẫn [cài skills](../installation.md) đã có riêng.

| Profile dự kiến | Thành phần | Cách dùng trên M1 16 GB |
|---|---|---|
| Core | S3-compatible storage local, ClickHouse 1 node, Python/dbt CLI | Luồng nhỏ và unit/integration tests hằng ngày |
| Distributed | Object storage + ClickHouse 2 shard × 1 replica | Dừng Airflow/catalog; kiểm tra sharding và cross-shard queries |
| Pipeline | Airflow + metadata DB, Spark local, ClickHouse | Giảm dataset/worker; bật Spark theo job; không chạy catalog cùng lúc |
| Governance | OpenMetadata + dependencies tương thích bản pin | Dừng Airflow/Spark; dùng dbt artifacts, reconnect ClickHouse khi ingestion cần |
| Replication, mở rộng | 2 shard × 2 replica + Keeper | Chỉ làm nếu đủ RAM/giờ hoặc thuê máy theo phiên; không phải điều kiện để hoàn thành lab 2×1 |

Khởi đầu giới hạn Docker VM khoảng 8 GB RAM và dữ liệu lab khoảng 10 GB; đây là
ngân sách thử nghiệm, chưa phải cấu hình đã benchmark. Kiểm tra dung lượng trống,
swap và OOM trước khi tăng dữ liệu. Nếu catalog vượt ngân sách thì chạy phiên
cloud riêng; vẫn cần thực hiện ingestion, không coi sơ đồ lineage là catalog chạy thật.
Không chạy toàn bộ stack thường trực. Cleanup chỉ xóa tài nguyên của lab sau khi
lưu evidence; không dùng lệnh prune toàn máy có thể xóa tài nguyên project khác.

Chọn một Airflow major version, một bộ dbt Core/adapter tương thích, ClickHouse,
Spark/Java và catalog khi bắt đầu từng thành phần, từ tuần 2; khóa version/image
digest trong repo. Kiểm tra image ARM64 trên macOS và kiến trúc máy Linux.
Nếu dùng emulation thì ghi rõ,
không dùng số đo đó làm kết luận hiệu năng production. Tách virtual environments
hoặc containers khi dependencies xung đột; không lấy `latest` làm cấu hình tái tạo.

**Trần chi tiêu thực tế là 30 USD cho mỗi tháng lịch:**

| Hạng mục | Hạn mức nội bộ/tháng |
|---|---:|
| Compute theo phiên khi lab local không đủ | 18 USD |
| S3, requests, volume, network và phần phụ trợ | 5 USD |
| Dự phòng thuế, sai số và chi phí còn treo | 7 USD |

Đây là phân bổ ngân sách, không phải báo giá AWS. Trước mỗi phiên, tính giá vùng,
giờ máy, volume, IPv4 và egress; chỉ chạy nếu tổng dự kiến còn trong hạn mức.
Đặt cảnh báo 10/20/25 USD, ngừng tạo tài nguyên khi dự báo tổng vượt 25 USD để giữ
dự phòng. Billing alerts có độ trễ và **không phải hard cap**. Gắn owner/TTL,
tự tắt compute theo phiên, dọn volume/IP/snapshot/bucket versions không cần dùng,
kiểm tra bill tuần hai lần. Không dựng EKS/NAT gateway hay cluster luôn bật.
Kiểm tra IAM với S3 thật bằng dữ liệu nhỏ; S3-compatible local không chứng minh
AWS IAM. Không phụ thuộc free tier để cam kết chi phí. AI có ledger riêng.

## Dùng bộ Codex skills hiện có

Không cần thêm skill ở giai đoạn này. Chất lượng câu trả lời cần được kiểm chứng
bằng docs, tests và kết quả lab; số sao của repo nguồn không chứng minh chất lượng DE.

| Skill | Thời điểm và nhiệm vụ cụ thể |
|---|---|
| `socratic-tutor` | Hỏi từng câu theo rubric đầu vào; gợi ý theo tầng, chưa đưa lời giải trước khi tự thử; ôn cách quãng sau 1/3/7 ngày |
| `data-architect` | Tuần 2/3/7/8: phản biện requirements, sharding, SCD, privacy, recovery và chi phí; yêu cầu nêu giả định |
| `data-review` | Tuần 1/3/4/6: review grain, SQL, incremental, schema contracts, cross-shard correctness; yêu cầu counterexample |
| `requesting-code-review` | Khi có diff Python/DAG/CI: review theo acceptance criteria, bằng chứng test và lỗi có thể tái hiện |
| `data-platform-reliability-reviewer` | Tuần 1/5/7/8: phân tích crash points, retry, partial write, replay/backfill, alert và runbook |

Prompt mẫu: “Dùng $data-review review diff hiện tại theo tiêu chí tuần 4 trong
docs/learning/vinfast-8-week-plan.md. Với mỗi lỗi, chỉ ra fixture tái hiện và tác
động tới metric. Phân biệt kết quả đã chạy với suy luận; không tự sửa trước khi
tôi giải thích nguyên nhân.”

Ghi learning log gồm: tự làm được gì; AI đã giúp gì; nhận định AI nào bị bác bỏ;
test/nguồn dùng để kiểm tra. Mỗi tuần phải có một phần tự giải thích hoặc sửa lỗi
không dùng AI. Mỗi PR mô tả bằng tiếng Anh để luyện yêu cầu written English.

## Tiêu chí kết thúc

Nghiệm thu theo [đặc tả capstone](vinfast-capstone.md), không chấm bằng số video
đã xem. Tự triển khai lại một lát cắt pipeline, giải thích failure modes và bảo vệ
quyết định thiết kế. Bài đánh giá cuối dùng tình huống mới cùng rubric đầu vào:
mọi nhóm đạt ít nhất 2/4, SQL/modelling và ClickHouse ít nhất 3/4; đây là mốc nội
bộ của lộ trình, không phải chuẩn tuyển dụng VinFast.

Nếu đạt: dùng evidence để ứng tuyển DE theo JD, tiếp tục rèn Senior/Architect
qua capacity planning, replication/resilience, nhiều team/data domains và các
quyết định production thật. Nếu chưa đạt: chọn 1–2 nhóm còn yếu cho vòng 2 tuần
tiếp theo và ghi rõ phần chưa có kinh nghiệm production.

## Tài liệu ưu tiên

Đọc theo bài đang làm; không cần hoàn thành tất cả trước khi code. Tra tài liệu
đúng version đã pin, đặc biệt Airflow và dbt-clickhouse.

- [ClickHouse: ReplacingMergeTree](https://clickhouse.com/docs/engines/table-engines/mergetree-family/replacingmergetree)
- [ClickHouse: Distributed engine](https://clickhouse.com/docs/engines/table-engines/special/distributed)
- [ClickHouse: dbt integration và giới hạn](https://clickhouse.com/docs/integrations/dbt)
- [Airflow: best practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
- [Spark: SQL performance tuning](https://spark.apache.org/docs/latest/sql-performance-tuning.html)
- [dbt: incremental models](https://docs.getdbt.com/docs/build/incremental-models)
- [OpenMetadata: connectors](https://docs.open-metadata.org/connectors)
- [AWS S3: security best practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)
- [Kimball: dimensional modeling techniques](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/)
