from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Text, Float,
    ForeignKey
)

from sqlalchemy.orm import mapper, relationship, synonym

from games.domainmodel import model

# global variable giving access to the MetaData (schema) information of the database
metadata = MetaData()

publishers_table = Table(
    'publishers', metadata,
    Column('name', String(255), primary_key=True)  # nullable=False, unique=True)
)

games_table = Table(
    'games', metadata,
    Column('game_id', Integer, primary_key=True),
    Column('game_title', Text, nullable=False),
    Column('game_price', Float, nullable=False),
    Column('release_date', String(50), nullable=False),
    Column('game_description', String(255), nullable=True),
    Column('game_image_url', String(255), nullable=True),
    Column('game_website_url', String(255), nullable=True),
    Column('publisher_name', ForeignKey('publishers.name'))
)

genres_table = Table(
    'genres', metadata,
    # For genre again we only have name.
    Column('genre_name', String(64), primary_key=True, nullable=False)
)

games_genres_table = Table(
    'game_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('game_id', ForeignKey('games.game_id')),
    Column('genre_name', ForeignKey('genres.genre_name'))
)

users_table = Table(
    'users', metadata,
    Column('user_id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(64), nullable=False),
    Column('password', String(64), nullable=False),
)

favourites_table = Table(
    'favourites', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.user_id')),
    Column('game_ids', Text, nullable=True)
)

reviews_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('game_id', ForeignKey('games.game_id')),
    Column('user_id', ForeignKey('users.user_id')),
    Column('review_text', String(64), nullable=False),
    Column('rating', Integer, nullable=False)
)


def map_model_to_tables():
    mapper(model.Publisher, publishers_table, properties={
        '_Publisher__publisher_name': publishers_table.c.name,
    })

    mapper(model.Game, games_table, properties={
        '_Game__game_id': games_table.c.game_id,
        '_Game__game_title': games_table.c.game_title,
        '_Game__price': games_table.c.game_price,
        '_Game__release_date': games_table.c.release_date,
        '_Game__description': games_table.c.game_description,
        '_Game__image_url': games_table.c.game_image_url,
        '_Game__website_url': games_table.c.game_website_url,
        '_Game__publisher': relationship(model.Publisher),
        '_Game__genres': relationship(model.Genre, secondary=games_genres_table),
        '_Game__reviews': relationship(model.Review, back_populates='_Review__game')
    })

    mapper(model.Genre, genres_table, properties={
        '_Genre__genre_name': genres_table.c.genre_name,
    })

    mapper(model.User, users_table, properties={
        '_User__user_id': users_table.c.user_id,
        '_User__username': users_table.c.username,
        '_User__password': users_table.c.password,
        '_User__reviews': relationship(model.Review, back_populates='_Review__user')
    })

    mapper(model.Review, reviews_table, properties={
        '_Review__comment': reviews_table.c.review_text,
        '_Review__rating': reviews_table.c.rating,
        '_Review__user': relationship(model.User, back_populates='_User__reviews'),
        '_Review__game': relationship(model.Game, back_populates='_Game__reviews'),
    })