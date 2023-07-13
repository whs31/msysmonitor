import psutil
from termcolor import colored, cprint

battery_percent = 0
battery_charging = False


def fetch_data():
    global battery_percent
    global battery_charging

    battery_percent = psutil.sensors_battery().percent
    battery_charging = psutil.sensors_battery().power_plugged


def print_data():
    cprint("SYSTEM STATUS", "black", "on_light_grey", attrs=["bold"])
    charge_status = 'charging' if battery_charging else 'discharging'
    print(f'🗲 Battery: {battery_percent}%, {charge_status}')


if __name__ == '__main__':
    fetch_data()
    print_data()
