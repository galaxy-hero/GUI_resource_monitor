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

class Partition(Model):
    path = TextField(unique=True)

    class Meta:
        database = db

class DiskMonitor(Model):
    value = FloatField()
    partition = ForeignKeyField(Partition)
    time = DateTimeField(default=datetime.now)

    class Meta:
        database = db

class NetworkReceiveMonitor(Model):
    value = IntegerField()
    time = DateTimeField(default=datetime.now)

    class Meta:
        database = db

class NetworkSentMonitor(Model):
    value = IntegerField()
    time = DateTimeField(default=datetime.now)

    class Meta:
        database = db

if __name__ == '__main__':
    db.connect()
    db.drop_tables([CPUMonitor, MemoryMonitor, DiskMonitor, Partition, NetworkReceiveMonitor, NetworkSentMonitor])
    db.create_tables([CPUMonitor, MemoryMonitor, DiskMonitor, Partition, NetworkReceiveMonitor, NetworkSentMonitor])