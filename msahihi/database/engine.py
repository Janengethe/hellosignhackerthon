#!/usr/bin/env python3
"""
Engine Module
"""
from typing import Any
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()


class Agent(Base, UserMixin):
    __tablename__ = "agent"

    id = Column(Integer, nullable=False, primary_key=True)
    agent_no = Column(String(10), nullable=False)
    agent_name = Column(String(100), nullable=False)
    email = Column(String(250), unique=True, nullable=False)
    password = Column(String(20), nullable=False)
    transaction = relationship("Transaction", backref="agent")

    def __repr__(self):
        return '<Agent %r>' % self.agent_name

    def __init__(self, *args, **kwargs) -> None:
        self.agent_no = ""
        self.agent_name = ""
        self.password = ""
        self.email = ""

        for k, v in kwargs.items():
            if k == 'password':
                Agent.__set_password(self, v)
            else:
                setattr(self, k, v)

    def __set_password(self, password: str) -> None:
        """
            Encrypts password
        """
        secure_pw = generate_password_hash(password)
        setattr(self, 'password', secure_pw)


class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(Integer, nullable=False, primary_key=True)
    national_id = Column(String(10), nullable=False)
    txn_type = Column(String(1), nullable=False)
    value = Column(Integer, nullable=False)
    txn_id = Column(String(10), nullable=False, unique=True)

    agent_id = Column(Integer, ForeignKey('agent.id'), nullable=False)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.national_id = ""
        self.txn_type = ""
        self.value = 0
        self.txn_id = ""

        for k, v in kwargs.items():
            setattr(self, k, v)

class DB():
    __engine = None
    __session = None

    def __init__(self) -> None:
        self.__engine = create_engine("sqlite:///db.db")
        self.__session = Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(factory)
        self.__session = Session

    def save(self, obj):
        try:
            self.__session.add(obj)
            self.__session.commit()
        except ValueError:
            self.__session.rollback()

    def get_agent_by_id(self, agent_id):
        try:
            obj = self.__session.query(Agent).filter_by(id=agent_id).first()
            return obj
        except TypeError:
            print("No Agent by that Id")
            return None

    def get_agent_by_no(self, agent_no):
        try:
            obj = self.__session.query(Agent).filter_by(agent_no=agent_no).first()
            return obj
        except ValueError:
            print("No such Agent Number")
            return None

    def delete(self, obj):
        self.__session.delete(obj)
        self.__session.commit()
        self.__session.flush()

    def all(self, agent_id):
        try:
            obj = self.__session.query(Transaction).filter_by(agent_id=agent_id).all()
            return obj
        except(IndexError, TypeError):
            return None

    def reload(self):
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine, expire_on_commit=False))

    def close(self):
        self.__session.close()
