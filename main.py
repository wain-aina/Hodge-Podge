import sqlite3
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_login import UserMixin
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///joints.db' #sets our local databse as the alternative during local production
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class CafeForm(FlaskForm):
    cafe = StringField('Hub Name', validators=[DataRequired()])
    location_url = StringField('Location', validators=[DataRequired()])
    img_url = StringField('Share a photo of the place via link', validators=[URL(require_tld=True, message=None)])
    music = StringField("What is the DJ's flavour", validators=[DataRequired()])
    price = StringField('Is the venue pricey or affordable?', validators=[DataRequired()])
    eating_rating = SelectField('Food & Drinks 🍭', choices=["😇", "😇😇", "😇😇😇", "😇😇😇😇", "😇😇😇😇😇"], validators=[DataRequired()])
    secure_rating = SelectField('Security Strength 💪', choices=["💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"], validators=[DataRequired()])
    wifi_outlet =SelectField('Wi-Fi Speeds 🔌', choices=["⚡", "⚡⚡", "⚡⚡⚡", "⚡⚡⚡⚡", "⚡⚡⚡⚡⚡"], validators=[DataRequired()])
    special = StringField("Some special features i.e. Swimming pool, Pool Tables, Garden, Video Games")
    submit = SubmitField('Submit')

class Hotspot(db.Model):
    __tablename__ = "hotspots"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    place = db.Column(db.Integer, nullable=False)
    location_url = db.Column(db.String(250), unique=True, nullable=False)
    img_url = db.Column(db.String(250), unique=True, nullable=False)
    music_taste = db.Column(db.String(250), nullable=False)
    price = db.Column(db.String(250), nullable=False)
    eats = db.Column(db.Text, nullable=False)
    security = db.Column(db.String(250), nullable=False)
    internet = db.Column(db.String(250), nullable=False)
    exclusive = db.Column(db.String(250), nullable=False)

db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/spots')
def all_cafes():
    places = Hotspot.query.all()
    return render_template("cafes.html", all_spots=places)


@app.route('/add', methods=["GET", "POST"])
def add_joint():
    form = CafeForm()
    if form.validate_on_submit():
        new_joint = Hotspot(
          place = form.cafe.data,
          location_url = form.location_url.data,
          img_url = form.img_url.data,
          music_taste = form.music.data,
          price = form.price.data,
          eats = form.eating_rating.data,
          security = form.secure_rating.data,
          internet = form.wifi_outlet.data,
          exclusive = form.special.data
        )
        db.session.add(new_joint)
        db.session.commit()
        return redirect(url_for('all_cafes'))
    return render_template('add.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
