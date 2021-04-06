from myCalendar import Calendar
from statics import Statics
import asyncio
import time
import pickle
from datetime import datetime, timedelta, timezone, date
from discord.ext.commands import DefaultHelpCommand
from discord.ext.commands import Bot
from discord.ext.commands import CommandNotFound
from discord import Intents
from discord.utils import get
import discord

print('starting script')

intents = Intents.default()
intents.members = True
intents.reactions = True
# Change only the no_category default string
help_command = DefaultHelpCommand(no_category='Commands')
bot = Bot(command_prefix='$', intents=intents, help_command=help_command)

channel_bell_ring = None
channel_general = None


async def alertOnNextPeriod():
    global channel_bell_ring

    while True:
        try:
            # now = datetime.utcnow() - timedelta(hours=5)
            # dt = date.today()
            # morningmessagetime = datetime.combine(dt, datetime.min.time()) + timedelta(hours=7, minutes=58)
            # print('a')
            # if (abs((morningmessagetime - now).total_seconds()) <= 10):
            # day = await get_day()
            # await channel_general.send('Good morning! '+day)
            # pass
            # else:
            # print((morningmessagetime - now).total_seconds())
            # print('checking...')
            # await channel_general.send('checking...')
            time_left = Calendar.time_until_next_period()
            period = Calendar.next_period_json()
            if time_left <= 60:
                await channel_bell_ring.send(
                    'Time for <@&' + str(Statics.ROLES[Statics.CALENDAR_EVENTS[period['summary']]]) + '>!!')
            if 3 * 60 + 60 >= time_left >= 3 * 60:
                await channel_bell_ring.send(
                    '3 minutes until <@&' + str(Statics.ROLES[Statics.CALENDAR_EVENTS[period['summary']]]) + '>!!')
            #await asyncio.sleep(
                #57 - ((datetime.now(tz=timezone.utc) - datetime(1970, 1, 1, tzinfo=timezone.utc)).total_seconds() % 60))
            await asyncio.sleep(60)
        except:
            print('alert loop try failed')
            await asyncio.sleep(2)


async def resetRoles():
    server = bot.get_guild(Statics.SERVER_ID)
    mje = None
    for member in server.members:
        if str(member) == "MJE10#6928":
            mje = member

    for i in Statics.CALENDAR_EVENTS:
        print(i)
        await mje.send('Resetting role ' + i)
        role = server.get_role(Statics.ROLES[Statics.CALENDAR_EVENTS[i]])
        for member in server.members:
            if role not in member.roles:
                await member.add_roles(role)
        message = await bot.get_channel(Statics.CHANNEL_OPT_IN).fetch_message(
            Statics.MESSAGES[Statics.CALENDAR_EVENTS[i]])
        reactions = message.reactions[0].users()
        async for user in reactions:
            await user.remove_roles(role)

    await mje.send('Role reset complete.')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error


@bot.event
async def on_ready():
    global channel_bell_ring, channel_general

    print(f'Bot connected as {bot.user}')
    channel_bell_ring = bot.get_channel(Statics.CHANNEL_BELL_RING)
    channel_general = bot.get_channel(Statics.CHANNEL_GENERAL)
    await alertOnNextPeriod()


@bot.event
async def on_raw_reaction_add(reaction):
    global channel_general

    for i in Statics.MESSAGES:
        if Statics.MESSAGES[i] == reaction.message_id:
            server = bot.get_guild(Statics.SERVER_ID)
            role = server.get_role(Statics.ROLES[i])

            if reaction.event_type == "REACTION_ADD":
                await server.get_member(reaction.user_id).remove_roles(role)
                await channel_general.send(
                    'I removed notifications for ' + str(role) + ' for ' + str(server.get_member(reaction.user_id)))
            else:
                await server.get_member(reaction.user_id).add_roles(role)
                await channel_general.send(
                    'I reinstated notifications for ' + str(role) + ' for ' + str(server.get_member(reaction.user_id)))


@bot.event
async def on_raw_reaction_remove(reaction):
    await on_raw_reaction_add(reaction)


@bot.command(name='syed_messed_up', brief='Displays the number of times Syed has typed into Bell Ring.')
async def user_syed_messed_up(context):
    try:
        x = pickle.load(open(Statics.PATH_PICKLE_SYED, 'rb'))
    except:
        x = 0
    await context.send('Syed has messed up ' + str(x) + ' times!')


@bot.command(name='syed_messed_up_increment', hidden=True)
async def user_syed_messed_up_increment(context):
    if context.message.author.id == 159045740457361409:
        try:
            x = pickle.load(open(Statics.PATH_PICKLE_SYED, 'rb'))
        except:
            x = 0
        x += 1
        await context.send('Syed has messed up ' + str(x) + ' times!')
        pickle.dump(x, open(Statics.PATH_PICKLE_SYED, 'wb'))
    else:
        await context.send('Only mike energy can increment this value!')


@bot.command(name='syed_messed_up_decrement', hidden=True)
async def user_syed_messed_up_increment(context):
    if context.message.author.id == 159045740457361409:
        try:
            x = pickle.load(open(Statics.PATH_PICKLE_SYED, 'rb'))
        except:
            x = 1
        x -= 1
        await context.send('Syed has messed up ' + str(x) + ' times!')
        pickle.dump(x, open(Statics.PATH_PICKLE_SYED, 'wb'))
    else:
        await context.send('Only mike energy can increment this value!')


async def syed_messed_up_increment(message):
    try:
        x = pickle.load(open(Statics.PATH_PICKLE_SYED, 'rb'))
    except:
        x = 1
    x += 1
    await message.channel.send('Syed has messed up ' + str(x) + ' times!')
    pickle.dump(x, open(Statics.PATH_PICKLE_SYED, 'wb'))


@bot.command(name='hello', hidden=True)
async def fetchServerInfo(context):
    await context.send('hi')


@bot.command(name='ping', brief='Tests whether the bot is online.')
async def fetchServerInfo(context):
    await context.send('pong!')


@bot.command(name='fetch_events', hidden=True)
async def user_getEvents(context):
    Calendar.getEventsFromGoogle()
    await context.send('Events obtained')


@bot.command(name='ring', brief='Shows the amount of time until the next period.')
async def user_alert(context):
    await context.send(str(Calendar.next_period()))


@bot.command(name='day', brief='Shows the date, and whether it is a day 1 or day 2.')
async def user_get_day(context):
    await context.send(await get_day())


# @bot.command(name='cohort')
# async def user_get_cohort(context):
#     await context.send(await get_cohort())


@bot.command(name='reset_roles', hidden=True)
async def user_reset_roles(context):
    await context.send("Resetting roles... this might take a while...")
    await resetRoles()
    await context.send("Role reset complete!")


@bot.command(name='get_offset', hidden=True)
async def user_get_offset(context):
    offset = 0
    with open("data/cr_offset.txt", "r") as f:
        offset = int(f.read())
    await context.send("Offset is " + str(offset) + " seconds.")

async def get_day():
    ret_str = "Today is "
    now = datetime.today() - timedelta(hours=5)
    ret_str += Statics.DAYS_OF_WEEK[now.weekday()] + ", " + Statics.MONTHS[now.month] + " " + str(now.day) + "."
    day = Calendar.get_day()
    if day is not None:
        ret_str += " It is a Day " + day + "!"
    return ret_str


async def get_cohort():
    cohort = Calendar.get_cohort()
    if cohort is not None:
        return "Cohort " + cohort + " is in school!"
    else:
        return "There is no cohort in school today!"


@bot.command(name='schedule', brief='Shows the picture versions of the schedule.')
async def user_get_schedule(context):
    await context.send(file=discord.File(Statics.PATH_SCHEDULE_1_15))
    await context.send(file=discord.File(Statics.PATH_DAYS_MARCH))
    await context.send(file=discord.File(Statics.PATH_SCHEDULE_1_15__2_HOUR_DELAY))


@bot.event
async def on_message(message):
    # mje:159045740457361409,sy:334177612979240982,bell:761273344054001675,gen:761272775310180386
    # 804329598963417119
    if message.content.split(' ')[0] == '$say':
        await message.channel.send(' '.join(message.content.split(' ')[1:]))
    if message.content.split(' ')[0] == '$react':
        msg = await message.channel.fetch_message(int(message.content.split(' ')[1]))
        # await msg.add_reaction("\U0001F44D")
        await msg.add_reaction("❌")
    if message.content == "oi bellboi":
        await message.channel.send('wut m8')
    if message.author.id == 334177612979240982 and message.channel.id == 761273344054001675:
        await syed_messed_up_increment(message)
    if message.author.id == 159045740457361409 and message.content[:8] == "$offset ":
        with open("data/cr_offset.txt", "w") as f:
            f.write(message.content[8:])
        await message.channel.send("Set offset to " + message.content[8:] + " seconds.")

    await bot.process_commands(message)


print('starting bot')
bot.run("")
print('bad')
# while 1:
