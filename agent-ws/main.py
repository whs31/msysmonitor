import os
import time
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


def fetch_data():
    global battery_percent
    global battery_charging
    global os_boot_time
    global cpu_load_avg
    global cpu_load_per_core

    battery_percent = psutil.sensors_battery().percent
    battery_charging = psutil.sensors_battery().power_plugged

    os_boot_time = psutil.boot_time()

    cpu_load_avg = psutil.cpu_percent(interval=0.5, percpu=False)
    cpu_load_per_core = psutil.cpu_percent(interval=0.5, percpu=True)


def print_data():
    cprint("🖳 SYSTEM INFO                                                      ", "black", "on_light_grey", attrs=["bold", "underline"])
    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(os_boot_time)
    print(f'OS:\t\t {os_name}')
    print(f'Architecture:\t {os_machine}')
    print(f'Hostname:\t {os_hostname}')
    print(f'Boot time:\t {datetime.datetime.fromtimestamp(os_boot_time)}')
    print(f'Uptime:\t\t {uptime}')
    print('\n')

    cprint("🗠 SYSTEM STATUS                                                    ", "white", "on_dark_grey", attrs=["bold", "underline"])
    charge_status = 'charging' if battery_charging else 'discharging'
    print(f'🗲 Battery:\t {battery_percent}%, {charge_status}')
    print('\n')

    cprint("☰ CPU                                                              ", "white", "on_blue", attrs=["bold", "underline"])
    print(f'Model:\t\t {cpu_model}')
    print(f'Architecture:\t {cpu_arch}')
    print(f'Frequency:\t {cpu_freq}')
    print(f'Cores:\t\t {cpu_count}')
    print('\n')
    print(f'Average load:\t {cpu_load_avg}%')
    print(f'Load per core:\t {cpu_load_per_core}')
    print('\n')


if __name__ == '__main__':
    while True:
        fetch_data()
        os.system('cls' if os.name == 'nt' else 'clear')
        print_data()

        #time.sleep(1)

