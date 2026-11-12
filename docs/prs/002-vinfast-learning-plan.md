# PR: Lộ trình 8 tuần theo JD Data Engineer VinFast

## Vấn đề và kết quả

Repo đã có bộ Codex skills dùng lại giữa các project nhưng chưa có chương trình
học theo một JD cụ thể. Thay đổi này xác định lộ trình 112 giờ, bài đánh giá đầu
vào và capstone telemetry/after-sales/unstructured để tạo bằng chứng thực hành
cho ClickHouse, dbt, Airflow, Spark, catalog, privacy và workflow production.

Lịch được điều chỉnh sau bài trả lời đầu vào: giữ phần nền SQL/Python/Spark,
đưa cluster nhiều shard sang tuần 3 và tích hợp end-to-end từ tuần 2. Không yêu
cầu làm lại assessment; bài chưa có code chạy không được coi là năng lực đã
kiểm chứng. Không đăng nguyên văn câu trả lời hay điểm cá nhân trong repo.

Đầu vào đã chốt: 8 tuần, 2 giờ/ngày, chưa có lịch phỏng vấn, Mac M1 16 GB/256 GB,
30 USD cloud/tháng và AI riêng. Kinh nghiệm vận hành toàn bộ CP4D được dùng làm
nền cho reliability; không suy ra điểm ClickHouse/dbt từ số năm kinh nghiệm.

## Phạm vi và file chính

- `docs/learning/vinfast-8-week-plan.md`: ưu tiên theo evidence, lịch 8×14 giờ, cửa
  kiểm tra, resource profiles, ngân sách, dùng skills và tài liệu chính thức.
- `docs/learning/vinfast-baseline-assessment.md`: 105 phút tự làm + 15 phút review,
  sáu nhóm năng lực, fixture SQL và rubric tái sử dụng; không lưu điểm cá nhân.
- `docs/learning/vinfast-capstone.md`: contracts/grain, architecture, workload,
  modality scope, 11 acceptance criteria, PR backlog và evidence convention.
- `docs/learning/week-01-foundations.md`: bảy buổi 120 phút, fixture SQLite
  dùng Python standard library, bài tập, gates, troubleshooting và evidence.
- `README.md`: liên kết tới lộ trình, assessment, capstone và bài học tuần 1.

Chỉ thay đổi tài liệu. Không thêm dependencies, cài global skill, tạo cloud
resources hoặc triển khai lab trong PR này. Không đưa CV hoặc dữ liệu riêng vào repo.

## Quyết định và đánh đổi

Tuần 1 luyện các cơ chế trên fixture nhỏ; capstone tích hợp từ tuần 2. Ưu tiên
correctness trước khi thêm shard và orchestration; ClickHouse/dbt vẫn là phần
học sâu. CI/config được khởi tạo tuần 2, artifacts và tài liệu bổ sung mỗi tuần
để tuần 7/8 tập trung catalog, promotion và nghiệm thu. Media có metadata
extraction bắt buộc, ASR/OCR/embeddings nâng cao để mở
rộng; đây là giới hạn được ghi rõ, không coi là kinh nghiệm đa phương thức ở
production scale. Lab bắt buộc 2 shard × 1 replica; HA 2×2 là mở rộng.

Profiles chạy theo phiên để phù hợp M1 16 GB. Catalog vẫn cần ingestion thật;
nếu không vừa local, dùng compute theo phiên trong hạn mức. Không coi billing
alert là hard cap hoặc bảng phân bổ là báo giá. Lộ trình có 16 giờ review/buffer
trong 112 giờ và không hứa đạt Senior chỉ sau tám tuần.

## Cài đặt và sử dụng — Linux và macOS

Đọc Markdown chỉ cần Git và editor/browser. Bài tuần 1 cần Python 3.9+ với
sqlite3/SQLite 3.25+; không cần pip packages, Docker hoặc cloud account.
Các lệnh giống nhau trên Linux shell và macOS Terminal:

```sh
git clone https://github.com/dzisreal/DE_Improve_Skill.git
cd DE_Improve_Skill
git switch docs/vinfast-8-week-plan
```

Đọc plan rồi làm bài tuần 1 và ghi evidence. Assessment giữ làm rubric cho
người mới hoặc đánh giá lại bằng tình huống mới; không bắt người đã trả lời
làm lại trước khi bắt đầu.
Sau khi PR được merge, dùng `main` hoặc commit đã kiểm chứng. Cài và sử dụng
skills theo [installation](../installation.md) và [usage](../usage.md); chúng
không bắt buộc để đọc plan hoặc làm phần assessment độc lập.

Để cập nhật checkout sạch: `git pull --ff-only` trên nhánh tài liệu đang dùng.
Nếu nhánh chưa tồn tại ở máy cũ, `git fetch origin` trước `git switch`.
Nếu có thay đổi riêng, commit hoặc lưu chúng trước; không dùng reset để bỏ bài làm.
Gỡ bỏ riêng checkout không ảnh hưởng global skills; chỉ xóa sau khi đã lưu bài
làm cần giữ. PR này không cài dịch vụ cần uninstall.

## Kiểm chứng và giới hạn

- Review diff và `git diff --check`: chỉ Markdown, không có ứng dụng runtime,
  secrets, CV hoặc dữ liệu nội bộ.
- Kiểm tra liên kết Markdown nội bộ của các file thay đổi và balanced fences.
- Rà lại ngân sách: tám tuần đều 14 giờ; nhịp ngày 1–6 và ngày 7 đều 120 phút;
  ngân sách cloud 18 + 5 + 7 = 30 USD/tháng.
- Chạy nguyên block fixture Python từ hướng dẫn tuần 1 trên Linux: load 5 rows,
  script compile được và output `[(5,)]`. Fixture là scaffold, không phải lời
  giải của người học hoặc bằng chứng đã đạt learning gates.
- CI hiện có kiểm tra skill bundle trên Linux/macOS; không thay cho việc chạy
  bài học mới trên Mac. Chưa chạy fixture trên Mac của người học, chưa dựng lab
  stack, chạy Spark failure drill hoặc benchmark M1.
- Không thêm tests mirror nội dung Markdown hoặc chạy lại installer tests
  local cho thay đổi tài liệu. Lab compatibility/pins được xác minh khi thêm
  từng thành phần từ tuần 2; không tự nhận toàn stack đã tương thích.

## Quan hệ với PR nền và rollback

PR kế hoạch nối tiếp nhánh `feat/global-de-skills-bootstrap` vì PR #1 vẫn mở tại
thời điểm tạo. Review diff chỉ gồm tài liệu mới. Merge PR #1 trước, sau đó đổi
base của PR kế hoạch về `main` nếu GitHub chưa tự cập nhật; kiểm tra lại diff.
Không tự merge PR.

Rollback bằng revert commit tài liệu sau khi merge, hoặc đóng PR nếu chưa merge.
Không có migration, tài nguyên cloud hoặc thay đổi global cần hoàn tác. Giữ lại
bài làm/evidence phát sinh độc lập của người dùng khi điều chỉnh kế hoạch.
