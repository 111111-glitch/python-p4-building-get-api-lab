#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate
from models import Bakery, BakedGood, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def get_bakeries():
    bakeries = Bakery.query.all()
    return jsonify([bakery.to_dict() for bakery in bakeries])

@app.route('/bakeries/<int:id>')
def get_bakery(id):
    bakery = Bakery.query.get(id)
    if bakery:
        return jsonify(bakery.to_dict())
    else:
        return jsonify({'error': 'Bakery not found'}), 404

@app.route('/baked_goods/by_price')
def get_baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    return jsonify([good.to_dict() for good in baked_goods])

@app.route('/baked_goods/most_expensive')
def get_most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if most_expensive:
        return jsonify(most_expensive.to_dict())
    else:
        return jsonify({'error': 'No baked goods found'}), 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)
