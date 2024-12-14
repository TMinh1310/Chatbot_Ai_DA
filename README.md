
# Project Chat_bot_AI




## Mô tả về project

- đề tài : thiết kế chatbot ai với chức năng trả lời câu hỏi của người dùng về những kiến thức thiết kế IC tương tự ( dựa trên cuốn sách " Thiết kế IC tương tự " của cô Phạm Nguyễn Thanh Loan
- Database: "Design of Analog CMOS Intergrated Circuits” của Behzad Razavi. ​
- Thời gian phản hồi của chatbot: Nhanh, từ 1 tới 2 giây.​
- Mức độ chính xác của nội dung phản hồi: Cao, dữ liệu khớp 100% với Database.


## Cấu trúc hệ thống
- cấu trúc : Chatbot xây dựng dựa trên framework Rasa
  đây là sơ đồ cấu trúc của hệ thống:
  Sơ đồ tổng quát.png

## Hướng dẫn cài đặt
Cách cài đặt và sử dụng Chatbot_Ai : 

B1: Download tải tất cả các thư mục về máy tính.

B2: Mở file trên Pycharm ( không nên sử dụng Visual studio vì Pycharm tối ưu và dễ dàng cài đặt hơn )  

B3: Cài đặt tất cả các thư viện cần thiết tại file requirement.txt.

B4: cập nhật tên database, username và password để kết nối với file sql trong phần "tracker store".

B5: Mở 3 terminal khác nhau, nhập 3 lệnh sau:.
Tại terminal 1: rasa run -m models --enable-api --cors "*" --debug. ( bật api của rasa ) 
Tại terminal 2: rasa run actions. ( khởi chạy file actions )
Tại terminal 3: python run main.py. ( chạy gia diện web ) 
mở url của local web lên và sử dụng.
