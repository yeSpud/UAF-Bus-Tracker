from peewee import *

db = PostgresqlDatabase("postgres", user="postgres", password="postgres", host="uaf-bus-tracker-postgres-1", port=5432)

class BaseModel(Model):
    class Meta:
        database = db

class Route(BaseModel):
    name = CharField(unique=True)

class Stop(BaseModel):
    id = IntegerField(unique=True)
    name = CharField()
    route = ForeignKeyField(Route, backref="stops")

class Arrival(BaseModel):
    stop = ForeignKeyField(Stop, backref="arrivals")
    time = TimestampField()