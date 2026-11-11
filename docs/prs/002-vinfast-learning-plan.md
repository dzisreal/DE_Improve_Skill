# PR: Lộ trình 8 tuần theo JD Data Engineer VinFast

## Vấn đề và kết quả

Repo đã có bộ Codex skills dùng lại giữa các project nhưng chưa có chương trình
học theo một JD cụ thể. Thay đổi này xác định lộ trình 112 giờ, bài đánh giá đầu
vào và capstone telemetry/after-sales/unstructured để tạo bằng chứng thực hành
cho ClickHouse, dbt, Airflow, Spark, catalog, privacy và workflow production.

Đầu vào đã chốt: 8 tuần, 2 giờ/ngày, chưa có lịch phỏng vấn, Mac M1 16 GB/256 GB,
30 USD cloud/tháng và AI riêng. Kinh nghiệm vận hành toàn bộ CP4D được dùng làm
nền cho reliability; không suy ra điểm ClickHouse/dbt từ số năm kinh nghiệm.

## Phạm vi và file chính

- `docs/learning/vinfast-8-week-plan.md`: JD gap hypotheses, lịch 8×14 giờ, cửa
  kiểm tra, resource profiles, ngân sách, dùng skills và tài liệu chính thức.
- `docs/learning/vinfast-baseline-assessment.md`: 105 phút tự làm + 15 phút review,
  sáu nhóm năng lực, fixture SQL và rubric; chưa gán điểm cho người học.
- `docs/learning/vinfast-capstone.md`: contracts/grain, architecture, workload,
  modality scope, 11 acceptance criteria, PR backlog và evidence convention.
- `README.md`: liên kết tới ba tài liệu trên.

Chỉ thay đổi tài liệu. Không thêm dependencies, cài global skill, tạo cloud
resources hoặc triển khai lab trong PR này. Không đưa CV hoặc dữ liệu riêng vào repo.

## Quyết định và đánh đổi

Một capstone được tích hợp từ tuần 1 thay cho các bài rời rạc. Ưu tiên sâu
ClickHouse/dbt và correctness; Airflow/Spark được đánh giá trước để tái phân bổ
giờ. Media có metadata extraction bắt buộc, ASR/OCR/embeddings nâng cao để mở
rộng; đây là giới hạn được ghi rõ, không coi là kinh nghiệm đa phương thức ở
production scale. Lab bắt buộc 2 shard × 1 replica; HA 2×2 là mở rộng.

Profiles chạy theo phiên để phù hợp M1 16 GB. Catalog vẫn cần ingestion thật;
nếu không vừa local, dùng compute theo phiên trong hạn mức. Không coi billing
alert là hard cap hoặc bảng phân bổ là báo giá. Lộ trình có 16 giờ review/buffer
trong 112 giờ và không hứa đạt Senior chỉ sau tám tuần.

## Cài đặt và sử dụng — Linux và macOS

Tài liệu Markdown chỉ cần Git và editor/browser, không cần cloud account hoặc
cài Python/Docker. Các lệnh giống nhau trên Linux shell và macOS Terminal:

```sh
git clone https://github.com/dzisreal/DE_Improve_Skill.git
cd DE_Improve_Skill
git switch docs/vinfast-8-week-plan
```

Đọc plan, làm assessment trước, ghi evidence rồi điều chỉnh giờ theo rubric.
Sau khi PR được merge, dùng `main` hoặc commit đã kiểm chứng. Cài và sử dụng
skills theo [installation](../installation.md) và [usage](../usage.md); chúng
không bắt buộc để đọc plan hoặc làm phần assessment độc lập.

Để cập nhật checkout sạch: `git pull --ff-only` trên nhánh tài liệu đang dùng.
Nếu nhánh chưa tồn tại ở máy cũ, `git fetch origin` trước `git switch`.
Nếu có thay đổi riêng, commit hoặc lưu chúng trước; không dùng reset để bỏ bài làm.
Gỡ bỏ riêng checkout không ảnh hưởng global skills; chỉ xóa sau khi đã lưu bài
làm cần giữ. PR này không cài dịch vụ cần uninstall.

## Kiểm chứng và giới hạn

- Review diff và `git diff --check`: chỉ bốn tài liệu mới và README; không có code
  runtime, secrets hoặc dữ liệu cá nhân đính kèm.
- Kiểm tra liên kết Markdown nội bộ của các file thay đổi: tất cả đích tồn tại.
- Rà lại ngân sách: tám tuần đều 14 giờ, assessment 120 phút, ngân sách cloud
  18 + 5 + 7 = 30 USD/tháng.
- Thực hiện kiểm tra tài liệu trên Linux workspace. Không cần chạy lại installer
  tests cho thay đổi Markdown; không tuyên bố đã chạy lab hoặc benchmark M1.
- Hướng dẫn checkout dùng Git chuẩn trên Linux/macOS; chưa chạy lại checkout
  trên Mac của người học. Compatibility matrix và lab validation là đầu ra tuần 1.

## Quan hệ với PR nền và rollback

PR kế hoạch nối tiếp nhánh `feat/global-de-skills-bootstrap` vì PR #1 vẫn mở tại
thời điểm tạo. Review diff chỉ gồm tài liệu mới. Merge PR #1 trước, sau đó đổi
base của PR kế hoạch về `main` nếu GitHub chưa tự cập nhật; kiểm tra lại diff.
Không tự merge PR.

Rollback bằng revert commit tài liệu sau khi merge, hoặc đóng PR nếu chưa merge.
Không có migration, tài nguyên cloud hoặc thay đổi global cần hoàn tác. Giữ lại
bài làm/evidence phát sinh độc lập của người dùng khi điều chỉnh kế hoạch.
