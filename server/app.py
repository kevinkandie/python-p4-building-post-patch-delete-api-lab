#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# Home route
@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

# POST /baked_goods - Create a new baked good
@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    name = request.form.get('name')
    price = request.form.get('price')
    bakery_id = request.form.get('bakery_id')

    if not name or not price or not bakery_id:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        price = float(price)
        bakery_id = int(bakery_id)
    except ValueError:
        return jsonify({"error": "Invalid price or bakery_id"}), 400

    baked_good = BakedGood(name=name, price=price, bakery_id=bakery_id)
    db.session.add(baked_good)
    db.session.commit()

    return jsonify(baked_good.to_dict()), 201

# PATCH /bakeries/<int:id> - Update a bakery's name
@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = db.session.get(Bakery, id)
    if not bakery:
        return jsonify({"error": "Bakery not found"}), 404

    name = request.form.get('name')
    if name:
        bakery.name = name
        db.session.commit()

    return jsonify(bakery.to_dict()), 200

# DELETE /baked_goods/<int:id> - Delete a baked good
@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = db.session.get(BakedGood, id)
    if not baked_good:
        return jsonify({"error": "Baked good not found"}), 404

    db.session.delete(baked_good)
    db.session.commit()

    return jsonify({"message": "Baked good deleted successfully."}), 200

# Run the app
if __name__ == '__main__':
    app.run(port=5555, debug=True)
