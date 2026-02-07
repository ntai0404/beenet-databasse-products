## 📑 1. Kịch bản Điều hướng & Tìm kiếm Danh mục
- **Mô tả**: Người dùng đối mặt với hàng chục danh mục sản phẩm.
- **Thao tác**: 
  - Gõ từ khóa vào ô Search trên Sidebar hoặc dùng Quick Switcher.
  - Chọn danh mục từ danh sách đã được lọc.
- **Kết quả**: Hệ thống chuyển đổi sheet tức thì, bảng dữ liệu tự động thay đổi cấu trúc tương ứng.

## ➕ 2. Kịch bản Quản lý Dữ liệu linh hoạt

## ➕ 3. Kịch bản Thêm sản phẩm mới
- **Trạng thái**: Đang ở danh mục "Điện thoại".
- **Bước 1**: Nhấn nút "Thêm sản phẩm mới".
- **Bước 2 (Xác nhận)**: Hệ thống hiển thị popup hỏi: "Sản phẩm này là Dropbuy hay Non-Dropbuy?".
- **Bước 3**: Nếu chọn **Dropbuy**: Giao diện chuyển sang tab "BIỂU MẪU" với các trường trống.
- **Bước 4**: Nếu chọn **Non-Dropbuy**: Giao diện chuyển sang tab "BIỂU MẪU", hệ thống tự động sinh mã `N[STT]` (VD: N37) và khóa ô ID.
- **Bước 5**: Người dùng nhập liệu trong tab và nhấn "Lưu".
- **Bước 6**: Hệ thống khóa nút "Lưu" (Disable) để tránh nhấn đúp.
- **Kết quả**: Hệ thống lưu dữ liệu, đóng tab Biểu mẫu và chuyển về tab danh mục cũ, dòng mới hiện lên đầu bảng.

## ✏️ 4. Kịch bản Cập nhật (Edit)
- **Bước 1**: Nhấn icon Sửa trên dòng sản phẩm "iPhone 15".
- **Bước 2**: Giao diện chuyển đổi tức thì sang tab "BIỂU MẪU", tự động điền các thông tin hiện tại vào form.
- **Bước 3**: Người dùng sửa đổi dữ liệu cần thiết.
- **Bước 4**: Nhấn "Cập nhật".
- **Kết quả**: Hệ thống lưu dữ liệu, chuyển về tab danh mục cũ, dòng dữ liệu nhấp nháy màu xanh báo hiệu thành công.

## 🗑 5. Kịch bản Xóa dữ liệu
- **Bước 1**: Nhấn icon Xóa.
- **Bước 2**: Một popup xác nhận hiện lên: "Bạn có chắc chắn muốn xóa sản phẩm này khỏi hệ thống?".
- **Bước 3**: Người dùng nhấn "Đồng ý xóa".
- **Kết quả**: Dòng bị ẩn đi ngay lập tức trên web và bị xóa thực tế trong Google Sheet.

## ➕ 6. Kịch bản Thêm sản phẩm Non-Dropbuy (Chi tiết)
- **Mô tả**: Người dùng thêm sản phẩm "ngoài luồng", không có mã Dropbuy sẵn.
- **Bước 1**: Tại tab danh mục, nhấn "Thêm mới" -> Chọn "Non-Dropbuy".
- **Bước 2**: Hệ thống gọi API tự động tính toán STT và điền mã `N[STT]` (VD: `N37`).
- **Bước 3**: Chuyển sang tab "BIỂU MẪU" với ô ID Sản phẩm ở trạng thái chỉ đọc (Read-only).
- **Kết quả**: Sản phẩm được lưu và quản lý theo mã Nxx tăng dần, đảm bảo duy nhất.
