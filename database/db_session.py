from peewee import *
db = PostgresqlDatabase('application', host='localhost', port=5432, user='postgres', password='password')
db.connect()

