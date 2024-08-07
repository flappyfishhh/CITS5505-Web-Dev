from app import create_app, db
from flask_migrate import Migrate
from app.config import DeploymentConfig

flaskApp = create_app(DeploymentConfig)
migrate = Migrate(flaskApp,db)