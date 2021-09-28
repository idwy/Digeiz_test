from digeiz_api.app import db


class Account(db.Model):
    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    malls = db.relationship('Mall', cascade="all,delete", backref="account")

    def __init__(self, name):
        self.name = name


class Mall(db.Model):
    __tablename__ = "mall"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    units = db.relationship('Unit', cascade="all,delete")

    def __init__(self, name, account_id):
        self.name = name
        self.account_id = account_id


class Unit(db.Model):
    __tablename__ = "unit"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    mall_id = db.Column(db.Integer, db.ForeignKey('mall.id'))

    def __init__(self, name, mall_id):
        self.name = name
        self.mall_id = mall_id
