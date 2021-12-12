"""Flask app for Cupcakes"""
from flask import Flask, render_template, jsonify, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///cupcakes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secrets"
app.config ['DEBUG_TB_INTERCEPT_REDIRECTS']= False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()



"""Homepage"""
@app.route('/')
def root():
    return render_template("index.html")

@app.route('/api/cupcakes')
def list_all_cupcakes():
    cupcakes=[cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake_info(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    cupcake = Cupcake(
        flavor = request.json["flavor"],
        size = request.json["size"],
        rating = request.json["rating"],
        image = request.json["image"])

    db.session.add(cupcake)
    db.session.commit()


    return (jsonify(cupcake=cupcake.serialize()), 201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    """if an update is not put in, keep previous input"""
    cupcake.flavor = request.json.get('flavor', cupcake.flavor),
    cupcake.size = request.json.get('size', cupcake.size),
    cupcake.rating = request.json.get('rating', cupcake.rating),
    cupcake.image = request.json.get('image', cupcake.image)

    db.session.commit()


    return jsonify(cupcake=cupcake.serialize()) 

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    cupcake= Cupcake.query.get_or_404(cupcake_id)
    
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")
