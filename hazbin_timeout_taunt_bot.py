import discord
import asyncio
import random
import os
from datetime import datetime, timezone

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
MOD_CHANNEL_ID = int(os.getenv("MOD_CHANNEL_ID", "0"))

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)

timed_out_users = set()

TAUNTS = {
    "Charlie": {
        "color": 0xCC0000,
        "dms": [
            "Oh honey, I believe everyone deserves redemption... but you're really testing my faith right now!",
            "I know you can be better than this! The timeout is for your own good!",
            "Every soul can be saved! Even yours! ...Even if you are in timeout.",
            "The hotel is about second chances. You're on... like, your fifth one.",
            "'Im sure whatever you did, we can work through it! After your timeout."
        ],
        "mod_messages": [
            "Oh my ... looks like someone's in the naughty corner!",
            "I believe they can change! ...Eventually.",
            "This is a learning experience! For everyone!",
            "Every setback is a setup for a comeback!"
        ]
    },
    "Vaggie": {
        "color": 0x9B59B6,
        "dms": [
            "You're in timeout. Deal with it. Or do you want to make this worse?",
            "I've killed angels. You think I won't put you in timeout again?",
            "Rules exist for a reason. You broke them. Here we are.",
            "Don't test me. I'm already in a bad mood.",
            "The timeout is the least of your problems if you keep acting up."
        ],
        "mod_messages": [
            "Told you they'd end up here. Pathetic.",
            "One more incident and it's permanent.",
            "Look who finally got what was coming to them.",
            "I've been watching them. This was inevitable."
        ]
    },
    "Angel Dust": {
        "color": 0xFF69B4,
        "dms": [
            "Ooh, someone's in trou-ble! What'd you do, steal my look?",
            "Timeout? In THIS economy? Girl, I feel you.",
            "Don't worry, baby, I've been in way worse situations. Like, WAY worse.",
            "Aww, look at you all grounded and stuff. Kinda cute.",
            "If you're gonna be in timeout, at least make it entertaining!"
        ],
        "mod_messages": [
            "HA! Get rekt!",
            "Not so tough now, are ya?",
            "I've been there. It's boring as hell. Literally.",
            "Can I join? A promise to behave. ...Mostly."
        ]
    },
    "Alastor": {
        "color": 0x8B0000,
        "dms": [
            "How DELIGHTFUL! A little bird in a cage! This is wonderful entertainment!",
            "I do so ejoy watching sinners face consequences. It's almost musical!",
            "Don't worry, my dear. The radio waves carry even the loneliest of voices!",
            "I could get you out of timeout... for a price. But where's the fun in that?",
            "Rules are such fascinating constructs, aren't they?!Especially when you break them!"
        ],
        "mod_messages": [
            "STATIC! The sweet sound of justice!",
            "I could listen to their excuses all day! HAHAHA!",
            "This is the best show in Hell!",
            "Oh, this never gets old! The look on their face!"
        ]
    },
    "Husk": {
        "color": 0xFFA500,
        "dms": [
            "Heh. Sucks to be you. Get a drink when you're out. I'll pour.",
            "You know what I did when I got put in timeout? I passed out. Try it.",
            "Timeout's not so bad. Gives you time to think about your bad decisions.",
            "Welcome to the club. We have jackets. And existential dread.",
            "I've been in timeout for decades. You'll survive... probably."
        ],
        "mod_messages": [
            "Another one for the timeout club. Great.",
            "I give it an hour before they start whining.",
            "At least the bar's quiet while they're gone.",
            "Been there. It's boring. That's the point."
        ]
    },
    "Vox": {
        "color": 0x00BFFF, 
        "dms": [
            "Look at you! All mutted! How does that feel? I'd broadcast it if I were you.",
            "Alastor thinks he's funny. YOU're in timeout. Who's laughing now?",
            "I control the screens in Hell. You're not on any of them. How sad.",
            "You're trending for all the wrong reasons, pal.",
            "If you were on my network, I'd give you your own show: 'Consequences with [Your Name]'"
        ],
        "mod_messages": [
            "Caught on camera! Again!",
            "This one's a repeat offender. I love the consistency!",
            "Can we get a live feed of their timeout? For ratings?",
            "I'd put this on the news if anyone cared!"
        ]
    },
    "Valentino": {
        "color": 0x8B008B,
        "dms": [
            "Darling, you're ALL mine now. Well, for the duration of your timeout.",
            "Contracts don't have timeout clauses. But you do! How cute.",
            "I could make this timeout... disappear. For a price.",
            "You look so helpless. I love it.",
            "When you get out, we're signing a contract. No exceptions."
        ],
        "mod_messages": [
            "Theyd look good in my studio after this.",
            "I could use someone with their... attitude.",
            "Breaking rules is just a talent waiting to be exploited!",
            "I love watching them squirm."
        ]
    },
    "Cherri Bomb": {
        "color": 0xFF4500,
        "dms": [
            "TIMEOUT?!! That's nothing! I once got banned from THREE rings of Hell!",
            "Rules are meant to be broken, baby! ...But maybe not right now.",
            "When you get out, let's blow something up. It'll make you feel better!",
            "Don't let the man keep you down! ...Even if the man is technically right.",
            "I'd help you escape but honestly? You probably deserved it."
        ],
        "mod_messages": [
            "BOOM! Right in the consequences!",
            "They'll be back. They always come back.",
            "I've done way worse and never got caught. Amateurs.",
            "This is why I don't follow rules!"
        ]
    },
    "Lucifer": {
        "color": 0xFFD700,
        "dms": [
            "I literally fell from Heaven and I'm STILL more put together than you right now.",
            "Timeout? I invented consequences. You're welcome.",
            "You know who else got in trouble? Me. For giving humanity knowledge. Perspective!",
            "Ducks don't get put in timeout. Just saying.",
            "I could end your timeout with a snap. But I won't. Character building!"
        ],
        "mod_messages": [
            "I've seen this before. Trust me, it doesn't end well.",
            "They remind me of myself. That's... not a compliment.",
            "The apple doesn't fall far from the tree. And I'm the original apple.",
            "I've been dealing with troublemakers for millennia. This is nothing."
        ]
    }
}

CHARACTER_NAMES = list(TAUNTS.keys())

@client.event
async def on_ready():
    print(f"Timeout Taunt Bot is ready! Logged in as {client.user}")
    print(f"Mod channel ID: {MOD_CHANNEL_ID}")

@client.event
async def on_member_update(before, after):
    if before.timed_out_until != after.timed_out_until:
        if after.timed_out_until is not None:
            timed_out_users.add(after.id)
            print(f"{after.name} was timed out until {after.timed_out_until}")
        else:
            timed_out_users.discard(after.id)
            print(f"{after.name} was un-timed out")

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.author.id in timed_out_users:
        char_name = random.choice(CHARACTER_NAMES)
        char = TAUNTS[char_name]
        dm_taunt = random.choice(char["dms"])
        try:
            embed_dm = discord.Embed(
                title=f"ϔ⍓ {char_name} has a message for you!",
                description=f"*{\"}{}{ dm_taunt }\"}*",
                color=char["color"]
            )
            embed_dm.set_footer(text=f"ÌΌ {char_name} - Hazbin Hotel Timeout Taunts")
            await message.author.send(embed=embed_dm)
        except discord.Forbidden:
            print(f"Couldn't DM {message.author.name} - DS closed")
        if MOD_CHANNEL_ID:
            mod_channel = client.get_channel(MOD_CHANNEL_ID)
            if mod_channel:
                mod_taunt = random.choice(char["mod_messages"])
                embed_mod = discord.Embed(
                    title=f❣� {message.author.name} is in timeout and tried to speak!",
                    description=f"**They said:** {message.content}\n\n**{char_name} says:** *\"{}{} {mod_taunt} {\'}\*",
                    color=char["color"]
                )
                embed_mod.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
                embed_mod.set_footer(text=f"Ü⌠ {char_name} — Timeout Taunt  {message.author.id}")
                await mod_channel.send(embed=embed_mod)

client.run(DISCORD_TOKEN)
