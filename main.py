import discord
from discord.ext import commands
from typing import *
import asyncio

token = ""
guild_id = 1187823000934953060
channel_id = 1304329599576182836
role_id = 1304329666995425321
vanity_link = ".gg/femz"

started = False

bot = commands.Bot(
    command_prefix="s!",
    intents = discord.Intents.all()
)

async def send_alert_embed(type: Literal["added", "removed"], member: discord.Member):
    description = f"{member.mention} {type} \"{vanity_link}\" in their custom status."
    print(description)
    embed = discord.Embed(
        title = "Status Update",
        color = discord.Color.green() if type == "added" else discord.Color.red(),
        description = description
    )
    await bot.get_channel(channel_id).send(member.mention, embed = embed)

async def member_added_status(member: discord.Member):
    await member.add_roles(*[discord.Object(id=role_id)], reason="status update")
    await send_alert_embed("added", member)

async def member_removed_status(member: discord.Member):
    await member.remove_roles(*[discord.Object(id=role_id)], reason="status update")
    await send_alert_embed("removed", member)

async def check_member_activities(member: discord.Member):
    new_has_activity = False
    has_rep_role = False
    for activity in member.activities:
        if activity.type == discord.ActivityType.custom:
            if vanity_link in activity.name.lower():
                new_has_activity = True
    for role in member.roles:
        if role.id == role_id:
            has_rep_role = True
    if has_rep_role is True and new_has_activity is False:
        await member_removed_status(member)
    elif has_rep_role is False and new_has_activity is True:
        await member_added_status(member)

async def update_activities():
    guild = bot.get_guild(guild_id)
    while True:
        for member in guild.members:
            if not member.bot:
                await check_member_activities(member)
        await asyncio.sleep(0.2)

@bot.event
async def on_ready():
    print("ready")
    if not started:
        await update_activities()

bot.run(token)
