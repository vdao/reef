from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object('websiteconfig')

@app.route('/')
def hello_world():
    return 'Hello World! yyyyy'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404