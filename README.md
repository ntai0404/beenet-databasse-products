# BeenetData Setup Guide

Hệ thống quản lý dữ liệu Google Sheets chuyên nghiệp.

## 🚀 Cài đặt nhanh

1. **Tải mã nguồn và Cài đặt thư viện**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Cấu hình môi trường**:
   - Copy `.env.example` thành `.env`.
   - Điền các thông tin: `SHEET_URL`, `DEEPSEEK_API_KEY`, các thông tin Cloudinary, v.v.
   - `DEFAULT_LINK_ZALO` và `DEFAULT_LINK_NV` dùng để tự động điền thông tin liên hệ cho sản phẩm mới.

3. **Google Sheets API**:
   - Đặt file JSON credentials của Google Cloud vào thư mục gốc và đổi tên thành tên file bạn đã cấu hình trong `.env` (mặc định là `ggsheet-key.json`).
   - Chia sẻ Google Sheet cho email `client_email` trong file JSON với quyền **Editor**.

4. **Chạy ứng dụng**:
   ```bash
   python main.py
   ```
   Truy cập tại: `http://localhost:8080`

5. **Đăng nhập**:
   - Tài khoản: `admin`
   - Mật khẩu: `admin`

## 🛠 Cấu trúc dự án

- `main.py`: Ứng dụng FastAPI, routing và authentication.
- `sheets_service.py`: Xử lý logic kết nối Google Sheets.
- `templates/`: Giao diện HTML (Login, Dashboard).
- `static/`: CSS và Assets (Logo).
- `.env`: Lưu trữ API Key và cấu hình bảo mật.
