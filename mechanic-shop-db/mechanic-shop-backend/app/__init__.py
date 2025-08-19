# app/__init__.py
from flask import Flask, jsonify
from .config import Config, os
from .extensions import db, migrate, ma
from flask_swagger_ui import get_swaggerui_blueprint

def create_app(config_overrides=None):
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(Config)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "fallback_dev_secret")

    if config_overrides:
        app.config.update(config_overrides)

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    # --- Swagger UI ---
    SWAGGER_URL = "/docs"
    API_URL = "/swagger.json"
    swaggerui_bp = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={"app_name": "Mechanic Shop API"},
    )
    app.register_blueprint(swaggerui_bp, url_prefix=SWAGGER_URL)

    # provide the swagger.json endpoint
    from app.swagger import swagger_spec
    @app.route("/swagger.json")
    def swagger_json():
        return jsonify(swagger_spec)

    # --- Blueprints ---
    from .blueprints.customers.routes import customers_bp
    from .blueprints.Inventory.routes import inventory_bp
    from .blueprints.mechanics.routes import mechanics_bp
    from .blueprints.service_tickets.routes import tickets_bp
    from .blueprints.vehicles.routes import vehicles_bp
    from .blueprints.customers.ticket_routes import customer_ticket_bp
    from .blueprints.mechanics.mechanic_ticket_routes import mechanic_ticket_bp
    from .blueprints.auth.routes import auth_bp

    # Register with prefixes the tests expect
    app.register_blueprint(customers_bp,       url_prefix="/customers")
    app.register_blueprint(inventory_bp,       url_prefix="/inventory")
    app.register_blueprint(mechanics_bp,       url_prefix="/mechanics")
    app.register_blueprint(tickets_bp,         url_prefix="/service_tickets")  # ← fix
    # the following aren’t used by tests but keep them available
    app.register_blueprint(vehicles_bp,        url_prefix="/vehicles")
    app.register_blueprint(customer_ticket_bp, url_prefix="/customer")
    app.register_blueprint(mechanic_ticket_bp, url_prefix="/mechanic")
    app.register_blueprint(auth_bp)

    return app
