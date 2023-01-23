from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import sys


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///weather.db"
app.config['SECRET_KEY'] = 'secret_key'
db = SQLAlchemy()
db.init_app(app)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)


@app.route('/')
def index():
    cities = []
    for city in City.query.all():
        cities.append({'id': city.id, 'name': city.name, 'time': 'day', 'celsius': 18, 'state': 'Cold'})
    return render_template('index.html', cities=cities)


@app.route('/del', methods=['POST'])
def delete():
    id = request.form.get('id', None)
    city = City.query.filter_by(id=id).first()
    if city is None:
        flash("The city doesn't exist!")
    else:
        db.session.delete(city)
        db.session.commit()
    return redirect('/')


@app.route('/add', methods=['POST'])
def add():
    city_name = request.form.get('city_name', None)
    if 'city_name' is None or city_name in ['', "The city that doesn\'t exist!"]:
        flash("The city doesn't exist!")
    else:
        city = City.query.filter_by(name=city_name).first()
        if city is not None:
            flash("The city has already been added to the list!")
        else:
            db.session.add(City(name=city_name))
            db.session.commit()
    return redirect('/')


# don't change the following way to run flask:
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if len(sys.argv) > 1:
            arg_host, arg_port = sys.argv[1].split(':')
            app.run(host=arg_host, port=arg_port)
        else:
            app.run()
