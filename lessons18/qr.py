from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_url = None
    if request.method == 'POST':
        user_text = request.form['text']
        if user_text:
            qr_url = f'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={user_text}'
    return render_template('index.html', qr_url=qr_url)

if __name__ == '__main__':
    app.run(debug=True)
