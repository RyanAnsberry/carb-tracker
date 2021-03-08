from operator import invert
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///logs.db'
db = SQLAlchemy(app)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    carbs = db.Column(db.Integer, default=0)
    insulin = db.Column(db.Float, default=0)

    def __repr__(self):
        return '<Log %r >' % self.id

@app.route('/', methods=['GET'])
def index():
    logs = Log.query.order_by(Log.date_created).all()
    logs.reverse()
    return render_template('index.html', logs=logs)

@app.route('/add', methods=['GET', 'POST'])
def add():
    carb_data = request.form['carbs']
    insulin_data = request.form['insulin']
    new_log = Log(carbs=carb_data, insulin=insulin_data)
    db.session.add(new_log)
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)