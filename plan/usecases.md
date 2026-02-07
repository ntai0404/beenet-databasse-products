# User Experience Scenarios (Usecases) - SpentCMS 2.0

Tài liệu này mô tả các tình huống thực tế mà người quản trị (CTV) sẽ thực hiện trên SpentCMS 2.0, minh họa sức mạnh của giao diện động và các tính năng thông minh.

---

## 📑 1. Điều hướng & Quản lý Danh mục (Smart Inventory)
- **Tình huống**: Quản trị viên cần tìm và cập nhật kho hàng trong hàng chục danh mục sản phẩm (sheets).
- **Quy trình**:
    1. Sử dụng **Quick Search** trên Sidebar để lọc danh mục theo từ khóa.
    2. Click vào danh mục mục tiêu (Ví dụ: "Balo - Túi xách").
    3. Hệ thống ghi nhớ tab đang mở (Tab Persistence) giúp quay lại nhanh chóng sau khi chỉnh sửa.
- **Giá trị**: Giảm 80% thời gian tìm kiếm sheet so với thao tác trên Google Sheets thuần túy.

## ➕ 2. Thêm Sản phẩm Mới (Optimized Data Entry)
- **Tình huống**: CTV nhập sản phẩm mới với yêu cầu nhanh và chính xác nhất.
- **Quy trình**:
    1. Nhấn **"THÊM MỚI SẢN PHẨM"**.
    2. **Xác nhận loại**: Chọn "Dropbuy" hoặc "Non-Dropbuy" (Popup thông minh).
    3. **Auto-ID Logic**: Hệ thống tự động tính toán và điền mã ID (Ví dụ: `N42`) dựa trên dữ liệu hiện có trong sheet.
    4. **Smart Form**:
        - `Link Zalo` & `Link NV`: Tự động điền theo cấu hình mặc định.
        - `Địa chỉ`: Chọn 3 cấp từ dropdown (Tỉnh -> Quận -> Phường).
        - `Hình ảnh`: Multiselect và xem trước trong gallery trực quan.
    5. Nhấn **"LƯU"**.
- **Giá trị**: Chuẩn hóa dữ liệu ngay từ đầu, loại bỏ hoàn toàn lỗi typos (lỗi gõ tay).

## 🖼️ 3. Quản lý Đa phương thức (Multiple Media Management)
- **Tình huống**: Một sản phẩm cần hiển thị nhiều góc độ ảnh (Gallery) thay vì 1 ảnh duy nhất.
- **Quy trình**:
    1. Tại tab "BIỂU MẪU", nhấn **"+ THÊM ẢNH"**.
    2. Chọn 3-5 ảnh sản phẩm cùng lúc.
    3. Hệ thống hiển thị dưới dạng **Gallery Grid**. CTV có thể xóa vĩnh viễn những ảnh không ưng ý trước khi gửi.
    4. Cloudinary tự động xử lý và lưu trữ URLs bảo mật.
- **Giá trị**: Tăng tính chuyên nghiệp cho UI Web bán hàng, tối ưu dung lượng hiển thị.

## ✏️ 4. Hiệu chỉnh & Cập nhật (Dynamic Edit Flow)
- **Tình huống**: Cập nhật giá khuyến mãi hoặc địa chỉ kho cho một sản phẩm hiện có.
- **Quy trình**:
    1. Nhấn icon **Sửa** (✏️) trên hàng dữ liệu tương ứng.
    2. Hệ thống chuyển sang tab **"BIỂU MẪU"**, tự động phân tách chuỗi ảnh `|` thành Gallery và load đúng cấp địa chỉ từ GSheet.
    3. CTV thực hiện thay đổi và nhấn **"Cập nhật"**.
- **Giá trị**: Trải nghiệm chỉnh sửa mượt mà như một ứng dụng native (Native-like experience).

## 🗑️ 5. Quản lý Xóa dữ liệu (Safe Deletion)
- **Tình huống**: Loại bỏ sản phẩm hết hàng hoặc thông tin sai lệch.
- **Quy trình**:
    1. Nhấn icon **Xóa** (🗑️).
    2. Popup xác nhận xuất hiện để tránh thao tác nhầm.
    3. Xác nhận xóa -> Dòng biến mất tức thì trên Web và bị xóa thực tế trong Google Sheet.
- **Giá trị**: Đảm bảo an toàn dữ liệu, tránh mất mát thông tin ngoài ý muốn.
