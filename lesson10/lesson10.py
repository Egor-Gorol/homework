import flask
from flask import request, render_template, redirect, url_for
app = flask.Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/services')
def services():
    offerings = {
        'Web Development': ['Frontend', 'Backend', 'Full Stack'],
        'Data Science': ['Data Analysis', 'Machine Learning', 'Visualization'],
        'Digital Marketing': ['SEO', 'Content Marketing', 'Social Media']
    }
    return render_template('services.html', offerings=offerings)


app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)