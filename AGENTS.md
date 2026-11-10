# Quy tắc làm việc với repository

Repository dùng để tự học Data Engineering, phát triển năng lực Senior DE và Data
Architect, đồng thời lưu các công cụ có thể tái sử dụng giữa nhiều môi trường.

## Tài liệu bắt buộc cho từng PR

- Luôn viết tài liệu chi tiết cho từng PR. Tạo hoặc cập nhật một file trong
  `docs/prs/` theo chủ đề thay đổi, không phụ thuộc việc đã có số PR hay chưa.
- Mô tả vấn đề, mục tiêu, phạm vi, thiết kế cuối cùng, các file/thành phần chính,
  quyết định và đánh đổi, cách cài đặt, cách sử dụng, kiểm chứng, giới hạn và rollback.
- PR description phải tự đủ ngữ cảnh cho người không đọc chat, có liên kết tới
  tài liệu tương ứng và ghi rõ kiểm tra nào đã chạy, chưa chạy hoặc bị chặn.
- Cập nhật README và các hướng dẫn bị ảnh hưởng cùng PR. Khi phạm vi thay đổi,
  sửa tài liệu và PR description theo kết quả cuối cùng.

## Commit, push và khả năng tái sử dụng

- Luôn commit và push toàn bộ code, script, cấu hình, test, tài liệu và tài nguyên
  liên quan đến thay đổi lên nhánh làm việc trên GitHub; mở hoặc cập nhật PR để review.
  Đây là quy trình mặc định đã được chủ repo yêu cầu, trừ khi người dùng chỉ định khác.
- Không để thành phần cần thiết chỉ tồn tại trong chat, `/tmp`, global home hoặc
  môi trường cloud hiện tại. Một checkout mới phải đủ để tái tạo kết quả đã mô tả.
- Dùng nhánh riêng; không tự merge hoặc force-push. Kiểm tra diff và không đưa
  thay đổi không liên quan của người dùng vào commit.
- Giữ source, license, commit nguồn và các điều chỉnh của tài nguyên bên thứ ba.
  Với artifact có thể sinh lại như ZIP, commit source và script build; không cần
  commit binary trùng lặp. Ghi rõ cách tạo artifact và kiểm tra tính toàn vẹn.
- Không commit secrets, token, credential, dữ liệu khách hàng/ngân hàng hoặc CV
  cá nhân. Dùng dữ liệu giả lập và ví dụ cấu hình không chứa thông tin nhạy cảm.

## Cài đặt và sử dụng đa môi trường

- Mọi tính năng/công cụ có bước setup đều phải có hướng dẫn cài đặt **và sử dụng**
  cho Linux và macOS: prerequisites, lệnh chạy, đường dẫn, kiểm chứng, cập nhật,
  gỡ bỏ và xử lý lỗi thường gặp.
- Phân biệt project-local, user-global và môi trường cloud. Không mô tả việc cài
  trên cloud như thể đã cài trên Mac hoặc đồng bộ sang các máy khác.
- Ưu tiên Python standard library và đường dẫn có thể cấu hình; không hardcode
  `/workspace` hoặc tên người dùng trong công cụ dùng lại.
- Kiểm tra thay đổi ở phạm vi phù hợp; báo cáo trung thực môi trường đã chạy.
  CI Linux/macOS dùng để kiểm tra tính tương thích, không thay cho kiểm chứng
  chất lượng câu trả lời của AI hoặc kiểm tra UI Codex trên máy người dùng.

## Quy trình hoàn thành

1. Đọc trạng thái Git, remote và hướng dẫn hiện có.
2. Thực hiện thay đổi, tài liệu chi tiết và kiểm tra phù hợp.
3. Review diff, bảo đảm checkout mới có đủ tài nguyên cần thiết.
4. Commit, push nhánh và tạo/cập nhật PR với template của repo.
5. Báo cáo URL PR, kết quả kiểm tra và phần còn bị chặn nếu có.
