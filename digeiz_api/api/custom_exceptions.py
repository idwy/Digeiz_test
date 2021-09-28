from datetime import datetime


def current_time():
    return datetime.now()


class AccountNotFoundException(Exception):

    def __init__(self, account_id):
        self.account_id = account_id


class MallNotFoundException(Exception):

    def __init__(self, mall_id):
        self.mall_id = mall_id


class UnitNotFoundException(Exception):

    def __init__(self, unit_id):
        self.unit_id = unit_id
