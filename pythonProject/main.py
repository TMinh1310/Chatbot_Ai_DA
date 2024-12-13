from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def hello():
    if request.method == "GET":
        return render_template('index.html')
    else:
        # Lấy thông tin từ form
        user_message = request.form['user_message']
        noidungchathientai = request.form['chat_content']

        # Gửi POST request đến Rasa
        try:
            r = requests.post(
                'http://127.0.0.1:5005/webhooks/rest/webhook',
                json={"sender": "test", "message": user_message}
            )
            response_data = r.json()  # Chuyển phản hồi thành JSON
            print(response_data)  # Debug: In nội dung phản hồi

            # Xử lý nội dung phản hồi
            noidungchathientai += f"\n[BẠN]: {user_message}"

            if response_data and isinstance(response_data, list) and "text" in response_data[0]:
                bot_response = response_data[0]["text"]
            else:
                bot_response = "Không nhận được phản hồi hợp lệ từ BOT."

            noidungchathientai += f"\n[BOT]: {bot_response}"

        except (requests.exceptions.RequestException, IndexError, KeyError, ValueError) as e:
            print(f"Lỗi khi gửi hoặc xử lý phản hồi từ Rasa: {e}")
            noidungchathientai += "\n[BOT]: Lỗi phản hồi từ server."

        # Trả về nội dung tới giao diện người dùng
        return render_template('index.html', noidungchathientai=noidungchathientai)


# Chạy server Flask
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)