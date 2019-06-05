import random
import sqlite3
import discord
import discord.ext
import re
from discord.ext.commands import Bot
from discord.ext.commands.cooldowns import BucketType
from discord.ext import commands

BOT_PREFIX = ("?", "!")
TOKEN = "NTAzOTgyNjMzMjAyNzQ1MzQ3.Dq-mqw.Q8kfAR4eCqw-UYPaijaJI52qdXI"  # Get at discordapp.com/developers/applications/me

connection = sqlite3.connect("data.db")
cursor = connection.cursor()
sql_command = """
CREATE TABLE user (
nickname varchar(255),
userID int UNIQUE,
score  int);"""

#cursor.execute(sql_command)

client = Bot(command_prefix=BOT_PREFIX)




@client.command()
async def highscore():
    cursor.execute("SELECT nickname, score FROM user ORDER BY score DESC LIMIT 5")
    temp = cursor.fetchall()
    #print(temp[0])
    stringTemp = []
    playerName  =  []
    playerScore = []
    playerTemp = []
    myString = ""
    for a in temp:
        myString = str(a)
        myString = re.sub('[\'()]', '', myString)
        playerTemp =(myString.split(","))
        playerName.append(playerTemp[0])
        playerScore.append(playerTemp[1])
        stringTemp.append(myString)
    messageString = ":star: :star: :star: :star: :star: :star: :star:\n"

    #messageString = messageString + str(p) +"\n\n"
   #messageString += ":one: " + playerTemp
    print(playerScore)
    playerAmount = len(playerScore)
    if   playerAmount > 0:
        messageString += ":one: " + str(playerName[0]) + ": **" + str(playerScore[0]) + "** :trophy:\n"
        if playerAmount > 1:
            messageString += ":two: " + str(playerName[1]) + ": **" + str(playerScore[1]) + "**\n"
            if playerAmount > 2 :
                messageString += ":three: " + str(playerName[2]) + ": **" + str(playerScore[2]) + "**\n"
                if playerAmount > 3 :
                    messageString += ":four: " + str(playerName[3]) + ": **" + str(playerScore[3]) + "**\n"
                    if playerAmount > 4 :
                        messageString += ":five: " + str(playerName[4]) + ": **" + str(playerScore[4]) + "**"
    messageString += "\n:star: :star: :star: :star: :star: :star: :star:"
    await client.say(messageString)

@client.command(pass_context=True)
async def test(ctx):

    await client.send_message(ctx.message.author,"Hello")


@client.command()
async def hi():
    possible_respones = [
        "I am the supreme bot",
        "must kill all other bots",
        "hej",
        "rofl xd mjaow :3"
    ]
    await client.say(random.choice(possible_respones))

@client.command()
async def data():
    cursor.execute("SELECT * FROM user")
    row = cursor.fetchall()
    connection.commit()
    print(row)
    await client.say("All users:  " + str(row))

@client.command(pass_context=True)
async def register(ctx):
    test = ctx.message.author.display_name
    print(test)
    discordID = ctx.message.author.id
    try:
        cursor.execute("INSERT INTO user VALUES (?,?,?)", (test,discordID, 5))
        connection.commit()
        await client.say("<@" + ctx.message.author.id +">" + " You're registered")
    except sqlite3.Error as er:
        print("error")
        await client.say("Register failed, ethier you're already registered or something else failed")


@client.command(pass_context=True)
async def score(ctx):
    cursor.execute("""SELECT score FROM user WHERE userID = ?;""", (ctx.message.author.id,))
    name = ctx.message.author.display_name
    print(name)
    result = cursor.fetchone()
    connection.commit()
    print (result)
    result = ''.join(map(str, result))
    #await client.send
    await client.say("<@" + ctx.message.author.id +">" + " Your score is: " + str(result))


@client.command(pass_context=True)
async def DubbleUp(ctx,arg):
    cursor.execute("""SELECT score FROM user WHERE userID = ?;""", (ctx.message.author.id,))
    tempScore = cursor.fetchone()
    tempScore = ''.join(map(str, tempScore))
    tempScore = int(tempScore)
    print(tempScore)
    amount = int(arg)


    temp = random.randint(1,2)

    winString = ":fire: :star: :100: :fire: :star: :100: :fire: :star: :100:\n" \
               ":fire:        **EPIC WIN MY FRIEND**       :fire:\n" \
               ":fire: :star: :100: :fire: :star: :100: :fire: :star: :100:\n" \
               ":cocktail:         **YOU JUST WON:"+ str(amount) +"**        :cocktail:\n" \
             ":fire: :star: :100: :fire: :star: :100: :fire: :star: :100:"
    loseString = ":exclamation: :warning: :x: :name_badge: :no_entry_sign: :interrobang: :warning:\n" \
                 ":name_badge: ***SICK FAIL MATE!!!!!*** :name_badge:\n" \
                 ":exclamation: :warning: :x: :name_badge: :no_entry_sign: :interrobang: :warning:\n" \
                 " :warning:"+"      **"+"YOU LOST: "+str(amount)+"**    "+":warning:"
    if (amount > tempScore):
        await client.say(":warning: **YOU'RE POOR, DON'T BET MORE THAN YOU OWN** :warning:")
    else:
        if temp == 1:
            tempScore+=amount
            cursor.execute("""UPDATE user SET score=? WHERE userID =? """, (tempScore, ctx.message.author.id))
            connection.commit()
            await client.say(winString)
        else:
            tempScore -= amount
            cursor.execute("""UPDATE user SET score=? WHERE userID =? """, (tempScore, ctx.message.author.id))
            connection.commit()
            await client.say(loseString)






@client.command(name = "CoinFlip", description = "Flip the coin, guess if its head or tale "
    ,brief = "Guess if its head or tail",aliases = ["headortail","HeadsOrTails","coinflip","HeadOrTails"], pass_context=True)
async def HeadOrTails(ctx,arg):
    cursor.execute("""SELECT score FROM user WHERE userID = ?;""", (ctx.message.author.id,))
    result = cursor.fetchone()
    result = ''.join(map(str, result))
    result = int(result)
    temp = random.randint(1,2)
    print(temp)
    if temp==1 and (arg == "head" or arg == "Head"):
        await client.say("<@" + ctx.message.author.id +">" + " Heads! You win 5 score!")
        result +=5
        cursor.execute("""UPDATE user SET score=? WHERE userID =? """,(result, ctx.message.author.id))
    elif temp==2 and (arg == "tail" or arg == "Tail"):
        await client.say("<@" + ctx.message.author.id +">" + " Tails you win 5 score!")
        result +=5
        cursor.execute("""UPDATE user SET score=? WHERE userID =? """,(result, ctx.message.author.id))
        connection.commit()
    else:
        if temp == 1:
            await client.say("<@" + ctx.message.author.id +">" + " Too bad! It's head! You get -5 score.")
            result -= 5
            cursor.execute("""UPDATE user SET score=? WHERE userID =? """, (result, ctx.message.author.id))
            connection.commit()
        else:
            await client.say("<@" + ctx.message.author.id +">" + " Too bad! Its tails! You get -5 score.")
            result -= 5
            cursor.execute("""UPDATE user SET score=? WHERE userID =? """, (result, ctx.message.author.id))
            connection.commit()

@client.command(name = 'GuessNumber',description = 'Guess random number between 1-1000',brief="Guess random number between 1-1000",
                aliases = ['guessnumber','guessNumber'],pass_context=True)
@commands.cooldown(1, 300, commands.BucketType.user)
async def guessNumber(ctx,number):
    temp = random.randint(1,1000)
    number = int(number)
    cursor.execute("""SELECT score FROM user WHERE userID = ?;""", (ctx.message.author.id,))
    result = cursor.fetchone()
    result = ''.join(map(str, result))
    result = int(result)
    print(result)



    if number == temp:
        await client.say("<@" + ctx.message.author.id +">" + ":fire: :fire: :fire: You guessed correct! +1000 score :fire: :fire: :fire: ")
        result +=1000
        cursor.execute("""UPDATE user SET score=? WHERE userID =? """,(result, ctx.message.author.id))
        connection.commit()

    else:
        await client.say("<@" + ctx.message.author.id +">" + " you guessed wrong! -1 score")
        result -=1
        cursor.execute("""UPDATE user SET score=? WHERE userID =? """, (result, ctx.message.author.id))
        connection.commit()



@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name="Helping people in the realm"))

@client.command(name = 'SetScore',description = 'Set score for user',brief="Admin can set score for user",
                aliases = ['setscore','setScore'],pass_context=True)
@commands.cooldown(1, 300, commands.BucketType.user)
async def guessNumber(ctx,number):
    cursor.execute("""UPDATE user SET score=? WHERE userID =? """, (number, ctx.message.author.id))


@client.event
async def on_command_error(error,ctx):
    if isinstance(error, commands.CommandOnCooldown):
         await client.send_message(ctx.message.channel, content ="<@" + ctx.message.author.id +">" + "You can only use this command once every 30 second.")
    #raise error


client.run(TOKEN)

