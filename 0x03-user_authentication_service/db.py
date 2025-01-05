#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from typing import TypeVar
from user import Base
from user import User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ addes the user to the database"""
        Session = sessionmaker(bind=self._engine)
        self.__session = Session()
        ed_user = User(email=email, hashed_password=hashed_password)
        self.__session.add(ed_user)
        self.__session.commit()
        return ed_user

    def find_user_by(self, **kwargs) -> User:
        """find user by keyword arguments"""
        if not kwargs:
            raise InvalidRequestError()
        try:
            result = self.__session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound('no result found')
        except Exception as e:
            raise InvalidRequestError(f"not a valid request {str(e)}")

        return result
