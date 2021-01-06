import among
import discord

# reference links
# discord.py API reference: https://discordpy.readthedocs.io/en/latest/api.html#
# discord dev app portal: https://discord.com/developers/applications

client = discord.Client()

# dictionary for bot log messages
# stores as {int: channel} as {guild.id: channel}
log_channels = {}


# format for messages to go into log_channel
# eventually will have fancier formatting for logged messages and this will be more useful
async def log_message(guild, category, *args):
    msg = category

    for arg in args:
        msg += '\n' + arg

    try:
        await log_channels[guild].send(msg)
    except KeyError:
        print('guild {} has no log channel'.format(guild))


# checks if the user is an admin on the server
# list of bot admins is stored in admin_data.dat, is ignored from GitHub for security
# if the bot ever has multiple developers, this would be useful to be able to have the bot recognize users who are not
# necessarily admins of the guild be able to use the bot's administrative commands
def is_bot_admin(member):
    admins_file = open('ignored/admin_data.dat', 'r')  # open file

    # parse file to check user ids against list of bot admins
    for admin in admins_file:
        if admin == str(member.id):
            return True
    admins_file.close()  # close file

    try:
        return member.guild_permissions.administrator
    except AttributeError:
        return False


# read data from csv
async def read_csv_data():
    data_file = open("ignored/log_channels.csv", "r")  # open data_file

    # parse data_file to populate the log_channels dictionary
    for line in data_file:
        data = line.split(',')
        if len(data) == 2:
            channel = await client.fetch_channel(int(data[1]))
            log_channels.update({int(data[0]): channel})

    data_file.close()  # close data_file


@client.event
async def on_ready():
    await read_csv_data()
    print('discord.py library version {0.__version__}'.format(discord))


@client.event
async def on_connect():
    print('Connected as {0.user}'.format(client))


@client.event
async def on_disconnect():
    print('Disconnected from {0.user}'.format(client))

    # write data to file
    data_file = open("ignored/log_channels.csv", "w")  # open data_file
    # parse log_channels to write the data to file
    for guild in log_channels:
        data_file.write(str(guild) + ',' + str(log_channels[guild].id) + '\n')
    data_file.close()  # close data_file


@client.event
async def on_message_delete(message):
    await log_message(message.guild.id, '**MESSAGE_DELETION**',
                      '**user:**', message.author.name, '**message deleted:**', message.content)


@client.event
async def on_message_edit(before, after):
    if not before.content == after.content:
        await log_message(before.guild.id, '**MESSAGE_EDIT**', '**user:**', after.author.name,
                          '**previous text: **', before.content, '**new text:**', after.content)


@client.event
async def on_reaction_clear(message, reactions):
    await log_message(message.guild.id, '**REACTIONS_CLEARED**', '**user:**', message.author.name,
                      '**message:**', message.content, '**reactions removed:**', str(len(reactions)))


@client.event
async def on_guild_channel_create(channel):
    await log_message(channel.guild.id, '**CHANNEL_CREATED**',
                      '**channel:**', channel.name, '**category:**', channel.category.name)


@client.event
async def on_guild_channel_delete(channel):
    await log_message(channel.guild.id, '**CHANNEL_DELETED**',
                      '**channel:**', channel.name, '**category:**', channel.category.name)


@client.event
async def on_guild_channel_update(before, after):
    await log_message(before.guild.id, '**CHANNEL_EDITED**', '**previous_name:**', before.name,
                      '**previous_category:**', before.category.name, '**after_name:**', after.name,
                      '**after_category**', after.category.name)


@client.event
async def on_member_join(member):
    await log_message(member.guild.id, '**USER_JOIN**', '**user:**', member.name)


@client.event
async def on_member_leave(member):
    await log_message(member.guild.id, '**USER_LEFT**', '**user:**', member.name)


@client.event
async def on_member_ban(guild, user):
    await log_message(guild.id, '**USER_BANNED**', '**user:**', user.name)


@client.event
async def on_member_unban(guild, user):
    await log_message(guild.id, '**USER_UNBANNED**', '**user:**', user.name)


@client.event
async def on_guild_role_create(role):
    await log_message(role.guild.id, '**ROLE_CREATED**', '**role:**', role.name, '**mentionable:**', role.mentionable)


@client.event
async def on_guild_role_delete(role):
    await log_message(role.guild.id, '**ROLE_DELETED**', '**role:**', role.name, '**mentionable:**', role.mentionable)


@client.event
async def on_guild_role_update(before, after):
    await log_message(before.guild.id, '**ROLE_EDITED**', '**previous_role:**', before.name,
                      '**after_role:**', after.name)


@client.event
async def on_invite_create(invite):
    await log_message(invite.guild.id, '**INVITE_CREATED**', '**invite:**', invite.url,
                      '**uses:**', invite.max_uses, '**time:**', invite.max_age)


@client.event
async def on_invite_delete(invite):
    await log_message(invite.guild.id, '**INVITE_DELETED**', '**invite:**', invite.url,
                      '**uses:**', invite.max_uses, '**time:**', invite.max_age)


@client.event
async def on_error(event, *args, **kwargs):
    print('ERROR: ' + event)
    print(args)
    print(kwargs)


@client.event
async def on_message(message):
    # prevent the bot from replying to its own messages
    if message.author.bot:
        return

    # used to check if bot is online/connection
    if message.content == '$ping':
        await message.channel.send('pong!')

    # admin commands (multiple can be chained together)
    if is_bot_admin(message.author):
        # adds user as a bot admin
        if '-add_admin' in message.content:
            admin_data = open('ignored/admin_data.dat', 'a')  # open file
            mentions = []  # list of members who were added to send message after

            # parse the mentioned members
            for member in message.mentions:
                admin_data.write(str(member.id) + '\n')
                mentions.append(member.id)
            admin_data.close()  # close the file

            # send messages to confirm successful admin addition
            await message.channel.send('User(s) {} added as a bot administrator'.format(mentions))
            print('User(s) {} added as a bot administrator'.format(mentions))

        # sets this channel as the channel for logs
        if '-set_log' in message.content:
            log_channels.update({str(message.guild.id): message.channel})
            await message.channel.send('Channel set as the log channel')

        # removes this channel as the channel for logs
        if '-rm_log' in message.content:
            log_channels.pop(str(message.guild.id))
            await message.channel.send('Channel removed as the log channel')

        # close the connection
        if '-close' in message.content:
            await message.channel.send('Closing connection')
            await client.close()


# allows this to be used as a code library for another bot possibly
if __name__ == '__main__':
    token_file = open("ignored/token.txt", "r")  # get bot token from a file
    token = token_file.read()  # file in .gitignore for security
    token_file.close()  # close file

    client.run(token)
