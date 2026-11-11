# Kiểm tra, đóng gói và bảo trì

## Source of truth

`codex-global-skills/skills/` chứa toàn bộ nội dung được cài, bao gồm tài liệu tham
chiếu và license. `manifest.json` ghi repo upstream, commit chính xác, source path,
adaptations và SHA-256 của từng file. Không cần clone upstream khi cài trên máy mới.

`INSTALL-SOURCE.json` trong mỗi skill phải trùng metadata của manifest. Bản entry
upstream được giữ riêng nếu đã chỉnh để dùng với Codex. Bản reviewer platform có
`UPSTREAM-REVIEWER.md` và wrapper `SKILL.md`; các companion workflow chỉ là reference,
không được đăng ký thành hàng chục skills global.

`.gitattributes` đánh dấu cây tài nguyên skill là vendored và tắt kiểm tra whitespace
cho riêng cây đó để giữ nguyên byte upstream. Code và tài liệu của repo vẫn được
kiểm tra whitespace bình thường.

## Các lệnh kiểm tra

Chạy từ repo root trên Linux hoặc macOS:

```sh
python3 scripts/validate_bundle.py
python3 -m unittest discover -s tests -v
python3 scripts/package_skills.py
```

Validator kiểm tra tên, frontmatter cơ bản, source commit, license, provenance,
inventory và checksum. Codex app-server mới là bộ parse metadata cuối cùng; có
script kiểm tra optional trong repo. Unit tests dùng thư mục tạm, không ghi vào
skills thật của người dùng. Tests bao phủ cài mới, cài lại, check-only, xung đột,
source bị sửa, symlink, rollback khi copy lỗi và cài từ ZIP vừa build.

CI chạy cùng lệnh trên `ubuntu-latest` và `macos-latest`, Python 3.14. macOS CI kiểm
tra installer/filesystem; không đăng nhập Codex và không xác nhận UI trên Mac M1.

## Build ZIP

```sh
python3 scripts/package_skills.py
python3 scripts/package_skills.py --output /absolute/path/to/de-skills.zip
```

ZIP có tên thư mục gốc `codex-global-skills/`. Script chỉ đưa installer, README,
manifest và các file nằm trong manifest vào ZIP. Timestamp, thứ tự và quyền file
được chuẩn hóa; build lặp lại trong cùng runtime cho kết quả byte-identical.
Không cam kết byte-identical giữa các phiên bản thư viện nén khác nhau. Checksum
đi kèm kiểm chứng đúng artifact đã tạo.

ZIP, bytecode và kết quả tạm không commit vì có thể sinh lại. `verification.json`
từ lần cài cloud đầu tiên là kết quả cục bộ, không phải nguồn xác nhận CI hiện tại.

## Cập nhật upstream

1. Tạo nhánh, đọc diff của commit upstream muốn dùng và kiểm tra license.
2. Thay đúng tài nguyên của skill cần cập nhật; không chạy installer/hook upstream
   để kéo cả collection. Giữ các điều chỉnh Codex có chủ đích.
3. Cập nhật commit và adaptations trong `INSTALL-SOURCE.json` và manifest; đọc
   lại các hướng dẫn mới, đường dẫn tương đối và optional dependencies.
4. Tính lại SHA-256 cho các file đã review, bảo đảm inventory đúng. Không tự cập
   nhật hash chỉ để làm cho một lỗi checksum biến mất mà không kiểm tra diff.
5. Chạy validator, test, package và thử cài vào thư mục staging.
6. Ghi tài liệu PR, push toàn bộ thay đổi liên quan và chờ review. Khi cài phiên
   bản mới lên home người dùng, làm theo quy trình backup trong installation guide.

## Đánh giá chất lượng skill riêng

Để kiểm tra chất lượng câu trả lời, dùng các fixture có lỗi biết trước: SQL join
fan-out, replay không idempotent, thiết kế thiếu RPO/RTO và câu trả lời học viên
sai về delivery semantics. Ghi cả lỗi tìm được, báo động sai và thiếu bằng chứng.
Đây là đánh giá riêng, chưa được thực hiện bởi CI của PR đầu.
