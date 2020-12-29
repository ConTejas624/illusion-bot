import among
import discord

# reference links
# discord.py API reference: https://discordpy.readthedocs.io/en/latest/api.html#
# discord dev app portal: https://discord.com/developers/applications

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_disconnect():
    print('Disconnected from {0.user}'.format(client))


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
    if message.author.bot:
        return

    if message.content.startswith('$ping'):
        await message.channel.send('pong!')

    elif message.content.equals('$among us help'):
        among_us_help_string = 'example: $among <Jester> <users>'
        among_us_help_string += '\n<Jester>: \'-j\' if playing Jester mode'
        among_us_help_string += '\n<users> list of discord users, mention each user playing, not including the message author'
        await message.channel.send(among_us_help_string)

    elif message.content.startswith('$among'):
        jester = message.content.contains('-j')
        await play_among_us(message, jester)


async def play_among_us(message, jester_mode):
    players = [message.author]
    for member in message.mentions:
        players.append(member)

    game = among.AmongUs(players)

    if jester_mode:
        game.play_jester()
    else:
        game.play_vanilla()
    pass


token_file = open("resources\\token.txt", "r")  # get bot token from a file
token = token_file.read()  # file in .gitignore for security
token_file.close()

client.run(token)
