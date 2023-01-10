from flask import Flask, request, render_template,redirect
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:myDBpost@localhost/list-data'

db = SQLAlchemy(app)


class Code(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(4))


def __repr__(self):
        return f"Code: {self.code}"

def __init__(self,code):
        self.code = code

def format_code(event):
    return{
        "id" : event.id,
        "code" : event.code
    }    



class Facilities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    facilities = db.Column(db.String(50))
    
    def __repr__(self):
        return f"Facility: {self.facilities}"

def __init__(self,facilities):
        self.facilities = facilities
        
        
def format_facility(event):
    return{
        "id" : event.id,
        "facilities" : event.facilities
    } 
    
    
    
            
class PropertyInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(4))
    phone = db.Column(db.String(13))
    checkbox = db.Column(db.Boolean)
    charge = db.Column(db.Integer)
    facilities = db.Column(db.String(500))
    
    def __repr__(self):
        return f"phone: {self.phone}"

    def __init__(self,code,phone,checkbox,charge,facilities):
        self.code = code
        self.phone = phone
        self.checkbox = checkbox
        self.charge = charge
        self.facilities = facilities
        
        
def format_person_info(event):
    return{
        "id" : event.id,
        "code" : event.code,
        "phone" : event.phone,
        "checkbox" : event.checkbox,
        "charge" : event.charge,
        "facilities" : event.facilities
    }           

@app.route("/home",methods=["POST", "GET"])
@app.route("/")
def home():
    
    if request.method == "POST":
        newCodes = request.form["codes"]
        newfacilities = request.form["facilities"]
        t = Code(code=newCodes)
        d = Facilities(facilities=newfacilities)
        db.session.add(d)
        db.session.add(t)
        db.session.commit()
        return redirect("/")
    datas = Code.query.all()
    return render_template('index.html',data=datas)



@app.route("/codes", methods = ["GET"])
def get_codes():
    codes = Code.query.order_by(Code.id.asc()).all()
    code_list = []
    for event in codes:
        code_list.append(format_code(event))
    return {"code" : code_list}


@app.route("/faclities", methods = ["GET"])
def get_facilities():
    facilities = Facilities.query.order_by(Facilities.id.asc()).all()
    facility_list = []
    for event in facilities:
        facility_list.append(format_facility(event))
    return {"facilities" : facility_list}



@app.route("/personInfo", methods = ["POST"])
# @cross_origin(supports_credentials=True)
def create_person_info():
    code = request.json["code"]
    phone = request.json["phone"]
    checkbox = request.json["checkbox"]
    charge = request.json["charge"]
    facilities = request.json["facility"]
    event = PropertyInfo(code, phone, checkbox, charge, facilities)
    db.session.add(event)
    db.session.commit()
    return format_person_info(event)


if __name__ == "__main__":
    app.run(debug=True)
    
    
    
# from project_name import app, db
# app.app_context().push()
# db.create_all()
# . venv/bin/activate 
# sudo kill -9 `sudo lsof -t -i:5000` 