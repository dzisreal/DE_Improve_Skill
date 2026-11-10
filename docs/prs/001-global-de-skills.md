# PR đầu: bộ Codex DE skills global và quy trình tái sử dụng

## Vấn đề

Repository trước đó chỉ có README giới thiệu. Bộ skills đã chuẩn bị trong cloud
chưa được lưu lên GitHub đầy đủ; một môi trường mới chưa có đường dẫn cài đặt,
kiểm tra và sử dụng thống nhất. Quy tắc viết tài liệu và push thay đổi cũng chưa
được ghi thành hướng dẫn cho các chat làm việc sau.

## Kết quả mong muốn

Một checkout mới trên Linux hoặc macOS có thể kiểm tra và cài đúng năm skills vào
`~/.agents/skills/`. Người dùng có thể chuyển ZIP sang môi trường khác để cài offline.
Mọi PR tiếp theo phải có tài liệu chi tiết và push toàn bộ source/tài liệu liên quan.

## Thành phần

| Thành phần | Trách nhiệm |
|---|---|
| `AGENTS.md` | Quy trình tài liệu, commit/push/PR và tái tạo đa môi trường |
| `.github/pull_request_template.md` | Cấu trúc mô tả PR tự đủ ngữ cảnh |
| `codex-global-skills/skills/` | Nội dung năm skills, references, templates và license |
| `codex-global-skills/manifest.json` | Phiên bản upstream, adaptations và checksum |
| `codex-global-skills/install.py` | Cài user-global, preflight trước ghi, bảo vệ bản hiện có |
| `scripts/validate_bundle.py` | Kiểm tra inventory, metadata và nguồn gốc |
| `scripts/package_skills.py` | Tạo ZIP portable và SHA-256 từ source |
| `scripts/verify_codex_discovery.py` | Kiểm tra Codex nhận đủ user-global skills, không gọi model |
| `tests/test_installation.py` | Kiểm tra các hành vi ghi file và tính portable |
| `.github/workflows/validate.yml` | Kiểm tra Linux/macOS và lưu artifact |
| `docs/installation.md`, `docs/usage.md`, `docs/maintenance.md` | Hướng dẫn vận hành, sử dụng và bảo trì |

## Quyết định thiết kế

- **Vendor source đã pin:** máy đích không phải tải GitHub upstream khi cài, tránh
  trôi phiên bản. Đánh đổi là repo giữ một bản sao tài nguyên bên thứ ba.
- **Năm skill có phạm vi rõ:** tutor, data architect, generic code review, data
  review và platform reliability review. Không cài toàn bộ collection upstream.
- **Chỉnh tương thích có lưu bản gốc:** xử lý optional dependencies, review-only
  scope, WIP diffs và subagent fallback. Giữ nguồn gốc từng thay đổi trong manifest.
- **Không ghi đè:** installer preflight tất cả conflict trước khi ghi, bỏ qua bản
  giống hệt và rollback thư mục mới nếu copy lỗi. Cập nhật phiên bản khác cần backup
  bản cũ; không có chức năng tự nâng cấp hay xóa chỉnh sửa cá nhân.
- **Global theo OS user:** không ghi project-local skill và không sửa global
  AGENTS.md. `AGENTS.md` mới ở repo này áp dụng quy trình riêng của repo.
- **Artifact sinh lại:** ZIP không commit trùng với source; script và CI tạo ZIP
  kèm checksum. Tất cả nội dung cần để build nằm trong GitHub repository.

## Cài đặt và sử dụng

Lệnh nhanh sau checkout nhánh PR:

```sh
python3 scripts/validate_bundle.py
python3 codex-global-skills/install.py --check
python3 codex-global-skills/install.py
```

Mở chat Codex mới, ví dụ: `Dùng $data-review review các SQL changes so với main.`
Hướng dẫn riêng Linux/macOS, prerequisites, cập nhật, uninstall và troubleshooting:
[installation](../installation.md). Chọn reviewer và ví dụ từng vai trò:
[usage](../usage.md).

## Kiểm chứng

- Đã kiểm tra lần cài cloud trước PR: Codex app-server nhận đủ năm skills ở scope
  `user`, enabled, không có lỗi parse, từ hai working directory khác nhau.
- Đã chạy trên Linux cloud, Python 3.12.14: validator 5 skills / 128 pinned files,
  8 unit tests thành công, build ZIP và cài từ ZIP trong test thành công.
- Script discovery đưa vào PR đã chạy với Codex CLI 0.167.0-alpha.4: đủ năm skill,
  scope `user`, enabled, từ repo và một thư mục tạm độc lập.
- CI được cấu hình chạy trên Linux và macOS; trạng thái thực tế xem checks của PR.
  Không diễn giải việc có workflow là đã chạy thành công trên macOS.
- Chưa kiểm tra UI Codex trên Mac M1 của người dùng, chưa benchmark chất lượng
  tutor/reviewer và chưa kết nối production hoặc IBM Cloud Pak for Data.

## Giới hạn

Checksum chỉ kiểm tra tính toàn vẹn theo manifest, không xác nhận mọi lời khuyên
trong tài liệu upstream là đúng. Giá sản phẩm, thông số phiên bản và compliance
cần đối chiếu nguồn hiện hành. MCP configs chỉ là template; không chứa credential
thật và không được tự kích hoạt. Cài cloud không tự đồng bộ sang Mac.

## Rollback

Trước cài phiên bản khác, sao lưu các skill có chỉnh sửa ra ngoài cây được Codex
quét. Khi cần rollback, di chuyển bản mới ra khỏi `~/.agents/skills/`, phục hồi bản
cũ và tạo chat mới. Không xóa cả `.agents`; không ảnh hưởng built-in skills khác.
Rollback thay đổi repo thực hiện bằng revert commit/PR sau review; PR này không
thay đổi dữ liệu cloud hay database cần migration ngược.
