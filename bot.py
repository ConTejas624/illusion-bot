import among
import discord

# reference links
# discord.py API reference: https://discordpy.readthedocs.io/en/latest/api.html#
# discord dev app portal: https://discord.com/developers/applications

client = discord.Client()

# data file
data_file = open("data.csv", "r")

# channel for bot log messages
log_channel = None


@client.event
async def on_ready():
    global log_channel
    log_channel = await client.fetch_channel(521829000029405184)

    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_disconnect():
    print('Disconnected from {0.user}'.format(client))

    # write data to file
    global data_file
    data_file = open("data.csv", "w")
    data_file.write(str(log_channel.id))


@client.event
async def on_message_delete(message):
    pass


@client.event
async def on_bulk_message_delete(messages):
    pass


@client.event
async def on_message_edit(before, after):
    pass


@client.event
async def on_reaction_add(reaction, user):
    pass


@client.event
async def on_reaction_remove(reaction, user):
    pass


@client.event
async def on_reaction_clear(message, reactions):
    pass


@client.event
async def on_guild_channel_create(channel):
    pass


@client.event
async def on_guild_channel_delete(channel):
    pass


@client.event
async def on_guild_channel_update(before, after):
    pass


@client.event
async def on_guild_channel_pins_update(channel, last_pin):
    pass


@client.event
async def on_member_join(member):
    pass


@client.event
async def on_member_leave(member):
    pass


@client.event
async def on_member_ban(guild, user):
    pass


@client.event
async def on_member_unban(guild, user):
    pass


@client.event
async def on_member_update(before, after):
    pass


@client.event
async def on_guild_join(guild):
    pass


@client.event
async def on_guild_remove(guild):
    pass


@client.event
async def on_guild_update(guild):
    pass


@client.event
async def on_guild_role_create(role):
    pass


@client.event
async def on_guild_role_delete(role):
    pass


@client.event
async def on_guild_role_update(before, after):
    pass


@client.event
async def on_guild_emojis_update(guild, before, after):
    pass


@client.event
async def on_invite_create(invite):
    pass


@client.event
async def on_invite_delete(invite):
    pass


@client.event
async def on_message(message):
    global log_channel

    # prevent the bot from replying to its own messages
    if message.author.bot:
        return

    # used to check if bot is online/connection
    if message.content == '$ping':
        await message.channel.send('pong!')

    if message.content == '$test':
        await log_channel.send('test')

    if message.content == '$disconnect':
        await message.channel.send('closing')
        await client.close()


token_file = open("ignored\\token.txt", "r")  # get bot token from a file
token = token_file.read()  # file in .gitignore for security
token_file.close()

client.run(token)
