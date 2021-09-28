from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy

flask_api = Flask(__name__)
flask_api.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_api.db'
app = Api(app=flask_api)
db = SQLAlchemy(flask_api)


def init_db(db):
    from digeiz_api.database.models import Account, Mall, Unit
    db.create_all()


def init_controller_nspaces():
    from digeiz_api.api.endpoints.accounts import ns_accounts
    from digeiz_api.api.endpoints.malls import ns_malls
    from digeiz_api.api.endpoints.units import ns_units


init_db(db)
init_controller_nspaces()

if __name__ == '__main__':
    app.run(debug=True)
