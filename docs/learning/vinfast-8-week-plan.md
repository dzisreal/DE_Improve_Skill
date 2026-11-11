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

## Đánh giá khoảng cách với JD

Đây là giả thuyết để phân bổ thời gian, chưa phải kết quả đánh giá năng lực.
Thông tin chưa có trong hồ sơ được coi là **chưa kiểm chứng**, không phải chưa biết.

| Năng lực | Bằng chứng ban đầu | Ưu tiên và bằng chứng cần bổ sung |
|---|---|---|
| SQL, Python, Spark | Đã dùng trong công việc DE | P1: kiểm tra window, late data, typed package, joins/shuffle; rút ngắn phần đã vững |
| Vận hành, incident, reliability | Phụ trách toàn bộ CP4D | P1: chuyển thành runbook, SLO, replay/backfill và recovery drill của stack mới |
| AWS S3, IAM | Có kinh nghiệm AWS | P1: xác minh least privilege, versioned objects, secrets và chi phí |
| ClickHouse nhiều shard | Chưa có bằng chứng trong thông tin hiện có | P0: engines, ORDER BY, partition/shard key, correctness, distributed joins |
| dbt, dimensional models, SCD | Chưa được kiểm chứng đủ | P0: grain, incremental, SCD2 và tests có tình huống sai |
| Airflow | Mức độ tự thiết kế/vận hành cần đánh giá | P1: parse time, data interval, retries, idempotency, backfill |
| Unstructured → dữ liệu query được | Chưa được kiểm chứng đủ | P0: metadata contract, extraction, quarantine, versioning, lineage |
| Catalog, privacy, erasure | Kinh nghiệm platform có liên quan; workflow cụ thể chưa rõ | P1: lineage thật và xóa dữ liệu xuyên các lớp |
| Architecture, English, critical AI review | Cần sản phẩm và tình huống cụ thể | Xuyên suốt: ADR, PR, giải thích trade-off và giới hạn kiểm chứng |

P0 = học sâu và phải demo; P1 = đánh giá rồi bổ sung. Kubernetes/EKS, GitOps,
embeddings/vector search là phần mở rộng sau các tiêu chí bắt buộc; không dựng
lại CP4D để chứng minh lại kỹ năng đã có.

## Cách học và cách điều chỉnh

- Ngày 1 làm [bài đánh giá 120 phút](vinfast-baseline-assessment.md). Chỉ chấm
  sau khi có câu trả lời/code; không suy điểm từ số năm kinh nghiệm.
- Nhịp một buổi thông thường: 20 phút đọc tài liệu, 70 phút tự làm, 20 phút
  kiểm chứng/giải thích, 10 phút ghi learning log bằng tiếng Anh. Buổi assessment
  và mock interview có lịch riêng.
- Mỗi tuần có 12 giờ làm bài và 2 giờ review/bù lỗi. Nếu còn lỗi correctness,
  dùng phần dự phòng và bỏ bài mở rộng trước; không chuyển tuần chỉ vì đã hết lịch.
- Mỗi tuần chọn một quyết định để viết ADR ngắn: yêu cầu, lựa chọn, phương án
  thay thế, trade-off, bằng chứng và điều kiện cần xem xét lại.
- Nếu một nhóm đạt 3–4/4 ở đầu vào và demo được, chuyển tối đa 4 giờ ôn cơ bản
  sang nhóm yếu. Giữ bài nghiệm thu và tổng 112 giờ. Nếu hết dự phòng mà vẫn
  chưa đạt, ghi rõ phần thiếu và dành một vòng học tiếp theo, không đánh dấu hoàn thành.

## Lịch theo tuần

| Tuần | Nội dung, phân bổ đúng 14 giờ | Đầu ra và cửa kiểm tra |
|---|---|---|
| 1 — Baseline và luồng đầu tiên | Assessment 2h; môi trường/pin versions 4h; requirements + contracts 2h; Python ingest + SQL staging/mart tối thiểu 4h; review 2h | Một batch dữ liệu giả lập đi hết object storage → raw → staging → mart trên ClickHouse một node. Typed Python package có test; ghi grain, UTC, event key, owner và lệnh tái tạo Linux/macOS. Chưa cần Airflow/dbt cho luồng đầu tiên. |
| 2 — ClickHouse nhiều shard | Engines/keys/EXPLAIN 3h; lab 2 shard 1 replica 4h; duplicates, late versions và distributed joins 3h; benchmark + ADR 2h; review 2h | Cùng fixture cho cùng kết quả trên 1 và 2 shard; retry không làm KPI tăng; giải thích tại sao ORDER BY không phải unique constraint và ReplacingMergeTree không tự khử trùng toàn cụm. Có so sánh query plan/read rows trước và sau tối ưu. |
| 3 — dbt và modelling | Chuyển staging/marts sang dbt 3h; facts + SCD2 + incremental 5h; tests/docs/reconciliation 3h; review SQL do AI viết 1h; review tuần 2h | Fact grain rõ; SCD2 không chồng khoảng; late data/backfill cho cùng kết quả với full rebuild trên fixture. `dbt build` và docs chạy được; chọn strategy theo phiên bản adapter đã pin. |
| 4 — Airflow + Spark | DAG/retry/data interval 3h; Spark dedup/window/joins 4h; tích hợp ingestion → Spark → dbt 3h; failure/replay drill 2h; review 2h | Không gọi mạng hoặc xử lý nặng khi parse DAG; kill task sau partial write rồi rerun vẫn đúng. Spark explain và metrics chỉ ra shuffle/skew; backfill một khoảng không phá partition khác. |
| 5 — Unstructured | Contract + manifest + versioning 2h; parse logs/text/PDF 4h; image/audio/video metadata 2h; quarantine/reprocess/tests 2h; mart + lineage mapping 2h; review 2h | Text và một PDF đọc được thành nội dung query được; ảnh/audio/video có metadata thật từ file. Mỗi modality có fixture hợp lệ và hỏng. Thay extractor version tạo kết quả có truy vết; chạy lại cùng version không tạo bản trùng. |
| 6 — Governance và vận hành | OpenMetadata ingestion + lineage 4h; classification/IAM/secrets 2h; erasure/restore drill 3h; DQ/SLO/runbooks 3h; review 2h | Catalog có bảng, owner, dbt lineage và liên kết nguồn unstructured. Analyst bị từ chối dữ liệu restricted. Một yêu cầu xóa giả lập được theo dõi đến raw/staging/mart/extracted artifacts; restore không tái xuất bản dữ liệu đã xóa. |
| 7 — Promotion và recovery | Dev/staging/prod config + CI 4h; schema change/rollback 3h; shard outage/backfill drill 3h; rehearsal từ checkout mới 2h; review 2h | Cùng artifact chạy với config khác; không hardcode endpoint/secret. CI tests trước merge; production giả lập có bước approval và bằng chứng rollback. Đo recovery thực tế, không gọi lab 2×1 là HA. |
| 8 — Hoàn thiện và ứng tuyển | Đóng lỗi nghiệm thu 4h; demo + architecture review 3h; SQL/Python/system-design mock 3h; CV/English evidence 2h; tổng kết 2h | Demo 15 phút; README/runbooks tái tạo được; evidence matrix đầy đủ; mock và đánh giá cuối. Viết rõ đã kiểm chứng gì và chưa kiểm chứng gì. |

### Nhịp 7 ngày

Ngày 1–2 hiểu vấn đề và thiết kế; ngày 3–4 xây luồng chính; ngày 5 tạo lỗi và
đối chiếu kết quả; ngày 6 tài liệu/PR/demo; ngày 7 review và bù lỗi. Đây là nhịp
tham khảo; bảng giờ của từng tuần là ngân sách chính, không cộng thêm một lịch
học thứ hai. Có thể dồn ngày nghỉ nếu vẫn giữ tổng 14 giờ/tuần.

## Môi trường và ngân sách

Thiết kế lab local-first; đây là kế hoạch setup, **chưa có Compose stack hoặc
lab code trong PR tài liệu này**. Tuần 1 sẽ tạo script, config và hướng dẫn
Linux/macOS có kiểm chứng. Hướng dẫn [cài skills](../installation.md) đã có riêng.

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
Spark/Java và catalog ở tuần 1; khóa version/image digest trong repo. Kiểm tra
image ARM64 trên macOS và kiến trúc máy Linux. Nếu dùng emulation thì ghi rõ,
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
| `data-architect` | Tuần 1/2/6/8: phản biện requirements, sharding, SCD, privacy, recovery và chi phí; yêu cầu nêu giả định |
| `data-review` | Tuần 2/3/5: review grain, SQL, incremental, schema contracts, cross-shard correctness; yêu cầu counterexample |
| `requesting-code-review` | Khi có diff Python/DAG/CI: review theo acceptance criteria, bằng chứng test và lỗi có thể tái hiện |
| `data-platform-reliability-reviewer` | Tuần 4/6/7: phân tích crash points, retry, partial write, replay/backfill, alert và runbook |

Prompt mẫu: “Dùng $data-review review diff hiện tại theo tiêu chí tuần 3 trong
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
