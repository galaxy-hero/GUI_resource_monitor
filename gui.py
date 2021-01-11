from models import CPUMonitor, MemoryMonitor, Partition, DiskMonitor
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



def animate_cpu(i, line, x_array, y_array):
    cpu_entry = CPUMonitor.select().order_by(CPUMonitor.time.desc()).first()
    if cpu_entry is None:
        return
    y_array.pop(0)
    y_array.append(cpu_entry.value)
    line.set_data(x_array, y_array)

def animate_ram(i, line, x_array, y_array):
    ram_entry = MemoryMonitor.select().order_by(MemoryMonitor.time.desc()).first()
    if ram_entry is None:
        return
    y_array.pop(0)
    y_array.append(ram_entry.value)
    line.set_data(x_array, y_array)

def animate_partition(i, line, x_array, y_array, partition):
    disk_entry = DiskMonitor.select().where(DiskMonitor.partition == partition).order_by(DiskMonitor.time.desc()).first()
    if not disk_entry:
        return
    y_array.pop(0)
    y_array.append(disk_entry.value)
    line.set_data(x_array, y_array)

def plot_entry(root, row=1, column=1, title='', ani_cb=None, extra_args=None):
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
                                  fargs=[line, xar, yar] + (extra_args if extra_args else []),
                                  interval=2000, blit=False)
    return ani

cpu = plot_entry(root, ani_cb=animate_cpu, title='CPU Usage')
ram = plot_entry(root, row=1, column=2, ani_cb=animate_ram, title='RAM Usage')
first_part = 1
partition_animations = []
for partition in Partition.select():
    partition_animations.append(plot_entry(root, ani_cb=animate_partition, row=2, column=first_part, title="Partition {} usage".format(partition.path), extra_args=[partition]))
    first_part += 1

start_date = tkcalendar.DateEntry(root, width=30, year=2021)
start_date.grid(row=1, column=3)

end_date = tkcalendar.DateEntry(root, width=30, year=2021)
end_date.grid(row=1, column=4)
option_val = StringVar(root)
option_val.set("cpu")
report = OptionMenu(root, option_val, "cpu", "ram", "disk")
report.grid(row=1, column=5)

generate_button = Button(root, text="Generate Plot", command=None)
generate_button.grid(row=1, column=6)

root.mainloop()