from flask import Blueprint, request, jsonify
from models import db, Apartment

apartments_bp = Blueprint("apartments", __name__, url_prefix="/apartments")

#Create Apartment
@apartments_bp.route("/", methods=["POST"])
def create_apartment():
    data = request.get_json()
    apartment = Apartment(
        name = data["name"],
        location = data["location"],
        no_of_units = data["no_of_units"]
    )
    db.session.add(apartment)
    db.session.commit()
    return jsonify({"message": "Apartment created", "id": apartment.id}), 201

#Read all apartments
@apartments_bp.route("/", methods=['GET'])
def get_apartments():
    apartments = Apartment.query.all()
    return jsonify([
        {"id": a.id, "name": a.name, "location": a.location, "no_of_units": a.no_of_units}
        for a in apartments
    ])

#Read single Apartment
@apartments_bp.route("/<int:id>", methods=['GET'])
def get_apartment(id):
    apartment = Apartment.query.get_or_404(id)
    return jsonify({"id": apartment.id, "name": apartment.name, "location": apartment.location, "no_of_units": apartment.no_of_units})

#update apartment
@apartments_bp.route("<int:id>", methods=["PUT"])
def update_apartment(id):
    data = request.get_json()
    apartment = Apartment.query.get_or_404(id)
    apartment.name = data.get("name", apartment.name)
    apartment.location = data.get("location", apartment.location)
    apartment.no_of_units = data.get("no_of_units", apartment.no_of_units)
    db.session.commit()
    return jsonify({"message": f"Apartment {id} updated"})

#delete apartment
@apartments_bp.route("<int:id>", methods=["DELETE"])
def delete_apartment(id):
    apartment = Apartment.query.get_or_404(id)
    db.session.delete(apartment)
    db.session.commit()
    return jsonify({"message": f"{apartment.name} has been deleted!!"})
