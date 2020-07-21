#To Do List:
# Make SQL database and store info there
# Combine this with netdata script
# Allow ability to chose which script to use
# Make telnet script automatic with a manual feture also allowed
import os
directory = os.getcwd()
import telnetlib
import time
import re
import colorama
import sqlite3
from sqlite3 import *
from datetime import datetime
import tkinter
from tkinter import *
host = 'play.totalfreedom.me'
port = 'REDACTED'
database = directory + r"/preformance_checker.db"
# Main server is 20215, Beta is 8765
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
Firstrun = False
#main stuff
def get_data():
    print(f'{GREEN}Attempting to log telnet data to database...')
    t = telnetlib.Telnet(host,port)
    time.sleep(3)
    i = 0
    outputlist = ['']
    t.write(b'gc\n')
    print(CYAN)
    while i is not 3:
        if i is 2:
            t.close()
            i = 3
            outputlist.insert(1, outputlist[1] + ':END STRING')
            continue
        output = t.read_very_eager().decode()
        if output is not '':
            outputlist.insert(1,output)
            #print(output)
            time.sleep(1)
            i = i + 1

    strings = re.split(":", outputlist[1])

    #string decoder
    i = 0
    string_list_length = len(strings)
    print(GREEN)
    while i is not string_list_length:
        item = strings[i]
        #print(strings[i])
        if 'Uptime' in item:
            Uptime = strings[i+1]
            print(f'{MAGENTA}Uptime:' + Uptime)
        try:
            if 'Current TPS' in strings[i]:
                re.compile('\d.')
                TPS = re.findall('[0-9][0-9].[0-9][0-9]\r\n', strings[i])
                print(f'{MAGENTA}TPS: ' + TPS[0])
        except IndexError:
            #print(f'{RED}There was an error while logging the TPS\n')
            re.compile('\d.')
            TPS = re.findall('[0-9][0-9]\r\n', strings[i])
            print(f'{MAGENTA}TPS: ' + TPS[0])
        if 'Maximum memory' in item:
            max_mem = strings[i+1]
            print(f'{MAGENTA}Maximum memory:' + max_mem)
        if 'Allocated memory' in item:
            allocated_mem = strings[i+1]
            print(f'{MAGENTA}Allocated memory:' + allocated_mem)
        if 'Free memory' in item:
            free_mem = strings[i+1]
            print(f'{MAGENTA}Free memory:' + free_mem)
        #worlds
        if 'World "world"' in item:
            overworld = strings[i+1]
            print(f'{RED}World stats:\n\nOverworld:' + overworld)
        if 'Nether "world_nether"' in item:
            nether = strings[i+1]
            print(f'{RED}Nether:' + nether)
        if 'The End "world_the_end"' in item:
            end = strings[i+1]
            print(f'{RED}Nether:' + end)
        if 'World "flatlands"' in item:
            flatlands = strings[i+1]
            print(f'{RED}Flatlands:' + flatlands)
        if 'World "adminworld"' in item:
            adminworld = strings[i+1]
            print(f'{RED}Admin world:' + adminworld)
        if 'World "masterbuilderworld"' in item:
            mbworld = strings[i+1]
            print(f'{RED}Master builder world:' + mbworld)
        if 'World "hubworld"' in item:
            hub = strings[i+1]
            print(f'{RED}Hub world:' + hub)
        if 'World "plotworld"' in item:
            plots = strings[i+1]
            print(f'{RED}Plot world:' + plots)
        #time.sleep(0.5)
        i = i+1
    today = datetime.now()
    current_date = today.strftime("%A, %B %d, %Y at %I:%M:%S %p")
    #print(Firstrun)
    if Firstrun is True:
        if checkauto.get() is True:
            automaticly = 'Automatic Check'
        if checkauto.get() is False:
            automaticly = 'Manual Check'
        autotimer = 0
        conn = create_connection(database)
        today = datetime.now()
        current_date = today.strftime("%A, %B %d, %Y at %I:%M:%S %p")
        if checkauto.get() is True:
            automaticly = 'Automatic Check'
        else:
            automaticly = 'Manual Check'
        with conn:
            # create a new project
            data = (current_date,automaticly,TPS[0],Uptime,max_mem,allocated_mem,free_mem,overworld,nether,end,flatlands,adminworld,mbworld,hub,plots);
            add_data(conn, data)
        print(f'{GREEN}Successfully logged')
        update_auto()
get_data()

#SQL
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
def main():
    sql_create_telnet_stats_table = """CREATE TABLE IF NOT EXISTS telnet_stats (
                                timestamp text,
                                automatic text,
                                tps_stat text,
                                uptime_stat text,
                                maximum_memory text,
                                allocated_memory text,
                                free_memory text,
                                overworld_stats text,
                                nether_stats text,
                                end_stats text,
                                flatlands_stats text,
                                adminworld_stats text,
                                mbworld_stats text,
                                hub_stats text,
                                plotworld_stats text
                            );"""
    # create a database connection
    conn = create_connection(database)
    # create table
    if conn is not None:
        create_table(conn, sql_create_telnet_stats_table)
    else:
        print("Error! cannot create the database connection.")
if __name__ == '__main__':
    main()
#importing strings into database
def add_data(conn, data):
    """
    Create a new project into the projects table
    :param conn:
    :param data:
    :return:
    """
    sql = ''' INSERT INTO telnet_stats(timestamp, automatic, tps_stat, uptime_stat, maximum_memory, allocated_memory, free_memory, overworld_stats, nether_stats, end_stats, flatlands_stats, adminworld_stats, mbworld_stats, hub_stats, plotworld_stats)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()
    return cur.lastrowid
def update_auto():
    autotimer = 0
    while checkauto.get() is True:
        if autotimer <= 300:
            time.sleep(1)
            autotimer = autotimer + 1
        if autotimer is 300 or autotimer > 300:
            print('trying to log data')
            get_data()

Firstrun = True

master = Tk()
Button(master, text='Run Manual Check', command=get_data).pack()
checkauto = BooleanVar()
c1 = Checkbutton(master, text = 'Enable Automatic Checks', variable = checkauto, command=update_auto)
c1.pack()
mainloop()
