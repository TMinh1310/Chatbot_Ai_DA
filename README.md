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
