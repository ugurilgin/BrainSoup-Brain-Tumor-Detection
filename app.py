############## < Import Files > ##############

from flask import Flask
from flask import request
from flask import render_template,redirect,url_for,session
from flask_mail import Mail,Message
from flask_mysqldb import  MySQL
import os
import secrets
from datetime import date
#import mysql.connector
############## </ Import Files > ##############

app=Flask(__name__,template_folder='templates')
app.secret_key=os.urandom(24)
############## < Mail Information > ##############
usermail="infobrainsoup@gmail.com"
userpassword="BraiN2020TumordetectSouP1994"
############## </ Mail Information > ##############

############## < App Settings > ##############
############## < MySQL Settings > ##############
#conn=mysql.connector.connect(host="127.0.0.1",user="root",password="",database="brainsoup",use_pure=False)
#cursor=conn.cursor()
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "brainsoup"
############## </MySQL Settings > ############## 
############## < Mail Settings > ##############
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']=usermail
app.config['MAIL_PASSWORD']=userpassword
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
############## </Mail Settings > ############## 

############## </ App Settings > ##############

mail=Mail(app)
mysql=MySQL(app)
@app.route('/')
def index():
    if 'user_auth' in session:
        
        return render_template('index.html',isim=openName,menu="menu")
    else:
        return render_template('index.html')
@app.route('/terms')
def terms():
    return render_template('terms.html')
@app.route('/privacy')
def privacy():
    return render_template('privacy.html')
@app.route('/login')
def login():
    if 'user_auth' in session:
        return redirect(url_for('index'))
    else:
        return render_template('login.html')
@app.route('/register')
def signup():
    if 'user_auth' in session:
        return redirect(url_for('index'))
    else:
        return render_template('register.html')
@app.route('/AddPatients')
def showAddPatients():
    if 'user_auth' in session:
        return render_template('patientsadd.html',isim=openName,menu="menu")
    else:
        return redirect(url_for('login'))
@app.route('/profile')
def profile():
    if 'user_auth' in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM `users` WHERE `email` LIKE  %(email)s  ",{'email': userName}) 
        users=cursor.fetchall()
        return render_template('profile.html',isim=users[0][1],name=users[0][1],surname=users[0][2],email=users[0][3],password=users[0][4],menu="menu")
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    if 'user_auth' in session:
        session.pop('user_auth')
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))
@app.route('/braintumordetect')
def tumor():
    if 'user_auth' in session:
        return render_template('braintumordetect.html',menu="menu")
    else:
        return redirect(url_for('login'))
@app.route('/loginValidation',methods=['POST'])
def login_Validation():
    email=request.form.get("email")
    password=request.form.get("password")
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM `users` WHERE `email` LIKE %(email)s AND `password` LIKE %(password)s AND `ban` LIKE '0' ",{'email': email,'password':password})

    users=cursor.fetchall()
    if len(users)>0:
        global userName
        global openName
        global doctor
        session['user_auth']=users[0][6]
        doctor=users[0][6]
        userName=users[0][3]
        openName=users[0][1]
        print(userName)
        return redirect(url_for('index'))
        
    else:
        return render_template('login.html',error="E-Mail veya Şifre Hatalı")

@app.route('/addPatients',methods=['POST'])
def add_Patients():
    email=request.form.get("email")
    tcno=request.form.get("tcno")
    birth=request.form.get("birth")
    today=date.today()
    name=request.form.get("name")
    surname=request.form.get("surname")
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM `patients` WHERE `TC` LIKE %(tcno)s ",{'tcno': tcno})
    users=cursor.fetchall()
    if len(users)>0:
        return render_template('patientsadd.html',error="Bu Hasta Zaten Kayıtlı")
    else:
        cursor.execute("INSERT INTO `patients` (`TC`,`name`,`surname`,`email`,`birthdate`,`date`,`doctor`,`ban`) VALUES( %(TC)s,%(name)s,%(surname)s,%(email)s,%(birthdate)s,%(date)s,%(doctor)s,%(ban)s)",{'TC': tcno,'name':name,'surname':surname,'email':email,'birthdate':birth,'date':today,'doctor':doctor,'ban':'0'})  
        mysql.connection.commit()
        return redirect(url_for('showAddPatients'))

@app.route('/addUser',methods=['POST'])
def add_User():
    email=request.form.get("email")
    password=request.form.get("password")
    name=request.form.get("name")
    surname=request.form.get("surname")
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM `users` WHERE `email` LIKE %(email)s ",{'email': email})
    users=cursor.fetchall()
    if len(users)>0:
        return render_template('register.html',error="Bu E-Mail Adresiyle Üye Zaten Kayıtlı")
    else:
        cursor.execute("INSERT INTO `users` (`name`,`surname`,`email`,`password`,`ban`,`user_auth`) VALUES( %(name)s,%(surname)s,%(email)s,%(password)s,%(ban)s,%(user_auth)s)",{'name': name,'surname':surname,'email':email,'password':password,'ban':'0','user_auth':secrets.token_hex()})  
        mysql.connection.commit()
        return redirect(url_for('login'))
        
@app.route('/updateUser',methods=['POST'])
def update_User():
    email=userName
    password=request.form.get("password")
    name=request.form.get("name")
    surname=request.form.get("surname")
    cursor = mysql.connection.cursor()
    if 'Update' in request.form:
        try:
            cursor.execute("UPDATE `users`  SET `name` = %(name)s ,`surname` = %(surname)s,`password` = %(password)s WHERE `email` = %(email)s",{'name': name,'surname':surname,'password':password,'email':email})  
            mysql.connection.commit()
            return redirect(url_for('profile'))
        except:
            return render_template('profile.html',error="Kayıt Güncellenemedi")  
    elif 'Delete' in request.form:
        try:
            cursor.execute("UPDATE `users`  SET `ban` = '1'  WHERE `email` = %(email)s",{'email':email})  
            mysql.connection.commit()
            session.pop('user_auth')
            return redirect(url_for('index'))
        except:
            return render_template('profile.html',error="Kayıt Silinemedi")   
    else:
        pass
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





if __name__ == "__main__":
    app.run(host='0.0.0.0',port='5000')
