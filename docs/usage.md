# Sử dụng bộ skills

Cách gọi trong chat giống nhau trên Linux và macOS. Với CLI, chạy `codex` từ project
cần làm việc; với ứng dụng Codex, mở project đó rồi tạo chat mới. Gõ `$<tên-skill>`
hoặc yêu cầu rõ vai trò bằng ngôn ngữ tự nhiên.

## Chọn đúng vai trò

| Nhu cầu | Skill | Đầu vào cần có |
|---|---|---|
| Học, đánh giá và ôn tập | `socratic-tutor` | Chủ đề, mục tiêu, thời gian; bài làm độc lập |
| Chọn/đánh giá kiến trúc | `data-architect` | Workload, yêu cầu, constraints, sơ đồ và phương án hiện tại |
| Review Python/Bash/tooling | `requesting-code-review` | Phạm vi diff, requirements, cách chạy test |
| Review SQL/dbt/model | `data-review` | Diff, grain, source/target, contracts, downstream và bằng chứng data diff nếu có |
| Review reliability platform | `data-platform-reliability-reviewer` | Sơ đồ data flow, retry/checkpoint, SLA, runbook, log/metrics đã làm sạch |

## Ví dụ dùng ngay

```text
Dùng $socratic-tutor đánh giá CDC và idempotency ở mức Senior DE.
Hỏi từng câu, chưa đưa đáp án trước khi tôi thử. Buổi học 2 giờ.
```

```text
Dùng $data-architect phản biện thiết kế trong docs/design.md.
Nêu giả định, phương án thay thế, chi phí vận hành, RPO/RTO và tiêu chí thử nghiệm.
```

```text
Dùng $requesting-code-review review thay đổi Python của nhánh này so với main.
Requirements ở docs/spec.md. Chỉ báo findings có bằng chứng; chưa sửa code.
```

```text
Dùng $data-review review cả staged và unstaged SQL changes.
Kiểm tra grain, join cardinality, idempotency và các consumer chịu ảnh hưởng.
```

```text
Dùng $data-platform-reliability-reviewer review runbook Kafka/Spark này.
Tập trung việc crash sau ghi sink nhưng trước checkpoint, replay và reconciliation.
```

Các đường dẫn ví dụ phải thay bằng file thật trong project. Không có warehouse
connection thì review tĩnh vẫn thực hiện được, nhưng không được gọi đó là kiểm
chứng dữ liệu production. Cung cấp dữ liệu giả lập để tái hiện lỗi.

## Quy trình tự học gợi ý

1. Tutor đánh giá một chủ đề và giao bài theo khoảng trống đã thấy.
2. Người học viết thiết kế; architecture reviewer phản biện trade-off.
3. Người học implement; chọn reviewer theo loại code/dữ liệu.
4. Chạy test, giải thích vì sao sửa lỗi, rồi tutor kiểm tra lại ở tình huống khác.
5. Lưu bài làm, quyết định và kết quả vào repo học qua PR.

Tutor có lệnh `save state` để xuất trạng thái gọn. Nếu cần lưu lâu dài, yêu cầu
ghi vào file trong repo học; bản upstream không tự cung cấp hệ thống đồng bộ trí nhớ.

## Global không có nghĩa là luôn bật

Mỗi skill chỉ nên áp dụng khi task tương ứng. Không tải tất cả reference cho mọi
câu hỏi. Một project ứng dụng có thể dùng tutor và code reviewer mà không dùng
data reviewer. Hướng dẫn của project và yêu cầu hiện tại của người dùng được ưu tiên.

Reviewers có thể dùng subagent khi runtime và quyền của phiên làm việc hỗ trợ;
nếu không, bản tương thích chạy từng lượt riêng và nêu giới hạn. Cài skill không
tự kích hoạt hook, subagent, issue tracker, gửi bình luận hay cấp quyền production.

## Phần không nằm trong bộ cài

- Không cài full Superpowers hoặc các collection khác.
- Không cài Ponytail, dbt Labs skills hay system-design-tutor trong bundle năm skill này.
- Không cài Spark, Kafka, Airflow, dbt hoặc IBM Cloud Pak for Data.
- Reviewer platform có reference cho nhiều hệ thống, không phải bộ tài liệu vận
  hành IBM chính thức. Cần đối chiếu version và tài liệu nhà cung cấp khi dùng.
- Chưa có benchmark chứng minh các skill này làm tăng năng lực người học hoặc
  phát hiện đủ lỗi DE; các bài test repository kiểm tra packaging và installer.
