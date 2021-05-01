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
    config.add_section("STRINGS")
    config.set("STRINGS", "DEFAULT_SUB_STRING", 'mosquitto_sub -h "test.mosquitto.org" -p "1883" -t')
    config.set("STRINGS", "DEFAULT_PUB_STRING", 'mosquitto_pub - h "test.mosquitto.org" - p "1883" - t')
    config.set("STRINGS", "DEFAULT_EXPL_TOPIC", 'digitransit')
    config.set("STRINGS", "DEFAULT_EXPL_MSG", '-m {"@type": "TransportationRoute", "operator": {"@type": "Organization", "idLocal": 6},"vehicle": {"@type": "Vehicle", "idLocal": 464,"location": {"@type": "Location", "latitude": 69.69, "longitude": 69.69}}}')

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

def expl_msg(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    while(1):
        click.echo(os.system(get_setting(PATH, "STRINGS", "default_pub_string") + ' \"' +
            get_setting(PATH, "STRINGS", "default_expl_topic") + '\" ' +
            get_setting(PATH, "STRINGS", "default_expl_msg")))

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
@click.option(
    '--expl', is_flag=True, callback=expl_msg, expose_value=False, is_eager=True, help='Wtf'
)

def main():
    """
        Tool for sniffing mosquitto broker and sending wrong data to server.
    """

if __name__ == '__main__':
    main()
