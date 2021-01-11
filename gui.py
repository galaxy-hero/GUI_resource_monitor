from models import CPUMonitor, MemoryMonitor, Partition, DiskMonitor

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
    y_array.pop(0)
    y_array.append(cpu_entry.value)
    line.set_data(x_array, y_array)

def animate_ram(i, line, x_array, y_array):
    ram_entry = MemoryMonitor.select().order_by(MemoryMonitor.time.desc()).first()
    y_array.pop(0)
    y_array.append(ram_entry.value)
    line.set_data(x_array, y_array)



def plot_entry(root, row=1, column=1, title='', ani_cb=None, extra_args=None):
    xar = list(range(60))
    yar = [0 for i in range(60)]

    fig = plt.figure(figsize=(7, 2), dpi=100)
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
root.mainloop()