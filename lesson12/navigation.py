import flask
from flask import request, render_template, redirect, url_for


app = flask.Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/countrise')
def countrise():
    place = {
        'Італія': ['Рим', 'Венеція', 'Флоренція'],
        'Франція': ['Париж', 'Ліон', 'Марсель'],
        'Японія': ['Токіо', 'Кіото', 'Осака']
    }
    return render_template('countrise.html',  place=place)
     

if __name__ == '__main__':
    app.run(debug=True)


  
