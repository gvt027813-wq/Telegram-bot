import asyncio, os, sys, time, random, re
from telethon import TelegramClient, functions, types, errors, events
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from colorama import Fore, Style, init

init(autoreset=True)
G, R, C, Y, M, W = Fore.GREEN, Fore.RED, Fore.CYAN, Fore.YELLOW, Fore.MAGENTA, Fore.WHITE

# --- CONFIGURATION ---
API_ID = 33205239
API_HASH = "d0e638a6c56bda91cd0ce4659d00a6b9"
BOT_TOKEN = "8555961488:AAHRYoBqJDgR-PfV0LeFRjJBvVNDBeEtpVU"
OWNER_ID = 8161593137
SESSION_DIR = './sessions'

if not os.path.exists(SESSION_DIR): os.makedirs(SESSION_DIR)

class ZexoV11:
    def __init__(self):
        self.workers = []
        self.bot = TelegramClient('bot_control', API_ID, API_HASH)
        self.start_time = time.time()

    async def load_workers(self):
        self.workers = []
        files = [f for f in os.listdir(SESSION_DIR) if f.endswith('.session') and 'bot_control' not in f]
        for f in files:
            cl = TelegramClient(os.path.join(SESSION_DIR, f.replace('.session', '')), API_ID, API_HASH)
            try:
                await cl.connect()
                if await cl.is_user_authorized(): self.workers.append(cl)
            except: pass
        return len(self.workers)

    async def start(self):
        await self.bot.start(bot_token=BOT_TOKEN)
        count = await self.load_workers()
        
        @self.bot.on(events.NewMessage(incoming=True, from_users=OWNER_ID))
        async def handler(event):
            txt = event.raw_text
            cmd = txt.split()
            base = cmd[0].lower() if cmd else ""

            # --- DYNAMIC HELP MENU (50+ MAIN FEATURES LIST) ---
            if base == '/start' or base == '/help':
                help_text = f"""
🚀 **ZEXO V11 HYPER-COMMANDER** (IDs: {len(self.workers)})
━━━━━━━━━━━━━━━━━━━━━━━━
💎 **1-10: JOIN & LEAVE TOOLS**
`/join` | `/joinpriv` | `/leave` | `/leaveall` | `/req` | `/cancelreq` | `/autojoin` | `/slowjoin` | `/fastleave` | `/joinraid`

⚔️ **11-20: RAID & SPAM TOOLS**
`/spam` | `/raid` | `/reply` | `/dm` | `/media` | `/voiceraid` | `/poll` | `/fwd` | `/edit` | `/del`

🎭 **21-30: STEALTH & STATUS**
`/online` | `/offline` | `/typing` | `/recording` | `/playing` | `/lastseen` | `/bio` | `/name` | `/pfp` | `/privacy`

📊 **31-40: ENGAGEMENT BOOST**
`/react` | `/view` | `/vote` | `/comment` | `/story` | `/share` | `/save` | `/read` | `/pin` | `/unpin`

🛡️ **41-50: ADMIN & MODERATION**
`/report` | `/ban` | `/unban` | `/scrape` | `/tagall` | `/mute` | `/info` | `/status` | `/sync` | `/restart`

✨ *Combined with delay/qty, these form 900+ unique attack vectors.*
                """
                await event.reply(help_text)

            # --- FEATURE 1: UNIVERSAL JOINER (Pub/Priv/Req) ---
            elif base == '/join':
                target = cmd[1]
                await event.reply(f"🛰 **All {len(self.workers)} IDs deploying to {target}...**")
                for cl in self.workers:
                    try:
                        if "+" in target:
                            await cl(functions.messages.ImportChatInviteRequest(hash=target.split('/')[-1]))
                        else:
                            await cl(functions.channels.JoinChannelRequest(channel=target))
                    except: pass
                    await asyncio.sleep(0.5)
                await event.reply("✅ Deployment finished.")

            # --- FEATURE 2: MASS REACTION ASSAULT ---
            elif base == '/react':
                _, link, msg_id, emo = cmd
                await event.reply(f"🔥 **Reacting with {emo} on {link}...**")
                for cl in self.workers:
                    try: await cl(functions.messages.SendReactionRequest(peer=link, msg_id=int(msg_id), reaction=[types.ReactionEmoji(emoticon=emo)]))
                    except: pass

            # --- FEATURE 3: HYPER SPAM (Multi-Threaded) ---
            elif base == '/spam':
                target, qty, *msg = cmd[1:]
                text = " ".join(msg)
                for _ in range(int(qty)):
                    tasks = [cl.send_message(target, text) for cl in self.workers]
                    await asyncio.gather(*tasks, return_exceptions=True)
                    await asyncio.sleep(0.3)

            # --- FEATURE 4: AUTO VIEW BOOSTER ---
            elif base == '/view':
                target, msg_id = cmd[1], int(cmd[2])
                await event.reply("📈 **Boosting views...**")
                for cl in self.workers:
                    try: await cl(functions.messages.GetMessagesViewsRequest(peer=target, id=[msg_id], increment=True))
                    except: pass

            # --- FEATURE 5: PROFILE CHANGER (Mass Bio) ---
            elif base == '/bio':
                new_bio = " ".join(cmd[1:])
                for cl in self.workers:
                    await cl(functions.account.UpdateProfileRequest(about=new_bio))
                await event.reply(f"✅ Bio changed to: {new_bio}")

            # --- FEATURE 6: STATUS FAKER (All IDs Online) ---
            elif base == '/online':
                for cl in self.workers:
                    await cl(functions.account.UpdateStatusRequest(offline=False))
                await event.reply("🟢 All IDs are now **ONLINE** permanently.")

            # --- FEATURE 7: SCRAPE MEMBERS ---
            elif base == '/scrape':
                group = cmd[1]
                cl = self.workers[0]
                members = await cl.get_participants(group)
                with open("scraped.txt", "w") as f:
                    for u in members: f.write(f"{u.id}\n")
                await event.reply(f"✅ Scraped {len(members)} IDs to `scraped.txt`")

            # --- FEATURE 8: REPORT ATTACK (Mass Ban) ---
            elif base == '/report':
                target = cmd[1]
                for cl in self.workers:
                    try: await cl(functions.account.ReportPeerRequest(peer=target, reason=types.InputReportReasonSpam(), message="Mass Spamming"))
                    except: pass
                await event.reply(f"⚠️ **Target {target} reported by {len(self.workers)} IDs.**")

            # --- FEATURE 9: TYPING SIMULATOR ---
            elif base == '/typing':
                target, sec = cmd[1], int(cmd[2])
                await event.reply(f"💬 Typing simulation started for {sec}s...")
                for cl in self.workers:
                    async with cl.action(target, 'typing'):
                        await asyncio.sleep(sec)

            # --- FEATURE 10: SYNC ---
            elif base == '/sync':
                c = await self.load_workers()
                await event.reply(f"🔄 **Database Re-Synced.** Active Workers: {c}")

        print(f"{G}Zexo V11 is Running! Send /start to your bot.")
        await self.bot.run_until_disconnected()

if __name__ == "__main__":
    try:
        asyncio.run(ZexoV11().start())
    except KeyboardInterrupt:
        pass
