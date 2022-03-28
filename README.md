# quan-ly-diem-danh
## 1. Mục tiêu
Ứng dụng hỗ trợ giảng viên điểm danh sinh viên trong các buổi học trực tuyến bằng nhận diện khuôn mặt.
## 2. Các thư viện và công nghệ được sử dụng
### 2.1. Các thư viện được sử dụng cho việc thiết kế giao diện
- tkinter: Thư viện GUI tiêu chuẩn của Python.
- tkcalendar: Thư viện hỗ trợ việc chọn ngày.
- PIL: Thư viện xử lý hình ảnh.
### 2.2. Các thư viện được sử dụng cho việc xuất file
- pandas: Thư viện mã nguồn mở cho phép thực hiện thao tác và phân tích dữ liệu.
- openpyxl: Thư viện để xử lý file các file Excel.
### 2.3. Các thư viện được sử dụng cho việc nhận diện
- numpy: Thư viện toán học mạnh mẽ và được sử dụng rộng rãi.
- opencv: Thư viện mã nguồn mở cho xử lý về thị giác máy tính.
- face_recognition: Thư viện nhận diện khuôn mặt.
### 2.4. Một số thư viện và module khác
- os và shutil: Cung cấp các chức năng được sử dụng để tương tác với hệ điều hành.
- sqlite3: Dữ liệu sẽ được lưu trong 1 CSDL SQLite và ta cần module này để kết nối và thao tác với CSDL. 
- time: Cho phép xử lý các tác vụ liên quan đến thời gian.
- re: Làm việc với biểu thức chính quy (Regular Expression).
- io: Cung cấp các phương tiện chính để xử lý các loại I/O khác nhau.
- locale: Giúp giải quyết vấn đề ngôn ngữ.
## 3. Các chức năng chính
### 3.1. Sinh viện
- Xem danh sách sinh viên và thông tin của từng sinh viên.
- Thêm/Sửa/Xóa thông tin sinh viên.
### 3.2. Nhận diện
- Nhập các ảnh màn hình có các khuôn mặt sinh viên để nhận diện.
- Sau khi bấm nút 'Xác nhận', thông tin điểm danh sẽ được lưu.
### 3.3. Điểm danh
- Cho phép thay đổi các thông tin liên quan đến thông tin điểm danh gần nhất.
  - Điểm danh bù.
  - Xóa điểm danh.
### 3.4. Thống kê.
- Xem thông tin điểm danh trong toàn bộ khóa học.
- Xuất file thống kê với 2 định dạng là csv và xlsx.
## 4. Các thành viên
- Bùi Tiến Dũng
- Trần Thế Nam
- Phạm Vũ Anh Quân
