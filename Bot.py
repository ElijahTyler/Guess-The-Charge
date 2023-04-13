import re
import json
import discord
from discord.ext import commands
import GuessTheCharge

with open('token.json', 'r') as f:
    token = json.load(f)['token']

intents = discord.Intents.all()
intents.members = True
intents.presences = True
intents.messages = True
client = commands.Bot(command_prefix="$", intents=intents)

@client.event
async def on_ready():
    print(f"Logged on")

@client.event
async def on_message(message):
    if message.author == client.user: return
    if message.author.bot: return

    if message.content.startswith("$"): # read potential command
        await client.process_commands(message)

@client.command()
async def about(ctx):
    await ctx.send("Version 1.01 - scoreboard is online!")

@client.command()
async def gtc(ctx):
    message_content_no_command = re.sub(r'\$gtc', '', ctx.message.content).strip()
    print(message_content_no_command)

    f = open('scores.json', 'r')
    database = json.load(f)
    f.close()

    if message_content_no_command == 'score':
        user = f"{str(ctx.author.name)}#{int(ctx.author.discriminator)}"
        
        if user in database.keys():
            score = database[user]
            await ctx.send(f"Score for {user}: {score} pts")
        else:
            await ctx.send("You haven't played yet!")
        return
    elif message_content_no_command == 'scoreboard':
        def compile_spot(user, score):
            claritin = f'{user} - {score} pts'
            return claritin
        
        await ctx.send("Searching for top scores...")
        # find the top 3 scores in the database
        database_names = []
        database_scores = []
        for name in database.keys():
            database_names.append(name)
            database_scores.append(database[name])
        top_names = []
        for i in range(3):
            # find max score value, and then find its index in database_scores
            for i in range(len(database_scores)):
                if max(database_scores) == database_scores[i]: # list index out of range
                    top_name = database_names[i]
                    top_score = database_scores[i]
                    database_names.remove(database_names[i])
                    database_scores.remove(database_scores[i])
                    break
            top_names.append(compile_spot(top_name, top_score))
        
        await ctx.send(f"Scoreboard:\n1. {top_names[0]}\n2. {top_names[1]}\n3. {top_names[2]}")
        return
    elif message_content_no_command:
        await ctx.send(f"Unknown gtc command: {message_content_no_command}")
        return

    splash = ":blue_circle::oncoming_police_car::red_circle:"
    await ctx.send(f"{splash} GUESS THE CHARGE {splash}")
    
    mugshot, correct_charge, charges = GuessTheCharge.main()
    await ctx.send(mugshot) # show mugshot
    for i in range(3):
        await ctx.send(f'{i+1}. {charges[i]}') # print list of charges to guess from

    await ctx.send("Please enter your guess (1-3):")

    def check(message):
        return message.author != client

    message = await client.wait_for("message", check=check)
    if message.content in ['1','2','3']: # if valid guess
        guess = int(message.content) - 1
        if charges[guess] == correct_charge:
            game_end_message= "Bail has been posted :fire: you win!"

            user = f"{str(message.author.name)}#{int(message.author.discriminator)}"
            if user in database:
                # increment score if in database
                database[user] += 1
            else:
                # add player to database
                database[user] = 1

            # write new score to scores.json
            with open('scores.json', 'w') as outfile:
                json.dump(database, outfile)
        else:
            game_end_message = f"Life without parole :skull: correct answer was: {correct_charge}"
        await ctx.send(game_end_message)
    else:
        await ctx.send("Bad guess, play again")

client.run(token)