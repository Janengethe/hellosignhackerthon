#!/usr/bin/env python3
"""
Engine Module
"""
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm.session import Session

Base = declarative_base()

class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(Integer, nullable=False, primary_key=True)
    national_id = Column(String(10), nullable=False)
    txn_type = Column(String(1), nullable=False)
    value = Column(Integer, nullable=False)
    txn_id = Column(String(10), nullable=False, unique=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    agent_id = Column(Integer, ForeignKey('agent.id'))

class Agent(Base):
    __tablename__ = "agent"

    id = Column(Integer, nullable=False, primary_key=True)
    agent_no = Column(String(10), nullable=False)
    agent_name = Column(String(100), nullable=False)
    transaction = relationship("Transaction", backref="agent")

class Customer(Base):
    __tablename__ = "customer"

    id = Column(Integer, nullable=False, primary_key=True)
    national_id = Column(String(10), nullable=False)
    name = Column(String(250), nullable=False)
    transaction = relationship("Transaction", backref="customer")

    def __repr__(self):
        return '<User %r>' % self.name

class DB:
    
    def __init__(self) -> None:
        self.engine = create_engine("sqlite:///db.db", echo=True)
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)
        self.__session = None

    @property
    def _session(self):
        if self.__session is None:
            DBSession = sessionmaker(bind=self.engine)
            self.__session = DBSession()
        return self.__session

    
