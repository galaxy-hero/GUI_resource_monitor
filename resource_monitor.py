"""
Script used to gather system resources and insert them in a local PostgreSQL database every 1 seconds
"""
import resources, models
from time import sleep

partitions = []
for partition in resources.get_system_partitions():
    part, _ = models.Partition.get_or_create(path=partition)
    partitions.append(part)

while True:
    models.CPUMonitor.insert(value=resources.get_CPU_usage()).execute()
    models.MemoryMonitor.insert(value=resources.get_memory_usage()).execute()

    for partition in partitions:
        models.DiskMonitor.insert(value=resources.get_disk_usage(partition.path), partition=partition).execute()

    network_data = resources.get_network_bytes()
    models.NetworkSentMonitor.insert(value=network_data.bytes_sent).execute()
    models.NetworkReceiveMonitor.insert(value=network_data.bytes_recv).execute()
    sleep(1)
