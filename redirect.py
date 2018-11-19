from flask import Flask, redirect
from waitress import serve
app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return redirect('http://45.76.61.64:8080/')

if __name__ == '__main__':
    serve(app, listen="0.0.0.0:8080")
