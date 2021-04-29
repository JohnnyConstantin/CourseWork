'''
Module for parsing logs of sniff_broker.py

Written by Johnny 2021
'''
import json
from time import ctime
import click
from sniff_broker import get_setting, PATH
import re
import os

#For clearing Temp.txt
def Clear_Temp():
    click.echo("Clearing Temp file...")
    f = open(get_setting(PATH, "LOG_PATHS", "LOG_TEMP"), 'w+')
    f.seek(0)
    f.close()

#todo
def Term_parse():
    click.echo("df")

#Returning list for vnc connect: ip port password
def Vnc_Parse():
    click.echo("Vnc parsing...")
    temp = open(get_setting(PATH, "LOG_PATHS", "LOG_TEMP"))
    temp_file = temp.read()
    regex = re.compile(r'/wisepaas/RMM/[0-9a-zA-Z-/]+agentactionack\s.+vncServerPassword.+"}')
    line = regex.search(temp_file)
    data = temp_file[line.start()+97:line.end()]
    credentials = json.loads(data)
    with open(get_setting(PATH, "LOG_PATHS", "LOG_VNC"), "w") as vnc:
         vnc.write(f"Time:{ctime()}\nIP:{credentials['vncServerIP']}\nPort:{credentials['vncServerPort']}\nPassword: "
                   f"{credentials['vncServerPassword']}")
    return [credentials['vncServerIP'], credentials['vncServerPort'], credentials['vncServerPassword']]

def ID_Logs():
    click.echo("Logging Id's...")
    with open(get_setting(PATH, "LOG_PATHS", "log_sniffing"), "r") as logs:
        str1 = logs.read()
        IDs = list(set(re.findall(r'[0-9]+-[0-9]+-[0-9]+-[0-9]+-[0-9a-zA-Z]+', str1)))
        for dirs in IDs:
            file_path = f'Sources\\Logs\\{dirs}'
            if not os.path.exists(file_path):
                click.echo(os.system(f'mkdir {file_path} && cd {file_path} && NUL>{dirs}.txt && cd ..'))
                os.system(f'findstr "{dirs}" Sources\Logs\Logs_sniff.txt > {file_path}\\{dirs}.txt')
            else:
                click.echo(os.system(f'cd {file_path}'))
                os.system(f'findstr "{dirs}" Sources\Logs\Logs_sniff.txt > {file_path}\\{dirs}.txt')

