import os
import json
import time
import random
import datetime
import shutil
import subprocess
import webbrowser
import getpass
import calendar
import requests

# ================== AYARLAR ==================
VERSION = "3.0"
START_DIR = os.path.join(os.path.expanduser("~"), "Desktop")
START_TIME = time.time()
HISTORY = []
ALIASES = {}
NOTES = []

AI_KEYS_FILE = "ai_keys.json"

AI_PROVIDERS = {
    "1": {
        "name": "ChatGPT",
        "model": "gpt-4o-mini",
        "url": "https://api.openai.com/v1/chat/completions"
    },
    "2": {
        "name": "Gemini",
        "model": "gemini-pro",
        "url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    },
    "3": {
        "name": "Grok",
        "model": "grok-beta",
        "url": "https://api.x.ai/v1/chat/completions"
    }
}

# ================== BAŞLAT ==================
os.system("cls")
os.system("color 0a")
os.system("title KGConsole v3.0")

current_dir = START_DIR

if not os.path.exists(AI_KEYS_FILE):
    with open(AI_KEYS_FILE, "w") as f:
        json.dump({}, f)

# ================== YARDIM ==================
HELP_TEXT = """
/help                yardım
clear                ekranı temizle
exit                 çıkış

cd / ls / pwd / tree
add / cat / edit / del
mkdir / rmdir / rename
copy / move / find / grep

history / alias / unalias
time / date / uptime / disk
rand / passgen / calc

weather şehir
translate tr-en metin
http(s)://site

game guess | rps
joke | quote | roll | flip
note add/list/del

ai      🤖 yapay zeka menüsü
"""

# ================== YARDIMCI ==================
def load_ai_keys():
    with open(AI_KEYS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_ai_keys(keys):
    with open(AI_KEYS_FILE, "w", encoding="utf-8") as f:
        json.dump(keys, f, indent=2)

def show_tree(path, lvl=0):
    try:
        for item in os.listdir(path):
            full = os.path.join(path, item)
            print("  " * lvl + "|-- " + item)
            if os.path.isdir(full):
                show_tree(full, lvl + 1)
    except:
        pass

# ================== AI CHAT ==================
def ai_chat(choice):
    keys = load_ai_keys()
    provider = AI_PROVIDERS[choice]
    name = provider["name"]

    if name not in keys:
        keys[name] = input(f"{name} API key: ").strip()
        save_ai_keys(keys)

    api_key = keys[name]
    messages = []

    print(f"🤖 {name} başladı (exit çıkış)")

    while True:
        user = input("AI > ")
        if user.lower() == "exit":
            break

        messages.append({"role": "user", "content": user})

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": provider["model"],
            "messages": messages,
            "temperature": 0.7
        }

        try:
            r = requests.post(provider["url"], headers=headers, json=data)
            reply = r.json()["choices"][0]["message"]["content"]
        except:
            print("❌ AI hatası")
            continue

        print(f"{name} >", reply)
        messages.append({"role": "assistant", "content": reply})

        # DOSYA ALGILAMA
        fname = None
        l = user.lower()
        if "python" in l:
            fname = "code.py"
        elif "javascript" in l:
            fname = "script.js"
        elif "html" in l:
            fname = "index.html"
        elif "txt" in l:
            fname = "note.txt"

        if fname:
            with open(os.path.join(current_dir, fname), "w", encoding="utf-8") as f:
                f.write(reply)
            print(f"📁 {fname} oluşturuldu")

# ================== ANA ==================
print(f"KGConsole v{VERSION} 🐱   (/help)")

while True:
    try:
        cmd = input(f"{current_dir}> ").strip()
        if not cmd:
            continue

        HISTORY.append(cmd)

        if cmd == "/help":
            print(HELP_TEXT)
            continue

        if cmd == "exit":
            break

        if cmd == "clear":
            os.system("cls")
            continue

        # ---- AI ----
        if cmd == "ai":
            print("""
1) ChatGPT
2) Gemini
3) Grok
""")
            c = input("Seçim: ").strip()
            if c in AI_PROVIDERS:
                ai_chat(c)
            else:
                print("Geçersiz seçim")
            continue

        # ---- DİZİN ----
        if cmd == "pwd":
            print(current_dir)
            continue

        if cmd.startswith("cd "):
            p = cmd[3:].strip('"')
            if os.path.isdir(p):
                current_dir = p
            else:
                print("Klasör yok")
            continue

        if cmd == "ls":
            for i in os.listdir(current_dir):
                print(i)
            continue

        if cmd == "tree":
            show_tree(current_dir)
            continue

        # ---- DOSYA ----
        if cmd.startswith("add "):
            open(os.path.join(current_dir, cmd[4:]), "w").close()
            print("Dosya oluşturuldu")
            continue

        if cmd.startswith("cat "):
            path = os.path.join(current_dir, cmd[4:])
            if os.path.exists(path):
                print(open(path, "r", encoding="utf-8").read())
            continue

        if cmd.startswith("edit "):
            path = os.path.join(current_dir, cmd[5:])
            print(":q çıkış")
            with open(path, "a", encoding="utf-8") as f:
                while True:
                    l = input()
                    if l == ":q":
                        break
                    f.write(l + "\n")
            continue

        if cmd.startswith("del "):
            os.remove(os.path.join(current_dir, cmd[4:]))
            print("Silindi")
            continue

        if cmd.startswith("mkdir "):
            os.makedirs(os.path.join(current_dir, cmd[6:]), exist_ok=True)
            continue

        # ---- SİSTEM ----
        if cmd == "time":
            print(datetime.datetime.now().strftime("%H:%M:%S"))
            continue

        if cmd == "date":
            print(datetime.date.today())
            continue

        if cmd == "uptime":
            print(int(time.time() - START_TIME), "sn")
            continue

        if cmd == "joke":
            print(random.choice([
                "Python yılan değildir.",
                "Kod çalışıyorsa dokunma.",
                "Bug var çünkü hayat zor."
            ]))
            continue

        print("Bilinmeyen komut")

    except Exception as e:
        print("Hata:", e)
