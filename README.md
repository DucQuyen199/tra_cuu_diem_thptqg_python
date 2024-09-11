# Tra Cứu Điểm Thi Trung Học Phổ Thông Quốc Gia

## Mô tả dự án

Ứng dụng này là một trang web đơn giản, sử dụng Flask để tra cứu điểm thi THPT Quốc gia từ cơ sở dữ liệu SQL Server. Người dùng có thể nhập Số Báo Danh (SBD) để truy vấn điểm số các môn thi.

## Các tính năng chính

- Kết nối đến cơ sở dữ liệu SQL Server.
- Tra cứu điểm thi dựa trên Số Báo Danh (SBD).
- Định dạng điểm số phù hợp:
  - Điểm > 100: chia cho 100.
  - Điểm từ 10 đến 100: chia cho 10.
  - Điểm < 10: giữ nguyên.
- Hiển thị kết quả trên giao diện người dùng.

## Yêu cầu hệ thống

- Python 3.x
- Flask
- pyodbc
- SQL Server (bạn cần một cơ sở dữ liệu SQL Server đang hoạt động)

## Cài đặt

### 1. Clone dự án về máy

```bash
git clone https://github.com/DucQuyen199/tra_cuu_diem_thptqg_python.git
cd tra_cuu_diem_thptqg_python
```

### 2. Tạo môi trường ảo (tùy chọn nhưng được khuyến khích)

```bash
python -m venv venv
source venv/bin/activate  # Trên Windows: venv\Scripts\activate
```

### 3. Cài đặt các thư viện cần thiết

```bash
pip install -r requirements.txt
```

> Nếu không có file `requirements.txt`, bạn có thể cài đặt thủ công như sau:
```bash
pip install Flask pyodbc
```

### 4. Cấu hình kết nối đến SQL Server

Trong mã nguồn `app.py`, hàm `get_db_connection()` đã được cấu hình để kết nối đến SQL Server. Bạn cần kiểm tra và thay đổi các thông tin sau cho phù hợp với cấu hình của bạn:

```python
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost;'
    'DATABASE=thptqg24;'
    'UID=sa;'
    'PWD=123456aA@$'
)
```

- `SERVER`: Thay đổi thành địa chỉ server của bạn.
- `DATABASE`: Tên cơ sở dữ liệu bạn đang sử dụng.
- `UID`: Tên người dùng SQL Server.
- `PWD`: Mật khẩu của tài khoản SQL Server.

### 5. Khởi chạy ứng dụng

Sau khi hoàn tất cấu hình, bạn có thể khởi động ứng dụng Flask:

```bash
python app.py
```
Ứng dụng sẽ chạy trên `http://localhost:5000`.

## Sử dụng

- Truy cập `http://localhost:5000` trên trình duyệt của bạn.
- Nhập Số Báo Danh (SBD) và nhấn `Tra cứu` để xem kết quả điểm thi.

## Đóng góp

Nếu bạn muốn đóng góp vào dự án này, vui lòng tạo một pull request hoặc mở một issue trên GitHub.

## License

Dự án này được phân phối theo giấy phép MIT. Xem chi tiết trong file LICENSE.
