from peewee import *
from playhouse.postgres_ext import PostgresqlExtDatabase
from datetime import datetime

db = PostgresqlExtDatabase('resource_monitor', user='postgres', password='admin')

class CPUMonitor(Model):
    """
    Table for storing CPU usage percent data
    Fields:
      - value: the percent value of CPU usage
      - time: the time when the CPU usage had that value
    """
    value = FloatField()
    time = DateTimeField(default=datetime.now)

    class Meta:
        database = db

class MemoryMonitor(Model):
    """
    Table for storing memory (RAM) usage
    Fields:
      - value: the percent of used up RAM
      - time: the time when the RAM usage had that value
    """
    value = FloatField()
    time = DateTimeField(default=datetime.now)

    class Meta:
        database = db

class Partition(Model):
    """
    Table for storing a list of local disk partitions
    Fields:
       - path: the path of the partition (e.g. C:\\)
    """
    path = TextField(unique=True)

    class Meta:
        database = db

class DiskMonitor(Model):
    """
    Table for storing disk usage
    Fields:
      - value: the percent of partition space used
      - partition: reference to a Partition entry
      - time: the time when the partition had that storage usage

    """
    value = FloatField()
    partition = ForeignKeyField(Partition)
    time = DateTimeField(default=datetime.now)

    class Meta:
        database = db

class NetworkReceiveMonitor(Model):
    """
    Table used for storing received bytes over the network
    Fields:
      - value: the value (in bytes) of the received bytes over the network
      - time: the time at the received bytes had the value
    """
    value = IntegerField()
    time = DateTimeField(default=datetime.now)

    class Meta:
        database = db

class NetworkSentMonitor(Model):
    """
    Table used for storing sent bytes over the network
    Fields:
      - value: the value (in bytes) of the sent bytes over the network
      - time: the time at the sent bytes had the value
    """
    value = IntegerField()
    time = DateTimeField(default=datetime.now)

    class Meta:
        database = db

if __name__ == '__main__':
    db.connect()
    db.drop_tables([CPUMonitor, MemoryMonitor, DiskMonitor, Partition, NetworkReceiveMonitor, NetworkSentMonitor])
    db.create_tables([CPUMonitor, MemoryMonitor, DiskMonitor, Partition, NetworkReceiveMonitor, NetworkSentMonitor])