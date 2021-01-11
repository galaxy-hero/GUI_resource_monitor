from models import CPUMonitor, MemoryMonitor, Partition, DiskMonitor, NetworkSentMonitor, NetworkReceiveMonitor
import tkcalendar
from tkinter import *
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
style.use('ggplot')

root = Tk()
root.geometry('800x700+200+100')
root.title('Resource Monitor')
root.state('zoomed')
root.config(background='#fafafa')


def generate_plot():
    """
    Generates a plot based on the `start_date`, `end_date` and `option_val` values
    :return: None
    """
    start = start_date.get_date()
    end = end_date.get_date()
    if end < start:
        return
    query_model = None
    if option_val.get() == "cpu":
        query_model = CPUMonitor
    elif option_val.get() == "ram":
        query_model = MemoryMonitor
    elif option_val.get() == "disk":
        query_model = DiskMonitor
    elif option_val.get() == "net_recv":
        query_model = NetworkReceiveMonitor
    elif option_val.get() == "net_sent":
        query_model = NetworkSentMonitor
    if not query_model:
        return
    query = list(query_model.select().where(query_model.time.between(start, end)))
    x_array = [i for i in range(1, len(query) + 1)]
    y_array = [i.value for i in query]
    fig, ax = plt.subplots()
    ax.plot(x_array, y_array)
    ax.set(ylabel=option_val.get(), xlabel='time', title='{} usage'.format(option_val.get()))
    ax.grid()
    plt.show()


def animate_cpu(i, line, x_array, y_array, ax1):
    """
    Callback used for animating CPU usage
    :param i: The current frame index (counter) provided by `FuncAnimation` object
    :param line: Drawn line in plot (Matplotlib)
    :param x_array: x values for plot
    :param y_array: y values for plot
    :param ax1: Figure object (Matplotlib)
    :return: None
    """
    cpu_entry = CPUMonitor.select().order_by(CPUMonitor.time.desc()).first()
    if cpu_entry is None:
        return
    y_array.pop(0)
    y_array.append(cpu_entry.value)
    line.set_data(x_array, y_array)

def animate_ram(i, line, x_array, y_array, ax1):
    """
    Callback used for animating RAM usage
    :param i: The current frame index (counter) provided by `FuncAnimation` object
    :param line: Drawn line in plot (Matplotlib)
    :param x_array: x values for plot
    :param y_array: y values for plot
    :param ax1: Figure object (Matplotlib)
    :return: None
    """
    ram_entry = MemoryMonitor.select().order_by(MemoryMonitor.time.desc()).first()
    if ram_entry is None:
        return
    y_array.pop(0)
    y_array.append(ram_entry.value)
    line.set_data(x_array, y_array)

def animate_partition(i, line, x_array, y_array, ax1, partition):
    """
    Callback used for animating one partition
    :param i: The current frame index (counter) provided by `FuncAnimation` object
    :param line: Drawn line in plot (Matplotlib)
    :param x_array: x values for plot
    :param y_array: y values for plot
    :param ax1: Figure object (Matplotlib)
    :param partition: `models.Partition` entry representing the database entry for a specific partition
    :return: None
    """
    disk_entry = DiskMonitor.select().where(DiskMonitor.partition == partition).order_by(DiskMonitor.time.desc()).first()
    if not disk_entry:
        return
    y_array.pop(0)
    y_array.append(disk_entry.value)
    line.set_data(x_array, y_array)

def animate_network_sent(i, line, x_array, y_array, ax1):
    """
    Callback used for animating the network sent bytes
    :param i: The current frame index (counter) provided by `FuncAnimation` object
    :param line: Drawn line in plot (Matplotlib)
    :param x_array: x values for plot
    :param y_array: y values for plot
    :param ax1: Figure object (Matplotlib)
    :return: None
    """
    nw_sent_entry = NetworkSentMonitor.select().order_by(NetworkSentMonitor.time.desc()).first()
    if nw_sent_entry is None:
        return
    y_array.pop(0)
    y_array.append(nw_sent_entry.value / (1024 ** 2))
    ax1.set_ylim(0, 100)
    line.set_data(x_array, y_array)

def animate_network_recv(i, line, x_array, y_array, ax1):
    """
    Callback used for animating the network received bytes
    :param i: The current frame index (counter) provided by `FuncAnimation` object
    :param line: Drawn line in plot (Matplotlib)
    :param x_array: x values for plot
    :param y_array: y values for plot
    :param ax1: Figure object (Matplotlib)
    :return: None
    """
    nw_recv_entry = NetworkReceiveMonitor.select().order_by(NetworkReceiveMonitor.time.desc()).first()
    if nw_recv_entry is None:
        return
    y_array.pop(0)
    y_array.append(nw_recv_entry.value / (1024 ** 2))
    ax1.set_ylim(0, 500)
    line.set_data(x_array, y_array)

def plot_entry(root, row=1, column=1, title='', ani_cb=None, extra_args=None, percent=True):
    """
    Function used for generating one plot, used to show usage of a specific resource
    :param root: the root Tk object
    :param row: the row of the grid where the plot is to be placed
    :param column: the column of the grid where the plot is to be placed
    :param title: the title of the plot
    :param ani_cb: the callback for the animation object
    :param extra_args: Additional arguments to be provided to the callback
    :param percent:
    :return:
    """
    xar = list(range(60))
    yar = [0 for i in range(60)]

    fig = plt.figure(figsize=(5, 2), dpi=100)
    ax1 = fig.add_subplot(1, 1, 1)

    ax1.set_ylim(0, 100)
    ax1.set_xlim(0, 60)
    ax1.set_title(title)
    line, = ax1.plot(xar, yar, 'r')
    plotcanvas = FigureCanvasTkAgg(fig, root)
    plotcanvas.get_tk_widget().grid(column=column, row=row)
    ani = animation.FuncAnimation(fig,
                                  ani_cb,
                                  fargs=[line, xar, yar, ax1] + (extra_args if extra_args else []),
                                  interval=2000, blit=False)
    return ani

cpu = plot_entry(root, ani_cb=animate_cpu, title='CPU Usage')
ram = plot_entry(root, row=1, column=2, ani_cb=animate_ram, title='RAM Usage')
first_part = 1
partition_animations = []
for partition in Partition.select():
    partition_animations.append(plot_entry(root,
                                           ani_cb=animate_partition,
                                           row=2, column=first_part,
                                           title="Partition {} usage".format(partition.path),
                                           extra_args=[partition]))
    first_part += 1

nw_sent = plot_entry(root,
                     row=3,
                     column=1,
                     percent=False,
                     ani_cb=animate_network_sent,
                     title='Network Sent Bytes Usage')
nw_recv = plot_entry(root,
                     row=3,
                     column=2,
                     percent=False,
                     ani_cb=animate_network_recv,
                     title='Network Received Bytes Usage')

start_date = tkcalendar.DateEntry(root, width=30, year=2021)
start_date.grid(row=1, column=3)

end_date = tkcalendar.DateEntry(root, width=30, year=2021)
end_date.grid(row=1, column=4)
option_val = StringVar(root)
option_val.set("cpu")
report = OptionMenu(root, option_val, "cpu", "ram", "disk", "net_sent", "net_recv")
report.grid(row=1, column=5)

generate_button = Button(root, text="Generate Plot", command=generate_plot)
generate_button.grid(row=1, column=6)

root.mainloop()