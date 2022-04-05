from flask import Flask,render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('Search Page.html')

if __name__=="_main_":
    app.run(debug=True)

