import pytest
from sqlalchemy.exc import IntegrityError

from app import app
from models import db, User, Recipe

class TestRecipe:
    '''Recipe in models.py'''

    def create_user(self):
        user = User(
            username="testuser",
            image_url="https://via.placeholder.com/150",
            bio="Test bio"
        )
        user.password_hash = "password123"
        db.session.add(user)
        db.session.commit()
        return user

    def test_has_attributes(self):
        '''has attributes title, instructions, and minutes_to_complete.'''
        
        with app.app_context():
            Recipe.query.delete()
            User.query.delete()
            db.session.commit()

            user = self.create_user()

            recipe = Recipe(
                title="Delicious Shed Ham",
                instructions="""Or kind rest bred with am shed then. In""" + \
                    """ raptures building an bringing be. Elderly is detract""" + \
                    """ tedious assured private so to visited. Do travelling""" + \
                    """ companions contrasted it. Mistress strongly remember""" + \
                    """ up to. Ham him compass you proceed calling detract.""" + \
                    """ Better of always missed we person mr. September""" + \
                    """ smallness northward situation few her certainty""" + \
                    """ something.""",
                minutes_to_complete=60,
                user_id=user.id
            )

            db.session.add(recipe)
            db.session.commit()

            new_recipe = Recipe.query.filter(Recipe.title == "Delicious Shed Ham").first()

            assert new_recipe.title == recipe.title
            assert new_recipe.instructions == recipe.instructions
            assert new_recipe.minutes_to_complete == 60
            assert new_recipe.user_id == user.id

    def test_requires_title(self):
        '''requires each record to have a title.'''

        with app.app_context():
            Recipe.query.delete()
            User.query.delete()
            db.session.commit()

            user = self.create_user()

            recipe = Recipe(
                instructions="Some instructions with more than 50 characters." * 2,
                minutes_to_complete=20,
                user_id=user.id
            )
            
            with pytest.raises(IntegrityError):
                db.session.add(recipe)
                db.session.commit()

    def test_requires_50_plus_char_instructions(self):
        '''must raise either an IntegrityError or a ValueError if instructions < 50 characters.'''
        with app.app_context():
            Recipe.query.delete()
            User.query.delete()
            db.session.commit()

            user = self.create_user()

            with pytest.raises((IntegrityError, ValueError)):
                recipe = Recipe(
                    title="Generic Ham",
                    instructions="Too short",
                    minutes_to_complete=20,
                    user_id=user.id
                )
                db.session.add(recipe)
                db.session.commit()
