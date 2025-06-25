#!/usr/bin/env python3

from random import randint, choice as rc
from faker import Faker

from app import app
from models import db, Recipe, User

fake = Faker()

with app.app_context():
    print("Deleting all records...")
    db.session.query(Recipe).delete()
    db.session.query(User).delete()
    db.session.commit()  # ✅ Ensure deletions are committed

    print("Creating users...")

    users = []
    usernames = set()

    for _ in range(20):
        username = fake.first_name()
        while username in usernames:
            username = fake.first_name()
        usernames.add(username)

        user = User(
            username=username,
            bio=fake.paragraph(nb_sentences=3),
            image_url=fake.image_url()
        )
        user.password_hash = f"{username}password"  # ✅ Use property setter
        users.append(user)

    db.session.add_all(users)
    db.session.commit()  # ✅ Save users so we can reference IDs

    print("Creating recipes...")

    recipes = []
    for _ in range(100):
        user = rc(users)
        instructions = fake.paragraph(nb_sentences=8)

        recipe = Recipe(
            title=fake.sentence(),
            instructions=instructions,
            minutes_to_complete=randint(15, 90),
            user_id=user.id  # ✅ Associate with existing user
        )
        recipes.append(recipe)

    db.session.add_all(recipes)
    db.session.commit()

    print("✅ Seeding complete.")
