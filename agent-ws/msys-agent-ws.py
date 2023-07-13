import os
import platform
import datetime

import psutil
import cpuinfo
from termcolor import colored, cprint

battery_percent = 0
battery_charging = False

os_name = platform.system() + ' ' + platform.release()
os_machine = platform.machine()
os_hostname = platform.node()
os_boot_time = 0

p_cpu_info = cpuinfo.get_cpu_info()
cpu_model = p_cpu_info['brand_raw']
cpu_freq = p_cpu_info['hz_advertised_friendly']
cpu_arch = p_cpu_info['arch_string_raw']
cpu_count = psutil.cpu_count()
cpu_load_avg = 0
cpu_load_per_core = 0

ram_total = 0
ram_free = 0
ram_swap_total = 0
ram_swap_free = 0

disk_mounts = 0
disk_total = 0
disk_free = 0
disk_r = 0
disk_w = 0

net_r = 0
net_w = 0

temperatures = 0
fans = 0

process_info = 0
process_list = 0


def fetch_data():
    global battery_percent
    global battery_charging
    global os_boot_time
    global cpu_load_avg
    global cpu_load_per_core
    global ram_total
    global ram_free
    global ram_swap_total
    global ram_swap_free
    global disk_mounts
    global disk_total
    global disk_free
    global disk_r
    global disk_w
    global net_r
    global net_w
    global temperatures
    global fans
    global process_info
    global process_list

    battery_percent = psutil.sensors_battery().percent
    battery_charging = psutil.sensors_battery().power_plugged

    os_boot_time = psutil.boot_time()

    cpu_load_avg = psutil.cpu_percent(interval=0.5, percpu=False)
    cpu_load_per_core = psutil.cpu_percent(interval=0.5, percpu=True)

    ram_total = psutil.virtual_memory()[0]
    ram_free = psutil.virtual_memory()[1]
    ram_swap_total = psutil.swap_memory().total
    ram_swap_free = psutil.swap_memory().free

    p_mounts = psutil.disk_partitions(all=False)
    p_mounts_clean = []
    for mount in p_mounts:
        p_mounts_clean.append(mount.device)
    disk_mounts = p_mounts_clean
    disk_total = psutil.disk_usage('/').total
    disk_free = psutil.disk_usage('/').free
    disk_r = psutil.disk_io_counters(nowrap=False).read_bytes
    disk_w = psutil.disk_io_counters(nowrap=False).write_bytes

    net_r = psutil.net_io_counters(nowrap=False).bytes_recv
    net_w = psutil.net_io_counters(nowrap=False).bytes_sent

    temperatures = psutil.sensors_temperatures()
    fans = psutil.sensors_fans()

    process_info = len(psutil.pids())
    i = psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent'])
    temp = []
    for process in i:
        temp.append([process.pid, process.name(), process.cpu_percent(), process.memory_percent()])
    process_list = temp


def print_data():
    cprint("🖳 SYSTEM INFO                                                                               ",
           "black", "on_light_grey", attrs=["bold", "underline"])
    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(os_boot_time)
    print(f'OS:\t\t\t {os_name}')
    print(f'Architecture:\t\t {os_machine}')
    print(f'Hostname:\t\t {os_hostname}')
    print(f'Boot time/uptime:\t {datetime.datetime.fromtimestamp(os_boot_time)}, {uptime}')
    print('\n')

    cprint("🗠 SYSTEM STATUS                                                                             ",
           "white", "on_dark_grey", attrs=["bold", "underline"])
    charge_status = 'charging' if battery_charging else 'discharging'
    print(f'🗲 Battery:\t\t {battery_percent}%, {charge_status}')
    print('\n')

    cprint("☰ CPU                                                                                       ",
           "white", "on_blue", attrs=["bold", "underline"])
    print(f'Model:\t\t\t {cpu_model}')
    print(f'Architecture:\t\t {cpu_arch}')
    print(f'Frequency:\t\t {cpu_freq}')
    print(f'Cores:\t\t\t {cpu_count}')
    print(f'Average load:\t\t {cpu_load_avg}%')
    print(f'Load per core:\t\t {cpu_load_per_core}')
    print('\n')

    cprint("☰ MEMORY                                                                                    ",
           "white", "on_yellow", attrs=["bold", "underline"])
    print(f'RAM:\t\t\t {ram_free / 1024000000} GB free out of {ram_total / 1024000000} GB')
    print(f'\t\t\t {100 - ram_free / ram_total * 100}% loaded')
    print(f'Swap file:\t\t {ram_swap_free / 1024000000} GB free out of {ram_swap_total / 1024000000} GB')
    print(f'\t\t\t {100 - ram_swap_free / ram_swap_total * 100}% loaded')
    print('\n')

    cprint("☰ DISK                                                                                      ",
           "white", "on_green", attrs=["bold", "underline"])
    print(f'Mounts:\t\t\t {disk_mounts}')
    print(f'Disk usage:\t\t {disk_free / 1024000000} GB free out of {disk_total / 1024000000} GB')
    print(f'\t\t\t {100 - disk_free / disk_total * 100}% loaded')
    print(f'R/W load:\t\t {disk_r / 1024} KB R / {disk_w / 1024} KB W')
    print('\n')

    cprint("☰ NETWORK                                                                                   ",
           "white", "on_magenta", attrs=["bold", "underline"])
    print(f'R/W load:\t\t {net_r / 1024} KB Received / {net_w / 1024} KB Sent')
    print('\n')

    cprint("☰ SENSORS                                                                                   ",
           "white", "on_red", attrs=["bold", "underline"])
    print(f'Temperatures:\t\t {temperatures}')
    print(f'Fans:\t\t\t {fans}')
    print('\n')

    cprint("☰ PROCESSES                                                                                 ",
           "black", "on_white", attrs=["bold", "underline"])
    print(f'Running processes:\t {process_info} processes')
    print(f'Process list:\t\t {process_list}')
    print('\n')


if __name__ == '__main__':
    while True:
        fetch_data()
        os.system('cls' if os.name == 'nt' else 'clear')
        print_data()