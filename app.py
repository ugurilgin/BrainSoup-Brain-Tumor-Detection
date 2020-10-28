from flask import Flask
from flask import request
from flask import render_template
from flask_mail import Mail,Message

app=Flask(__name__,template_folder='templates')

usermail="infobrainsoup@gmail.com"
userpassword="BraiN2020TumordetectSouP1994"
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']=usermail
app.config['MAIL_PASSWORD']=userpassword
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mail=Mail(app)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/register')
def signup():
    return render_template('register.html')
@app.route('/braintumordetect')
def tumor():
    return render_template('braintumordetect.html')
@app.route('/form',methods=['POST'])
def form():
    name=request.form.get("name")
    email=request.form.get("email")
    subject=request.form.get("subject")
    msg=request.form.get("message")
    full_message="Maili Gönderinin \n  Adı:"+name+" \n Mail Adresi: "+email+" \n Mail Konusu:"+subject+" \n Maili:"+msg
    message=Message(email+" 'dan gelen  "+subject+" Maili",sender=usermail,recipients=[usermail])
    message.body=full_message
    mail.send(message)
    return render_template('response.html')

#test
"""@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()"""
if __name__ == "__main__":
    app.run(host='0.0.0.0',port='8888')