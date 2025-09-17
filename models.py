from collections import UserList
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Apartment(db.Model):
    __tablename__ = "apartments"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    no_of_units = db.Column(db.Integer, nullable=False)

    units = db.relationship("House", backref="apartment", lazy=True)

class House(db.Model):
    __tablename__ = "houses"
    id = db.Column(db.Integer, primary_key=True)
    apartment_id = db.Column(db.Integer, db.ForeignKey("apartments.id"), nullable=False)
    house_no = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(120))
    comments = db.Column(db.Text)
    rent = db.Column(db.Float, nullable=False)

    tenant = db.relationship("Tenant", backref="house", uselist=False)

class Tenant(db.Model):
    __tablename__ = "tenants"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20))
    house_id = db.Column(db.Integer, db.ForeignKey("houses.id"), nullable=False)
    date_rented = db.Column(db.Date, default=datetime.utcnow)

    def duration_in_months(self):
        today = datetime.utcnow().date()
        delta = (today.year - self.date_rented.year) * 12 + (today.month - self.date_rented.month)
        return max(delta, 0)
    
    def total_rent_paid(self):
        if not self.house:
            return 0
        return self.duration_in_months() * self.house.rent
