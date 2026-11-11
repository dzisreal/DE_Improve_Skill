# DE Improve Skill

Môi trường tự học hướng tới **Senior Data Engineer / Data Architect**, cùng bộ
Codex skills có thể cài global và tái sử dụng trên Linux, macOS hoặc cloud workspace.

## Bắt đầu

Chuẩn bị Git, Python **3.9+** và Codex. Installer chỉ dùng Python standard library,
không cần pip, Node.js, cloud account hoặc credential.

```sh
git clone https://github.com/dzisreal/DE_Improve_Skill.git
cd DE_Improve_Skill
# Trước khi PR đầu tiên được merge, checkout nhánh này:
git switch feat/global-de-skills-bootstrap
python3 scripts/validate_bundle.py
python3 codex-global-skills/install.py --check
python3 codex-global-skills/install.py
```

Sau khi merge, dùng `main` hoặc một commit đã được kiểm chứng thay cho nhánh PR.
Mở chat Codex mới sau khi cài. Mặc định skills nằm trong `~/.agents/skills/`, dùng
cho mọi project của **cùng tài khoản trên cùng máy**. Cài trên cloud không tự cài
trên Mac hay môi trường cloud khác.

## Bộ skills

| Skill | Nhiệm vụ | Nguồn |
|---|---|---|
| `socratic-tutor` | Đánh giá, hỏi đáp và ôn tập theo từng kỹ năng | Jane Street |
| `data-architect` | Phản biện kiến trúc dữ liệu, recovery, governance và trade-off | Magnus |
| `requesting-code-review` | Review code Python/tooling theo requirements và test | Superpowers |
| `data-review` | Review SQL/model, grain, contracts và downstream impact | Aurora Payments |
| `data-platform-reliability-reviewer` | Review retry, replay, checkpoint và vận hành platform | Vaquar Khan |

Ví dụ: `Dùng $socratic-tutor đánh giá kiến thức CDC của tôi, hỏi từng câu.`
Ví dụ: `Dùng $data-review review thay đổi SQL trên nhánh này so với main.`

## Tài liệu

- [Lộ trình VinFast: 8 tuần, 2 giờ/ngày](docs/learning/vinfast-8-week-plan.md)
- [Bài đánh giá đầu vào: 120 phút](docs/learning/vinfast-baseline-assessment.md)
- [Đặc tả dự án thực hành và tiêu chí nghiệm thu](docs/learning/vinfast-capstone.md)
- [Cài đặt, cập nhật và gỡ bỏ trên Linux/macOS](docs/installation.md)
- [Sử dụng skills và phân biệt phạm vi global/project](docs/usage.md)
- [Kiểm tra, đóng gói và bảo trì nguồn](docs/maintenance.md)
- [Tài liệu PR đầu: global DE skills](docs/prs/001-global-de-skills.md)
- [Quy tắc cộng tác](AGENTS.md)
- [Nguồn và checksum từng file](codex-global-skills/manifest.json)

## Kiểm tra và đóng gói

```sh
python3 scripts/validate_bundle.py
python3 -m unittest discover -s tests -v
python3 scripts/package_skills.py
```

Artifact được tạo tại `dist/codex-global-skills.zip`, kèm file SHA-256. Source của
các skill đã được lưu trong repo: cài từ checkout hoặc ZIP không phải tải lại
upstream. CI chạy kiểm tra trên Linux và macOS.

## Phạm vi

Installer không sửa global `AGENTS.md`, không cài hook, không kết nối MCP và không
tạo tài nguyên cloud. Các MCP JSON đi kèm là ví dụ cấu hình chưa được kích hoạt.
Tài nguyên bên thứ ba giữ license riêng trong thư mục skill tương ứng. Kiểm tra
cài đặt không phải benchmark chứng minh chất lượng dạy học hoặc review của AI.
