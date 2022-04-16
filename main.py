from urllib import response
from flask import Flask,render_template,request,jsonify,Response
from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS
from chat import get_response
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/sanjivani'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class contact(db.Model):
    Sno=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80),unique=False, nullable=False)
    email=db.Column(db.String(20),nullable=False)
    phone=db.Column(db.String(12),nullable=False)
    message=db.Column(db.String(120),nullable=False)

class Appointment(db.Model):
    Sno=db.Column(db.Integer,primary_key=True)
    full_name=db.Column(db.String(80),unique=False, nullable=False)
    email=db.Column(db.String(50),nullable=False)
    phone_num=db.Column(db.String(12),nullable=False)
    area=db.Column(db.String(120),nullable=False)
    city=db.Column(db.String(120),nullable=False)
    state=db.Column(db.String(120),nullable=False)
    code=db.Column(db.Integer,nullable=False)
    date=db.Column(db.String(12),nullable=True)
@app.route("/")
def home():
    return render_template("index.html") 

@app.route("/about_us")
def about():
    return render_template("about_us.html") 

@app.route("/services")
def services():
    return render_template("services.html") 

@app.route("/contact_us", methods=['GET','POST'])
def Contact():
    if(request.method=="POST"):
        '''add entry to database'''
        name=request.form.get('name')
        email=request.form.get('email')
        phone=request.form.get('phone')
        message=request.form.get('message')
        entry=contact(name=name,email=email,phone=phone,message=message)
        db.session.add(entry)
        db.session.commit()
    return render_template("contact_us.html") 

@app.route("/index2",methods=['GET','POST'])
def appointment():
    if(request.method=="POST"):
        '''add entry to database'''
        full_name=request.form.get('full_name')
        phone_num=request.form.get('phone_num')
        email=request.form.get('email')
        date=request.form.get('date')
        area=request.form.get('area')
        city=request.form.get('city')
        state=request.form.get('state')
        code=request.form.get('code')
        entry=Appointment(full_name=full_name,phone_num=phone_num,email=email,date=date,area=area,city=city,state=state,code=code)
        db.session.add(entry)
        db.session.commit()
    return render_template("index2.html")

@app.route("/chatbot", methods=['GET','POST'])
def chatbot():    
    if request.method=='POST':
        @app.post("/predict")  
        def predict():
            text=request.get_json().get('message')
            #TODO: check if text is valid
            response=get_response(text)
            message={'answer':response}
            return jsonify(message)
    return render_template("chatbot.html")     
# CORS(app,resources=r'/chatbot/*')
# CORS(app,origins=["http://127.0.0.1:5000/chatbot/predict"])
# @app.route("/chatbot/predict", methods=['POST'])

@app.post("/predict")    
def predict():
    text=request.get_json().get('message')
    #TODO: check if text is valid
    response=get_response(text)
    message={'answer':response}
    return jsonify(message)

if __name__=="__main__":
    app.run(debug=True)