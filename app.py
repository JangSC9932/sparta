from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
db = SQLAlchemy(app)

class Person(db.Model):
    person_id = db.Column(db.Integer, primary_key=True)
    person_like = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'{self.person_id} | {self.person_nm} | {self.person_intro} | {self.person_like} | {self.person_image_url}'

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    person_list = Person.query.all()
    total_likes = sum(person.person_like for person in person_list)  # 총 좋아요 수 계산
    return render_template('index.html', data=person_list, total_likes=total_likes)  # total_likes를 템플릿에 전달

@app.route("/addLike")
def add_like():
    person_id = request.args.get("person_id")
    person = Person.query.filter_by(person_id=person_id).first()
    person.person_like += 1
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/person/<int:person_id>")
def get_person(person_id):
    person = Person.query.get_or_404(person_id)
    return render_template('person.html', person=person)

if __name__ == "__main__":
    app.run(debug=True)
