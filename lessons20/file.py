from flask import Flask, render_template, request
import os


app = Flask(__name__)
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('upload.html')
    
    user_file = request.files.get('file')
    file_path = os.path.join(UPLOAD_FOLDER, user_file.filename)
    user_file.save(file_path)
    
    with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
    return render_template('upload.html', file_content=content)


if __name__ == '__main__':
    app.run(debug=True)
