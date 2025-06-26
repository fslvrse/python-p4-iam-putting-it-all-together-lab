#!/usr/bin/env python3

from random import randint, choice as rc
from faker import Faker

from app import app
from models import db, Recipe, User

fake = Faker()

with app.app_context():
    print("Deleting all records...")
    Recipe.query.delete()
    User.query.delete()

    users = []
    usernames = set()

    print("Creating users...")
    for _ in range(20):
        username = fake.unique.first_name()
        user = User(
            username=username,
            image_url=fake.image_url(),
            bio=fake.paragraph(nb_sentences=3),
        )
        user.password_hash = f"{username}password"
        users.append(user)

    db.session.add_all(users)
    db.session.commit()

    print("Creating recipes...")
    recipes = []

    for _ in range(100):
        user = rc(users)
        recipe = Recipe(
            title=fake.sentence(),
            instructions=fake.paragraph(nb_sentences=8) + " This makes it long enough to pass validation.",
            minutes_to_complete=randint(10, 90),
            user_id=user.id
        )
        recipes.append(recipe)

    db.session.add_all(recipes)
    db.session.commit()

    print("✅ Seeding complete.")
