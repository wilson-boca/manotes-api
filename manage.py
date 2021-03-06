#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import sys

from app import initialize

manager = Manager(initialize.web_app)


def register_migrate(manager):
    from app.models import db, Note, User
    migrate = Migrate(initialize.web_app, db)
    manager.add_command('db', MigrateCommand)
    return migrate


if __name__ == '__main__':
    if 'db' in sys.argv:
        migrate = register_migrate(manager)
    manager.run()
