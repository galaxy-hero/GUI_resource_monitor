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
    sleep(2)
