from flask import Flask, jsonify, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from random import choice
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)

class Cafe(db.Model):
    """add name, map_url, img_url, location, 
    seats, has_toilet, has_wifi has_sockets, can_take_calls, coffee_price"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/random", methods=["get"])
def random():
    cafe_list = db.session.execute(db.select(Cafe)).scalars().all()
    random_cafe = choice(cafe_list)
    return jsonify({"cafe": random_cafe.to_dict()})

@app.route("/all")
def all_cafes():
    all_cafes = db.session.execute(db.select(Cafe).order_by(Cafe.id)).scalars().all()
    cafes = []
    for cafe in all_cafes:
        cafes.append(cafe.to_dict())

    return jsonify(cafes)

@app.route("/search")
def search():
    loc = request.args.get('loc')
    selected_cafes = db.session.execute(db.select(Cafe).where(Cafe.name == loc)).scalars().all()
    
    if selected_cafes:
        return jsonify({'cafes': [cafe.to_dict() for cafe in selected_cafes]})
    else:
        return jsonify({'error': {'not found': "Sorry we don't have a cafe in that location"}})
    
@app.route("/add", methods=["POST"])
def post_new_cafe():
    new_cafe = Cafe(
        name = request.form.get('name'),
        map_url = request.form.get('map_url'),
        img_url = request.form.get('img_url'),
        location = request.form.get('location'),
        seats = request.form.get('seats'),
        has_toilet = bool(request.form.get('toilets')),
        has_wifi = bool(request.form.get('wifi')),
        has_sockets = bool(request.form.get('sockets')),
        can_take_calls = bool(request.form.get('calls')),
        coffee_price = request.form.get('coffee_price'),
    )
    db.session.add(new_cafe)
    db.session.commit()

    return jsonify(response = {"success": "Succesfully Aded the new caffee."})

if __name__ == '__main__':
    app.run(debug=True)
