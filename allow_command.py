"""
Created on Fri Aug 27 15:11:53 2021

@author: dylanorrell

"""
############ IMPORTS ############

from multiprocessing import context
import discord
import asyncio
import nest_asyncio
nest_asyncio.apply()
from discord.ext import commands, tasks
import pymongo
from pymongo import MongoClient
import hikari
import lightbulb
from hikari import api

############ MONGODB CONNECTION ############

cluster = MongoClient("mongodb+srv://djo:password1234@cluster0.bhpgu.mongodb.net")
print(cluster)
db = cluster['hunter']
print(db)
collection = db['hunter']
print(collection)

############ DISCORD SETUP - COMMANDS ############

bot = lightbulb.BotApp(token = 'OTQxOTA1MjkxMTUzNDA4MDUw.YgcvqQ.lEDRqdJ2EUPJzMt5xsMG4C5ND7k',
 default_enabled_guilds=(856981718623059989)
 )
@bot.listen(hikari.StartedEvent)
async def on_started(event):
    print('Ready to accept allowlist submissions!')

@bot.listen(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    if isinstance(event.exception, lightbulb.CommandInvocationError):
        await event.context.respond(f"🥺 Something went wrong during invocation of command `{event.context.command.name}`.")
        raise event.exception

    # Unwrap the exception to get the original cause
    exception = event.exception.__cause__ or event.exception

    if isinstance(exception, lightbulb.NotOwner):
        await event.context.respond("🔒 You are not the owner of this bot.")
    elif isinstance(exception, lightbulb.CommandIsOnCooldown):
        await event.context.respond(f"⏳ This command is on cooldown. Retry in `{exception.retry_after:.2f}` seconds.")
    elif isinstance(exception, lightbulb.CheckFailure):
        await event.context.respond(f"🙅‍♂️ This command can only be used in the designated allowlist channel.")
    elif ...:
        ...
    else:
        raise exception
        

#restrict command to a specific channel by channel id
@lightbulb.Check
def channel_only(ctx):
    return ctx.channel_id == 942130397964288101

@bot.command
@lightbulb.add_cooldown(500.0, 1, lightbulb.UserBucket)
@lightbulb.option('address','Your wallet address')
@lightbulb.add_checks(channel_only) #adds channel id restriction check
@lightbulb.command('allowlist','Adds your wallet address to the project allowlist')
@lightbulb.implements(lightbulb.SlashCommand)
async def allowlist(ctx):
    author = str(ctx.author)
    addy = str(ctx.options.address)
    
    myquery = { "_id": author }
    if (collection.count_documents(myquery) == 0):
        post = {"_id" : author,"address" : ctx.options.address}
        collection.insert_one(post)
        #add role (by id) to member object from user
        await ctx.member.add_role(942097802857701376)
        await ctx.respond(f'✅ Your address {addy} has been successfully added to the allowlist!', flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond('❌ You have already added an address to the allowlist!', flags=hikari.MessageFlag.EPHEMERAL)
bot.run()


############ DISCORD SETUP ############

""" #doesn't require a command, so use empty string here
bot = commands.Bot(command_prefix='!')
client=discord.Client()

@bot.event
async def on_ready(): 
    print('We have logged in as {0.user}'.format(bot))
    
############ DISCORD COMMAND ############

@bot.command()
async def whitelist (ctx):
    await ctx.message.add_reaction('✅')
    user = ctx.author
    role = user.top_role
    displayname = ctx.author.display_name
    print(user)
    print(role)
    await ctx.message.author.send (f'Hey {displayname}! Your highest role is {role}')
    await ctx.message.author.send ('What address would you like to whitelist?')
    #response = await bot.wait_for('message', check=message_check(channel=ctx.author.dm_channel))
    def check(msg):
        return msg.content.startswith('0x')
    try:
        response = await bot.wait_for('message', check=check, timeout=15)
        addy = response.content
        print (user, role, addy)
        myquery = { "_id": str(user) }
        if (collection.count_documents(myquery) == 0):
                  post = {"_id": str(user), "role": str(role), "address" : str(addy)}
                  collection.insert_one(post)
                  await response.add_reaction('✅')
                  await ctx.message.author.send (f'🤘❤️ LFG! {addy} is whitelisted! 👀 Stay up to date on project news over at <#847109630030250026>')
        else:
            await response.add_reaction('❌')
            await ctx.message.author.send (f'😎 You have already submitted an addrress to be whitelisted.')

    except asyncio.TimeoutError:
        await ctx.message.author.send('😢 Your whitelist request has timed out. 🚀 Please try the !whitelist command again in <#879734307768389642>')

    return(role)

bot.run('TOKEN') """
