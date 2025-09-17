from flask import Blueprint, request, jsonify
from models import db, Tenant

tenants_bp = Blueprint("tenants", __name__, url_prefix="/tenants")

# Create Tenant
@tenants_bp.route("/", methods=["POST"])
def create_tenant():
    data = request.get_json()
    tenant = Tenant(
        firstname=data["firstname"],
        lastname=data["lastname"],
        email=data["email"],
        phone_number=data.get("phone_number"),
        house_id=data["house_id"],
        date_rented=data.get("date_rented")
    )
    db.session.add(tenant)
    db.session.commit()
    return jsonify({"message": "Tenant created", "id": tenant.id}), 201

# Get all Tenants
@tenants_bp.route("/", methods=["GET"])
def get_tenants():
    tenants = Tenant.query.all()
    return jsonify([
        {
            "id": t.id,
            "name": f"{t.firstname} {t.lastname}",
            "email": t.email,
            "phone_number": t.phone_number,
            "house_id": t.house_id,
            "months_lived": t.duration_in_months(),
            "total_rent_paid": t.total_rent_paid()
        }
        for t in tenants
    ])

# Get a single Tenant
@tenants_bp.route("/<int:id>", methods=["GET"])
def get_tenant(id):
    tenant = Tenant.query.get_or_404(id)
    return jsonify({
            "id": tenant.id,
            "name": f"{tenant.firstname} {tenant.lastname}",
            "email": tenant.email,
            "phone_number": tenant.phone_number,
            "house_id": tenant.house_id,
            "months_lived": tenant.duration_in_months(),
            "total_rent_paid": tenant.total_rent_paid()
        })

# Update Tenant
@tenants_bp.route("/<int:id>", methods=["PUT"])
def update_tenant(id):
    data = request.get_json()
    tenant = Tenant.query.get_or_404(id)
    tenant.firstname = data.get("firstname", tenant.firstname)
    tenant.lastname = data.get("lastname", tenant.lastname)
    tenant.email = data.get("email", tenant.email)
    tenant.phone_number = data.get("phone_number", tenant.phone_number)
    tenant.house_id = data.get("house_id", tenant.house_id)
    db.session.commit()
    return jsonify({"message": "Tenant updated"})

# Delete Tenant
@tenants_bp.route("/<int:id>", methods=["DELETE"])
def delete_tenant(id):
    tenant = Tenant.query.get_or_404(id)
    db.session.delete(tenant)
    db.session.commit()
    return jsonify({"message": f"{tenant.firstname} {tenant.lastname} has been deleted"})
