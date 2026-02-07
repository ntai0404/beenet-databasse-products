# Thiết kế Front-end (FE) - SheetFlow 2.0

Giao diện được thiết kế để xử lý lượng lớn danh mục (Multi-sheet) với trải nghiệm người dùng tối ưu.

## 🎨 Hệ thống Giao diện Động (Dynamic UI System)

### 1. Adaptive Color Palette
- Sử dụng **CSS Variables** (`--primary`, `--accent`, `--bg`) để tự động điều chỉnh màu sắc theo danh mục.

### 2. Glassmorphism & Adaptive Blur
- Hiệu ứng kính mờ cho các thành phần nổi, đảm bảo thẩm mỹ hiện đại và độ tương phản tốt.

## 🏗 Giải pháp Điều hướng Đa danh mục (Smart Navigation)

### 1. Sidebar "Thông minh"
- **Quick Search Filter**: Lọc danh mục nhanh chóng.
- **Tab Persistence**: Ghi nhớ tab đang truy cập khi chuyển đổi.

### 2. Tab Biểu mẫu (Professional CMS Layout - v27.0)
- **Thay thế Modal**: Mọi thao tác Thêm/Sửa sẽ diễn ra trong Tab "BIỂU MẪU" với không gian rộng rãi.
- **Cấu trúc Bất đối xứng (70/30)**: Thay thế grid đơn giản bằng bố cục Dashboard chuyên nghiệp.
    - **Cột Chính (70%)**: Chứa Card "Thông tin sản phẩm" và Card "Truyền thông" (Upload ảnh lớn làm điểm nhấn).
    - **Sidebar (30%)**: Chứa Card "Hệ thống" (ID Sản phẩm, Giá) và Card "Vận chuyển/Shop".
- **Visual Hierarchy**: Sử dụng Card-based UI với layered shadows, bo góc 16px và typography phân cấp rõ rệt.

## 🧩 Các thành phần UI chi tiết

### 1. Data Viewport (Vùng dữ liệu)
- **Horizontal Scrolling**: Cố định cột "Thao tác" và "Tên sản phẩm".

### 2. Dynamic Forms (Tab-based)
- **Product Type Selection**: Popup xác nhận "Dropbuy / Non-Dropbuy" trước khi nhảy sang Tab Biểu mẫu.
- **Pre-fetch ID Tức thì**: Gọi API lấy mã ID (Nxx hoặc Dropbuy) ngay khi khởi tạo tab để điền sẵn cho người dùng.
- **Context Awareness**: Tab Biểu mẫu tự động thay đổi cấu trúc trường dựa trên Sheet mục tiêu đang làm việc.
- **Back Navigation**: Nút "Hủy" hoặc sau khi "Lưu" sẽ đưa người dùng quay lại Tab sản phẩm trước đó.
