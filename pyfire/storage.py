# -*- coding: utf-8 -*-
"""
    pyfire.storage
    ~~~~~~~~~~~~~~

    Storage provider, SQLAlchemy for now, maybe later we use NoSQL like
    the cool kids do, though Ninjas to protect tape databases are better

    :copyright: 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

__all__ = ['engine', 'Base', 'Session']

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import pyfire.configuration as config
from pyfire.jid import JID
from pyfire.logger import Logger

log = Logger(__name__)

engine = create_engine(config.get('database', 'dburi'))

Base = declarative_base(bind=engine)
Session = scoped_session(sessionmaker())

from sqlalchemy.types import TypeDecorator, VARCHAR

class JIDString(TypeDecorator):
    """Represents a full JID encoded as unicode string.

    Usage::

        JIDString

    """

    impl = VARCHAR

    def __init__(self):
        super(JIDString, self).__init__(3072)

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = str(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = JID(value)
        return value