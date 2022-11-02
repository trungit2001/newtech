# Run project?
## 0. Cài đặt môi trường:
⚠️ Thực hiện ở thư mục gốc của git này `(./root)`
```python
python -m venv env
env\Scripts\activate
python -m pip install -r requirements.txt
```
⚠️ Chuyển thư mục làm việc vào thư mục chứa project này trước khi chạy các lệnh tiếp theo (dùng lệnh `cd`)
***
## 1. Tạo database trước bằng lệnh sau:
Khởi tạo database và insert một số dữ liệu có sẵn trong thư mục `data`. Thực hiện bằng cách chạy lệnh dưới đây
```python
python database.py
```
Sau khi chạy, một database có tên như trong file `settings.py` sẽ được tạo tại thư mục hiện tại (`working dir`) và database cũng đã có dữ liệu, tiếp hành truy vấn. Nếu lần sau chạy lại, cần phải xác nhận để xóa database cũ.
***
## 2. Chạy file main:
Toàn bộ câu truy vấn trong bài tập được thực hiện tại file `main.py`. Chạy bằng lệnh dưới và xem kết quả thực hiện truy vấn dữ liệu tương ứng theo từng bài tập.
```python
python main.py
```