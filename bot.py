import among
import discord

# reference links
# discord.py API reference: https://discordpy.readthedocs.io/en/latest/api.html#
# discord dev app portal: https://discord.com/developers/applications

client = discord.Client()

# data file
try:
    data_file = open("data.csv", "r")
except FileNotFoundError:
    data_file = open("data.csv", "w")

# channel for bot log messages
log_channel = None


# format for messages to go into log_channel
# eventually will have fancier formatting for logged messages and this will be more useful
async def log_message(category, tag, user, description, text):
    msg = category
    msg += "\n" + tag + ": " + user
    msg += "\n" + description + text

    await log_channel.send(msg)


async def long_log_message(category, tag, user, description, text, desc2, txt2):
    msg = category
    msg += "\n" + tag + ": " + user
    msg += "\n" + description + text
    msg += "\n" + desc2 + txt2

    await log_channel.send(msg)


@client.event
async def on_ready():
    global log_channel
    log_channel = await client.fetch_channel(521829000029405184)

    print('discord.py library version {0.__version__}'.format(discord))
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
    await log_message('MESSAGE_DELETION', 'user', message.author.name, 'message deleted: ', message.content)


@client.event
async def on_bulk_message_delete(messages):
    pass


@client.event
async def on_message_edit(before, after):
    await log_message('MESSAGE_EDIT', 'user', after.author.name, 'previous text: ', before.content)


@client.event
async def on_reaction_add(reaction, user):
    pass


@client.event
async def on_reaction_remove(reaction, user):
    pass


@client.event
async def on_reaction_clear(message, reactions):
    await long_log_message('REACTIONS_CLEARED', 'user', message.author.name, 'message: ', message.content,
                           'reactions removed: ', str(len(reactions)))


@client.event
async def on_guild_channel_create(channel):
    await log_message('CHANNEL_CREATED', 'channel', channel.name, 'category: ', channel.category.name)


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
        pass

    if message.content == '$disconnect':
        await message.channel.send('closing')
        await client.close()


token_file = open("ignored\\token.txt", "r")  # get bot token from a file
token = token_file.read()  # file in .gitignore for security
token_file.close()

client.run(token)
