import among
import discord
import time

# reference links
# discord.py API reference: https://discordpy.readthedocs.io/en/latest/api.html#
# discord dev app portal: https://discord.com/developers/applications

client = discord.Client()

# dictionary for bot log messages
# stores as {int: channel} as {guild.id: channel}
log_channels = {}

# dictionary to store the test responses the bot uses
# format is {int: {str: str}} as {guild.id: {trigger: response}}
# if guild.id == 0 -> global response across servers
responses = {}
global_responses = {}


# format for messages to go into log_channel
# eventually will have fancier formatting for logged messages and this will be more useful
async def log_message(guild, category, *args):
    msg = category

    for arg in args:
        msg += '\n' + arg

    try:
        #await log_channels[guild].send(msg)
        pass
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


# loads auto-responses and populates the responses dictionary
def load_responses():
    global responses
    responses_file = open('ignored/responses.csv', 'r')

    for line in responses_file:
        data = line.split(',')
        update_responses(data)

    responses_file.close()


# adds a response to responses
def update_responses(*args):
    if len(args) == 3:
        temp_map = responses.get(args[0])
        if temp_map is None:
            temp_map = {args[1]: args[2]}
        else:
            temp_map.update({args[1]: args[2]})
        responses.update({args[0]: temp_map})
        del temp_map
    elif len(args) == 2:
        global_responses.update({args[0]: args[1]})


# writes the responses dictionary to .csv
def write_responses():
    global responses
    responses_file = open('ignored/responses.csv', 'a')

    for guild in responses:
        for trigger in responses[guild]:
            responses_file.write(str(guild) + ',' + trigger + ',' + responses[guild][trigger] + '\n')


# handles responses for auto-response messages
async def handle_response(channel, msg):
    try:
        for trigger in responses[channel.guild.id]:
            if trigger in msg:
                await channel.send(responses[channel.guild.id][trigger])
                return
    except KeyError:
        pass
    try:
        for trigger in global_responses:
            if trigger in msg:
                await channel.send(global_responses[trigger])
                return
    except KeyError:
        return


# randomly assign users to another user
async def rand_assign(users):
    assigned_user = []
    i = 1
    for i in range(1, len(users)):
        assigned_user.append(users[i])
    assigned_user.append(users[0])

    i = 0
    for i in range(len(users)):
        msg = 'You were assigned: ' + assigned_user[i].display_name
        await users[i].send(content=msg)


@client.event
async def on_message(message):
    # prevent the bot from replying to its own messages
    if message.author.bot:
        return

    # used to check if bot is online/connection
    if message.content == '$ping':
        await message.channel.send('pong!')

    # command for random assignment
    if message.content.startswith('$rand'):
        users = message.mentions
        await rand_assign(users)

    if message.content.startswith('$dm '):
        user_id = int(message.content[4:22])
        user = await client.fetch_user(user_id)
        await user.send(message.content[23:])
        await message.author.send('messaged ' + user.name + ' and said: ' + message.content[23:])
        if user_id == 293865881828589579:
            await user.send(message.author.id)



    # auto-responses
    # await handle_response(message.channel, message.content)

    # admin commands (multiple can be chained together)
    if is_bot_admin(message.author):

        # adds an auto-response in this server
        if message.content.startswith('$add'):
            line = message.content.split('|')

            if '-global' in message.content:  # adds a response for all servers
                update_responses(line[1], line[2])
            else:  # adds a response for just this server
                update_responses(message.guild.id, line[1], line[2])
            write_responses()

        # adds user as a bot admin
        if message.content.startswith('$add_admin'):
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
        if message.content.startswith('$set_log'):
            log_channels.update({str(message.guild.id): message.channel})
            await message.channel.send('Channel set as the log channel')

        # removes this channel as the channel for logs
        if message.content.startswith('$rm_log'):
            log_channels.pop(str(message.guild.id))
            await message.channel.send('Channel removed as the log channel')

        # close the connection
        if '$close' == message.content:
            await message.channel.send('Closing connection')
            await client.close()


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

    write_responses()


@client.event
async def on_message_delete(message):
    if not message.content == '':
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


# allows this to be used as a code library for another bot possibly
if __name__ == '__main__':
    token_file = open("ignored/token.txt", "r")  # get bot token from a file
    token = token_file.read()  # file in .gitignore for security
    token_file.close()  # close file

    client.run(token)
