from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class Feedback(db.Model):
    """feedback given by user"""

    __tablename__ = "feedback"

    id = db.Column(db.Integer,primary_key=True, autoincrement=True, unique=True)
    title = db.Column(db.String(100), nullable=False) 
    content = db.Column(db.Text, nullable=False) 
    username = db.Column(db.String(20), db.ForeignKey('users.username'), nullable=False)




class User(db.Model):
    """Site user."""

    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)    
    last_name = db.Column(db.String(30), nullable=False)           
    email = db.Column(db.String(50), nullable=False, unique=True)

    feedback = db.relationship("Feedback", backref="user", cascade="all,delete")

    # start_register
    @classmethod
    def register(cls, username, password, first_name, last_name, email):
        """Register a user, hashing their password."""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        user = cls(
            username=username,
            password=hashed_utf8,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        db.session.add(user)
        return user

    # start_authenticate
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False
    # end_authenticate    
