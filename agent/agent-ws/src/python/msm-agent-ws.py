import os
import platform
import datetime
import argparse
import sys
import time
import subprocess
import json
import socket
import math
from typing import Final

import psutil
import cpuinfo
from termcolor import colored, cprint


PRINT_INFO: Final[bool] = True
PRINT_PROC: Final[bool] = False
PRINT_JSON: Final[bool] = False


def run(cmd):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, check=True, encoding="utf-8") \
            .stdout \
            .strip()
    except:
        return None


def guid():
    if sys.platform == 'darwin':
        return run(
            "ioreg -d2 -c IOPlatformExpertDevice | awk -F\\\" '/IOPlatformUUID/{print $(NF-1)}'",
        )

    if sys.platform == 'win32' or sys.platform == 'cygwin' or sys.platform == 'msys':
        return run('wmic csproduct get uuid').split('\n')[2] \
            .strip()

    if sys.platform.startswith('linux'):
        return run('cat /var/lib/dbus/machine-id') or \
            run('cat /etc/machine-id')

    if sys.platform.startswith('openbsd') or sys.platform.startswith('freebsd'):
        return run('cat /etc/hostid') or \
            run('kenv -q smbios.system.uuid')


name = 'INVALID_NAME'
ip = ''
port = 0
hwid = guid()

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
    print(f'Temperatures:\t\t')
    for a in temperatures:
        print(f'\t\t\t {a}')
    print(f'Fans:\t\t\t {fans}')
    print('\n')

    cprint("☰ PROCESSES                                                                                 ",
           "black", "on_white", attrs=["bold", "underline"])
    print(f'Running processes:\t {process_info} processes')
    if PRINT_PROC:
        print(f'Process list:\t\t {process_list}')
    print('\n')


def encode():
    dictionary = {
        "head/name": name,
        "head/uuid": hwid,
        "os/name": os_name,
        "os/machine": os_machine,
        "os/hostname": os_hostname,
        "os/boottime": os_boot_time,
        "cpu/model": cpu_model,
        "cpu/arch": cpu_arch,
        "cpu/frequency": cpu_freq,
        "cpu/core-count": cpu_count,
        "cpu/load-avg": cpu_load_avg,
        "cpu/load-per-core": cpu_load_per_core,
        "ram/total": ram_total,
        "ram/free": ram_free,
        "ram/swap-total": ram_swap_total,
        "ram/swap-free": ram_swap_free,
        "disk/mounts": disk_mounts,
        "disk/total": disk_total,
        "disk/free": disk_free,
        "disk/r": disk_r,
        "disk/w": disk_w,
        "net/r": net_r,
        "net/w": net_w,
        "sns/battery": battery_percent,
        "sns/bat-cs": battery_charging,
        "sns/temp": temperatures,
        "sns/fans": fans,
        "proc/ttl": process_info,
        "proc/ls": process_list
    }

    encoded = json.dumps(dictionary)
    if PRINT_JSON:
        print(encoded)
    return encoded


def progress(x):
    if x == 0:
        print('-')
    if x == 1:
        print('/')
    if x == 2:
        print('|')
    if x == 3:
        print('\\')


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='MSM Agent for workstation')
    parser.add_argument('name', type=str, help='Unique name for agent instance')
    parser.add_argument('ip', type=str, help='Target IPv4-address')
    parser.add_argument('port', type=int, help='Target port')
    args = parser.parse_args()
    name = args.name
    ip = args.ip
    port = args.port

    print(f'Agent name: {name}')
    print(f'Target address: {ip}:{port}')
    print(f'Unique HWID: {hwid}')

    time.sleep(1)

    i = 0
    while True:
        fetch_data()
        os.system('cls' if os.name == 'nt' else 'clear')
        if PRINT_INFO:
            print_data()
        e = encode()
        if i < 3:
            i += 1
        else:
            i = 0
        progress(i)

        try:
            s.sendto(e.encode('utf-8'), (ip, port))
            #msgFromServer = s.recvfrom(65535)
            #msg = "Message from Server {}".format(msgFromServer[0])
            #print(msg)
        except ConnectionRefusedError:
            print('Exception:', ConnectionRefusedError)
