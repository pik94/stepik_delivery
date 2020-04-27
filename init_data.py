from pathlib import Path
from typing import NoReturn

import pandas as pd

from delivery_site import app, db_model
from delivery_site import config as cfg
from delivery_site.database import Category, Meal, User


def main() -> NoReturn:
    path = Path.cwd()
    categories = pd.read_csv(path / 'categories.csv', header=0)
    categories.rename(columns={'id': 'category_id', 'title': 'cat_title'},
                      inplace=True)
    meals = pd.read_csv(path / 'meals.csv', header=0)

    data = pd.merge(categories, meals, on='category_id')
    categories = data.groupby(by=['cat_title'])['category_id'].mean()
    categories = {category_id: Category(title=title)
                  for title, category_id in categories.items()}

    meals = [
        Meal(
            title=row['title'],
            price=row['price'],
            description=row['description'],
            picture=row['picture'],
            category_id=row['category_id'],
            category=categories[row['category_id']])
        for _, row in data.iterrows()
    ]

    default_user = User(id=0,
                        email=cfg.ADMIN_LOGIN,
                        password=User.hash_password(cfg.ADMIN_PASSWORD))
    with app.app_context():
        db_model.session.add_all(meals)
        db_model.session.add_all(categories.values())
        db_model.session.add(default_user)
        db_model.session.commit()


if __name__ == '__main__':
    main()
