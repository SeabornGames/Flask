from example_flask_app.settings.global_import import *
from example_flask_app.endpoints.user.models import User
from seaborn.flask_server.models import ApiModel
from seaborn.timestamp.timestamp import cst_now, datetime_to_str

from sqlalchemy.ext.associationproxy import association_proxy

log.trace("Importing endpoint account.models")
import re

ACCOUNT_STATUS_ENUM = ['Active',
                       'Locked',
                       'Suspended',
                       'Closed']

GENERIC_REGEX = re.compile(r'^[A-Za-z0-9_]{2,30}$')


class Account(db.Model, ApiModel):
    __tablename__ = "account"
    __table_args__ = {'extend_existing': True}

    account_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usr.user_id'))
    name = db.Column(db.String, default=datetime_to_str, unique=True)
    funds = db.Column(db.Float, default=0.0)
    status = db.Column(db.Enum(*ACCOUNT_STATUS_ENUM, name='account_status'),
                       default=ACCOUNT_STATUS_ENUM[0])
    created_timestamp = db.Column(db.DateTime(timezone=True), default=cst_now)

    users = association_proxy('user_access', 'user')

    @classmethod
    def keys(cls):
        return ['account_id', 'name', 'user_id', 'funds', 'user_ids']

    @property
    def user_ids(self):
        """
        :return: list of int of users who are authorized on this account
        """
        return [access.user_id for access in self.user_access]

    @property
    def is_active(self):
        return self.status == 'Active'

    @classmethod
    def validator_name(cls, name, **kwargs):
        """ This will determine if the user name is valid"""
        assert GENERIC_REGEX.match(name), 'Invalid Account name: %s' % name

    @classmethod
    def validate_status(cls, status, **kwargs):
        assert status in ACCOUNT_STATUS_ENUM, "Account status is not valid"
