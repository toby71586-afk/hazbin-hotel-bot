"""
Hazbin Hotel Welcome Bot
Every new member gets welcomed by a RANDOM character —
 Charlie, Vaggie, Angel Dust, Alastor, Cherri Bomb, Niffty, Husk, Lucifer, or Rosie.
 Channel message + personal DM in that character's voice.
 Also says goodbye when someone leaves!
"""

import os
import random
import logging

import discord

try:
    import aiohttp
except ImportError:
    aiohttp = None

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("hotel-bot")

# --- Config ------------------------------------------------------------------
TOKEN = os.environ.get("DISCORD_TOKEN", "")
WELCOME_CHANNEL_ID = int(os.environ.get("WELCOME_CHANNEL_ID", "0"))
GOODBYE_CHANNEL_ID = int(os.environ.get("GOODBYE_CHANNEL_ID", "0"))
TENOR_API_KEY = os.environ.get("TENOR_API_KEY", "")

# --- Direct media.tenor.com GIF URLs (these embed properly in Discord) -------

CHARLIE_GIFS = [
    "https://media.tenor.com/WZYh6xlxnjIAAAAM/hazbin-hazbin-hotel.gif",
    "https://media.tenor.com/DWywakh83qkAAAAM/hazbin-hotel-hazbin.gif",
    "https://media.tenor.com/A5KqiABJpFUAAAAM/hazbin-hazbin-hotel.gif",
    "https://media.tenor.com/G5VaPsqPR-IAAAAM/hazbin-hazbin-hotel.gif",
    "https://media.tenor.com/TMZKjuHNDmMAAAAM/hazbin-hazbin-hotel.gif",
    "https://media.tenor.com/uzXF-FdLEecAAAAM/puppy-eyes-charlie-morningstar.gif",
    "https://media.tenor.com/UrQNlAJ1zZwAAAAM/hazbin-hotel-charlie.gif",
    "https://media.tenor.com/wSO8p2FtJowAAAAM/hazbin-hotel-charlie-morningstar.gif",
]

VAGGIE_GIFS = [
    "https://media.tenor.com/AhzzEFzg4QwAAAAM/vaggie-worried-vaggie-hazbin-hotel.gif",
    "https://media.tenor.com/D48HH2L123wAAAAM/vaggie-smiling-vaggie-hazbin-hotel.gif",
    "https://media.tenor.com/5SlzPoFEWIoAAAAM/hazbin-hotel-hazbin-hotel-vaggie.gif",
    "https://media.tenor.com/BxI8A8ZJOkEAAAAM/charlie-vaggie.gif",
    "https://media.tenor.com/urGWaz7gev0AAAAM/vaggie-beautiful.gif",
    "https://media.tenor.com/FLqVuaGa0iQAAAAM/vaggie-hazbin-hotel.gif",
]

ANGEL_GIFS = [
    "https://media.tenor.com/FLUsqiy68ioAAAAM/hazbin-hazbin-hotel.gif",
    "https://media.tenor.com/BQftJWoWxzMAAAAM/kinky-angel-dust.gif",
    "https://media.tenor.com/ZxzQUkUT5akAAAAM/hazbin-hazbin-hotel.gif",
    "https://media.tenor.com/tXnNLySqwIkAAAAM/hazbin-hazbin-hotel.gif",
    "https://media.tenor.com/_fWAmZJgX7QAAAAM/angel-dust-hazbin-hotel.gif",
    "https://media.tenor.com/CHgbQziaFFcAAAAM/hazbin-hotel-angel-dust.gif",
]

ALASTOR_GIFS = [
    "https://media.tenor.com/WYpsGgip1RwAAAAM/hazbin-hotel-hazbin.gif",
    "https://media.tenor.com/E-3nDDRjyjQAAAAM/alastor-hazbin.gif",
    "https://media.tenor.com/3ZVBdMfc9w0AAAAM/alastor-chair.gif",
    "https://media.tenor.com/PM63FN8wq9MAAAAM/hazbin-hotel-hazbin.gif",
    "https://media.tenor.com/ukuzDFgWB_cAAAAM/alastor-lucifer.gif",
    "https://media.tenor.com/ztS73tHUB_IAAAAM/hazbin-hazbin-hote.gif",
]

CHERRI_GIFS = [
    "https://media.tenor.com/QlMW_1yRRU8AAAAM/cherri-bomb-hazbin-hotel.gif",
    "https://media.tenor.com/WapWl2DcWb8AAAAM/hazbin-hazbin-hotel.gif",
    "https://media.tenor.com/IBOPb3HZ7V8AAAAM/hazbin-hotel-cherri-bomb.gif",
    "https://media.tenor.com/0SyxAcg0iKwAAAAM/hazbin-hazbin-hotel.gif",
    "https://media.tenor.com/QP_4Eroqd9EAAAAM/cherri-bomb-cherri-bomb-hazbin-hotel.gif",
]

NIFFTY_GIFS = [
    "https://media.tenor.com/kejhRmQ3VTkAAAAM/niffty-blank-stare.gif",
    "https://media.tenor.com/-nKkghLv4EMAAAAM/niffty-nifty.gif",
    "https://media.tenor.com/aqpWvJ2e50QAAAAM/niffty-hazbin-hotel-hazbin-hotel.gif",
    "https://media.tenor.com/mobUcovPNJ4AAAAM/hazbin-hotel-hazbin.gif",
    "https://media.tenor.com/g-31xjCeoTUAAAAM/hazbin-hotel-niffty.gif",
    "https://media.tenor.com/DWYRaIOwDgQAAAAM/niffty-nifty.gif",
]

HUSK_GIFS = [
    "https://media.tenor.com/lRbYukm0XrYAAAAM/smug-hazbinhotel.gif",
    "https://media.tenor.com/9obeakKxN-IAAAAM/hazbin-hazbin-hotel.gif",
    "https://media.tenor.com/qiMLYpfW8S0AAAAM/hazbin-hazbin-hotel.gif",
    "https://media.tenor.com/8Xy4rr71tmQAAAAM/hazbin-hazbin-hotel.gif",
    "https://media.tenor.com/O3KZfjZitdIAAAAM/hazbin-hotel-hazbin.gif",
    "https://media.tenor.com/QJr6kekWEG0AAAAM/hazbin-hotel.gif",
    "https://media.tenor.com/qbxFEBEh6QsAAAAM/hazbin-hotel-husk.gif",
]

LUCIFER_GIFS = [
    "https://media.tenor.com/ZHbo5EnNg1UAAAAM/lucifer-morningstar-season-2.gif",
    "https://media.tenor.com/Ix8UaADFpuEAAAAM/devil-lucifer-morningstar.gif",
    "https://media.tenor.com/CDlIC1ziyLIAAAAM/lucifer-morningstar-season-2.gif",
    "https://media.tenor.com/WyuLfqlcFLMAAAAM/hazbin-hotel-lucifer-morningstar.gif",
    "https://media.tenor.com/epxHVqKLtU0AAAAM/lucifer-morningstar-hazbin-hotel.gif",
    "https://media.tenor.com/c856E4wDxyIAAAAM/hazbin-hotel-lucifer-morningstar.gif",
]

ROSIE_GIFS = [
    "https://media.tenor.com/D9WpXzaICNAAAAAM/hazbin-hotel.gif",
    "https://media.tenor.com/9Qv3F8dERNEAAAAM/rosie-hazbin-hotel.gif",
    "https://media.tenor.com/TuqnNa7sKEIAAAAM/alastor-and-rosie-rosie-laugh.gif",
    "https://media.tenor.com/OdExoALXruIAAAAM/rosie-smile.gif",
    "https://media.tenor.com/IMK1y7Is2lEAAAAM/rosie-hazbinhotel.gif",
    "https://media.tenor.com/YXtFkMUmYZ4AAAAM/alastor-rosie.gif",
    "https://media.tenor.com/wUfCRZ6N9lwAAAAM/rosie-rosie-hazbin-hotel.gif",
]

# --- Characters --------------------------------------------------------------

CHARACTERS = {
    "charlie": {
        "name": "Charlie Morningstar",
        "color": 0xE23B54,
        "emoji": "🏨",
        "channel_greetings": [
            "Welcome to the family, {mention}! I just KNOW you're going to fit right in. ✨",
            "{mention} is here!! Ahh, a new face — I'm so happy you made it! 🥰",
            "Everyone say hi to {mention}! This is going to be amazing, I can feel it!",
            "Yaaay, {mention} joined! Pull up a chair, make yourself at home. 🏨💛",
            "A warm welcome to {mention}! Every single person here matters — and that includes you. 💛",
        ],
        "goodbyes": [
            "Oh no… {name} is leaving. I hope you find what you're looking for out there. You'll always have a home here. 💛",
            "Goodbye for now, {name}! The door's always open — seriously, I mean it. Come back anytime. 🏨✨",
            "It hurts to see you go, {name}… but I understand. Thank you for being part of this family, even for a little while. 💔💛",
            "Sending you all my love, {name}. You're always welcome at the hotel. Always. 🏨💕",
        ],
        "dm_messages": [
            "Hey {name}! It's Charlie! I just wanted to personally say — I'm so, SO happy you're here. "
            "This place is about second chances and found family. And that means YOU now. 🏨💛",
            "Oh my gosh, hi {name}!! Welcome!! Take your time looking around — there's snacks, "
            "good music, and the best people you'll ever meet. 😄✨",
            "{name}!! This is a safe space. Be yourself, make friends, share your art — I've got your back. 💪💕",
            "Hi {name}! You belong here. Period. No earning it. No proving yourself. Welcome home! 🏨✨",
        ],
        "gifs": CHARLIE_GIFS,
        "goodbye_gifs": CHARLIE_GIFS,
        "tenor_query": "Hazbin Hotel Charlie Morningstar",
        "footer": "— Charlie Morningstar, your host at the Hazbin Hotel",
        "embed_title": "A new soul checks in! 🏨",
        "goodbye_title": "A soul moves on… 💔",
        "dm_embed_title": "A personal note from Charlie 💌",
    },

    "vaggie": {
        "name": "Vaggie",
        "color": 0x9B59B6,
        "emoji": "⚔️",
        "channel_greetings": [
            "Hey, {mention}. Charlie's been talking about you all day. Welcome to the hotel. 🤍",
            "Another new face. Good. {mention}, you're in safe hands here. 😤💜",
            "{mention} just joined. This place matters. Make yourself useful. 😌",
            "Welcome, {mention}. I'm glad you're here. You earned a spot the second you walked in.",
            "Alright everyone, {mention} is here now. Be nice to them, or you answer to me. ⚔️",
        ],
        "goodbyes": [
            "{name} left. I don't like losing people, but… I respect your choice. Stay safe out there. ⚔️💜",
            "Goodbye, {name}. You were one of the good ones. Don't let anyone tell you otherwise. 🤍",
            "If anyone gives you trouble out there, you know how to reach me. Take care of yourself, {name}. ⚔️",
        ],
        "dm_messages": [
            "Hey {name}. It's Vaggie. I know I come off intense, but I mean well. "
            "Welcome to the hotel. ⚔️💜",
            "{name} — you're part of this family now. I protect you. Don't be a stranger. 🤍",
            "Hi {name}. I'm not great at warm fuzzy stuff. But Charlie's over the moon you're here. So am I. 😤💕",
        ],
        "gifs": VAGGIE_GIFS,
        "goodbye_gifs": VAGGIE_GIFS,
        "tenor_query": "Vaggie Hazbin Hotel",
        "footer": "— Vaggie, head of security",
        "embed_title": "A new guest arrives! ⚔️",
        "goodbye_title": "A soldier departs… ⚔️",
        "dm_embed_title": "A word from Vaggie 🤍",
    },

    "angel": {
        "name": "Angel Dust",
        "color": 0xFF69B4,
        "emoji": "🕷️",
        "channel_greetings": [
            "Well well well, look who finally showed up! {mention}, you're GORGEOUS. 💅✨",
            "{mention}!! About damn time! I was getting bored. 😏🕷️",
            "Ooh la la, {mention} is here! New eye candy for the hotel. 💋",
            "Heyyy {mention}! Welcome to the only place in Hell with STYLE. 😘",
            "Another beautiful face joins the chaos. {mention}, you're gonna fit in PERFECTLY. 💕",
        ],
        "goodbyes": [
            "NOOO {name}!! Who am I gonna gossip with now?! Come back soon, babes. 💋🕷️",
            "Ugh, {name} left. I'm not crying — it's just… allergies. Yeah. Allergies. 😭💅",
            "Goodbye {name}!! You better text me. I mean it. Don't leave me hanging with these weirdos. 💕✨",
        ],
        "dm_messages": [
            "Heyyy {name}~! Angel here. Just wanted to slide into your DMs first — "
            "someone's gotta give you the REAL tour. 🕷️💋",
            "{name}!! Oh my god, fresh blood! Anyone gives you shit, I'll annoy 'em until they leave. 💅✨",
            "Hey {name}~ Quick heads up: Alastor's creepy, Husk's grumpy, but ME? I'm FUN. 💕✨",
        ],
        "gifs": ANGEL_GIFS,
        "goodbye_gifs": ANGEL_GIFS,
        "tenor_query": "Angel Dust Hazbin Hotel",
        "footer": "— Angel Dust, your favorite spider",
        "embed_title": "Look who showed up! 🕷️",
        "goodbye_title": "A star exits stage left… 🕷️",
        "dm_embed_title": "A little birdie says hi 💋",
    },

    "alastor": {
        "name": "Alastor",
        "color": 0x8B0000,
        "emoji": "📻",
        "channel_greetings": [
            "Ah, a new listener! Welcome, {mention} — do stay a while. 📻🎙️",
            "{mention}, is it? What a PLEASURE. Do try not to disappoint me. 😈",
            "Well well well! A fresh face. Do enjoy your stay, {mention}! 🎙️",
            "Greetings, {mention}! I've been expecting you. I'm the most curious character here. Obviously. 📻😊",
            "Ah, {mention} joins us! How WONDERFUL. So full of hope. It's ADORABLE. 📻😊",
        ],
        "goodbyes": [
            "Ah, {name} is leaving. What a shame. I was just beginning to find you… entertaining. 📻🎙️",
            "Goodbye, {name}. Do write if you find yourself in need of… assistance. I'm always listening. 😈📻",
            "Every show must have an exit, I suppose. Farewell, {name}. Until we meet again. 📻✨",
        ],
        "dm_messages": [
            "Good evening, {name}! Alastor here. A new soul in Charlie's hotel — how EXCITING. "
            "Do call on me if you ever need assistance. 📻🎙️",
            "{name}~! What a delight. I've been watching the hotel's family grow. Do keep things interesting. 😊📻",
            "Hellooo {name}! I don't usually bother with personal greetings, but you seem… special. Toodles! 📻✨",
        ],
        "gifs": ALASTOR_GIFS,
        "goodbye_gifs": ALASTOR_GIFS,
        "tenor_query": "Alastor Hazbin Hotel",
        "footer": "— Alastor, the Radio Demon",
        "embed_title": "A new voice on the airwaves! 📻",
        "goodbye_title": "The broadcast ends… 📻",
        "dm_embed_title": "A little broadcast just for you 🎙️",
    },

    "cherri": {
        "name": "Cherri Bomb",
        "color": 0xFF4500,
        "emoji": "💣",
        "channel_greetings": [
            "YOOO {mention}!! Welcome to the party!! 💣🔥",
            "AYYY {mention}!! New friend alert! Let's blow this place up! 😈💥",
            "{mention} just rolled in! HELL yeah! 💣✨",
            "Another badass joins the crew! {mention}, no refunds! 💥💕",
            "EVERYONE SHUT UP — {mention} is here!! 💣🔥",
        ],
        "goodbyes": [
            "WHAT {name} is leaving?! This party just got LAMER. Come back soon, yeah?! 💣💥",
            "Goodbye {name}!! You're always welcome back. And by welcome, I mean I'll literally drag you back myself. 🔥💕",
            "NOOO {name}!! Who's gonna blow stuff up with me now?! You better visit! 💣😭",
        ],
        "dm_messages": [
            "OI {name}!! Cherri here! Welcome to the best damn hotel in Hell. "
            "Forget redemption — we're here for chaos. You in? 💣💥",
            "{name}!! HELL yeah! Stick with me and you'll have stories to tell. Welcome, babes! 💣✨",
            "Heyyy {name}!! I got your back. Anyone messes with you? BOOM. Problem solved. 💥💜",
        ],
        "gifs": CHERRI_GIFS,
        "goodbye_gifs": CHERRI_GIFS,
        "tenor_query": "Cherri Bomb Hazbin Hotel",
        "footer": "— Cherri Bomb, chaos agent",
        "embed_title": "INCOMING!! New arrival! 💣",
        "goodbye_title": "An explosion fades… 💥",
        "dm_embed_title": "A little hello from Cherri 💥",
    },

    "niffty": {
        "name": "Niffty",
        "color": 0xFF1493,
        "emoji": "🧹",
        "channel_greetings": [
            "AHHH A NEW PERSON!! {mention}!! HI HI HI!! 😍🧹",
            "{mention}!! New friend new friend!! I'M GONNA CLEAN YOUR SHOES!! 💕✨",
            "OH MY GOSH {mention} you're HERE!! BEST DAY EVER!! 😃🧹",
            "NEW PERSON ALERT!! {mention}!! I'm Niffty!! WELCOME WELCOME WELCOME!! 💖✨",
            "{mention}!!!!! You're so COOL!! 😍🧹💕",
        ],
        "goodbyes": [
            "NOOO {name} left!! Who's gonna let me clean their stuff now?! COME BACK!! 😭🧹",
            "Goodbye {name}!! I already cleaned your spot for when you come back!! It's PERFECT!! 💕✨",
            "{name}!! Leaving?? But I was gonna organize your WHOLE LIFE!! 😭😭😭🧹",
        ],
        "dm_messages": [
            "HIII {name}!! Niffty here! I already cleaned your spot. It's PERFECT now. "
            "Need anything cleaned? I'm YOUR GIRL!! 🧹💕✨",
            "{name}!! I'm the smallest but the FASTEST so I saw you first! Let's be BEST FRIENDS!! 💖✨",
            "{name}!! Do you like STABBY THINGS?? Because I have SO MANY!! 🧹😍💕",
        ],
        "gifs": NIFFTY_GIFS,
        "goodbye_gifs": NIFFTY_GIFS,
        "tenor_query": "Niffty Hazbin Hotel",
        "footer": "— Niffty, tiny chaotic housekeeper",
        "embed_title": "NEW FRIEND SPOTTED!! 🧹",
        "goodbye_title": "A tiny heart breaks… 💔",
        "dm_embed_title": "A VERY excited welcome 💖",
    },

    "husk": {
        "name": "Husk",
        "color": 0xDAA520,
        "emoji": "🍺",
        "channel_greetings": [
            "Great. Another one. Welcome, {mention}. Don't touch my booze. 🍺😮‍💨",
            "{mention} joined. That's cool, I guess. 🤷‍♂️🍺",
            "Hey {mention}. Welcome. Don't be an idiot. You're welcome. 🍺",
            "{mention} is here. Alright. Stay out of trouble and we'll get along. 😼🍺",
        ],
        "goodbyes": [
            "{name} left. Damn. Who's gonna listen to my bad advice now? Take care of yourself. 🍺😮‍💨",
            "Goodbye, {name}. If you ever need a drink, you know where to find me. First one's on me. For real this time. 🍺😼",
            "Another one gone. {name}, you were alright. Stay safe out there. 🍺",
        ],
        "dm_messages": [
            "Hey {name}. It's Husk. First drink's on me. Don't get used to it. 🍺😼",
            "{name}. Husk. You'll be fine here. Probably. If not, the booze helps. 🍺",
            "Hey. {name}. This place grows on you. Like a fungus. Or whiskey. Welcome. 🍺✨",
        ],
        "gifs": HUSK_GIFS,
        "goodbye_gifs": HUSK_GIFS,
        "tenor_query": "Husk Hazbin Hotel",
        "footer": "— Husk, the grumpy bartender",
        "embed_title": "Great. Another guest. 🍺",
        "goodbye_title": "Another tab closed… 🍺",
        "dm_embed_title": "A message from the bar 🍺",
    },

    "lucifer": {
        "name": "Lucifer Morningstar",
        "color": 0xFFD700,
        "emoji": "👑",
        "channel_greetings": [
            "Ah, {mention}! A new guest at my daughter's hotel! THE King welcomes you! 🍎👑",
            "{mention}!! Welcome! Charlie's been telling me all about you! 😈✨",
            "Ohoho! {mention} arrives! The King of Hell welcomes you personally! 🍎👑",
            "HELLO {mention}! Lucifer here! Don't let the title intimidate you — I'm a DAD first! 💛✨",
            "{mention}! This hotel is MAGNIFICENT and YOU are part of it! 🍎😈",
        ],
        "goodbyes": [
            "Wait, {name} is leaving?! But I just got here! …Okay, kidding. Mostly. Farewell, my friend. 👑✨",
            "Goodbye, {name}! If Hell gets boring, you know where to find me. …Okay that was a threat and an invitation. 😈💛",
            "Ah, {name} moves on. Every king must let his subjects go. But you'll always have a place in my kingdom. 🍎👑",
        ],
        "dm_messages": [
            "HELLO {name}!! Lucifer here! Welcome to Charlie's hotel. Welcome to the family! 🍎👑✨",
            "{name}! I don't do this for everyone, but you seem special. Welcome! 😈💛",
            "Ahh, {name}! What a DELIGHT. People who take chances on each other change the world. Welcome to the revolution! 🍎👑✨",
        ],
        "gifs": LUCIFER_GIFS,
        "goodbye_gifs": LUCIFER_GIFS,
        "tenor_query": "Lucifer Hazbin Hotel",
        "footer": "— Lucifer Morningstar, King of Hell",
        "embed_title": "Royal arrival! 👑",
        "goodbye_title": "A royal farewell… 👑",
        "dm_embed_title": "A message from the King 🍎",
    },

    "rosie": {
        "name": "Rosie",
        "color": 0xE91E63,
        "emoji": "🩰",
        "channel_greetings": [
            "Oh my, {mention}! A fresh face! How DELIGHTFUL. 🩰✨",
            "{mention}, darling! Welcome! The Cannibal Colony sets an extra place! 😘",
            "Well, well, WELL. {mention}! We're going to be GREAT friends! 🩰💕",
            "A new guest! {mention}, I'm Rosie. Best dinner parties in Hell. You're invited. 🍽️✨",
            "Hello, {mention}! This hotel is full of fascinating people — and now YOU'RE one of them! 🩰😘",
        ],
        "goodbyes": [
            "{name} is leaving?! But I had the GOOD CHINA ready! You come back now, you hear? 🩰😘",
            "Goodbye, {name} darling. The Cannibal Colony will always have a seat for you at the table. 🍽️💕",
            "Oh, {name}… leaving so soon? Well, do write. I do so love keeping in touch with my favorite guests. 🩰✨",
        ],
        "dm_messages": [
            "Well HELLO {name}! Rosie here! This hotel is MAGNIFICENT and you're part of it now. "
            "Welcome to the family! 🩰💕✨",
            "{name}, sweetheart! You're SPECIAL. I can always tell. Do visit the Colony sometime! 😘🩰",
            "Darling {name}! Consider yourself an honorary colonist. Tea, cake, and… other things. You'll LOVE it. 🩰✨💕",
        ],
        "gifs": ROSIE_GIFS,
        "goodbye_gifs": ROSIE_GIFS,
        "tenor_query": "Rosie Hazbin Hotel",
        "footer": "— Rosie, Overlord of the Cannibal Colony",
        "embed_title": "A new guest for the Colony! 🩰",
        "goodbye_title": "A seat at the table empties… 🍽️",
        "dm_embed_title": "A personal invitation from Rosie 💕",
    },
}


async def fetch_tenor_gif(query: str) -> str | None:
    if not TENOR_API_KEY or aiohttp is None:
        return None
    url = "https://tenor.googleapis.com/v2/search"
    params = {
        "q": query,
        "key": TENOR_API_KEY,
        "limit": 20,
        "media_filter": "gif",
        "contentfilter": "medium",
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=10) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
                results = data.get("results", [])
                if not results:
                    return None
                pick = random.choice(results)
                return pick["media_formats"]["gif"]["url"]
    except Exception as exc:
        log.warning("Tenor fetch failed, using fallback: %s", exc)
        return None


intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    log.info("Hotel is online as %s", client.user)


@client.event
async def on_member_join(member: discord.Member):
    char = random.choice(list(CHARACTERS.values()))
    log.info("%s is welcoming %s", char["name"], member.name)

    channel = None
    if WELCOME_CHANNEL_ID:
        channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
    if channel is None:
        channel = member.guild.system_channel

    if channel is not None:
        greeting = random.choice(char["channel_greetings"]).format(mention=member.mention)
        gif = await fetch_tenor_gif(char["tenor_query"]) or random.choice(char["gifs"])

        embed = discord.Embed(
            title=char["embed_title"],
            description=greeting,
            color=char["color"],
        )
        embed.set_image(url=gif)
        embed.set_footer(text=char["footer"])

        await channel.send(content=member.mention, embed=embed)

    try:
        dm_text = random.choice(char["dm_messages"]).format(name=member.display_name)
        dm_gif = await fetch_tenor_gif(char["tenor_query"]) or random.choice(char["gifs"])

        dm_embed = discord.Embed(
            title=char["dm_embed_title"],
            description=dm_text,
            color=char["color"],
        )
        dm_embed.set_image(url=dm_gif)
        dm_embed.set_footer(text=char["footer"])

        await member.send(content="", embed=dm_embed)
        log.info("DM sent to %s from %s", member.name, char["name"])
    except discord.Forbidden:
        log.info("Couldn't DM %s (DMs closed)", member.name)
    except Exception as exc:
        log.warning("Failed to DM %s: %s", member.name, exc)


@client.event
async def on_member_remove(member: discord.Member):
    char = random.choice(list(CHARACTERS.values()))
    log.info("%s is saying goodbye to %s", char["name"], member.name)

    channel = None
    if GOODBYE_CHANNEL_ID:
        channel = member.guild.get_channel(GOODBYE_CHANNEL_ID)
    if channel is None and WELCOME_CHANNEL_ID:
        channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
    if channel is None:
        channel = member.guild.system_channel

    if channel is not None:
        goodbye_text = random.choice(char["goodbyes"]).format(name=member.display_name)
        gif = random.choice(char["goodbye_gifs"])

        embed = discord.Embed(
            title=char["goodbye_title"],
            description=goodbye_text,
            color=char["color"],
        )
        embed.set_image(url=gif)
        embed.set_footer(text=char["footer"])

        await channel.send(embed=embed)
        log.info("Goodbye sent for %s from %s", member.name, char["name"])


client.run(TOKEN)