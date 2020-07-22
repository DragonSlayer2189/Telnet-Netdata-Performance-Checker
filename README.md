# Telnet-Netdata-Performance-Checker
Made by Eric Bennett, also known as DragonSlayer2189

This code was primarily made for play.totalfreedom.me, but you may use this code, or excerpts of it in any projects you want.

This was made in python 3.7.2 and requires a few libraries, to install said libraries just run the following command

pip install -r requirements.txt

# What does this actually do?
basicly the telnet script allows you to connect to telnet (provided that you are already have access to telnet) and it will run the command /gc, then log the results in the database.

the netdata script reads the data from https://play.totalfreedom.me:19999, grabs some data from there, and puts it into the database.
each script will open a window with a button and a check box, clicking the button will run a manual check, and pressing the checkbox will make the script log automaticly every 5 minutes (may change it to longer idk).


# What data does this log?
The Telnet Script logs the following (for this when i say server i mean the minecraft server):

• Time that the data was checked.
  
• Wether it was logged automaticaly or manualy.

• The TPS of the server.

• The server's uptime.

• The maximum memory of the server's RAM.

• The allocated memory of the server's RAM.

• The amount of RAM not currently being used by the server.

• The statitcs (Entities, Chunks, ect.) of each of the worlds on the server.

The Netdata Script Logs the following (for this when i say the server i mean the physical server):

• The Time that the data was checked.

• Wether it was logged automaticaly or manualy.

• The current CPU usage reprecented as a percentage.

• The specific statics of the CPU also as a percentage (E.G softirq, iowait, user, and system).

• The amount of RAM free on the Server.

• The amount of RAM being used on the Server.

• The total RAM avalible on the server.

• The above 3 things but with Swap insted of RAM.

• The amount of CPU being used by the application "Java".

• The amount of RAM being used by the application "Java".

• The amount of Reads and Writes to the disk, represented in MiB/s.

• The temperature of each of the cores of the CPU, in celsius.

# Other Stuff

My code is pretty messy so feel free to make improvements and report issues and ill try to fix as many as i can
