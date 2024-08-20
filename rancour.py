import discord
import asyncio
import random
import os
from discord.ext import commands

# Discord Bot Setup
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)  # Disable the default help command

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_reaction_add(reaction, user):
    if reaction.message.channel.name == "✨drops-and-achievements":
        if str(reaction.emoji) == "⭐" and reaction.count == 5:
            highlights_channel = discord.utils.get(reaction.message.guild.text_channels, name="highlights")
            if highlights_channel:
                if reaction.message.attachments:
                    for attachment in reaction.message.attachments:
                        if any(attachment.filename.lower().endswith(ext) for ext in ['png', 'jpg', 'jpeg', 'gif']):
                            embed = discord.Embed(
                                title="Image Highlighted!",
                                description=f"**Original Post by {reaction.message.author.display_name}:**\n{reaction.message.content}",
                                color=discord.Color.gold()
                            )
                            embed.set_image(url=attachment.url)
                            embed.set_footer(text=f"Highlighted by {user.display_name}")
                            await highlights_channel.send(embed=embed)
                            await reaction.message.channel.send(f"{user.mention}, the image has been highlighted!", delete_after=10)
                else:
                    await reaction.message.channel.send(f"{user.mention}, no image found in the message to highlight.", delete_after=10)
            else:
                await reaction.message.channel.send(f"{user.mention}, could not find the highlights channel.", delete_after=10)

# Dice roll command
@bot.command()
async def roll(ctx, sides: int):
    # Delete the user's command message
    await ctx.message.delete()

    if sides < 1:
        await ctx.send("Please enter a number greater than 0!")
        return

    result = random.randint(1, sides)
    await ctx.send(f"You rolled a {result} on a {sides}-sided die.")

# Say command with optional image
@bot.command()
async def say(ctx, *, message: str):
    # Delete the user's command message
    await ctx.message.delete()

    # Check if the message contains an image URL
    if message.startswith("http://") or message.startswith("https://"):
        await ctx.send(message)
    else:
        await ctx.send(message)

# Say with image URL
@bot.command()
async def say_with_image(ctx, *, args: str):
    # Delete the user's command message
    await ctx.message.delete()

    # Split the args string into the message and the image URL
    split_args = args.rsplit(' ', 1)
    
    if len(split_args) == 2:
        message = split_args[0]
        image_url = split_args[1]

        # Create an embed with the message and set the image
        embed = discord.Embed(description=message)
        embed.set_image(url=image_url)

        await ctx.send(embed=embed)
    else:
        await ctx.send("Please provide both a message and an image URL.")

# Help command
@bot.command()
async def help(ctx):
    # Delete the user's command message
    await ctx.message.delete()

    embed = discord.Embed(
        title="Bot Commands",
        description="Here's a list of commands you can use:",
        color=discord.Color.blue()
    )
    embed.add_field(name="!roll <number of sides>", value="Rolls a single die with the specified number of sides.", inline=False)
    embed.add_field(name="!say <message>", value="Sends a message as the bot.", inline=False)
    embed.add_field(name="!say_with_image <message> <image_url>", value="Sends a message with an image as the bot.", inline=False)
    embed.add_field(name="!help", value="Displays this help message.", inline=False)

    await ctx.send(embed=embed)

# Retrieve the bot token from the Railway environment variable
bot.run(os.getenv('DISCORD_BOT_TOKEN'))
