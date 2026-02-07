# Thiết kế Back-end (BE) - SheetFlow 2.0

Back-end đóng vai trò cung cấp dữ liệu cấu hình và xử lý các thao tác CRUD trên kiến trúc đa sheet linh hoạt.

## 🧱 Module Backend Chuyên sâu

### 1. Module Cấu hình & Theme
- **Theme API**: Cung cấp endpoint trả về các biến CSS màu sắc nếu được cấu hình từ server, cho phép giao diện thay đổi tone màu mà không cần sửa file tĩnh.

### 2. Smart Sheet Manager (`sheets_service.py`)
- **Metadata Cache**: Lưu trữ danh sách tất cả các sheets cùng với cấu trúc header của chúng vào bộ nhớ đệm (Cache) để giảm thiểu request tới Google API.
- **Adaptive Fetching**: Tự động xác định vùng dữ liệu (Range) cần lấy để tránh việc tải quá nhiều dữ liệu dư thừa.

### 3. ID Auto-Generator API
- **Sequential ID Logic**: Cung cấp endpoint để quét sheet và tính toán số thứ tự tiếp theo cho các mã định danh dạng `N[STT]`, đảm bảo tính duy nhất và liên tục.

### 4. Admin Division Proxy (`/api/provinces`, `/api/districts`, `/api/wards`)
- **Vietnam Provinces API Proxy**: Tích hợp API hành chính công của Việt Nam để cung cấp dữ liệu cho dropdown địa chỉ. Sử dụng `httpx` với `follow_redirects=True` để đảm bảo ổn định.

### 5. Configuration & Defaults API (`/api/defaults`)
- **Contact Defaults**: Trả về các giá trị mặc định cho `Link Zalo` và `Link NV` từ biến môi trường (`.env`), giúp CTV tiết kiệm thời gian nhập liệu.

### 6. Cloudinary Integration (`/upload`)
- **Media Hosting**: Chuyển đổi từ lưu trữ base64 sang hosting chuyên nghiệp trên Cloudinary. Endpoint `/upload` thực hiện đẩy ảnh lên nền tảng và trả về URL bảo mật (`secure_url`).

## 🔄 Luồng thực thi Tối ưu

### 1. Luồng Tải danh mục (Dynamic Inventory)
1. Browser gửi yêu cầu lấy danh sách danh mục.
2. BE trả về mảng chứa `tag` (nhóm) và `title` (tên sheet).
3. FE render Sidebar dựa trên cấu trúc phân cấp này.

### 2. Luồng thao tác dữ liệu
- Mọi yêu cầu CRUD (`add`, `update`, `delete`) đều đi kèm với định danh `sheet_name`.
- SS (SheetsService) sẽ thực hiện logic kiểm tra cấu trúc cột (Self-healing) trước khi ghi dữ liệu để đảm bảo không ghi lệch cột nếu cấu trúc sheet thay đổi.
- **Multiple Image Storage**: Các URL ảnh được ghép thành chuỗi phân cách bởi ký tự `|` (pipe) trước khi lưu vào cột `Link ảnh`, cho phép lưu trữ không giới hạn ảnh trong 1 ô duy nhất.
