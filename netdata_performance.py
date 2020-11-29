
import asyncio
import aiohttp
import json
from netdata import *
import netdata
import colorama
import os
import sqlite3
from sqlite3 import *
import tkinter
from tkinter import *
from datetime import datetime
import time
import nest_asyncio
import os.path
nest_asyncio.apply()

host = 'play.totalfreedom.me'
port = '19999'

colorama.init()
BLACK = colorama.Fore.BLACK
RED = colorama.Fore.RED
GREEN = colorama.Fore.GREEN
YELLOW = colorama.Fore.YELLOW
BLUE = colorama.Fore.BLUE
MAGENTA = colorama.Fore.MAGENTA
CYAN = colorama.Fore.CYAN
WHITE = colorama.Fore.WHITE
RESET = colorama.Fore.RESET
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
database = os.path.join(BASE_DIR, "preformance_checker.db")

Firstrun = False
async def main():
    """Get the data from a Netdata instance."""
    async with aiohttp.ClientSession() as session:
        data = Netdata(host, loop, session,port)
        # Get data for the CPU
        await data.get_data("system.cpu")
        print(CYAN)
        #iowait, softirq, user, and system
        softirq = round(data.values['softirq'],2)
        print('Softirq:')
        print(softirq)
        iowait = round(data.values['iowait'],2)
        print('Iowait:')
        print(iowait)
        user = round(data.values['user'],2)
        print('User:')
        print(user)
        system = round(data.values['system'],2)
        print('System:')
        print(system)
        #Overall percentage
        print(YELLOW)
        cpu_percent = round(system + user + iowait + softirq,2)
        print('CPU Usage (%):')
        print(cpu_percent)

        #Ram Stuff
        await data.get_data('system.ram')
        print(RED)
        free_ram = round(data.values['free'] / 1000, 2)
        print('Free Ram (GB):')
        print(free_ram)
        used_ram = round(data.values['used'] / 1000, 2)
        print('Used Ram (GB):')
        print(used_ram)
        total_ram = round(used_ram + free_ram + (data.values['cached'] / 1000) + (data.values['buffers'] / 1000), 2)
        print(MAGENTA)
        print('Total Ram (GB):')
        print(total_ram)

        await data.get_data('system.swap')
        print(GREEN)
        free_swap = round(data.values['free'] / 1000, 2)
        print('Free Swap Memory (GB):')
        print(free_swap)
        used_swap = round(data.values['used'] / 1000, 2)
        print('Used Swap Memory (GB):')
        print(used_swap)
        total_swap = round(used_swap + free_swap, 2)
        print(WHITE)
        print('Total Swap Memory (GB):')
        print(total_swap)

        # "Java" cpu/ram usage
        await data.get_data('apps.cpu')
        print(YELLOW)
        java_cpu = round(data.values['java'] / 8, 2)
        print('"Java" Cpu Usage (%):')
        print(java_cpu)
        await data.get_data('apps.mem')
        java_ram = round(data.values['java'] / 1000, 2)
        print('"Java" Ram Usage (GB):')
        print(java_ram)

        #Disk Usage
        await data.get_data('disk.md3')
        print(f'{RED}DISK READ/WRITES MAY BE SLIGHTLY OFF')
        print(BLUE)
        reads = round(data.values['reads'] / 800.389, 2)
        print('Reads per Operation (MiB):')
        print(reads)
        writes = round(data.values['writes'] / 800.389,2)
        print('Writes per Operation (MiB):')
        print(writes)

        #Core Temps
        await data.get_data('sensors.coretemp_isa_0000_temperature')
        print(MAGENTA)
        core0_temp = data.values['Core 0']
        print('Core 0 Temperature (Celcius):')
        print(core0_temp)
        core1_temp = data.values['Core 1']
        print('Core 1 Temperature (Celcius):')
        print(core1_temp)
        core2_temp = data.values['Core 2']
        print('Core 2 Temperature (Celcius):')
        print(core2_temp)
        core3_temp = data.values['Core 3']
        print('Core 3 Temperature (Celcius):')
        print(core3_temp)
    if Firstrun is True:
        conn = create_connection(database)
        today = datetime.now()
        current_date = today.strftime("%A, %B %d, %Y at %I:%M:%S %p")
        if checkauto.get() is True:
            automaticly = 'Automatic Check'
        else:
            automaticly = 'Manual Check'
        with conn:
            # create a new project
            #timestamp, automatic, cpu_percentage, softirq_stat, iowait_stat, user_stat, system_stat, ram_free, ram_used, ram_total, swap_free, swap_used, swap_total, cpu_java, ram_java, disk_reads, disk_writes, temp_core0, temp_core1, temp_core2, temp_core3
            data_stats = (current_date,automaticly,cpu_percent, softirq, iowait, user, system, free_ram, used_ram, total_ram, free_swap, used_swap, total_swap, java_cpu, java_ram, reads, writes, core0_temp, core1_temp, core2_temp, core3_temp);
            add_data(conn, data_stats)
        print(f'{GREEN}Successfully logged')
        autotimer = 0
        update_auto()
    else:
        print(f'{GREEN}Netdata Checker has been initalized')

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

#SQL Shit
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
def startup():
    sql_create_netdata_stats_table = """CREATE TABLE IF NOT EXISTS netdata_stats (
                                timestamp text,
                                automatic text,
                                cpu_percentage text,
                                softirq_stat text,
                                iowait_stat text,
                                user_stat text,
                                system_stat text,
                                ram_free text,
                                ram_used text,
                                ram_total text,
                                swap_free text,
                                swap_used text,
                                swap_total text,
                                cpu_java text,
                                ram_java text,
                                disk_reads text,
                                disk_writes text,
                                temp_core0 text,
                                temp_core1 text,
                                temp_core2 text,
                                temp_core3 text
                            );"""
    # create a database connection
    conn = create_connection(database)
    # create table
    if conn is not None:
        create_table(conn, sql_create_netdata_stats_table)
    else:
        print("Error! cannot create the database connection.")
if __name__ == '__main__':
    startup()

#importing strings into database
def add_data(conn, data):
    """
    Create a new project into the projects table
    :param conn:
    :param data:
    :return:
    """
    sql = ''' INSERT INTO netdata_stats(timestamp, automatic, cpu_percentage, softirq_stat, iowait_stat, user_stat, system_stat, ram_free, ram_used, ram_total, swap_free, swap_used, swap_total, cpu_java, ram_java, disk_reads, disk_writes, temp_core0, temp_core1, temp_core2, temp_core3)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()
    return cur.lastrowid


def update_auto():
    autotimer = 0
    while checkauto.get() is True:
        if autotimer <= 3600:
            time.sleep(1)
            autotimer = autotimer + 1
            print(autotimer)
        if autotimer is 3600 or autotimer > 3600:
            print(f'{WHITE}Attempting to automaticly log netdata information')
            get_data()
    
    
def get_data():
    loop.run_until_complete(main())
Firstrun = True


master = Tk()
Button(master, text='Run Manual Check', command=get_data).pack()
checkauto = BooleanVar()
c1 = Checkbutton(master, text = 'Enable Automatic Checks', variable = checkauto, command=update_auto)
c1.pack()
mainloop()
