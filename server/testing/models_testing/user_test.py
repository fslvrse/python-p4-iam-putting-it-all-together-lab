from sqlalchemy.exc import IntegrityError
import pytest

from app import app
from models import db, User, Recipe

class TestUser:
    '''User in models.py'''

    def test_has_attributes(self):
        '''has attributes username, _password_hash, image_url, and bio.'''

        with app.app_context():

            User.query.delete()
            db.session.commit()

            user = User(
                username="Liz",
                image_url="https://prod-images.tcm.com/Master-Profile-Images/ElizabethTaylor.jpg",
                bio="""Dame Elizabeth Rosemond Taylor DBE (February 27, 1932 - March 23, 2011) was a British-American actress."""
            )
            user.password_hash = "whosafraidofvirginiawoolf"

            db.session.add(user)
            db.session.commit()

            created_user = User.query.filter(User.username == "Liz").first()

            assert created_user.username == "Liz"
            assert created_user.image_url == "https://prod-images.tcm.com/Master-Profile-Images/ElizabethTaylor.jpg"
            assert created_user.bio.startswith("Dame Elizabeth Rosemond Taylor")

            with pytest.raises(AttributeError):
                created_user.password_hash

    def test_requires_username(self):
        '''requires each record to have a username.'''

        with app.app_context():

            User.query.delete()
            db.session.commit()

            user = User(
                image_url="https://example.com",
                bio="Bio here"
            )
            user.password_hash = "testpassword"

            with pytest.raises(IntegrityError):
                db.session.add(user)
                db.session.commit()

    def test_requires_unique_username(self):
        '''requires each record to have a unique username.'''

        with app.app_context():

            User.query.delete()
            db.session.commit()

            user_1 = User(
                username="Ben",
                image_url="https://example.com/1",
                bio="First Ben"
            )
            user_1.password_hash = "password123"

            user_2 = User(
                username="Ben",
                image_url="https://example.com/2",
                bio="Second Ben"
            )
            user_2.password_hash = "password456"

            db.session.add(user_1)
            db.session.commit()

            with pytest.raises(IntegrityError):
                db.session.add(user_2)
                db.session.commit()

    def test_has_list_of_recipes(self):
        '''has records with lists of recipes records attached.'''

        with app.app_context():

            User.query.delete()
            Recipe.query.delete()
            db.session.commit()

            user = User(
                username="Prabhdip",
                image_url="https://example.com",
                bio="Food enthusiast"
            )
            user.password_hash = "hamlover123"

            recipe_1 = Recipe(
                title="Delicious Shed Ham",
                instructions="""Or kind rest bred with am shed then. In raptures building an bringing be. Elderly is detract tedious assured private so to visited. Do travelling companions contrasted it. Mistress strongly remember up to. Ham him compass you proceed calling detract. Better of always missed we person mr. September smallness northward situation few her certainty something.""",
                minutes_to_complete=60,
            )
            recipe_2 = Recipe(
                title="Hasty Party Ham",
                instructions="""As am hastily invited settled at limited civilly fortune me. Really spring in extent an by. Judge but built gay party world. Of so am he remember although required. Bachelor unpacked be advanced at. Confined in declared marianne is vicinity.""",
                minutes_to_complete=30,
            )

            user.recipes.append(recipe_1)
            user.recipes.append(recipe_2)

            db.session.add(user)
            db.session.commit()

            # Confirm user and recipe IDs were generated
            assert user.id is not None
            assert recipe_1.id is not None
            assert recipe_2.id is not None

            # Confirm recipes were attached to user
            assert recipe_1 in user.recipes
            assert recipe_2 in user.recipes
