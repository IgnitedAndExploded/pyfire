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
from pyfire.logger import Logger

log = Logger(__name__)

engine = create_engine(config.get('database', 'dburi'))

Base = declarative_base(bind=engine)
Session = scoped_session(sessionmaker())
