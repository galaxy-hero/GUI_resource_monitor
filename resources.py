import psutil


def get_CPU_usage():
    psutil.cpu_percent()
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    return psutil.virtual_memory().percent

def get_disk_usage(partition):
    return psutil.disk_usage(partition).percent

def get_system_partitions():
    partitions = psutil.disk_partitions(all=True)
    result = []
    for partition in partitions:
        if partition.opts == 'rw,fixed':
            result.append(partition.mountpoint)
    return result

if __name__ == '__main__':
    #print("CPU usage is: ")
    print(get_system_partitions())