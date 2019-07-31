import logging
import configparser
import sys
import os.path
import time
import asyncio

import discord
import requests

# Logger Setup
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Discord Setup
client = discord.Client()

# Config Parsing
config = configparser.ConfigParser()

if not os.path.isfile('config.ini'):
    logger.error('No config.ini present')
    sys.exit()

config.read('config.ini')


async def watch_server_status():
    while True:
        logger.info('Updating server status @ {}'.format(time.time()))

        try:
            response = requests.get(
                'https://api.mcsrvstat.us/2/{}'.format(config['Minecraft']['ServerIP'])).json()

            if 'hostname' in response:
                name = response['hostname']
            else:
                name = response['ip']
            if response['online']:
                status_string = '{current}/{max} playing on {name}'.format(
                    current=response['players']['online'],
                    max=response['players']['max'],
                    name=name
                )
            else:
                status_string = '{name} is offline :('.format(
                    name=name
                )
        except:
            status_string = "I'm having trouble right now!"

        status = discord.Game(status_string)
        await client.change_presence(activity=status)
        logger.info(
            'Successfully updated. New Status: {}'.format(status_string))
        await asyncio.sleep(120)


@client.event
async def on_ready():
    logger.info('Server Monitor Started')
    logger.info('Using Discord Account {}'.format(client.user))
    logger.info('Watching MC Server {}'.format(
        config['Minecraft']['ServerIP']))
    await watch_server_status()

client.run(str(config['Discord']['Token']))
