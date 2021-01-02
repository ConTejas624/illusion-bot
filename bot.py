import among
import discord

# reference links
# discord.py API reference: https://discordpy.readthedocs.io/en/latest/api.html#
# discord dev app portal: https://discord.com/developers/applications

client = discord.Client()

# dictionary for bot log messages
# stores {guild.id: channel}
log_channels = {}


# format for messages to go into log_channel
# eventually will have fancier formatting for logged messages and this will be more useful
async def log_message(guild, category, *args):
    if len(args) < 3:
        return

    msg = category

    for arg in args:
        msg += '\n' + arg

    try:
        await log_channels[guild].send(msg)
    except KeyError:
        print('guild {} has no log channel'.format(guild))


@client.event
async def on_ready():
    data_file = open("log_channels.csv", "r")
    for line in data_file:
        data = line.split(',')
        channel = await client.fetch_channel(int(data[1]))
        log_channels.update({int(data[0]): channel})

    print('discord.py library version {0.__version__}'.format(discord))
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_disconnect():
    print('Disconnected from {0.user}'.format(client))

    # write data to file
    data_file = open("log_channels.csv", "w")
    for guild in log_channels:
        data_file.write(str(guild) + ',' + str(log_channels[guild].id))
    data_file.close()


@client.event
async def on_message_delete(message):
    await log_message(message.guild.id, 'MESSAGE_DELETION',
                      'user:', message.author.name, 'message deleted:', message.content)


@client.event
async def on_bulk_message_delete(messages):
    pass


@client.event
async def on_message_edit(before, after):
    await log_message(before.guild.id, 'MESSAGE_EDIT', 'user:', after.author.name, 'previous text: ', before.content)


@client.event
async def on_reaction_add(reaction, user):
    pass


@client.event
async def on_reaction_remove(reaction, user):
    pass


@client.event
async def on_reaction_clear(message, reactions):
    await log_message(message.guild.id, 'REACTIONS_CLEARED', 'user:', message.author.name,
                      'message:', message.content, 'reactions removed:', str(len(reactions)))


@client.event
async def on_guild_channel_create(channel):
    await log_message(channel.guild.id, 'CHANNEL_CREATED',
                      'channel:', channel.name, 'category:', channel.category.name)


@client.event
async def on_guild_channel_delete(channel):
    await log_message(channel.guild.id, 'CHANNEL_DELETED',
                      'channel:', channel.name, 'category:', channel.category.name)


@client.event
async def on_guild_channel_update(before, after):
    await log_message(before.guild.id, 'CHANNEL_EDITED', 'previous_name:', before.name, 'previous_category: ',
                      before.category.name, 'after_name:', after.name, 'after_category', after.category.name)


@client.event
async def on_guild_channel_pins_update(channel, last_pin):
    pass


@client.event
async def on_member_join(member):
    await log_message(member.guild.id, 'USER_JOIN', 'user:', member.name)


@client.event
async def on_member_leave(member):
    await log_message(member.guild.id, 'USER_LEFT', 'user:', member.name)


@client.event
async def on_member_ban(guild, user):
    await log_message(guild.id, 'USER_BANNED', 'user:', user.name)


@client.event
async def on_member_unban(guild, user):
    await log_message(guild.id, 'USER_UNBANNED', 'user:', user.name)


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
    await log_message(role.guild.id, 'ROLE_CREATED', 'role:', role.name, 'mentionable:', role.mentionable)


@client.event
async def on_guild_role_delete(role):
    await log_message(role.guild.id, 'ROLE_DELETED', 'role:', role.name, 'mentionable:', role.mentionable)


@client.event
async def on_guild_role_update(before, after):
    await log_message(before.guild.id, 'ROLE_EDITED', 'previous_role:', before.name, 'after_role:', after.name)


@client.event
async def on_guild_emojis_update(guild, before, after):
    pass


@client.event
async def on_invite_create(invite):
    await log_message(invite.guild.id, 'INVITE_CREATED', 'invite:', invite.url,
                      'uses:', invite.max_uses, 'time:', invite.max_age)


@client.event
async def on_invite_delete(invite):
    await log_message(invite.guild.id, 'INVITE_DELETED', 'invite:', invite.url,
                      'uses:', invite.max_uses, 'time:', invite.max_age)


@client.event
async def on_message(message):
    # prevent the bot from replying to its own messages
    if message.author.bot:
        return

    # used to check if bot is online/connection
    if message.content == '$ping':
        await message.channel.send('pong!')

    # admin things that I want the bot to do (eventually will be open to any admin role)
    if message.author.id == 794788646153748500:

        # sets this channel as the channel for logs
        if '-set_log' in message.content:
            log_channels.update({str(message.guild.id): message.channel})
            await message.channel.send('Channel set as the log channel')

        # close the connection
        if '-close' in message.content:
            await message.channel.send('Closing connection')
            await client.close()


token_file = open("ignored\\token.txt", "r")  # get bot token from a file
token = token_file.read()  # file in .gitignore for security
token_file.close()

client.run(token)
