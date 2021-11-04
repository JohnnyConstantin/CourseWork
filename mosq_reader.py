import os
import click


def get_data():
    click.echo(os.system("sudo mosquitto_sub -h \"192.168.2.230\" -p \"1883\" -t \""
                         "/we/are/legion/\" -v > log.json"))


if __name__ == '__main__':
    get_data()
