from peewee import *
from playhouse.postgres_ext import PostgresqlExtDatabase
from datetime import datetime

db = PostgresqlExtDatabase('resource_monitor', user='postgres', password='admin')

class CPUMonitor(Model):
    value = FloatField()
    time = DateTimeField(default=datetime.now)

    class Meta:
        database = db

class MemoryMonitor(Model):
    value = FloatField()
    time = DateTimeField(default=datetime.now)

    class Meta:
        database = db

class DiskMonitor(Model):
    value = FloatField()
    time = DateTimeField(default=datetime.now)

    class Meta:
        database = db

if __name__ == '__main__':
    db.connect()
    db.create_tables([CPUMonitor, MemoryMonitor, DiskMonitor])