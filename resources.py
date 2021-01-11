import psutil


def get_CPU_usage():
    psutil.cpu_percent()
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    return psutil.virtual_memory().percent

def get_disk_usage():
    return psutil.disk_usage('E:\\').percent

def get_disk_space():
    return 0

if __name__ == '__main__':
    #print("CPU usage is: ")
    print(get_disk_usage())