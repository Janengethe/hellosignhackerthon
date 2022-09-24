from werkzeug.security import generate_password_hash
from app import db
from flask_login import UserMixin

class Agent(db.Model, UserMixin):
    __tablename__ = "agent"

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    agent_no = db.Column(db.String(10), nullable=False)
    agent_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    transaction = db.relationship("Transaction", backref="agent")
    
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


class Transaction(db.Model):
    __tablename__ = "transaction"

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    national_id = db.Column(db.String(10), nullable=False)
    txn_type = db.Column(db.String(1), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    txn_id = db.Column(db.String(10), nullable=False, unique=True)

    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'), nullable=False)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.national_id = ""
        self.txn_type = ""
        self.value = 0
        self.txn_id = ""

        for k, v in kwargs.items():
            setattr(self, k, v)
