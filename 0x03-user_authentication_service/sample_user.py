#!/usr/bin/python3
"""construct a database table called users"""
from sqlalchemy import create_engine, Table, Column, Integer,
String, MetaData, ForeignKey

engine = create_engine('sqlite:///:memory:', echo=True)
metadata = MetaData()
users = Table('users', metadata,
            Column('id', Integer, primary_key=True),
            Column('email', String, nullable=False),
            Column('hashes_password' String, nullable=False),
            Column('session_id', String, nullable=True),
            Column('reset_token', String, nullable=True)
              )
metadata.create_all(engine)
