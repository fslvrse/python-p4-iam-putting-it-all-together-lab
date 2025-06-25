from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=True)
    image_url = db.Column(db.String, nullable=False, default="https://via.placeholder.com/150")
    bio = db.Column(db.String, nullable=False, default="No bio provided.")

    recipes = db.relationship('Recipe', backref='user', cascade='all, delete-orphan')

    serialize_rules = ('-recipes.user',)

    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password hashes may not be viewed.")

    @password_hash.setter
    def password_hash(self, password):
        if password is None or password == "":
            raise ValueError("Password must be present.")
        password_bytes = password.encode('utf-8')
        password_hash = bcrypt.generate_password_hash(password_bytes)
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        if password is None:
            return False
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))

    @validates('username')
    def validate_username(self, key, username):
        if not username or username.strip() == "":
            raise ValueError("Username must be present.")
        return username

    def __repr__(self):
        return f'<User {self.username}>'


class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String, nullable=False)
    minutes_to_complete = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    serialize_rules = ('-user.recipes',)

    @validates('title')
    def validate_title(self, key, title):
        if not title or title.strip() == "":
            raise ValueError("Title must be present.")
        return title

    @validates('instructions')
    def validate_instructions(self, key, instructions):
        if not instructions or len(instructions.strip()) < 50:
            raise ValueError("Instructions must be at least 50 characters.")
        return instructions

    @validates('minutes_to_complete')
    def validate_minutes_to_complete(self, key, minutes):
        if minutes is None:
            raise ValueError("Minutes to complete must be provided.")
        if not isinstance(minutes, int):
            raise ValueError("Minutes to complete must be an integer.")
        return minutes

    def __repr__(self):
        return f'<Recipe {self.title}>'