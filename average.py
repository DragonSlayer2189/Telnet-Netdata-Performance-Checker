import os
import os.path
directory = os.getcwd()
import time
from datetime import datetime
import re
import colorama
import sqlite3
from sqlite3 import *
import tkinter
from tkinter import *
from datetime import timedelta
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
data1 = []
data2 = []
data3 = []
data4 = []
data5 = []
data6 = []
data7 = []
data8 = []
data9 = []
data10 = []
data11 = []
data12 = []
data13 = []

#print('Running\n')
#connect to sql db
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

def select_all_telnet_data(conn):
    """
    Query all rows in the telnet_stats table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM TELNET_STATS")

    rows = cur.fetchall()

    for row in rows:
        #nan- timestamp, nan- automatic, 1- tps, 2-uptime, 3-max_mem, 4-allo_mem, 5-free_mem
        #6- overworld, 7- nether, 8- end, 9- flatlands, 10- adminworld, 11- mbworld, 12- hub, 13- plotworld 
        data1.insert(0, row[2])
        #uptime is hard
        data2.insert(1, row[3])
        data3.insert(0, row[4])
        data4.insert(0, row[5])
        data5.insert(0, row[6])
        data6.insert(0, row[7])
        data7.insert(0, row[8])
        data8.insert(0, row[9])
        data9.insert(0, row[10])
        data10.insert(0, row[11])
        data11.insert(0, row[12])
        data12.insert(0, row[13])
        data13.insert(0, row[14])

conn = create_connection(database)
with conn:
    select_all_telnet_data(conn)
       
#data1 - tps
tps = []
for item in data1:
    tps.insert(0, float(item))
print(f'{MAGENTA}Average TPS:')
avg_tps = sum(tps) / len(tps)
print(round(avg_tps,2))

#data2 - uptime
#Example String :  1 hour 6 minutes 11 seconds
re.compile('\d.')
stats2 = []
for item in data2:
    stats = re.split('u', item)
    stats2.extend(stats)

hours = []
minutes = []
seconds = []

for item in stats2:
    if 'ho' in item:
        HOUR = re.findall('[0-9][0-9]', item)
        for item in HOUR:
            hours.insert(0, int(item))
    if 'ho' in item:
        HOUR = re.findall('[0-9]', item)
        for item in HOUR:
            hours.insert(0, int(item))
    if 'min' in item:
        MIN = re.findall('[0-9][0-9]', item)
        for item in MIN:
            minutes.insert(0, int(item))
    if 'min' in item:
        MIN = re.findall('[0-9]', item)
        for item in MIN:
            minutes.insert(0, int(item))
    if 'sec' in item:
        SEC = re.findall('[0-9][0-9]', item)
        for item in SEC:
            seconds.insert(0, int(item))
    if 'sec' in item:
        SEC = re.findall('[0-9]', item)
        for item in SEC:
            seconds.insert(0, int(item))
uptime = []
i = 0
string_list_length = len(seconds)
while i is not string_list_length:
    try:
        str_time = str(hours[i]) + ":" + str(minutes[i]) + ":" + str(seconds[i])
        uptime.insert(0, str_time)
    except IndexError:
        try:
            str_time = "0" + ":" + str(minutes[i]) + ":" + str(seconds[i])
            uptime.insert(0, str_time)
        except IndexError:
            str_time= "0" + ":" + "0" + ":" + str(seconds)
            uptime.insert(0, str_time)

    i = i+1
average_time_formated = str(timedelta(seconds=sum(map(lambda f: int(f[0])*3600 + int(f[1])*60 + int(f[2]), map(lambda f: f.split(':'), uptime)))/len(uptime)))
avg_hours, avg_minutes, avg_seconds = re.split(":", average_time_formated)
#print (average_time_formated)
print(f'{WHITE}Average Uptime:')
print(avg_hours, "Hours",avg_minutes,"Minutes",round(float(avg_seconds),2),"Seconds")
avg_uptime = avg_hours + " Hours " + avg_minutes + " Minutes " + avg_seconds + " Seconds "

#data3 - max_mem
max_mem = []
for item in data3:
    re.compile('\d.')
    MAX = re.findall('[0-9][0-9][0-9][0-9]', item.replace(",",""))
    for item in MAX:
        max_mem.insert(0, int(item))
print(f'{RED}Average Maximum Memory:')
avg_max_mem = sum(max_mem) / len(max_mem)
print(round(avg_max_mem,2),"MBs")

#data4 - allo_mem
allo_mem = []
for item in data4:
    re.compile('\d.')
    ALLO = re.findall('[0-9][0-9][0-9][0-9]', item.replace(",",""))
    for item in ALLO:
        allo_mem.insert(0, int(item))
print(f'{GREEN}Average Allocated Memory:')
avg_allo_mem = sum(allo_mem) / len(allo_mem)
print(round(avg_allo_mem,2),"MBs")

#data5 - free_mem
free_mem = []
for item in data5:
    re.compile('\d.')
    FREE = re.findall('[0-9][0-9][0-9][0-9]', item.replace(",",""))
    for item in FREE:
        free_mem.insert(0, int(item))
print(f'{YELLOW}Average Free Memory:')
avg_free_mem = sum(free_mem) / len(free_mem)
print(round(avg_free_mem,2),"MBs")

#data6 - overworld
#Example String :  339 chunks, 0 entities, 329 tiles.
stats2 = []
for item in data6:
    stats = re.split(', ', item)
    stats2.extend(stats)
#print(stats2)
chunks = []
entities = []
tiles = []

#chunks
for item in stats2:
    if 'chunks' in item:
        CHUNK = re.findall('[0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in CHUNK:
            chunks.insert(0, int(item))
    if 'chunks' in item:
        CHUNK = re.findall('[0-9][0-9][0-9]', item.replace(",",""))
        for item in CHUNK:
            chunks.insert(0,int(item))
    if 'chunks' in item:
        CHUNK = re.findall('[0-9][0-9]', item.replace(",",""))
        for item in CHUNK:
            chunks.insert(0,int(item))
    if 'chunks' in item:
        CHUNK = re.findall('[0-9]', item.replace(",",""))
        for item in CHUNK:
            chunks.insert(0,int(item))

#entities
for item in stats2:
    if 'entities' in item:
        ENT = re.findall('[0-9][0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0, int(item))
    if 'entities' in item:
        ENT = re.findall('[0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0, int(item))
    if 'entities' in item:
        ENT = re.findall('[0-9][0-9][0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0,int(item))
    if 'entities' in item:
        ENT = re.findall('[0-9][0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0,int(item))
    if 'entities' in item:
        ENT = re.findall('[0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0,int(item))

#tiles
for item in stats2:
    if 'tiles' in item:
        TILE = re.findall('[0-9][0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0, int(item))
    if 'tiles' in item:
        TILE = re.findall('[0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0, int(item))
    if 'tiles' in item:
        TILE = re.findall('[0-9][0-9][0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0,int(item))
    if 'tiles' in item:
        TILE = re.findall('[0-9][0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0,int(item))
    if 'tiles' in item:
        TILE = re.findall('[0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0,int(item))

#averages
print(f'{BLUE}Overworld Averages:')
avg_chunks_overworld = sum(chunks) / len(chunks)
avg_entities_overworld = sum(entities) / len(entities)
avg_tiles_overworld = sum(tiles) / len(tiles)
print(round(avg_chunks_overworld,2),"Chunks")
print(round(avg_entities_overworld,2),"Entities")
print(round(avg_tiles_overworld,2),"Tiles")

#data7 - nether
stats2 = []
for item in data7:
    stats = re.split(', ', item)
    stats2.extend(stats)
#print(stats2)
chunks = []
entities = []
tiles = []

#chunks
for item in stats2:
    if 'chunks' in item:
        CHUNK = re.findall('[0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in CHUNK:
            chunks.insert(0, int(item))
    if 'chunks' in item:
        CHUNK = re.findall('[0-9][0-9][0-9]', item.replace(",",""))
        for item in CHUNK:
            chunks.insert(0,int(item))
    if 'chunks' in item:
        CHUNK = re.findall('[0-9][0-9]', item.replace(",",""))
        for item in CHUNK:
            chunks.insert(0,int(item))
    if 'chunks' in item:
        CHUNK = re.findall('[0-9]', item.replace(",",""))
        for item in CHUNK:
            chunks.insert(0,int(item))

#entities
for item in stats2:
    if 'entities' in item:
        ENT = re.findall('[0-9][0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0, int(item))
    if 'entities' in item:
        ENT = re.findall('[0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0, int(item))
    if 'entities' in item:
        ENT = re.findall('[0-9][0-9][0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0,int(item))
    if 'entities' in item:
        ENT = re.findall('[0-9][0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0,int(item))
    if 'entities' in item:
        ENT = re.findall('[0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0,int(item))

#tiles
for item in stats2:
    if 'tiles' in item:
        TILE = re.findall('[0-9][0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0, int(item))
    if 'tiles' in item:
        TILE = re.findall('[0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0, int(item))
    if 'tiles' in item:
        TILE = re.findall('[0-9][0-9][0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0,int(item))
    if 'tiles' in item:
        TILE = re.findall('[0-9][0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0,int(item))
    if 'tiles' in item:
        TILE = re.findall('[0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0,int(item))

#averages
print(f'{CYAN}Nether Averages:')
avg_chunks_nether = sum(chunks) / len(chunks)
avg_entities_nether = sum(entities) / len(entities)
avg_tiles_nether = sum(tiles) / len(tiles)
print(round(avg_chunks_nether,2),"Chunks")
print(round(avg_entities_nether,2),"Entities")
print(round(avg_tiles_nether,2),"Tiles")

#data8 - End
stats2 = []
for item in data8:
    stats = re.split(', ', item)
    stats2.extend(stats)
#print(stats2)
chunks = []
entities = []
tiles = []

#chunks
for item in stats2:
    if 'chunks' in item:
        CHUNK = re.findall('[0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in CHUNK:
            chunks.insert(0, int(item))
    if 'chunks' in item:
        CHUNK = re.findall('[0-9][0-9][0-9]', item.replace(",",""))
        for item in CHUNK:
            chunks.insert(0,int(item))
    if 'chunks' in item:
        CHUNK = re.findall('[0-9][0-9]', item.replace(",",""))
        for item in CHUNK:
            chunks.insert(0,int(item))
    if 'chunks' in item:
        CHUNK = re.findall('[0-9]', item.replace(",",""))
        for item in CHUNK:
            chunks.insert(0,int(item))

#entities
for item in stats2:
    if 'entities' in item:
        ENT = re.findall('[0-9][0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0, int(item))
    if 'entities' in item:
        ENT = re.findall('[0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0, int(item))
    if 'entities' in item:
        ENT = re.findall('[0-9][0-9][0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0,int(item))
    if 'entities' in item:
        ENT = re.findall('[0-9][0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0,int(item))
    if 'entities' in item:
        ENT = re.findall('[0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0,int(item))

#tiles
for item in stats2:
    if 'tiles' in item:
        TILE = re.findall('[0-9][0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0, int(item))
    if 'tiles' in item:
        TILE = re.findall('[0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0, int(item))
    if 'tiles' in item:
        TILE = re.findall('[0-9][0-9][0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0,int(item))
    if 'tiles' in item:
        TILE = re.findall('[0-9][0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0,int(item))
    if 'tiles' in item:
        TILE = re.findall('[0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0,int(item))

#averages
print(f'{BLUE}End Averages:')
avg_chunks_end = sum(chunks) / len(chunks)
avg_entities_end = sum(entities) / len(entities)
avg_tiles_end = sum(tiles) / len(tiles)
print(round(avg_chunks_end,2),"Chunks")
print(round(avg_entities_end,2),"Entities")
print(round(avg_tiles_end,2),"Tiles")

#data9 - Flatlands
stats2 = []
for item in data9:
    stats = re.split(', ', item)
    stats2.extend(stats)
#print(stats2)
chunks = []
entities = []
tiles = []

#chunks
for item in stats2:
    if 'chunks' in item:
        CHUNK = re.findall('[0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in CHUNK:
            chunks.insert(0, int(item))
    if 'chunks' in item:
        CHUNK = re.findall('[0-9][0-9][0-9]', item.replace(",",""))
        for item in CHUNK:
            chunks.insert(0,int(item))
    if 'chunks' in item:
        CHUNK = re.findall('[0-9][0-9]', item.replace(",",""))
        for item in CHUNK:
            chunks.insert(0,int(item))
    if 'chunks' in item:
        CHUNK = re.findall('[0-9]', item.replace(",",""))
        for item in CHUNK:
            chunks.insert(0,int(item))

#entities
for item in stats2:
    if 'entities' in item:
        ENT = re.findall('[0-9][0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0, int(item))
    if 'entities' in item:
        ENT = re.findall('[0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0, int(item))
    if 'entities' in item:
        ENT = re.findall('[0-9][0-9][0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0,int(item))
    if 'entities' in item:
        ENT = re.findall('[0-9][0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0,int(item))
    if 'entities' in item:
        ENT = re.findall('[0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0,int(item))

#tiles
for item in stats2:
    if 'tiles' in item:
        TILE = re.findall('[0-9][0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0, int(item))
    if 'tiles' in item:
        TILE = re.findall('[0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0, int(item))
    if 'tiles' in item:
        TILE = re.findall('[0-9][0-9][0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0,int(item))
    if 'tiles' in item:
        TILE = re.findall('[0-9][0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0,int(item))
    if 'tiles' in item:
        TILE = re.findall('[0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0,int(item))

#averages
print(f'{CYAN}Flatlands Averages:')
avg_chunks_flatlands = sum(chunks) / len(chunks)
avg_entities_flatlands = sum(entities) / len(entities)
avg_tiles_flatlands = sum(tiles) / len(tiles)
print(round(avg_chunks_flatlands,2),"Chunks")
print(round(avg_entities_flatlands,2),"Entities")
print(round(avg_tiles_flatlands,2),"Tiles")

#data10 - Adminworld
stats2 = []
for item in data10:
    stats = re.split(', ', item)
    stats2.extend(stats)
#print(stats2)
chunks = []
entities = []
tiles = []

#chunks
for item in stats2:
    if 'chunks' in item:
        CHUNK = re.findall('[0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in CHUNK:
            chunks.insert(0, int(item))
    if 'chunks' in item:
        CHUNK = re.findall('[0-9][0-9][0-9]', item.replace(",",""))
        for item in CHUNK:
            chunks.insert(0,int(item))
    if 'chunks' in item:
        CHUNK = re.findall('[0-9][0-9]', item.replace(",",""))
        for item in CHUNK:
            chunks.insert(0,int(item))
    if 'chunks' in item:
        CHUNK = re.findall('[0-9]', item.replace(",",""))
        for item in CHUNK:
            chunks.insert(0,int(item))

#entities
for item in stats2:
    if 'entities' in item:
        ENT = re.findall('[0-9][0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0, int(item))
    if 'entities' in item:
        ENT = re.findall('[0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0, int(item))
    if 'entities' in item:
        ENT = re.findall('[0-9][0-9][0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0,int(item))
    if 'entities' in item:
        ENT = re.findall('[0-9][0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0,int(item))
    if 'entities' in item:
        ENT = re.findall('[0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0,int(item))

#tiles
for item in stats2:
    if 'tiles' in item:
        TILE = re.findall('[0-9][0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0, int(item))
    if 'tiles' in item:
        TILE = re.findall('[0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0, int(item))
    if 'tiles' in item:
        TILE = re.findall('[0-9][0-9][0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0,int(item))
    if 'tiles' in item:
        TILE = re.findall('[0-9][0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0,int(item))
    if 'tiles' in item:
        TILE = re.findall('[0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0,int(item))

#averages
print(f'{BLUE}Adminworld/Staffworld Averages:')
avg_chunks_adminworld = sum(chunks) / len(chunks)
avg_entities_adminworld = sum(entities) / len(entities)
avg_tiles_adminworld = sum(tiles) / len(tiles)
print(round(avg_chunks_adminworld,2),"Chunks")
print(round(avg_entities_adminworld,2),"Entities")
print(round(avg_tiles_adminworld,2),"Tiles")

#data11 - mbworld
stats2 = []
for item in data11:
    stats = re.split(', ', item)
    stats2.extend(stats)
#print(stats2)
chunks = []
entities = []
tiles = []

#chunks
for item in stats2:
    if 'chunks' in item:
        CHUNK = re.findall('[0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in CHUNK:
            chunks.insert(0, int(item))
    if 'chunks' in item:
        CHUNK = re.findall('[0-9][0-9][0-9]', item.replace(",",""))
        for item in CHUNK:
            chunks.insert(0,int(item))
    if 'chunks' in item:
        CHUNK = re.findall('[0-9][0-9]', item.replace(",",""))
        for item in CHUNK:
            chunks.insert(0,int(item))
    if 'chunks' in item:
        CHUNK = re.findall('[0-9]', item.replace(",",""))
        for item in CHUNK:
            chunks.insert(0,int(item))

#entities
for item in stats2:
    if 'entities' in item:
        ENT = re.findall('[0-9][0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0, int(item))
    if 'entities' in item:
        ENT = re.findall('[0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0, int(item))
    if 'entities' in item:
        ENT = re.findall('[0-9][0-9][0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0,int(item))
    if 'entities' in item:
        ENT = re.findall('[0-9][0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0,int(item))
    if 'entities' in item:
        ENT = re.findall('[0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0,int(item))

#tiles
for item in stats2:
    if 'tiles' in item:
        TILE = re.findall('[0-9][0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0, int(item))
    if 'tiles' in item:
        TILE = re.findall('[0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0, int(item))
    if 'tiles' in item:
        TILE = re.findall('[0-9][0-9][0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0,int(item))
    if 'tiles' in item:
        TILE = re.findall('[0-9][0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0,int(item))
    if 'tiles' in item:
        TILE = re.findall('[0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0,int(item))

#averages
print(f'{CYAN}Master Builder World Averages:')
avg_chunks_mbworld = sum(chunks) / len(chunks)
avg_entities_mbworld = sum(entities) / len(entities)
avg_tiles_mbworld = sum(tiles) / len(tiles)
print(round(avg_chunks_mbworld,2),"Chunks")
print(round(avg_entities_mbworld,2),"Entities")
print(round(avg_tiles_mbworld,2),"Tiles")

#data12 - hub
stats2 = []
for item in data12:
    stats = re.split(', ', item)
    stats2.extend(stats)
#print(stats2)
chunks = []
entities = []
tiles = []

#chunks
for item in stats2:
    if 'chunks' in item:
        CHUNK = re.findall('[0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in CHUNK:
            chunks.insert(0, int(item))
    if 'chunks' in item:
        CHUNK = re.findall('[0-9][0-9][0-9]', item.replace(",",""))
        for item in CHUNK:
            chunks.insert(0,int(item))
    if 'chunks' in item:
        CHUNK = re.findall('[0-9][0-9]', item.replace(",",""))
        for item in CHUNK:
            chunks.insert(0,int(item))
    if 'chunks' in item:
        CHUNK = re.findall('[0-9]', item.replace(",",""))
        for item in CHUNK:
            chunks.insert(0,int(item))

#entities
for item in stats2:
    if 'entities' in item:
        ENT = re.findall('[0-9][0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0, int(item))
    if 'entities' in item:
        ENT = re.findall('[0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0, int(item))
    if 'entities' in item:
        ENT = re.findall('[0-9][0-9][0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0,int(item))
    if 'entities' in item:
        ENT = re.findall('[0-9][0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0,int(item))
    if 'entities' in item:
        ENT = re.findall('[0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0,int(item))

#tiles
for item in stats2:
    if 'tiles' in item:
        TILE = re.findall('[0-9][0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0, int(item))
    if 'tiles' in item:
        TILE = re.findall('[0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0, int(item))
    if 'tiles' in item:
        TILE = re.findall('[0-9][0-9][0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0,int(item))
    if 'tiles' in item:
        TILE = re.findall('[0-9][0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0,int(item))
    if 'tiles' in item:
        TILE = re.findall('[0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0,int(item))

#averages
print(f'{BLUE}Hub World Averages:')
avg_chunks_hub = sum(chunks) / len(chunks)
avg_entities_hub = sum(entities) / len(entities)
avg_tiles_hub = sum(tiles) / len(tiles)
print(round(avg_chunks_hub,2),"Chunks")
print(round(avg_entities_hub,2),"Entities")
print(round(avg_tiles_hub,2),"Tiles")

#data13 - plotworld
stats2 = []
for item in data13:
    stats = re.split(', ', item)
    stats2.extend(stats)
#print(stats2)
chunks = []
entities = []
tiles = []

#chunks
for item in stats2:
    if 'chunks' in item:
        CHUNK = re.findall('[0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in CHUNK:
            chunks.insert(0, int(item))
    if 'chunks' in item:
        CHUNK = re.findall('[0-9][0-9][0-9]', item.replace(",",""))
        for item in CHUNK:
            chunks.insert(0,int(item))
    if 'chunks' in item:
        CHUNK = re.findall('[0-9][0-9]', item.replace(",",""))
        for item in CHUNK:
            chunks.insert(0,int(item))
    if 'chunks' in item:
        CHUNK = re.findall('[0-9]', item.replace(",",""))
        for item in CHUNK:
            chunks.insert(0,int(item))

#entities
for item in stats2:
    if 'entities' in item:
        ENT = re.findall('[0-9][0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0, int(item))
    if 'entities' in item:
        ENT = re.findall('[0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0, int(item))
    if 'entities' in item:
        ENT = re.findall('[0-9][0-9][0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0,int(item))
    if 'entities' in item:
        ENT = re.findall('[0-9][0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0,int(item))
    if 'entities' in item:
        ENT = re.findall('[0-9]', item.replace(",",""))
        for item in ENT:
            entities.insert(0,int(item))

#tiles
for item in stats2:
    if 'tiles' in item:
        TILE = re.findall('[0-9][0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0, int(item))
    if 'tiles' in item:
        TILE = re.findall('[0-9][0-9][0-9][0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0, int(item))
    if 'tiles' in item:
        TILE = re.findall('[0-9][0-9][0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0,int(item))
    if 'tiles' in item:
        TILE = re.findall('[0-9][0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0,int(item))
    if 'tiles' in item:
        TILE = re.findall('[0-9]', item.replace(",",""))
        for item in TILE:
            tiles.insert(0,int(item))

#averages
print(f'{CYAN}Plot World Averages:')
avg_chunks_plotworld = sum(chunks) / len(chunks)
avg_entities_plotworld = sum(entities) / len(entities)
avg_tiles_plotworld = sum(tiles) / len(tiles)
print(round(avg_chunks_adminworld,2),"Chunks")
print(round(avg_entities_adminworld,2),"Entities")
print(round(avg_tiles_adminworld,2),"Tiles")



#SQL
def main():
    sql_create_avg_stats_table = """CREATE TABLE IF NOT EXISTS avg_stats (
                                avg_tps text,
                                avg_uptime text,
                                avg_max_mem text,
                                avg_allo_mem text,
                                avg_free_mem text,
                                avg_chunks_overworld text,
                                avg_entities_overworld text,
                                avg_tiles_overworld text,
                                avg_chunks_nether text,
                                avg_entities_nether text,
                                avg_tiles_nether text,
                                avg_chunks_end text,
                                avg_entities_end text,
                                avg_tiles_end text,
                                avg_chunks_flatlands text,
                                avg_entities_flatlands text,
                                avg_tiles_flatlands text,
                                avg_chunks_adminworld text,
                                avg_entities_adminworld text,
                                avg_tiles_adminworld text,
                                avg_chunks_mbworld text,
                                avg_entities_mbworld text,
                                avg_tiles_mbworld text,
                                avg_chunks_hub text,
                                avg_entities_hub text,
                                avg_tiles_hub text,
                                avg_chunks_plotworld text,
                                avg_entities_plotworld text,
                                avg_tiles_plotworld text
                            );"""
    # create a database connection
    conn = create_connection(database)
    # create table
    if conn is not None:
        create_table(conn, sql_create_avg_stats_table)
    else:
        print("Error! cannot create the database connection.")
if __name__ == '__main__':
    main()
#29 values
def add_data(conn, data):
    """
    Create a new project into the projects table
    :param conn:
    :param data:
    :return:
    """
    sql = ''' INSERT INTO avg_stats(avg_tps, avg_uptime, avg_max_mem, avg_allo_mem, avg_free_mem, avg_chunks_overworld, avg_entities_overworld, avg_tiles_overworld, avg_chunks_nether, avg_entities_nether, avg_tiles_nether, avg_chunks_end, avg_entities_end, avg_tiles_end, avg_chunks_flatlands, avg_entities_flatlands, avg_tiles_flatlands, avg_chunks_adminworld, avg_entities_adminworld, avg_tiles_adminworld, avg_chunks_mbworld, avg_entities_mbworld, avg_tiles_mbworld, avg_chunks_hub, avg_entities_hub, avg_tiles_hub, avg_chunks_plotworld, avg_entities_plotworld, avg_tiles_plotworld)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()
    return cur.lastrowid


data = (avg_tps, avg_uptime, avg_max_mem, avg_allo_mem, avg_free_mem, avg_chunks_overworld, avg_entities_overworld, avg_tiles_overworld, avg_chunks_nether, avg_entities_nether, avg_tiles_nether, avg_chunks_end, avg_entities_end, avg_tiles_end, avg_chunks_flatlands, avg_entities_flatlands, avg_tiles_flatlands, avg_chunks_adminworld, avg_entities_adminworld, avg_tiles_adminworld, avg_chunks_mbworld, avg_entities_mbworld, avg_tiles_mbworld, avg_chunks_hub, avg_entities_hub, avg_tiles_hub, avg_chunks_plotworld, avg_entities_plotworld, avg_tiles_plotworld);
add_data(conn, data)