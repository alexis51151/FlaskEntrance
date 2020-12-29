from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
from flask import request, jsonify, make_response
from werkzeug import secure_filename # For upload 
from flask_login import LoginManager 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
class Scans(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15))
    img = db.Column(db.String(50))
    link = db.Column(db.String(50))
    chapter = db.Column(db.Integer)
    
    
        
db.create_all()
#db.session.close() 
@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')
    
@app.route('/scans', methods =['GET', 'POST'])
def show_all():
    if request.method == 'POST':
        req = request.get_json()
        scan = db.session.query(Scans).filter(Scans.id == req['id']).first()
        scan.name = req['title']
        scan.link = req['link']
        scan.chapter = req['chapter']
        db.session.commit()
        print(req)
        res = make_response(jsonify({"message": "OK"}), 200)
        
    else:
        new_scan = Scans(name='test',chapter=5)
        db.session.add(new_scan)
        db.session.commit()
    return render_template('scans.html',scans=Scans.query.all())

@app.route('/uploader', methods=['POST'])
def upload():
    if request.method == 'POST':
        f = request.files['image']
        id = request.form['id']
        print(f)
        f.save('D:\\Users\\alexi_000\\Desktop\\Cours-TELECOM-SudParis\\Informatique\\Flask\\static\\user_imgs\\' + id)
    return 'OK'

if __name__ == "__main__":
    app.run(debug=True)