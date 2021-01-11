import psutil


def get_CPU_usage():
    """
    Queries the current CPU usage and returns the percent value of it
    :return: The current CPU usage percent
    :rtype: float
    """
    psutil.cpu_percent()
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    """
    Queries the currently used memory (RAM) percent
    :return: The percent of RAM usage
    :rtype: float
    """
    return psutil.virtual_memory().percent

def get_disk_usage(partition):
    """
    Queries the current storage usage for `partition`
    :param partition: The path of the partition to be queried (e.g. C:\\)
    :return: The percent of space usage for `partition`
    :rtype: float
    """
    return psutil.disk_usage(partition).percent

def get_system_partitions():
    """
    Queries the list of rw,fixed partitions on the system
    :return: Returns the list of rw,fixed partitions on the system
    :rtype: list
    """
    partitions = psutil.disk_partitions(all=True)
    result = []
    for partition in partitions:
        if partition.opts == 'rw,fixed':
            result.append(partition.mountpoint)
    return result

def get_network_bytes():
    """
    Queries the currently, system-wide, network usage
    :return: Returns the following fields:
         - bytes_sent:   number of bytes sent
         - bytes_recv:   number of bytes received
         - packets_sent: number of packets sent
         - packets_recv: number of packets received
         - errin:        total number of errors while receiving
         - errout:       total number of errors while sending
         - dropin:       total number of incoming packets which were dropped
         - dropout:      total number of outgoing packets which were dropped
                         (always 0 on macOS and BSD)
    """
    psutil.net_io_counters.cache_clear()
    return psutil.net_io_counters(nowrap=False)

if __name__ == '__main__':
    #print("CPU usage is: ")
    print(get_network_bytes())