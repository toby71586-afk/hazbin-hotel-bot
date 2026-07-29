"""
Hazbin Hotel Welcome Bot
Every new member gets welcomed by a RANDOM character from the hotel —
Charlie, Vaggie, Angel Dust, Alastor, Cherri Bomb, Niffty, Husk, Lucifer, or Rosie.
Channel message + personal DM in that character's voice.
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
TENOR_API_KEY = os.environ.get("TENOR_API_KEY", "")

# --- Fallback GIFs -----------------------------------------------------------

CHARLIE_GIFS = [
    "https://tenor.com/view/hazbin-hotel-charlie-morningstar-happy-excited-gif-25547896",
    "https://tenor.com/view/charlie-morningstar-hazbin-hotel-smile-gif-25392011",
    "https://tenor.com/view/hazbin-hotel-charlie-happy-cheer-gif-26421783",
    "https://tenor.com/view/charlie-morningstar-hazbin-hotel-excited-gif-27009845",
]

VAGGIE_GIFS = [
    "https://tenor.com/view/vaggie-hazbin-hotel-gif-21149320",
    "https://tenor.com/view/hazbin-hotel-vaggie-gif-25547887",
    "https://tenor.com/view/vaggie-hazbin-hotel-smile-gif-27009848",
    "https://tenor.com/view/vaggie-hazbin-hotel-happy-gif-26421789",
]

ANGEL_GIFS = [
    "https://tenor.com/view/angel-dust-hazbin-hotel-gif-21149322",
    "https://tenor.com/view/angel-dust-hazbin-hotel-gif-25547891",
    "https://tenor.com/view/angel-dust-hazbin-hotel-dance-gif-26421791",
    "https://tenor.com/view/angel-dust-hazbin-hotel-flirt-gif-27009850",
]

ALASTOR_GIFS = [
    "https://tenor.com/view/alastor-hazbin-hotel-gif-21149321",
    "https://tenor.com/view/alastor-hazbin-hotel-radio-demon-gif-25547892",
    "https://tenor.com/view/alastor-hazbin-hotel-smile-gif-26421790",
    "https://tenor.com/view/alastor-hazbin-hotel-laugh-gif-27009849",
]

CHERRI_GIFS = [
    "https://tenor.com/view/cherri-bomb-hazbin-hotel-gif-25547893",
    "https://tenor.com/view/cherri-bomb-hazbin-hotel-explosion-gif-26421792",
    "https://tenor.com/view/cherri-bomb-hazbin-hotel-party-gif-27009846",
]

NIFFTY_GIFS = [
    "https://tenor.com/view/niffty-hazbin-hotel-gif-25547894",
    "https://tenor.com/view/niffty-hazbin-hotel-clean-gif-26421788",
    "https://tenor.com/view/niffty-hazbin-hotel-hyper-gif-27009847",
]

HUSK_GIFS = [
    "https://tenor.com/view/husk-hazbin-hotel-gif-25547895",
    "https://tenor.com/view/husk-hazbin-hotel-cat-gif-26421786",
    "https://tenor.com/view/husk-hazbin-hotel-grumpy-gif-27009844",
]

LUCIFER_GIFS = [
    "https://tenor.com/view/lucifer-hazbin-hotel-gif-25547897",
    "https://tenor.com/view/lucifer-hazbin-hotel-king-of-hell-gif-26421785",
    "https://tenor.com/view/lucifer-hazbin-hotel-dad-gif-27009843",
]

ROSIE_GIFS = [
    "https://tenor.com/view/rosie-hazbin-hotel-gif-27123456",
    "https://tenor.com/view/rosie-hazbin-hotel-cannibal-colony-gif-27123457",
    "https://tenor.com/view/rosie-hazbin-hotel-elegant-gif-27123458",
    "https://tenor.com/view/rosie-hazbin-hotel-queen-gif-27123459",
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
            "Yaaay, {mention} joined! Pull up a chair, make yourself at home. We're so glad you're here!",
            "A warm welcome to {mention}! Every single person here matters — and that includes you. 💛",
        ],
        "dm_messages": [
            "Hey {name}! It's Charlie! I just wanted to personally say — I'm so, SO happy you're here. "
            "This place is about second chances and found family. And that means YOU now. If you ever "
            "need someone to talk to, I'm always around. Welcome home. 🏨💛",

            "Oh my gosh, hi {name}!! Welcome welcome welcome!! I've been so excited for you to get here. "
            "Take your time looking around — there's snacks, good music, and the best people you'll ever "
            "meet. Seriously. I'm not biased at all. 😄✨",

            "{name}!! Ahhh it's so good to see you! I know joining a new place can feel a little scary, "
            "but I promise — this is a safe space. Be yourself, make friends, share your art, whatever "
            "you love. I've got your back. Always. 💪💕",

            "Hi {name}! Charlie here! 💫 I just wanted to reach out and say you're already part of the "
            "family the second you joined. No earning it. No proving yourself. You belong here. Period. "
            "Can't wait to see you around the hotel! 🏨✨",
        ],
        "gifs": CHARLIE_GIFS,
        "tenor_query": "Hazbin Hotel Charlie Morningstar happy",
        "footer": "— Charlie Morningstar, your host at the Hazbin Hotel",
        "embed_title": "A new soul checks in! 🏨",
        "dm_embed_title": "A personal note from Charlie 💌",
    },

    "vaggie": {
        "name": "Vaggie",
        "color": 0x9B59B6,
        "emoji": "⚔️",
        "channel_greetings": [
            "Hey, {mention}. Charlie's been talking about you all day. Welcome to the hotel. 🤍",
            "Another new face. Good. {mention}, you're in safe hands here — and I'll make sure it stays that way.",
            "{mention} just joined. Listen — this place matters. Charlie built it for people like you. Don't waste it. 😤💜",
            "Welcome, {mention}. I don't say this to everyone, but… I'm glad you're here. You earned a spot the second you walked in.",
            "Alright everyone, {mention} is here now. Be nice to them, or you answer to me. Consider yourself welcomed. 😌",
        ],
        "dm_messages": [
            "Hey {name}. It's Vaggie. I know I can come off a little intense, but… I mean well. "
            "Charlie believes in everyone who walks through those doors, and so do I. If anyone "
            "gives you trouble, you come to me. Got it? Welcome to the hotel. ⚔️💜",

            "{name} — Vaggie here. Quick and straight: you're part of this family now. "
            "Charlie's vision is real, and I protect it with everything I've got. That means "
            "I protect YOU too. Don't be a stranger. 🤍",

            "Hi {name}. Look, I'm not great at the whole… warm fuzzy thing. But Charlie's "
            "over the moon you're here, and honestly? So am I. This place works because of "
            "people like you. Welcome to the team. 😤💕",

            "{name}. Vaggie. I keep an eye on everyone in this hotel — in a good way. "
            "You need something, I'm here. You need space, I'll guard it. Just… be good "
            "to each other, alright? Welcome. ⚔️✨",
        ],
        "gifs": VAGGIE_GIFS,
        "tenor_query": "Vaggie Hazbin Hotel happy smile",
        "footer": "— Vaggie, head of security at the Hazbin Hotel",
        "embed_title": "A new guest arrives! ⚔️",
        "dm_embed_title": "A word from Vaggie 🤍",
    },

    "angel": {
        "name": "Angel Dust",
        "color": 0xFF69B4,
        "emoji": "🕷️",
        "channel_greetings": [
            "Well well well, look who finally showed up! {mention}, you're GORGEOUS. Welcome to the party. 💅✨",
            "{mention}!! About damn time! I was getting bored. You better be fun. 😏🕷️",
            "Ooh la la, {mention} is here! New eye candy for the hotel. Don't worry baby, I'll show you around. 💋",
            "Heyyy {mention}! Welcome to the Hazbin Hotel — the only place in Hell with STYLE. And that's me, mostly. 😘",
            "Another beautiful face joins the chaos. {mention}, you're gonna fit in PERFECTLY. Trust me, I know these things. 💕",
        ],
        "dm_messages": [
            "Heyyy {name}~! Angel Dust here. Just wanted to slide into your DMs first — "
            "someone's gotta give you the REAL tour of this place, and it sure as hell ain't Vaggie. 😏 "
            "You need gossip? protection? a drinking buddy? I'm your spider. Welcome to the hotel, babes. 🕷️💋",

            "{name}!! Oh my god, fresh blood! I mean — fresh FACE. Look, this place can be a lot, "
            "but you got me in your corner. Anyone gives you shit, you tell me and I'll make 'em "
            "regret it. Or at least annoy them until they leave. Either way. Welcome! 💅✨",

            "Hey {name}~ Angel here. Quick heads up: Alastor's creepy, Husk's grumpy, Niffty's… "
            "a lot. But ME? I'm FUN. Stick with me and you'll have a good time. Don't be a stranger, "
            "I don't bite unless you ask me to. 😘🕷️",

            "{name} babes! Just wanted to say I'm SO glad you're here. This hotel's actually "
            "growing on me — and I'm picky as hell. You being here? Already an upgrade. "
            "Come find me when you wanna actually have fun. 💕✨",
        ],
        "gifs": ANGEL_GIFS,
        "tenor_query": "Angel Dust Hazbin Hotel happy dance",
        "footer": "— Angel Dust, your favorite resident spider",
        "embed_title": "Look who decided to show up! 🕷️",
        "dm_embed_title": "A little birdie (spider?) says hi 💋",
    },

    "alastor": {
        "name": "Alastor",
        "color": 0x8B0000,
        "emoji": "📻",
        "channel_greetings": [
            "Ah, a new listener joins the broadcast! Welcome, {mention} — do stay a while. The reception here is… delightful. 📻🎙️",
            "{mention}, is it? What a PLEASURE to make your acquaintance. I do hope you'll find the entertainment to your liking. 😈",
            "Well well well! A fresh face for the hotel's little… experiment. Do try not to disappoint me, {mention}. I so dislike disappointment. 📻✨",
            "Greetings, {mention}! I've been expecting you. The hotel is full of curious characters — and I am, of course, the most curious of them all. Do enjoy your stay! 🎙️",
            "Ah, {mention} joins us! How WONDERFUL. I do so love meeting new people. They're always so… full of hope. It's ADORABLE. 📻😊",
        ],
        "dm_messages": [
            "Good evening, {name}! Alastor here, speaking to you through the miracle of modern technology. "
            "I must say, I've taken an interest in you. A new soul in Charlie's little hotel — how EXCITING. "
            "Do feel free to call on me if you ever need… assistance. I'm always happy to help. 📻🎙️",

            "{name}~! What a delight to have you here. I've been watching the hotel's little family grow, "
            "and I must say — you're a FINE addition to the collection. Do keep things interesting, won't you? "
            "I do so adore a good show. 😊📻",

            "Helloooo {name}! Alastor here, your friendly neighborhood radio demon. "
            "I don't usually bother with personal greetings, but you seem… special. "
            "Let's just say I'll be keeping an ear out for you. Stay out of trouble — "
            "or don't. Either way, it'll be entertaining for ME. 🎙️😈",

            "My dear {name}! What a pleasure to make your proper acquaintance. "
            "This hotel is full of delightful chaos, and I'm at the center of it all. "
            "If you ever want a proper tour — the REAL tour — you know where to find me. "
            "Toodles! 📻✨",
        ],
        "gifs": ALASTOR_GIFS,
        "tenor_query": "Alastor Hazbin Hotel radio demon smile",
        "footer": "— Alastor, the Radio Demon",
        "embed_title": "A new voice on the airwaves! 📻",
        "dm_embed_title": "A little broadcast just for you 🎙️",
    },

    "cherri": {
        "name": "Cherri Bomb",
        "color": 0xFF4500,
        "emoji": "💣",
        "channel_greetings": [
            "YOOO {mention}!! Welcome to the party!! Things are about to get EXPLOSIVE with you here! 💣🔥",
            "AYYY {mention}!! New friend alert! Don't be shy, let's blow this place up — metaphorically. Mostly. 😈💥",
            "{mention} just rolled in! HELL yeah! You look like you know how to have a good time. Let's GO! 💣✨",
            "Another badass joins the crew! {mention}, you're officially part of the chaos now. No refunds! 💥💕",
            "EVERYONE SHUT UP — {mention} is here!! Party's officially started. Welcome to the hotel, you beautiful disaster! 💣🔥",
        ],
        "dm_messages": [
            "OI {name}!! Cherri Bomb here! Just wanted to be the first to officially welcome you "
            "to the best damn hotel in Hell. Forget the redemption crap — we're here for the good "
            "times, the chaos, and the explosions. You in? Because I already like you. 💣💥",

            "{name}!! HELL yeah you made it! Listen — this place has a lot of rules and a lot of "
            "weirdos, but me? I'm simple. I like fun, I like fire, and I like people who don't "
            "take themselves too seriously. You seem cool. Let's cause some trouble. 🔥💕",

            "AYYY {name}! Cherri here. Quick rundown: Charlie's a sweetheart, Vaggie's a buzzkill, "
            "Angel's my bestie, Alastor's creepy as hell, and I'm the one who makes things "
            "interesting. Stick with me and you'll have stories to tell. Welcome to the hotel, babes! 💣✨",

            "Heyyy {name}!! Just wanted to say I'm stoked you're here. This place is actually "
            "kinda growing on me — and I don't say that about much. You're part of the crew now. "
            "That means I got your back. And if anyone messes with you? BOOM. Problem solved. 💥💜",
        ],
        "gifs": CHERRI_GIFS,
        "tenor_query": "Cherri Bomb Hazbin Hotel party explosion",
        "footer": "— Cherri Bomb, professional chaos agent",
        "embed_title": "INCOMING!! New arrival! 💣",
        "dm_embed_title": "A little hello from Cherri 💥",
    },

    "niffty": {
        "name": "Niffty",
        "color": 0xFF1493,
        "emoji": "🧹",
        "channel_greetings": [
            "AHHH A NEW PERSON!! {mention}!! HI HI HI I'M SO EXCITED!! Do you need anything cleaned?? 😍🧹",
            "{mention}!! {mention}!! {mention}!! New friend new friend new friend!! I'M GONNA CLEAN YOUR SHOES!! 💕✨",
            "OH MY GOSH {mention} you're HERE!! This is the BEST DAY EVER!! Do you like tiny things?? I LOVE tiny things!! 😃🧹",
            "NEW PERSON ALERT!! {mention}!! I'm Niffty!! I'm small and fast and I clean EVERYTHING!! WELCOME WELCOME WELCOME!! 💖✨",
            "{mention}!!!!! I saw you from across the lobby and I RAN here because I HAD to say hi!! You're so COOL!! 😍🧹💕",
        ],
        "dm_messages": [
            "HIII {name}!! It's Niffty!! I'm so SO so SO happy you're here!! "
            "I already cleaned your spot — don't worry, it's PERFECT now. "
            "If you ever need anything cleaned, organized, or stabbed a little bit, "
            "I'm YOUR GIRL!! Welcome welcome welcome!! 🧹💕✨",

            "{name}!! {name}!! {name}!! I keep saying your name because I like how it sounds!! "
            "This hotel is the BEST place and now YOU'RE here and everything is PERFECT!! "
            "Do you have any messes?? I LOVE messes!! Not in a bad way!! In a CLEANING way!! 😍🧹",

            "HELLO {name}!! Niffty here!! I'm the smallest but I'm the FASTEST so I saw you first!! "
            "This place is FULL of weirdos but they're GOOD weirdos. Especially me. "
            "I'm the BEST weirdo. Welcome to the hotel!! Let's be BEST FRIENDS!! 💖✨",

            "{name}!!!! I have a QUESTION for you!! Do you like STABBY THINGS?? "
            "Because I have SO MANY stabby things and I can show you ALL of them!! "
            "This is going to be the BEST friendship EVER!! Welcome welcome WELCOME!! 🧹😍💕",
        ],
        "gifs": NIFFTY_GIFS,
        "tenor_query": "Niffty Hazbin Hotel hyper cleaning",
        "footer": "— Niffty, the hotel's tiny chaotic housekeeper",
        "embed_title": "NEW FRIEND SPOTTED!! 🧹",
        "dm_embed_title": "A VERY excited welcome from Niffty 💖",
    },

    "husk": {
        "name": "Husk",
        "color": 0xDAA520,
        "emoji": "🍺",
        "channel_greetings": [
            "Great. Another one. Welcome, {mention}. Try not to make my job harder than it already is. 🍺😮‍💨",
            "{mention} joined. Yeah. That's cool. I guess. Don't touch my booze. 🤷‍♂️🍺",
            "Hey {mention}. I'm Husk. I tend bar. I listen to problems. I don't care about most of 'em. But uh… welcome anyway.",
            "Ugh, fine — {mention} is here. Welcome. Charlie's gonna make me give you a speech, so here it is: don't be an idiot. You're welcome. 🍺",
            "{mention}, huh. Alright. You seem alright. Stay out of trouble and we'll get along just fine. Probably. 😼🍺",
        ],
        "dm_messages": [
            "Hey {name}. It's Husk. Look, I'm not big on the whole 'welcome wagon' thing, "
            "but Charlie'd kill me if I didn't at least say something. So here: you're here, "
            "that's fine, don't cause too much trouble, and if you need a drink — first one's on me. "
            "Don't get used to it. 🍺😼",

            "{name}. Husk. I tend the bar, I play cards, I mind my own business. "
            "But I've been around long enough to know when someone's gonna fit in. "
            "And you? You'll be fine. Probably. If not, the booze helps. Welcome. 🍺",

            "Hey. {name}. I know this place seems like a lot — it is. Charlie's optimism, "
            "Vaggie's intensity, Angel's… everything. But it grows on you. "
            "Like a fungus. Or a good whiskey. Either way. Welcome to the hotel. 🍺✨",

            "{name}. Husk here. Quick and simple: this place is a circus, but it's OUR circus. "
            "You're part of it now. That means you got people who'll actually have your back, "
            "which is more than most folks in Hell can say. Don't waste it. Now get outta my DMs. 😼🍺",
        ],
        "gifs": HUSK_GIFS,
        "tenor_query": "Husk Hazbin Hotel grumpy bartender",
        "footer": "— Husk, the hotel's grumpy bartender",
        "embed_title": "Great. Another guest. 🍺",
        "dm_embed_title": "A message from the bar 🍺",
    },

    "lucifer": {
        "name": "Lucifer Morningstar",
        "color": 0xFFD700,
        "emoji": "👑",
        "channel_greetings": [
            "Ah, {mention}! A new guest at my daughter's delightful little hotel. Welcome! I do hope you enjoy your stay — the apples here are TO DIE for. 🍎👑",
            "{mention}!! Welcome welcome! Charlie's been telling me all about you. Well, not ALL about you — I'm her father, I don't need EVERY detail. But still! Welcome! 😈✨",
            "Ohoho! {mention} arrives! The King of Hell welcomes you personally — you don't get THAT every day. Make yourself at home. I insist. 🍎👑",
            "HELLO {mention}! Lucifer Morningstar, at your service! Don't let the title intimidate you — I'm a DAD first, king second. Charlie's project is IMPORTANT and so are YOU. Welcome! 💛✨",
            "{mention}! A fresh face! This hotel is going to be MAGNIFICENT, I can feel it. And YOU are part of that. How exciting! Don't you agree? Of course you do! 🍎😈",
        ],
        "dm_messages": [
            "HELLO {name}!! Lucifer here — the big guy himself! I just wanted to personally "
            "welcome you to Charlie's hotel. You know, when she first told me about this place, "
            "I thought she was CRAZY. But she's MY daughter, and I've learned that crazy "
            "is just another word for BRILLIANT. Welcome to the family! 🍎👑✨",

            "{name}! Lucifer Morningstar. I don't do this for everyone — actually, I don't do "
            "this for ANYONE. But you seem special. Charlie's got good instincts, and if SHE "
            "believes in you, then so do I. Also, between us? I'm her favorite parent. "
            "Don't tell Lilith I said that. Welcome to the hotel! 😈💛",

            "Ahh, {name}! What a DELIGHT to have you here. You know, I've been around for "
            "a VERY long time — since the beginning, actually — and I've learned one thing: "
            "people who take chances on each other? They're the ones who change the world. "
            "Or in this case, Hell. Welcome to the revolution. 🍎👑✨",

            "{name}!! Your new favorite king here! Just wanted to say I'm THRILLED you're "
            "part of this whole thing. This hotel is going to be LEGENDARY — mark my words. "
            "And you get to be here for it from the start! How COOL is that?? "
            "If you ever need a favor from the top… you know where to find me. 😈💛🍎",
        ],
        "gifs": LUCIFER_GIFS,
        "tenor_query": "Lucifer Hazbin Hotel king of hell",
        "footer": "— Lucifer Morningstar, King of Hell (and proud dad)",
        "embed_title": "Royal arrival! 👑",
        "dm_embed_title": "A message from the King himself 🍎",
    },

    "rosie": {
        "name": "Rosie",
        "color": 0xE91E63,
        "emoji": "🩰",
        "channel_greetings": [
            "Oh my, {mention}! A fresh face in the colony! How DELIGHTFUL. Do come in, I insist. We have SO much to discuss. 🩰✨",
            "{mention}, darling! Welcome, welcome! I do hope you're hungry — the Cannibal Colony always sets an extra place for new friends. Don't be shy! 😘",
            "Well, well, WELL. Look who's arrived! {mention}, you have the most WONDERFUL energy. I can already tell we're going to be GREAT friends. 🩰💕",
            "A new guest! {mention}, I'm Rosie. I run things in the Cannibal Colony — which means I run the BEST dinner parties in Hell. You're invited, of course. 🍽️✨",
            "Hello, {mention}! Rosie here. I've heard SUCH lovely things about you. This hotel is full of fascinating people, and now YOU'RE one of them. How EXCITING! 🩰😘",
        ],
        "dm_messages": [
            "Well HELLO there, {name}! Rosie here, Overlord of the Cannibal Colony and "
            "Charlie's dearest friend. I just HAD to reach out and welcome you personally. "
            "This hotel is going to be MAGNIFICENT — and you're part of it now, darling. "
            "If you ever want a proper meal, a bit of gossip, or just some ELEGANT company… "
            "you know where to find me. Welcome to the family! 🩰💕✨",

            "{name}, sweetheart! Rosie speaking. I have to say — I have an EXCELLENT eye "
            "for people, and you? You're SPECIAL. I can always tell. This place is full of "
            "misfits and miracles, and you fit RIGHT in. Do come visit the Colony sometime — "
            "I'll have the good china out. And the good… well, you'll see. 😘🩰",

            "Darling {name}! Rosie here, just popping in to say I'm THRILLED you've joined us. "
            "The Cannibal Colony doesn't welcome just ANYONE, you know — but Charlie's hotel "
            "guests are always an exception. Consider yourself an honorary colonist. "
            "We'll have TEA. And cake. And… other things. You'll LOVE it. 🩰✨💕",

            "Hellooo {name}~! Rosie at your service. Or rather, at your PLEASURE. "
            "I do so love meeting new people — especially ones with that certain… spark. "
            "And you have it, darling. I can always tell. Welcome to the Hazbin Hotel — "
            "the most FASCINATING place in all of Hell. Don't be a stranger now! 🩰😘✨",
        ],
        "gifs": ROSIE_GIFS,
        "tenor_query": "Rosie Hazbin Hotel cannibal colony elegant",
        "footer": "— Rosie, Overlord of the Cannibal Colony",
        "embed_title": "A new guest for the Colony! 🩰",
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


def _gif_image_url(gif: str) -> str:
    return gif if gif.lower().endswith(".gif") else discord.Embed.Empty


intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    log.info("Hotel is online as %s", client.user)


@client.event
async def on_member_join(member: discord.Member):
    # Pick a RANDOM character to welcome them
    char = random.choice(list(CHARACTERS.values()))
    log.info("%s is welcoming %s", char["name"], member.name)

    # --- 1. Channel welcome -------------------------------------------------
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
        embed.set_image(url=_gif_image_url(gif))
        embed.set_footer(text=char["footer"])

        await channel.send(content=member.mention, embed=embed)
        if gif.startswith("https://tenor.com/view/"):
            await channel.send(gif)

    # --- 2. DM welcome ------------------------------------------------------
    try:
        dm_text = random.choice(char["dm_messages"]).format(name=member.display_name)
        dm_gif = await fetch_tenor_gif(char["tenor_query"]) or random.choice(char["gifs"])

        dm_embed = discord.Embed(
            title=char["dm_embed_title"],
            description=dm_text,
            color=char["color"],
        )
        dm_embed.set_image(url=_gif_image_url(dm_gif))
        dm_embed.set_footer(text=char["footer"])

        await member.send(content="", embed=dm_embed)
        if dm_gif.startswith("https://tenor.com/view/"):
            await member.send(dm_gif)

        log.info("DM sent to %s from %s", member.name, char["name"])
    except discord.Forbidden:
        log.info("Couldn't DM %s (DMs closed)", member.name)
    except Exception as exc:
        log.warning("Failed to DM %s: %s", member.name, exc)


client.run(TOKEN)


# =============================================================================
# README
# =============================================================================
#
# 1. Go to https://discord.com/developers/applications -> New Application
# 2. Bot tab -> Add Bot -> Enable "Server Members Intent" -> Copy token
# 3. OAuth2 -> URL Generator -> scope: bot
#    Permissions: Send Messages, Embed Links, Read Message History
# 4. Open the URL, add bot to your server
# 5. pip install -U discord.py aiohttp
# 6. Set your token:
#    export DISCORD_TOKEN="your-bot-token"
#    export WELCOME_CHANNEL_ID="1234567890"   # optional
#    export TENOR_API_KEY="your-tenor-key"    # optional
# 7. python charlie_welcome_bot.py
# =============================================================================
