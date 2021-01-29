############## < Import Files > ##############

from flask import Flask
from flask import request ,jsonify
from flask import flash
from flask import render_template,redirect,url_for,session
from flask_mail import Mail,Message
from flask_mysqldb import  MySQL
import os
import secrets
from datetime import date
from EMail import  EMail
from Host import Host
import hashlib
from werkzeug.utils import secure_filename
from TumorExtractor import TumorExtractor
#import mysql.connector
############## </ Import Files > ##############
UPLOAD_FOLDER = 'static/uploads/input/'
ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg'}
app=Flask(__name__,template_folder='templates')
app.secret_key=os.urandom(24)
myMail=EMail()
myHost=Host()

############## < App Settings > ##############
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

############## < MySQL Settings > ##############

app.config['MYSQL_HOST'] = myHost.hostName #"localhost"
app.config['MYSQL_USER'] = myHost.hostUser#"root"
app.config['MYSQL_PASSWORD'] = myHost.hostPassword#""
app.config['MYSQL_DB'] = myHost.hostDB#"brainsoup"
############## </MySQL Settings > ############## 
############## < Mail Settings > ##############
app.config['MAIL_SERVER']=myMail.mailServer     #'smtp.gmail.com'
app.config['MAIL_PORT']=myMail.mailPort         #465
app.config['MAIL_USERNAME']=myMail.userName     #usermail
app.config['MAIL_PASSWORD']=myMail.userPassword #userpassword
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
############## </Mail Settings > ############## 

############## </ App Settings > ##############

############## < Web Assitant Pages > ########################################################################

mail=Mail(app)
mysql=MySQL(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/braintumordetect')
def tumor():
    if 'user_auth' in session:
        return render_template('braintumordetect.html',isim=openName,menu="menu",admin=adminstatus)
    else:
        return redirect(url_for('login'))
@app.route('/uploadTumor',methods=['POST'])
def uploadTumorFile():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Seçili Dosya Yok')
            return redirect(url_for('index'))
        file = request.files['file']
        if file.filename == '':
            flash('Seçili Dosya Yok')
            return redirect(url_for('index'))
        if file and allowed_file(file.filename):
            today=date.today()
            filename = secure_filename(file.filename)
            name=secrets.token_hex()
            fullname=name+"."+filename.rsplit('.', 1)[1].lower()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], fullname))
            a=TumorExtractor(os.path.join(app.config['UPLOAD_FOLDER'], fullname),name)
            out=a.predict()
            inimage="uploads/input/"+name+".jpg"
            if (out=="Pozitif"):
                outimage="uploads/output/yes/"+name+".jpg"
            else:
                outimage="uploads/output/no/"+name+".jpg"
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM `tumor` WHERE `TC` LIKE '00000000000' AND `ban` LIKE '1'  AND `doctor` LIKE  %(doctor)s  ",{'doctor': doctor})
            users=cursor.fetchall()
            if len(users)>0:
                cursor.execute("UPDATE `tumor`  SET `imgloc` = %(imgloc)s ,`tumorloc` = %(tumorloc)s,`result` = %(result)s WHERE `ban` = '1' AND  `TC` = '00000000000' AND `doctor` LIKE  %(doctor)s",{'imgloc': inimage,'tumorloc':outimage,'result':out,'doctor':doctor})  
                mysql.connection.commit()
                return redirect(url_for('resultTumor'))
            else:
                cursor.execute("INSERT INTO `tumor` (`TC`,`date`,`imgloc`,`tumorloc`,`doctor`,`result`,`ban`) VALUES( %(TC)s,%(date)s,%(imgloc)s,%(tumorloc)s,%(doctor)s,%(result)s,%(ban)s)",{'TC': '00000000000','date':str(today),'imgloc':inimage,'tumorloc':outimage,'doctor':doctor,'result':out,'ban':'1'})  
                mysql.connection.commit()
                return redirect(url_for('resultTumor'))
            
@app.route('/result')
def resultTumor():
    if 'user_auth' in session:
        global rTumor
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT imgloc,tumorloc,result FROM `tumor` WHERE `TC` LIKE '00000000000' AND `ban` LIKE '1' AND `doctor` LIKE  %(doctor)s  ",{'doctor': doctor}) 
        data=cursor.fetchall()
        if(len(data)>0):
            rTumor=data
            return render_template('result.html',isim=openName,menu="menu",admin=adminstatus,image=data[0][0],tumor=data[0][1],result=data[0][2])
        else:
            return redirect(url_for('tumor'))
    else:
        return redirect(url_for('login'))
@app.route('/AddTumor',methods=['POST'])
def addTumor():
    tc=request.form.get("tcno")
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM `patients` WHERE `TC` LIKE %(TC)s AND `doctor` LIKE %(doctor)s ",{'TC': tc,'doctor': doctor})
    users=cursor.fetchall()
    print(len(users))
    if len(users)<=0:
        return render_template('result.html',isim=openName,menu="menu",admin=adminstatus,image=rTumor[0][0],tumor=rTumor[0][1],result=rTumor[0][2],error="Hata: Bu TC Kimlik Nosuna Sahip Hasta Bulunamadı")
    else:
        cursor.execute("UPDATE `tumor`  SET `TC` = %(tc)s ,`cinsiyet` = %(cinsiyet)s,`birthdate` = %(birthdate)s,`ban` = %(ban)s WHERE `ban` = '1' AND  `TC` = '00000000000' AND `doctor` LIKE  %(doctor)s",{'tc': tc,'cinsiyet':users[0][9],'birthdate':users[0][5],'ban':'0','doctor':doctor})   
        mysql.connection.commit()
        return render_template('result.html',isim=openName,menu="menu",admin=adminstatus,image=rTumor[0][0],tumor=rTumor[0][1],result=rTumor[0][2],error="MR Sonucu Başarılı Bir Şekilde Kaydedildi.",link="a")
@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM `about` WHERE `id`='1' ")  
    indexdetail=cursor.fetchone()
    cursor.execute("SELECT * FROM `whous` WHERE `id`='1' ")  
    aboutdetail=cursor.fetchone()
    if 'user_auth' in session:
        return render_template('index.html',aboutdetail=aboutdetail,indexdetail=indexdetail,isim=openName,menu="menu",admin=adminstatus)
    else:
        return render_template('index.html',aboutdetail=aboutdetail,indexdetail=indexdetail)
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
@app.route('/resetpass',defaults={'key':'default'})
@app.route('/resetpass/<key>')
def resetpass(key):
    global changepass
    if key=="default":
        return render_template('reset.html',key=key)
    else:
        changepass=key
        return render_template('reset.html',key=key)
@app.route('/register')
def signup():
    if 'user_auth' in session:
        return redirect(url_for('index'))
    else:
        return render_template('register.html')

@app.route('/MRDetails' ,defaults={'id':'default'})
@app.route('/MRDetails/<id>')
def MRDetails(id):
    if 'user_auth' in session:
        if (id !="default"):
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM `tumor` WHERE `id` LIKE %(id)s AND `ban` LIKE '0' AND `doctor` LIKE  %(doctor)s  ",{'id': str(id),'doctor': doctor}) 
            tumordata=cursor.fetchone()
            if tumordata is None:
                return redirect(url_for('showViewMR'))
            else:
                tc=str(tumordata[1])
                
            cursor.execute("SELECT * FROM `patients` WHERE `TC` LIKE %(tc)s AND `ban` LIKE '0' AND `doctor` LIKE  %(doctor)s  ",{'tc': tc,'doctor': doctor}) 
            patientdata=cursor.fetchone()
            if len(patientdata)>0:
                return render_template('detailmr.html',isim=openName,menu="menu",admin=adminstatus,tumor=tumordata,patients=patientdata)
            else:
                return redirect(url_for('showViewMR'))
        else:
            return redirect(url_for('showViewMR'))
    else:
        return redirect(url_for('login'))
@app.route('/ViewPatients')
def showviewPatients():

    if 'user_auth' in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT count(`TC`) FROM `patients` WHERE `ban` LIKE '0' AND `doctor` LIKE  %(doctor)s  ",{'doctor': doctor}) 
        countpatients=cursor.fetchone()
        cursor.execute("SELECT count(`TC`) FROM `patients` WHERE `cinsiyet` LIKE 'Erkek' AND `ban` LIKE '0' AND `doctor` LIKE  %(doctor)s  ",{'doctor': doctor}) 
        male=cursor.fetchone()
        cursor.execute("SELECT count(`TC`) FROM `patients` WHERE `cinsiyet` LIKE 'Kadın' AND `ban` LIKE '0' AND `doctor` LIKE  %(doctor)s  ",{'doctor': doctor}) 
        female=cursor.fetchone()
        cursor.execute("SELECT count(`TC`) FROM `patients` WHERE TIMESTAMPDIFF(YEAR, `birthdate`, NOW())<18 AND `ban` LIKE '0' AND `doctor` LIKE  %(doctor)s  ",{'doctor': doctor}) 
        age1=cursor.fetchone()
        cursor.execute("SELECT count(`TC`) FROM `patients` WHERE TIMESTAMPDIFF(YEAR, `birthdate`, NOW())>=18 AND TIMESTAMPDIFF(YEAR, `birthdate`, NOW())<30 AND `ban` LIKE '0' AND `doctor` LIKE  %(doctor)s  ",{'doctor': doctor}) 
        age2=cursor.fetchone()
        cursor.execute("SELECT count(`TC`) FROM `patients` WHERE TIMESTAMPDIFF(YEAR, `birthdate`, NOW())>=30 AND TIMESTAMPDIFF(YEAR, `birthdate`, NOW())<65 AND `ban` LIKE '0' AND `doctor` LIKE  %(doctor)s  ",{'doctor': doctor}) 
        age3=cursor.fetchone()
        cursor.execute("SELECT count(`TC`) FROM `patients` WHERE TIMESTAMPDIFF(YEAR, `birthdate`, NOW())>=65  AND `ban` LIKE '0' AND `doctor` LIKE  %(doctor)s  ",{'doctor': doctor}) 
        age4=cursor.fetchone()
        cursor.execute("SELECT TC,name,surname,email,birthdate,date,cinsiyet FROM `patients` WHERE `ban` LIKE '0' AND `doctor` LIKE  %(doctor)s  ",{'doctor': doctor}) 
        data=cursor.fetchall()
        return render_template('patientsview.html',isim=openName,menu="menu",admin=adminstatus,data=data,sumpatient=countpatients[0],negative=male[0],possitive=female[0],male=male[0],female=female[0],age1=age1[0],age2=age2[0],age3=age3[0],age4=age4[0])
    else:
        return redirect(url_for('login'))
@app.route('/deleteReport',methods=['POST'])
def deleteReport():
    tc=request.form.get("tc")
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE `tumor`  SET `ban` = %(ban)s  WHERE `TC` = %(tc)s AND `doctor` = %(doctor)s ",{'ban':'1','tc': tc,'doctor':doctor})  
    mysql.connection.commit()
    return redirect(url_for('showViewMR'))
@app.route('/MRReports')
def showViewMR():
    if 'user_auth' in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT count(`TC`) FROM `tumor` WHERE `ban` LIKE '0' AND `doctor` LIKE  %(doctor)s  ",{'doctor': doctor}) 
        countpatients=cursor.fetchone()
        cursor.execute("SELECT count(`TC`) FROM `tumor` WHERE `result` LIKE 'Pozitif' AND `ban` LIKE '0' AND `doctor` LIKE  %(doctor)s  ",{'doctor': doctor}) 
        possitivepatients=cursor.fetchone()
        cursor.execute("SELECT count(`TC`) FROM `tumor` WHERE `result` LIKE 'Negatif' AND `ban` LIKE '0' AND `doctor` LIKE  %(doctor)s  ",{'doctor': doctor}) 
        negativepatients=cursor.fetchone()
        cursor.execute("SELECT count(`TC`) FROM `tumor` WHERE `cinsiyet` LIKE 'Erkek' AND `ban` LIKE '0' AND `doctor` LIKE  %(doctor)s  ",{'doctor': doctor}) 
        male=cursor.fetchone()
        cursor.execute("SELECT count(`TC`) FROM `tumor` WHERE `cinsiyet` LIKE 'Kadın' AND `ban` LIKE '0' AND `doctor` LIKE  %(doctor)s  ",{'doctor': doctor}) 
        female=cursor.fetchone()
        cursor.execute("SELECT count(`TC`) FROM `tumor` WHERE TIMESTAMPDIFF(YEAR, `birthdate`, NOW())<18 AND `ban` LIKE '0' AND `doctor` LIKE  %(doctor)s  ",{'doctor': doctor}) 
        age1=cursor.fetchone()
        cursor.execute("SELECT count(`TC`) FROM `tumor` WHERE TIMESTAMPDIFF(YEAR, `birthdate`, NOW())>=18 AND TIMESTAMPDIFF(YEAR, `birthdate`, NOW())<30 AND `ban` LIKE '0' AND `doctor` LIKE  %(doctor)s  ",{'doctor': doctor}) 
        age2=cursor.fetchone()
        cursor.execute("SELECT count(`TC`) FROM `tumor` WHERE TIMESTAMPDIFF(YEAR, `birthdate`, NOW())>=30 AND TIMESTAMPDIFF(YEAR, `birthdate`, NOW())<65 AND `ban` LIKE '0' AND `doctor` LIKE  %(doctor)s  ",{'doctor': doctor}) 
        age3=cursor.fetchone()
        cursor.execute("SELECT count(`TC`) FROM `tumor` WHERE TIMESTAMPDIFF(YEAR, `birthdate`, NOW())>=65  AND `ban` LIKE '0' AND `doctor` LIKE  %(doctor)s  ",{'doctor': doctor}) 
        age4=cursor.fetchone()
        cursor.execute("SELECT tumor.id,patients.TC,patients.name,patients.surname,patients.email,patients.birthdate,tumor.date,patients.cinsiyet FROM `patients` JOIN `tumor` ON patients.TC = tumor.TC WHERE tumor.ban LIKE '0' AND tumor.doctor LIKE  %(doctor)s  ",{'doctor': doctor}) 
        data=cursor.fetchall()
        return render_template('mrview.html',isim=openName,menu="menu",admin=adminstatus,data=data,sumpatient=countpatients[0],negative=negativepatients[0],possitive=possitivepatients[0],male=male[0],female=female[0],age1=age1[0],age2=age2[0],age3=age3[0],age4=age4[0])
    else:
        return redirect(url_for('login'))
@app.route('/AddPatients' ,defaults={'tc':'default'})
@app.route('/AddPatients/<tc>')
def showAddPatients(tc):
    global TCNo
    TCNo=tc
    if 'user_auth' in session:
        if TCNo=="default":
            return render_template('patientsadd.html',isim=openName,menu="menu",admin=adminstatus,tcno=tc)
        if TCNo!="default":
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT TC,name,surname,email,birthdate,cinsiyet FROM `patients` WHERE `TC` LIKE  %(TC)s AND `doctor` LIKE  %(doctor)s  ",{'TC': tc,'doctor':doctor}) 
            users=cursor.fetchall()
            return render_template('patientsadd.html',TCnosu=users[0][0],name=users[0][1],surname=users[0][2],email=users[0][3],birth=users[0][4],cinsiyet=users[0][5],isim=openName,menu="menu",admin=adminstatus,tcno=tc)
    else:
        return redirect(url_for('login'))
@app.route('/profile')
def profile():
    if 'user_auth' in session:
        today=date.today()
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM `users` WHERE `email` LIKE  %(email)s  ",{'email': userName}) 
        users=cursor.fetchall()
        cursor.execute("SELECT count(`TC`) FROM `tumor` WHERE `ban` LIKE '0' AND `doctor` LIKE  %(doctor)s  ",{'doctor': doctor}) 
        countpatients=cursor.fetchone()
        cursor.execute("SELECT count(`TC`) FROM `tumor` WHERE `result` LIKE 'Pozitif' AND `ban` LIKE '0' AND `doctor` LIKE  %(doctor)s  ",{'doctor': doctor}) 
        possitivepatients=cursor.fetchone()
        cursor.execute("SELECT count(`TC`) FROM `tumor` WHERE `result` LIKE 'Negatif' AND `ban` LIKE '0' AND `doctor` LIKE  %(doctor)s  ",{'doctor': doctor}) 
        negativepatients=cursor.fetchone()
        cursor.execute("SELECT count(`TC`) FROM `tumor` WHERE `cinsiyet` LIKE 'Erkek' AND `ban` LIKE '0' AND `doctor` LIKE  %(doctor)s  ",{'doctor': doctor}) 
        male=cursor.fetchone()
        cursor.execute("SELECT count(`TC`) FROM `tumor` WHERE `cinsiyet` LIKE 'Kadın' AND `ban` LIKE '0' AND `doctor` LIKE  %(doctor)s  ",{'doctor': doctor}) 
        female=cursor.fetchone()
        cursor.execute("SELECT count(`TC`) FROM `tumor` WHERE TIMESTAMPDIFF(YEAR, `birthdate`, NOW())<18 AND `ban` LIKE '0' AND `doctor` LIKE  %(doctor)s  ",{'doctor': doctor}) 
        age1=cursor.fetchone()
        cursor.execute("SELECT count(`TC`) FROM `tumor` WHERE TIMESTAMPDIFF(YEAR, `birthdate`, NOW())>=18 AND TIMESTAMPDIFF(YEAR, `birthdate`, NOW())<30 AND `ban` LIKE '0' AND `doctor` LIKE  %(doctor)s  ",{'doctor': doctor}) 
        age2=cursor.fetchone()
        cursor.execute("SELECT count(`TC`) FROM `tumor` WHERE TIMESTAMPDIFF(YEAR, `birthdate`, NOW())>=30 AND TIMESTAMPDIFF(YEAR, `birthdate`, NOW())<65 AND `ban` LIKE '0' AND `doctor` LIKE  %(doctor)s  ",{'doctor': doctor}) 
        age3=cursor.fetchone()
        cursor.execute("SELECT count(`TC`) FROM `tumor` WHERE TIMESTAMPDIFF(YEAR, `birthdate`, NOW())>=65  AND `ban` LIKE '0' AND `doctor` LIKE  %(doctor)s  ",{'doctor': doctor}) 
        age4=cursor.fetchone()
        return render_template('profile.html',isim=users[0][1],name=users[0][1],surname=users[0][2],email=users[0][3],password=users[0][4],menu="menu",admin=adminstatus,sumpatient=countpatients[0],negative=negativepatients[0],possitive=possitivepatients[0],male=male[0],female=female[0],age1=age1[0],age2=age2[0],age3=age3[0],age4=age4[0])
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    if 'user_auth' in session:
        session.pop('user_auth')
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/loginValidation',methods=['POST'])
def login_Validation():
    email=request.form.get("email")
    password=request.form.get("password")
    result = hashlib.md5(password.encode("utf-8")).hexdigest()
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM `users` WHERE `email` LIKE %(email)s AND `password` LIKE %(password)s AND `ban` LIKE '0' ",{'email': email,'password':result})

    users=cursor.fetchall()
    if len(users)>0:
        global userName
        global openName
        global doctor
        global adminstatus
        session['user_auth']=users[0][6]
        doctor=users[0][6]
        userName=users[0][3]
        openName=users[0][1]
        adminstatus=users[0][7]
        return redirect(url_for('index'))
        
    else:
        return render_template('login.html',error="E-Mail veya Şifre Hatalı")

@app.route('/addPatients',methods=['POST'])
def add_Patients():
    cursor = mysql.connection.cursor()

    if 'Update' in request.form:
        email=request.form.get("email")
        birth=request.form.get("birth")
        name=request.form.get("name")
        surname=request.form.get("surname")
        cinsiyet=request.form.get("cinsiyet")

        try:

            cursor.execute("UPDATE `patients`  SET `name` = %(name)s ,`surname` = %(surname)s,`email` = %(email)s,`birthdate` = %(birthdate)s ,`cinsiyet` = %(cinsiyet)s WHERE `TC` = %(TC)s AND `doctor` LIKE  %(doctor)s",{'name': name,'surname':surname,'email':email,'birthdate':birth,'TC':TCNo,'cinsiyet':cinsiyet,'doctor':doctor})  
            mysql.connection.commit()
            return render_template('patientsadd.html',error=" Hasta Bilgileri Başarılı Bir Şekilde Güncellendi.",link="a",isim=openName,menu="menu",admin=adminstatus) 
        except Exception as e:
            
            return render_template('patientsadd.html',error="Hata: Hasta Bilgileri Güncellenemedi ",isim=openName,menu="menu",admin=adminstatus,TCnosu=TCNo,name=name,surname=surname,email=email,birth=birth,cinsiyet=cinsiyet,tcno=TCNo) 
    elif 'Delete' in request.form:
        try:
            cursor.execute("UPDATE `patients`  SET `ban` = '1'  WHERE `TC` = %(TC)s",{'TC':TCNo})  
            mysql.connection.commit()
            return render_template('patientsadd.html',error=" Hasta Bilgileri Başarılı Bir Şekilde Silindi. ",link="a",isim=openName,menu="menu",admin=adminstatus) 

        except:
            return render_template('patientsadd.html',error="Kayıt Silinemedi",isim=openName,menu="menu",admin=adminstatus)   
    elif 'Add' in request.form:
        email=request.form.get("email")
        tcno=request.form.get("tcno")
        birth=request.form.get("birth")
        today=date.today()
        name=request.form.get("name")
        surname=request.form.get("surname")
        cinsiyet=request.form.get("cinsiyet")

        cursor.execute("SELECT * FROM `patients` WHERE `TC` LIKE %(tcno)s AND `doctor` LIKE  %(doctor)s ",{'tcno': tcno,'doctor':doctor})
        users=cursor.fetchall()
        if len(users)>0:
            return render_template('patientsadd.html',error="Bu Hasta Zaten Kayıtlı",isim=openName,menu="menu",tcno="default",admin=adminstatus)
        else:
            cursor.execute("INSERT INTO `patients` (`TC`,`name`,`surname`,`email`,`birthdate`,`date`,`doctor`,`ban`,`cinsiyet`) VALUES( %(TC)s,%(name)s,%(surname)s,%(email)s,%(birthdate)s,%(date)s,%(doctor)s,%(ban)s,%(cinsiyet)s)",{'TC': tcno,'name':name,'surname':surname,'email':email,'birthdate':birth,'date':today,'doctor':doctor,'ban':'0','cinsiyet':cinsiyet})  
            mysql.connection.commit()
            return render_template('patientsadd.html',error=" Hasta Bilgileri Başarılı Bir Şekilde Kaydedildi.",link="a",isim=openName,menu="menu",admin=adminstatus) 
    else:
        pass
@app.route('/addUser',methods=['POST'])
def add_User():
    email=request.form.get("email")
    password=request.form.get("password")
    name=request.form.get("name")
    surname=request.form.get("surname")
    result = hashlib.md5(password.encode("utf-8")).hexdigest()
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM `users` WHERE `email` LIKE %(email)s ",{'email': email})
    users=cursor.fetchall()
    if len(users)>0:
        return render_template('register.html',error="Hata: Bu E-Mail Adresiyle Üye Zaten Kayıtlı")
    else:
        cursor.execute("INSERT INTO `users` (`name`,`surname`,`email`,`password`,`ban`,`user_auth`,`admin`) VALUES( %(name)s,%(surname)s,%(email)s,%(password)s,%(ban)s,%(user_auth)s,%(admin)s)",{'name': name,'surname':surname,'email':email,'password':result,'ban':'0','user_auth':secrets.token_hex(),'admin':'0'})  
        mysql.connection.commit()
        return render_template('register.html',error="Kullanıcı Oluşturma İşlemi Başarıyla Tamamlandı. ",link="a")
        #return redirect(url_for('login'))

               
@app.route('/updateUser',methods=['POST'])
def update_User():
    email=userName
    password=request.form.get("password")
    name=request.form.get("name")
    surname=request.form.get("surname")
    result = hashlib.md5(password.encode("utf-8")).hexdigest()
    cursor = mysql.connection.cursor()
    if 'Update' in request.form:
        try:
            cursor.execute("UPDATE `users`  SET `name` = %(name)s ,`surname` = %(surname)s,`password` = %(password)s WHERE `email` = %(email)s",{'name': name,'surname':surname,'password':result,'email':email})  
            mysql.connection.commit()
            return redirect(url_for('profile'))
        except:
            return render_template('profile.html',error="Kayıt Güncellenemedi",isim=openName,menu="menu",admin=adminstatus,name=name,surname=surname,email=email,password=password)  
    elif 'Delete' in request.form:
        try:
            cursor.execute("UPDATE `users`  SET `ban` = '1'  WHERE `email` = %(email)s",{'email':email})  
            mysql.connection.commit()
            session.pop('user_auth')
            return redirect(url_for('index'))
        except:
            return render_template('profile.html',error="Kayıt Silinemedi",isim=openName,menu="menu",admin=adminstatus)   
    else:
        pass
@app.route('/form',methods=['POST'])
def form():
    name=request.form.get("name")
    email=request.form.get("email")
    subject=request.form.get("subject")
    msg=request.form.get("message")
    today=date.today()
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO `email` (`fullname`,`email`,`subject`,`message`,`date`,`ban`,`status`) VALUES( %(fullname)s,%(email)s,%(subject)s,%(message)s,%(date)s,%(ban)s,%(status)s)",{'fullname': name,'email':email,'subject':subject,'message':msg,'date':today,'ban':'0','status':'0'})    
    mysql.connection.commit()
    """full_message="Maili Gönderinin \n  Adı:"+name+" \n Mail Adresi: "+email+" \n Mail Konusu:"+subject+" \n Maili:"+msg
    message=Message(email+" 'dan gelen  "+subject+" Maili",sender=myMail.userName,recipients=[myMail.userName])
    message.body=full_message
    mail.send(message)"""

    return render_template('response.html',message="Mailiniz başarıyla gönderildi.En kısa sürede sizinle iletişime geçeceğiz")
@app.route('/changePassword',methods=['POST'])
def changePassword():
    password=request.form.get("password")
    secondpassword=request.form.get("secondpassword")
    if(password==secondpassword):
        result = hashlib.md5(password.encode("utf-8")).hexdigest()
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE `users`  SET `password` = %(password)s  WHERE `ban`='0' AND `user_auth` = %(key)s",{'key':changepass,'password':result})  
        mysql.connection.commit()
        return render_template('login.html',error="Şifreniz Başarıyla Değiştirildi.Yeni Şifrenizle Giriş Yapabilirsiniz")

@app.route('/resetPassword',methods=['POST'])
def resetPassword():
    try:
        email=request.form.get("email")
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT user_auth FROM `users` WHERE `email` LIKE  %(email)s  ",{'email': email}) 
        users=cursor.fetchall()
        if(len(users)>0):
            link="http://192.168.1.70:5000/resetpass/"+users[0][0]
            full_message="Merhabalar,\n\n Şifrenizi Yenilemek İçin Aşağıdaki Bağlantıyı Kullanabilirsiniz\n\n"+link+"\n\n\n İyi Günler Dileriz\n"
            message=Message("BrainSoup Şifre Yenileme İsteği",sender=myMail.userName,recipients=[email])
            message.body=full_message
            mail.send(message)
            return render_template('reset.html',error="Şifre Yenileme Mailiniz Başarıyla Gönderildi")
        else:
            return render_template('reset.html',error="Mail Gönderilemedi.Bu Maile Ait Kullanıcı Bulunamamıştır.")

    except :
        return render_template('reset.html',error="Mail Gönderilemedi.Bu Maile Ait Kullanıcı Bulunamamıştır.")

############## </Web Assitant Pages > #########################################################################################################################################


############## < Admin Pages > ################################################################################################################################################
@app.route('/admin')
def admin():
    if 'user_auth' in session:
       
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT admin FROM `users` WHERE `admin` LIKE  '1' AND `ban` LIKE '0' AND `user_auth` LIKE  %(doctor)s  ",{'admin':'1','doctor': doctor}) 
        data=cursor.fetchall()
        if(len(data)>0):
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT count(`id`) FROM `users` WHERE `ban` LIKE '0'  ")  
            users=cursor.fetchall()
            cursor.execute("SELECT count(`id`) FROM `patients` WHERE `ban` LIKE '0'  ")  
            patients=cursor.fetchall()
            cursor.execute("SELECT count(`id`) FROM `tumor` WHERE `ban` LIKE '0'  ")  
            tumors=cursor.fetchall()
            cursor.execute("SELECT count(`id`) FROM `email` WHERE `ban` LIKE '0'  ")  
            emails=cursor.fetchall()
            cursor.execute("SELECT count(`id`) FROM `email` WHERE `ban` LIKE '0' AND  `status` LIKE '0'")  
            unread=cursor.fetchall()
            cursor.execute("SELECT * FROM `email` WHERE `ban` LIKE '0' AND  `status` LIKE '0' ORDER BY id DESC LIMIT 5")  
            allmessage=cursor.fetchall()
            return render_template('admin.html',isim=openName,countuser=users[0][0],countpatient=patients[0][0],counttumor=tumors[0][0],countemail=emails[0][0],unread=unread[0][0],allmessage=allmessage)
        else:
            return redirect(url_for('profile'))
    else:
        return redirect(url_for('login'))
@app.route('/sendMailAdmin' ,defaults={'id':'default'})
@app.route('/sendMailAdmin<id>' )
def sendMailAdmin(id):
    if 'user_auth' in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT admin FROM `users` WHERE `admin` LIKE  '1' AND `ban` LIKE '0' AND `user_auth` LIKE  %(doctor)s  ",{'admin':'1','doctor': doctor}) 
        data=cursor.fetchall()
        if(len(data)>0):
            cursor.execute("SELECT count(`id`) FROM `email` WHERE `ban` LIKE '0' AND  `status` LIKE '0'")  
            unread=cursor.fetchall()
            cursor.execute("SELECT * FROM `email` WHERE `ban` LIKE '0' AND  `status` LIKE '0' ORDER BY id DESC LIMIT 5") 
            allmessage=cursor.fetchall()
            if(id=="default"):
                return render_template('sendmail.html',isim=openName,unread=unread[0][0],allmessage=allmessage)
            else:
                cursor.execute("SELECT email,subject FROM `email` WHERE `id` LIKE  %(id)s   ",{'id': id}) 
                readmail=cursor.fetchall()
                return render_template('sendmail.html',isim=openName,unread=unread[0][0],allmessage=allmessage,subject=readmail[0][1],email=readmail[0][0])
        else:
            return redirect(url_for('profile'))
    else:
        return redirect(url_for('login'))
@app.route('/senderMailAdmin',methods=['POST'])
def senderMailAdmin():
    if 'user_auth' in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT admin FROM `users` WHERE `admin` LIKE  '1' AND `ban` LIKE '0' AND `user_auth` LIKE  %(doctor)s  ",{'admin':'1','doctor': doctor}) 
        data=cursor.fetchall()
        if(len(data)>0):
            cursor.execute("SELECT count(`id`) FROM `email` WHERE `ban` LIKE '0' AND  `status` LIKE '0'")  
            unread=cursor.fetchall()
            cursor.execute("SELECT * FROM `email` WHERE `ban` LIKE '0' AND  `status` LIKE '0' ORDER BY id DESC LIMIT 5")  
            allmessage=cursor.fetchall()
            email=request.form.get("email")
            subject=request.form.get("subject")
            msg=request.form.get("message")
            try:
                message=Message(subject,sender=myMail.userName,recipients=[email])
                message.body=msg
                mail.send(message)
                return render_template('sendmail.html',isim=openName,unread=unread[0][0],allmessage=allmessage,error="Mailiniz Başarıyla Gönderildi.")

            except :
                return render_template('sendmail.html',isim=openName,unread=unread[0][0],allmessage=allmessage,error="Hata: Mailiniz Gönderilemedi.")
        else:
            return redirect(url_for('profile'))
    else:
        return redirect(url_for('login'))
@app.route('/viewdMailAdmin')
def viewdMailAdmin():
    if 'user_auth' in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT admin FROM `users` WHERE `admin` LIKE  '1' AND `ban` LIKE '0' AND `user_auth` LIKE  %(doctor)s  ",{'admin':'1','doctor': doctor}) 
        data=cursor.fetchall()
        if(len(data)>0):
            cursor.execute("SELECT count(`id`) FROM `email` WHERE `ban` LIKE '0' AND  `status` LIKE '0'")  
            unread=cursor.fetchall()
            cursor.execute("SELECT * FROM `email` WHERE `ban` LIKE '0' ") 
            datas=cursor.fetchall() 
            cursor.execute("SELECT * FROM `email` WHERE `ban` LIKE '0' AND  `status` LIKE '0'  ORDER BY id DESC LIMIT 5")
            allmessage=cursor.fetchall()
            return render_template('mailview.html',isim=openName,unread=unread[0][0],allmessage=allmessage,datas=datas)
        else:
            return redirect(url_for('profile'))
    else:
        return redirect(url_for('login'))
@app.route('/readMail' ,defaults={'id':'default'})
@app.route('/readMail/<id>')
def readMailAdmin(id):
    if 'user_auth' in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT admin FROM `users` WHERE `admin` LIKE  '1' AND `ban` LIKE '0' AND `user_auth` LIKE  %(doctor)s  ",{'admin':'1','doctor': doctor}) 
        data=cursor.fetchall()
        if(len(data)>0):
            cursor.execute("SELECT count(`id`) FROM `email` WHERE `ban` LIKE '0' AND  `status` LIKE '0'")  
            unread=cursor.fetchall()
            cursor.execute("SELECT * FROM `email` WHERE `ban` LIKE '0' AND  `status` LIKE '0' ORDER BY id DESC LIMIT 5")
            allmessage=cursor.fetchall()
            if id=="default":
                return redirect(url_for('viewdMailAdmin'))
            if id!="default":
                cursor = mysql.connection.cursor()
                cursor.execute("SELECT id,fullname,email,subject,message,date FROM `email` WHERE `id` LIKE  %(id)s AND `ban` LIKE  '0'  ",{'id': id}) 
                readmail=cursor.fetchall()
                cursor.execute("UPDATE `email`  SET `status` = %(status)s  WHERE `ban`='0' AND `id` = %(id)s",{'status':'1','id':id}) 
                mysql.connection.commit()
                return render_template('readmail.html',isim=openName,unread=unread[0][0],allmessage=allmessage,id=readmail[0][0],name=readmail[0][1],email=readmail[0][2],subject=readmail[0][3],message=readmail[0][4],date=readmail[0][5])
        else:
            return redirect(url_for('profile'))
    else:
        return redirect(url_for('login'))
@app.route('/operatorMailAdmin',methods=['POST'])
def operatorMailAdmin():
    if 'user_auth' in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT admin FROM `users` WHERE `admin` LIKE  '1' AND `ban` LIKE '0' AND `user_auth` LIKE  %(doctor)s  ",{'admin':'1','doctor': doctor}) 
        data=cursor.fetchall()
        if(len(data)>0):
            cursor.execute("SELECT count(`id`) FROM `email` WHERE `ban` LIKE '0' AND  `status` LIKE '0'")  
            unread=cursor.fetchall() 
            cursor.execute("SELECT * FROM `email` WHERE `ban` LIKE '0' AND  `status` LIKE '0' ORDER BY id DESC LIMIT 5")
            allmessage=cursor.fetchall()
            id=request.form.get("id")
            if 'Read' in request.form:
                    try:
                        cursor.execute("UPDATE `email`  SET `status` = %(status)s  WHERE `id` = %(id)s",{'status':'0','id':id})  
                        mysql.connection.commit()
                        return redirect(url_for('viewdMailAdmin'))
                    except:
                        return redirect(url_for('viewdMailAdmin')) 
            elif 'Delete' in request.form:
                try:
                    cursor.execute("UPDATE `email`  SET `ban` = %(status)s  WHERE `id` = %(id)s",{'status':'1','id':id})  
                    mysql.connection.commit()
                    return render_template('readmail.html',isim=openName,unread=unread[0][0],allmessage=allmessage,error="Mail Başarıyla Silindi",link="a")
                except:
                     return render_template('readmail.html',isim=openName,unread=unread[0][0],allmessage=allmessage,error="Hata: Mail Silinemedi")
            elif 'Answer' in request.form:
                try:
                    return redirect(url_for('sendMailAdmin',id=id))
                except:
                    return redirect(url_for('viewdMailAdmin')) 
            else:
                pass


            return render_template('mailview.html',isim=openName,unread=unread[0][0],allmessage=allmessage)
        else:
            return redirect(url_for('profile'))
    else:
        return redirect(url_for('login'))

@app.route('/viewUserAdmin')
def viewUserAdmin():
    if 'user_auth' in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT admin FROM `users` WHERE `admin` LIKE  '1' AND `ban` LIKE '0' AND `user_auth` LIKE  %(doctor)s  ",{'admin':'1','doctor': doctor}) 
        data=cursor.fetchall()
        if(len(data)>0):
            cursor.execute("SELECT count(`id`) FROM `email` WHERE `ban` LIKE '0' AND  `status` LIKE '0'")  
            unread=cursor.fetchall()
            cursor.execute("SELECT id,name,surname,email,admin FROM `users` WHERE `ban` LIKE '0' ") 
            datas=cursor.fetchall() 
            cursor.execute("SELECT * FROM `email` WHERE `ban` LIKE '0' AND  `status` LIKE '0'  ORDER BY id DESC LIMIT 5")
            allmessage=cursor.fetchall()
            return render_template('userview.html',isim=openName,unread=unread[0][0],allmessage=allmessage,datas=datas)
        else:
            return redirect(url_for('profile'))
    else:
        return redirect(url_for('login'))  
@app.route('/userSettings' ,defaults={'id':'default'})
@app.route('/userSettings/<id>')
def userSettingsAdmin(id):
    if 'user_auth' in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT admin FROM `users` WHERE `admin` LIKE  '1' AND `ban` LIKE '0' AND `user_auth` LIKE  %(doctor)s  ",{'admin':'1','doctor': doctor}) 
        data=cursor.fetchall()
        if(len(data)>0):
            cursor.execute("SELECT count(`id`) FROM `email` WHERE `ban` LIKE '0' AND  `status` LIKE '0'")  
            unread=cursor.fetchall()
            cursor.execute("SELECT * FROM `email` WHERE `ban` LIKE '0' AND  `status` LIKE '0' ORDER BY id DESC LIMIT 5")
            allmessage=cursor.fetchall()
            if id=="default":
                return redirect(url_for('viewUserAdmin'))
            if id!="default":
                cursor = mysql.connection.cursor()
                cursor.execute("SELECT id,name,surname,email,admin FROM `users` WHERE `id` LIKE  %(id)s AND `ban` LIKE  '0'  ",{'id': id}) 
                readmail=cursor.fetchall()
                return render_template('readuser.html',isim=openName,unread=unread[0][0],allmessage=allmessage,id=readmail[0][0],name=readmail[0][1],surname=readmail[0][2],email=readmail[0][3],isadmin=readmail[0][4])
        else:
            return redirect(url_for('profile'))
    else:
        return redirect(url_for('login'))
@app.route('/operatorUserAdmin',methods=['POST'])
def operatorUserAdmin():
    if 'user_auth' in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT admin FROM `users` WHERE `admin` LIKE  '1' AND `ban` LIKE '0' AND `user_auth` LIKE  %(doctor)s  ",{'admin':'1','doctor': doctor}) 
        data=cursor.fetchall()
        if(len(data)>0):
            cursor.execute("SELECT count(`id`) FROM `email` WHERE `ban` LIKE '0' AND  `status` LIKE '0'")  
            unread=cursor.fetchall() 
            cursor.execute("SELECT * FROM `email` WHERE `ban` LIKE '0' AND  `status` LIKE '0' ORDER BY id DESC LIMIT 5")
            allmessage=cursor.fetchall()
            id=request.form.get("id")
            email=request.form.get("email")
            if 'Answer' in request.form:
                    try:
                        cursor.execute("UPDATE `users`  SET `admin` = %(admin)s  WHERE `id` = %(id)s AND `email` = %(email)s ",{'admin':'1','id':id,'email':email})  
                        mysql.connection.commit()
                        return render_template('readuser.html',isim=openName,unread=unread[0][0],allmessage=allmessage,error="Kullanıcı Başarıyla Yönetici Yapıldı",link="a")
                    except:
                        return render_template('readuser.html',isim=openName,unread=unread[0][0],allmessage=allmessage,error="Hata: Kullanıcı Yönetici Yapılamadı") 
            elif 'Delete' in request.form:
                try:
                    cursor.execute("UPDATE `users`  SET `ban` = %(ban)s  WHERE `id` = %(id)s AND `email` = %(email)s",{'ban':'1','id':id,'email':email})  
                    mysql.connection.commit()
                    return render_template('readuser.html',isim=openName,unread=unread[0][0],allmessage=allmessage,error="Kullanıcı Başarıyla Silindi",link="a")
                except:
                    return render_template('readuser.html',isim=openName,unread=unread[0][0],allmessage=allmessage,error="Hata:Kullanıcı Silinemedi") 
            
            else:
                pass


        else:
            return redirect(url_for('profile'))
    else:
        return redirect(url_for('login'))
@app.route('/showIndexUpdate' )
def showIndexUpdate():
    if 'user_auth' in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT admin FROM `users` WHERE `admin` LIKE  '1' AND `ban` LIKE '0' AND `user_auth` LIKE  %(doctor)s  ",{'admin':'1','doctor': doctor}) 
        data=cursor.fetchall()
        if(len(data)>0):
            cursor.execute("SELECT count(`id`) FROM `email` WHERE `ban` LIKE '0' AND  `status` LIKE '0'")  
            unread=cursor.fetchall()
            cursor.execute("SELECT * FROM `email` WHERE `ban` LIKE '0' AND  `status` LIKE '0' ORDER BY id DESC LIMIT 5") 
            allmessage=cursor.fetchall()
            cursor.execute("SELECT * FROM `about` WHERE `id`='1' ") 
            indexdetail=cursor.fetchall()
            return render_template('indexsettings.html',isim=openName,unread=unread[0][0],allmessage=allmessage,indexdetail=indexdetail)
        else:
            return redirect(url_for('profile'))
    else:
        return redirect(url_for('login'))
@app.route('/updateIndex' ,methods=['POST'])
def updateIndex():
    if 'user_auth' in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT admin FROM `users` WHERE `admin` LIKE  '1' AND `ban` LIKE '0' AND `user_auth` LIKE  %(doctor)s  ",{'admin':'1','doctor': doctor}) 
        data=cursor.fetchall()
        if(len(data)>0):
            cursor.execute("SELECT count(`id`) FROM `email` WHERE `ban` LIKE '0' AND  `status` LIKE '0'")  
            unread=cursor.fetchall()
            cursor.execute("SELECT * FROM `email` WHERE `ban` LIKE '0' AND  `status` LIKE '0' ORDER BY id DESC LIMIT 5") 
            allmessage=cursor.fetchall()
            main=request.form.get("main")
            explain=request.form.get("explain")
            why=request.form.get("why")
            doctorwhy=request.form.get("doctorwhy")
            brainwhy=request.form.get("brainwhy")
            cloudwhy=request.form.get("cloudwhy")

  
            try:
                cursor.execute("UPDATE `about`  SET `title` = %(title)s,`detail` = %(detail)s ,`whyus` = %(whyus)s,`doctor` = %(doctor)s ,`brain` = %(brain)s,`cloud` = %(cloud)s WHERE `id` = '1' ",{'title':main,'detail':explain,'whyus':why,'doctor':doctorwhy,'brain':brainwhy,'cloud':cloudwhy})  
                mysql.connection.commit()
                cursor.execute("SELECT * FROM `about` WHERE `id`='1' ") 
                indexdetail=cursor.fetchall()
                return render_template('indexsettings.html',isim=openName,unread=unread[0][0],allmessage=allmessage,error="Kayıt Başarılı Bir Şekilde Güncellendi",indexdetail=indexdetail)
            except:
                cursor.execute("SELECT * FROM `about` WHERE `id`='1' ") 
                indexdetail=cursor.fetchall()
                return render_template('indexsettings.html',isim=openName,unread=unread[0][0],allmessage=allmessage,error="Hata:Kayıt Başarılı Bir Şekilde Güncellenemedi",indexdetail=indexdetail)
            
            
        else:
            return redirect(url_for('profile'))
    else:
        return redirect(url_for('login'))
@app.route('/showAboutUpdate' )
def showAboutUpdate():
    if 'user_auth' in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT admin FROM `users` WHERE `admin` LIKE  '1' AND `ban` LIKE '0' AND `user_auth` LIKE  %(doctor)s  ",{'admin':'1','doctor': doctor}) 
        data=cursor.fetchall()
        if(len(data)>0):
            cursor.execute("SELECT count(`id`) FROM `email` WHERE `ban` LIKE '0' AND  `status` LIKE '0'")  
            unread=cursor.fetchall()
            cursor.execute("SELECT * FROM `email` WHERE `ban` LIKE '0' AND  `status` LIKE '0' ORDER BY id DESC LIMIT 5") 
            allmessage=cursor.fetchall()
            cursor.execute("SELECT * FROM `whous` WHERE `id`='1' ") 
            aboutdetail=cursor.fetchall()
            return render_template('aboutsettings.html',isim=openName,unread=unread[0][0],allmessage=allmessage,aboutdetail=aboutdetail)
        else:
            return redirect(url_for('profile'))
    else:
        return redirect(url_for('login'))
@app.route('/updateAbout' ,methods=['POST'])
def updateAbout():
    if 'user_auth' in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT admin FROM `users` WHERE `admin` LIKE  '1' AND `ban` LIKE '0' AND `user_auth` LIKE  %(doctor)s  ",{'admin':'1','doctor': doctor}) 
        data=cursor.fetchall()
        if(len(data)>0):
            cursor.execute("SELECT count(`id`) FROM `email` WHERE `ban` LIKE '0' AND  `status` LIKE '0'")  
            unread=cursor.fetchall()
            cursor.execute("SELECT * FROM `email` WHERE `ban` LIKE '0' AND  `status` LIKE '0' ORDER BY id DESC LIMIT 5") 
            allmessage=cursor.fetchall()
            main=request.form.get("main")
            explain=request.form.get("explain")
            second=request.form.get("second")
            details2=request.form.get("details2")
            third=request.form.get("third")
            details3=request.form.get("details3")
            fourth=request.form.get("fourth")
            details4=request.form.get("details4")
            link=request.form.get("link")

        
            try:
                cursor.execute("UPDATE `whous`  SET `title` = %(title)s,`detail` = %(detail)s ,`title2` = %(title2)s,`detail2` = %(detail2)s ,`title3` = %(title3)s,`detail3` = %(detail3)s,`title4` = %(title4)s,`detail4` = %(detail4)s,`videolink` = %(link)s WHERE `id` = '1' ",{'title':main,'detail':explain,'title2':second,'detail2':details2,'title3':third,'detail3':details3,'title4':fourth,'detail4':details4,'link':link})  
                mysql.connection.commit()
                cursor.execute("SELECT * FROM `whous` WHERE `id`='1' ") 
                aboutdetail=cursor.fetchall()
                return render_template('aboutsettings.html',isim=openName,unread=unread[0][0],allmessage=allmessage,error="Kayıt Başarılı Bir Şekilde Güncellendi",aboutdetail=aboutdetail)
            except:
                cursor.execute("SELECT * FROM `whous` WHERE `id`='1' ") 
                aboutdetail=cursor.fetchall()
                return render_template('aboutsettings.html',isim=openName,unread=unread[0][0],allmessage=allmessage,error="Hata:Kayıt Başarılı Bir Şekilde Güncellenemedi",aboutdetail=aboutdetail)
            
            
        else:
            return redirect(url_for('profile'))
    else:
        return redirect(url_for('login'))
############## < /Admin Pages > ################################################################################################################################################


############## < Web API > ################################################################################################################################################

@app.route('/loginAPI',methods=['POST'])
def loginAPI():
    email=request.form.get("email")
    password=request.form.get("password")
    print("Email: "+email+"Password: "+password)
    result = hashlib.md5(password.encode("utf-8")).hexdigest()
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM `users` WHERE `email` LIKE %(email)s AND `password` LIKE %(password)s AND `ban` LIKE '0' ",{'email': email,'password':result})
    
    users=cursor.fetchall()
    if len(users)>0:
        info=[{"name":users[0][1],"email":users[0][3],"key":users[0][6]}]
        return jsonify(info)
        
      
    else:
        error=[{"error":"Kullanıcı Adı veya Şifre Yanlış"}]
        return jsonify(error) 
        

############## < /Web API > ################################################################################################################################################


if __name__ == "__main__":
    app.run(host='0.0.0.0',port='5000')
