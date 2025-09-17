from flask import Blueprint, request, jsonify
from models import db, House

houses_bp = Blueprint("houses", __name__, url_prefix="/houses")


#create a house
@houses_bp.route("/", methods=["POST"])
def create_house():
    data = request.get_json()

    house = House(
        apartment_id=data["apartment_id"],
        house_no=data["house_no"],
        description=data.get("description"),
        comments=data.get("comments"),
        rent=data["rent"]
    )

    db.session.add(house)
    db.session.commit()
    return jsonify({"message": "House created", "id": house.id}), 201

#Get all houses
@houses_bp.route("/", methods=["GET"])
def get_houses():
    houses = House.query.all()
    return jsonify([
        {"id": h.id, "house_no": h.house_no, "description": h.description, "rent": h.rent}
        for h in houses
    ])

#Get a single house
@houses_bp.route("/<int:id>", methods=["GET"])
def get_house(id):
    house = House.query.get_or_404(id)
    return jsonify({"id": house.id, "house_no": house.house_no, "description": house.description, "rent": house.rent}), 200

#Update a single house
@houses_bp.route("/<int:id>", methods=["PUT"])
def update_house(id):
    data = request.get_json()
    house = House.query.get_or_404(id)
    house.house_no = data.get("house_no", house.house_no)
    house.description = data.get("description", house.description)
    house.comments = data.get("comments", house.comments)
    house.rent = data.get("rent", house.rent)
    db.session.commit()
    return jsonify({"message": f"House {id} updated"})


#delete a house
@houses_bp.route("/<int:id>", methods=["DELETE"])
def delete_house(id):
    house = House.query.get_or_404(id)
    db.session.delete(house)
    db.session.commit()
    return jsonify({"message": f"{house.house_no} has been deleted!!"})
