#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from typing import TypeVar, Any, Mapping
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
        self.__session = self._session
        ed_user = User(email=email, hashed_password=hashed_password)
        self.__session.add(ed_user)
        self.__session.commit()
        return ed_user

    def find_user_by(self, **kwargs) -> User:
        """find user by keyword arguments"""
        self.__session = self._session
        if not kwargs:
            raise InvalidRequestError()
        try:
            result = self.__session.query(User).filter_by(**kwargs).one_or_none()
        except NoResultFound:
            raise NoResultFound('no result found')
        except Exception as e:
            raise InvalidRequestError(f"not a valid request {str(e)}")

        return result

    def update_user(self, user_id: int, **kwargs) -> None:
        """locates and updates a particular user"""
        user = self.find_user_by(id=user_id)
        if not user:
            raise ValueError('no user with tha id')
        for key in kwargs.keys():
            if not hasattr(user, key):
                raise ValueError(f'no attribute named {key}')
            user.key = kwargs.get(key)
        self.__session.commit()
        return
