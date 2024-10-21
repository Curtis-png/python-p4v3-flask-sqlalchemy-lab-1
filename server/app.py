from flask import Flask, jsonify
from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake_by_id(id):
    quake = Earthquake.query.get(id)
    if quake:
        return jsonify(quake.serialize()), 200
    return jsonify({"message": f"Earthquake {id} not found."}), 404

@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    return jsonify({"count": len(quakes), "quakes": [quake.serialize() for quake in quakes]}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure the database and tables are created
    app.run(port=5555)
