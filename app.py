from flask import Flask
from flask import request
from flask import render_template

app=Flask(__name__,template_folder='templates')
@app.route('/')
def index():
    return render_template('index.html')
#test
"""@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()"""
