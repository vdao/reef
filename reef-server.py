from flask_migrate import Migrate, upgrade
from reef import create_app, db

application = create_app()
migrate = Migrate(application, db)
