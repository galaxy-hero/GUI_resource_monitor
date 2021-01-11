import resources, models
from time import sleep

while True:
    models.CPUMonitor.insert(value=resources.get_CPU_usage()).execute()
    models.MemoryMonitor.insert(value=resources.get_memory_usage()).execute()
    models.DiskMonitor.insert(value=resources.get_disk_usage()).execute()

    sleep(2)
