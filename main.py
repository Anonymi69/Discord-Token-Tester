import discord
import os
import sys
import time
import threading
from colorama import init, Fore

init(autoreset=True)

ASCII_ART = [
    r"  _____  _                       _   ____        _     _______    _                _______        _            ",
    r" |  __ \(_)                     | | |  _ \      | |   |__   __|  | |              |__   __|      | |           ",
    r" | |  | |_ ___  ___ ___  _ __ __| | | |_) | ___ | |_     | | ___ | | _____ _ __      | | ___  ___| |_ ___ _ __ ",
    r" | |  | | / __|/ __/ _ \| '__/ _` | |  _ < / _ \| __|    | |/ _ \| |/ / _ \ '_ \     | |/ _ \/ __| __/ _ \ '__|",
    r" | |__| | \__ \ (_| (_) | | | (_| | | |_) | (_) | |_     | | (_) |   <  __/ | | |    | |  __/\__ \ ||  __/ |   ",
    r" |_____/|_|___/\___\___/|_|  \__,_| |____/ \___/ \__|    |_|\___/|_|\_\___|_| |_|    |_|\___||___/\__\___|_|   ",
]

ASCII_GRADIENT = [
    (255,   0,  0),
    (255,  60,  0),
    (255, 120,  0),
    (255, 180,  0),
    (255, 220,  0),
    (255, 255,  0),
]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_ascii():
    import shutil
    clear_screen()
    term_w = shutil.get_terminal_size().columns
    max_w  = max(len(line) for line in ASCII_ART)
    pad    = max((term_w - max_w) // 2, 0)
    indent = ' ' * pad
    print()
    for i, line in enumerate(ASCII_ART):
        r, g, b = ASCII_GRADIENT[i]
        print(f"\033[38;2;{r};{g};{b}m{indent}{line}\033[0m")
    print()
    ORANGE = "\033[38;2;255;140;0m"
    credit = "~ Made By GHO5T ~"
    print(Fore.GREEN + credit.center(term_w))
    print()

def animated_dots(prefix, duration=2.0):
    frames = ["   ", ".  ", ".. ", "..."]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        print(f"\r{Fore.MAGENTA}{prefix}{frames[i % len(frames)]}", end="", flush=True)
        time.sleep(0.25)
        i += 1
    print(f"\r{Fore.MAGENTA}{prefix}...   ", flush=True)

def animated_enter_prompt():
    msg = "  Press Enter To Exit"
    frames = ["   ", ".  ", ".. ", "..."]
    stop_event = threading.Event()

    def animate():
        i = 0
        while not stop_event.is_set():
            print(f"\r{Fore.MAGENTA}{msg}{frames[i % len(frames)]}", end="", flush=True)
            time.sleep(0.35)
            i += 1

    t = threading.Thread(target=animate, daemon=True)
    t.start()
    input()
    stop_event.set()
    t.join()

def main():
    print_ascii()
    time.sleep(2)

    token = input(Fore.CYAN + "  Enter your bot token: ").strip()

    if not token:
        animated_dots("  No token provided! Exiting", duration=2.0)
        sys.exit(0)

    animated_dots("  Validating", duration=4.0)

    intents = discord.Intents.default()
    client  = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(Fore.GREEN + f"\n  ✅ Logged in as {client.user}")
        await client.change_presence(
            status=discord.Status.online,
            activity=discord.Game(name="Active via Token Tester 🚀")
        )
        print(Fore.GREEN + "  Bot is now online and active.\n")

    try:
        client.run(token)
    except discord.LoginFailure:
        print(Fore.RED + "\n  ❌ Invalid token. Make sure you're using the right BOT token.")
    except discord.HTTPException as e:
        print(Fore.RED + f"\n  ❌ HTTP Error: {e}")
    except Exception as e:
        print(Fore.RED + f"\n  ⚠️  Unexpected Error: {e}")

    animated_enter_prompt()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        animated_dots("  Exiting", duration=2.0)
