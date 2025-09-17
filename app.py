from flask import Flask, jsonify
from flask_migrate import Migrate
from config import Config
from models import db, Apartment, House, Tenant
from routes.apartments import apartments_bp
from routes.houses import houses_bp
from routes.tenants import tenants_bp


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(apartments_bp)
app.register_blueprint(houses_bp)
app.register_blueprint(tenants_bp)


@app.route("/")
def home():
    return {"Message": "Miliki_Housing API is running!!"}


if __name__ == "__main__":
    app.run(debug=True)
