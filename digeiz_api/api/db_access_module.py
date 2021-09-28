from digeiz_api.app import db
from digeiz_api.database.models import Account, Mall, Unit
from digeiz_api.api.custom_exceptions import AccountNotFoundException, MallNotFoundException, UnitNotFoundException


def create_account(data):
    name = data.get('name')
    account = Account(name)
    db.session.add(account)
    db.session.commit()
    return account


def bulk_insert_accounts(data):
    names = data.get('names')
    accounts_to_insert = [Account(name) for name in names]
    db.session.bulk_save_objects(accounts_to_insert, return_defaults = True)
    db.session.commit()
    return accounts_to_insert


def update_account(account_id, data):

    if(Account.query.filter(Account.id == account_id).first() is not None):
        account = Account.query.filter(Account.id == account_id).one()
        account.name = data.get('name')
        db.session.commit()
        return account
    else:
        raise AccountNotFoundException(account_id)


def delete_account(account_id):
    if(Account.query.filter(Account.id == account_id).first() is not None):
        account = Account.query.filter(Account.id == account_id).one()
        db.session.delete(account)
        db.session.commit()
    else:
        raise AccountNotFoundException(account_id)


def create_mall(data):
    name = data.get('name')
    account_id = data.get('account_id')
    if(Account.query.filter(Account.id == account_id).first() is not None):
        mall = Mall(name, account_id)
        db.session.add(mall)
        db.session.commit()
        return mall
    else:
        raise AccountNotFoundException(account_id)


def update_mall(mall_id, data):

    if(Mall.query.filter(Mall.id == mall_id).first() is not None):
        mall = Mall.query.filter(Mall.id == mall_id).one()
        mall.name = data.get('name')
        db.session.commit()
        return mall
    else:
        raise MallNotFoundException(mall_id)


def delete_mall(mall_id):

    if(Mall.query.filter(Mall.id == mall_id).first() is not None):
        mall = Mall.query.filter(Mall.id == mall_id).one()
        db.session.delete(mall)
        db.session.commit()
    else:
        raise MallNotFoundException(mall_id)


def create_unit(data):
    name = data.get('name')
    mall_id = data.get('mall_id')
    if(Mall.query.filter(Mall.id == mall_id).first() is not None):
        unit = Unit(name, mall_id)
        db.session.add(unit)
        db.session.commit()
        return unit
    else:
        raise MallNotFoundException(mall_id)


def update_unit(unit_id, data):

    if(Unit.query.filter(Unit.id == unit_id).first() is not None):
        unit = Unit.query.filter(Unit.id == unit_id).one()
        unit.name = data.get('name')
        db.session.commit()
        return unit
    else:
        raise UnitNotFoundException(unit_id)


def delete_unit(unit_id):

    if(Unit.query.filter(Unit.id == unit_id).first() is not None):
        unit = Unit.query.filter(Unit.id == unit_id).one()
        db.session.delete(unit)
        db.session.commit()
    else:
        raise UnitNotFoundException(unit_id)
