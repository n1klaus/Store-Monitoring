#!/usr/bin/python3

from db.db_engine import DBEngine

db: DBEngine = DBEngine()
db.reload()
