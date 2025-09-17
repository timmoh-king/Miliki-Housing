from flask import Flask, jsonify
from models import db, Apartment, House, Tenant
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route("/")
def home():
    return {"Message": "Miliki_Housing API is running!!"}


if __name__ == "__main__":
    app.run(debug=True)
