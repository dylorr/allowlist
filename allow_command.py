## notes
# must add new IP address to access db

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

cluster = MongoClient("mongodb+srv://[username]:[password]@cluster0.bhpgu.mongodb.net")
print(cluster)
db = cluster[' ']
collection = db[' ']

############ CONSTANTS TO UPDATE ############

server_id = 
channel_id = 
role_id = 
bot_token = '[token]'

############ DISCORD SETUP - COMMANDS ############

bot = lightbulb.BotApp(token = bot_token,
 default_enabled_guilds=(server_id)
 )
@bot.listen(hikari.StartedEvent)
async def on_started(event):
    print('🤖 Ready to accept allowlist submissions!')

@bot.listen(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    if isinstance(event.exception, lightbulb.CommandInvocationError):
        await event.context.respond(f"🥺 Something went wrong during invocation of command `{event.context.command.name}`.", flags=hikari.MessageFlag.EPHEMERAL)
        raise event.exception

    # Unwrap the exception to get the original cause
    exception = event.exception.__cause__ or event.exception

    if isinstance(exception, lightbulb.NotOwner):
        await event.context.respond("🔒 You are not the owner of this bot.", flags=hikari.MessageFlag.EPHEMERAL)
    elif isinstance(exception, lightbulb.CommandIsOnCooldown):
        await event.context.respond(f"⏳ This command is on cooldown. Retry in `{exception.retry_after:.2f}` seconds.", flags=hikari.MessageFlag.EPHEMERAL)
    elif isinstance(exception, lightbulb.CheckFailure):
        await event.context.respond(f"🙅‍♂️ This command can only be used in the designated allowlist channel, <#{channel_id}>", flags=hikari.MessageFlag.EPHEMERAL)
    elif ...:
        ...
    else:
        raise exception
        
#restrict command to a specific channel by channel id
@lightbulb.Check
def channel_only(ctx):
    return ctx.channel_id == channel_id

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
        await ctx.member.add_role(role_id)
        await ctx.respond(f'✅ Your address `{addy}` has been successfully added to the allowlist!', flags=hikari.MessageFlag.EPHEMERAL)
    else:
        submitted_address = collection.find_one({"_id":author})['address']
        await ctx.respond(f'❌ Your address `{submitted_address}` has already been added to the allowlist!', flags=hikari.MessageFlag.EPHEMERAL)
bot.run()
