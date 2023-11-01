from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///task.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        task = Task(title=title, desc=desc)
        db.session.add(task)
        db.session.commit()
        
    allTask = Task.query.all() 
    return render_template('index.html', allTask=allTask)

@app.route('/show')
def products():
    allTask = Task.query.all()
    print(allTask)
    return 'this is products page'

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        task = Task.query.filter_by(sno=sno).first()
        task.title = title
        task.desc = desc
        db.session.add(task)
        db.session.commit()
        return redirect("/")
        
    task = Task.query.filter_by(sno=sno).first()
    return render_template('update.html', task=task)

@app.route('/delete/<int:sno>')
def delete(sno):
    task = Task.query.filter_by(sno=sno).first()
    db.session.delete(task)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

#app.app_context(): db = SQLAlchemy(app)
#python
#>>> from app import app, db
#>>> app.app_context().push()
#>>> db.create_all()
