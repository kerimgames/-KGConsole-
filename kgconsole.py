import os
os.system("title KGConsole v2.0")


import os  
import webbrowser
import getpass
import shutil
import time
import random
import datetime
import subprocess
import calendar
import winsound

# ------------------ AYARLAR ------------------
VERSION = "2.0"
START_DIR = os.path.join(os.path.expanduser("~"), "Desktop")
START_TIME = time.time()
ALIASES = {}
HISTORY = []
CONFIRM_DELETE = True
NOTES = []

# ------------------ RENK ------------------
os.system("color 0a")

# ------------------ YARDIM ------------------
HELP_TEXT = """
/help                 → yardım
/search kelime        → internette ara
/color XY             → renk değiştir (ör: 0a, 0c)

/dosya & klasör
cd YOL
pwd
ls
tree
add dosya.txt
cat dosya.txt
edit dosya.txt
del dosya.txt
mkdir klasör
rmdir klasör
rename eski yeni
copy kaynak hedef
move kaynak hedef
find dosya
grep kelime dosya

/sistem
history
!N                   → geçmişten çalıştır
alias k=komut
unalias k
whoami
about
clear
exit
time
date
uptime
disk
rand [min] [max]
passgen [uzunluk]
calc ifade
ip
ping host

/oyunlar & eğlence
game guess
game rps
joke
quote
roll
flip
timer saniye
stopwatch
beep
fortune
calendar

/notlar
note add metin
note list
note del N

/internet
http:site.com
https:site.com
weather şehir
translate tr-en metin
"""

# ------------------ FONKSİYONLAR ------------------
def show_tree(path, level=0):
    try:
        for item in os.listdir(path):
            full = os.path.join(path, item)
            print("  " * level + "|-- " + item)
            if os.path.isdir(full):
                show_tree(full, level + 1)
    except PermissionError:
        print("  " * level + "|-- [Erişim yok]")

def calculate(expr):
    try:
        return eval(expr)
    except:
        return "Hesaplama hatası"

def generate_password(length=8):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))

def play_guess():
    number = random.randint(1, 100)
    attempts = 0
    while True:
        guess = input("Tahmin et (1-100): ")
        try:
            guess = int(guess)
            attempts += 1
            if guess < number:
                print("Daha büyük")
            elif guess > number:
                print("Daha küçük")
            else:
                print(f"Doğru! {attempts} denemede")
                break
        except:
            print("Geçersiz sayı")

def play_rps():
    choices = ['taş', 'kağıt', 'makas']
    user = input("Seç (taş/kağıt/makas): ").lower()
    comp = random.choice(choices)
    print(f"Bilgisayar: {comp}")
    if user == comp:
        print("Berabere")
    elif (user == 'taş' and comp == 'makas') or (user == 'kağıt' and comp == 'taş') or (user == 'makas' and comp == 'kağıt'):
        print("Kazandın")
    else:
        print("Kaybettin")

def get_weather(city):
    weathers = ["Güneşli", "Yağmurlu", "Bulutlu", "Karlı"]
    return f"{city}: {random.choice(weathers)}, {random.randint(0,30)}°C"

def translate(lang, text):
    if lang == "tr-en":
        return f"Translated: {text.upper()}"
    return "Desteklenmiyor"

def get_joke():
    jokes = ["Neden tavuk karşıya geçti? Karşı tarafa ulaşmak için!", "Bilgisayarlar neden soğuktur? Klimaları yoktur!", "Python nedir? Yılan değil, programlama dili!"]
    return random.choice(jokes)

def get_quote():
    quotes = ["Hayat güzeldir.", "Kod yazmak sanattır.", "Öğrenmek bitmez.", "Yaratıcılık sonsuzdur."]
    return random.choice(quotes)

def roll_dice():
    return random.randint(1, 6)

def flip_coin():
    return "Yazı" if random.choice([True, False]) else "Tura"

def get_ip():
    try:
        result = subprocess.run(["ipconfig"], capture_output=True, text=True, shell=True)
        for line in result.stdout.split('\n'):
            if "IPv4 Address" in line:
                return line.split(':')[1].strip()
        return "Bulunamadı"
    except:
        return "Hata"

def ping(host):
    try:
        result = subprocess.run(["ping", "-n", "1", host], capture_output=True, text=True, shell=True)
        if "Reply from" in result.stdout:
            return "Ping başarılı"
        else:
            return "Ping başarısız"
    except:
        return "Hata"

def play_beep():
    winsound.Beep(1000, 500)

def get_fortune():
    fortunes = ["Bugün şanslısın.", "Dikkatli ol.", "Yeni fırsatlar gelecek.", "Macera seni bekliyor.", "Sakin ol ve düşün."]
    return random.choice(fortunes)

# ------------------ ANA ------------------
current_dir = START_DIR
print(f"KGConsole v{VERSION} 🐱  (/help yaz)")

while True:
    try:
        cmd = input(f"{current_dir}> ").strip()
        if not cmd:
            continue

        HISTORY.append(cmd)

        # alias çöz
        base = cmd.split()[0]
        if base in ALIASES:
            cmd = ALIASES[base] + cmd[len(base):]

        # geçmişten çalıştır
        if cmd.startswith("!"):
            idx = int(cmd[1:]) - 1
            if 0 <= idx < len(HISTORY):
                cmd = HISTORY[idx]
            else:
                print("Geçersiz numara")
                continue

        # ----- SLASH KOMUTLAR -----
        if cmd == "/help":
            print(HELP_TEXT)
            continue

        if cmd.startswith("/search "):
            q = cmd[8:].replace(" ", "+")
            webbrowser.open(f"https://www.google.com/search?q={q}")
            print("🔍 Arama açıldı")
            continue

        if cmd.startswith("/color "):
            code = cmd.split()[1]
            if len(code) == 2:
                os.system(f"color {code}")
            else:
                print("Örnek: /color 0a")
            continue

        # ----- ÇIKIŞ -----
        if cmd == "exit":
            break

        if cmd == "clear":
            os.system("cls")
            continue

        # ----- SİSTEM -----
        if cmd == "whoami":
            print(getpass.getuser())
            continue

        if cmd == "about":
            print(f"KGConsole v{VERSION} | Python mini terminal")
            continue

        if cmd == "history":
            for i, h in enumerate(HISTORY, 1):
                print(f"{i}: {h}")
            continue

        if cmd.startswith("alias "):
            name, real = cmd[6:].split("=", 1)
            ALIASES[name.strip()] = real.strip()
            print("Alias eklendi")
            continue

        if cmd.startswith("unalias "):
            ALIASES.pop(cmd.split()[1], None)
            print("Alias silindi")
            continue

        # ----- DİZİN -----
        if cmd == "pwd":
            print(current_dir)
            continue

        if cmd.startswith("cd "):
            path = cmd[3:].strip('"')
            if os.path.isdir(path):
                current_dir = path
            else:
                print("Klasör yok")
            continue

        if cmd == "ls":
            for item in os.listdir(current_dir):
                full = os.path.join(current_dir, item)
                print("[DIR]" if os.path.isdir(full) else "     ", item)
            continue

        if cmd == "tree":
            show_tree(current_dir)
            continue

        # ----- DOSYA -----
        if cmd.startswith("add "):
            open(os.path.join(current_dir, cmd[4:]), "w", encoding="utf-8").close()
            print("Dosya oluşturuldu")
            continue

        if cmd.startswith("cat "):
            path = os.path.join(current_dir, cmd[4:])
            if os.path.exists(path):
                print(open(path, "r", encoding="utf-8").read())
            else:
                print("Dosya yok")
            continue

        if cmd.startswith("edit "):
            path = os.path.join(current_dir, cmd[5:])
            print("Düzenleme modu (:q çıkış)")
            with open(path, "a", encoding="utf-8") as f:
                while True:
                    line = input()
                    if line == ":q":
                        break
                    f.write(line + "\n")
            continue

        if cmd.startswith("del "):
            path = os.path.join(current_dir, cmd[4:])
            if os.path.exists(path):
                if not CONFIRM_DELETE or input("Silinsin mi? (e/h): ").lower() == "e":
                    os.remove(path)
                    print("Silindi")
            else:
                print("Dosya yok")
            continue

        if cmd.startswith("mkdir "):
            os.makedirs(os.path.join(current_dir, cmd[6:]), exist_ok=True)
            print("Klasör oluşturuldu")
            continue

        if cmd.startswith("rmdir "):
            try:
                os.rmdir(os.path.join(current_dir, cmd[6:]))
                print("Klasör silindi")
            except:
                print("Klasör boş değil / hata")
            continue

        if cmd.startswith("rename "):
            _, old, new = cmd.split(maxsplit=2)
            os.rename(os.path.join(current_dir, old), os.path.join(current_dir, new))
            print("Yeniden adlandırıldı")
            continue

        # ----- İNTERNET -----
        if cmd.startswith("http:") or cmd.startswith("https:"):
            webbrowser.open(cmd)
            continue

        # ----- YENİ KOMUTLAR -----
        if cmd == "time":
            print(datetime.datetime.now().strftime("%H:%M:%S"))
            continue

        if cmd == "date":
            print(datetime.date.today())
            continue

        if cmd == "uptime":
            elapsed = time.time() - START_TIME
            print(f"Çalışma süresi: {int(elapsed // 3600)}s {int((elapsed % 3600) // 60)}d {int(elapsed % 60)}sn")
            continue

        if cmd == "disk":
            stat = shutil.disk_usage(current_dir)
            print(f"Toplam: {stat.total // (1024**3)}GB, Kullanılan: {stat.used // (1024**3)}GB, Boş: {stat.free // (1024**3)}GB")
            continue

        if cmd.startswith("rand"):
            parts = cmd.split()
            min_v = int(parts[1]) if len(parts) > 1 else 1
            max_v = int(parts[2]) if len(parts) > 2 else 100
            print(random.randint(min_v, max_v))
            continue

        if cmd.startswith("passgen"):
            length = int(cmd.split()[1]) if len(cmd.split()) > 1 else 8
            print(generate_password(length))
            continue

        if cmd.startswith("calc"):
            expr = cmd[5:]
            print(calculate(expr))
            continue

        if cmd.startswith("game"):
            game = cmd[5:].strip()
            if game == "guess":
                play_guess()
            elif game == "rps":
                play_rps()
            else:
                print("Oyun: guess veya rps")
            continue

        if cmd.startswith("note"):
            parts = cmd.split(maxsplit=2)
            if len(parts) < 2:
                print("Kullanım: note add/list/del")
                continue
            action = parts[1]
            if action == "add" and len(parts) > 2:
                NOTES.append(parts[2])
                print("Not eklendi")
            elif action == "list":
                for i, n in enumerate(NOTES, 1):
                    print(f"{i}: {n}")
            elif action == "del" and len(parts) > 2:
                idx = int(parts[2]) - 1
                if 0 <= idx < len(NOTES):
                    NOTES.pop(idx)
                    print("Not silindi")
                else:
                    print("Geçersiz numara")
            continue

        if cmd.startswith("weather"):
            city = cmd[8:].strip()
            print(get_weather(city))
            continue

        if cmd.startswith("translate"):
            parts = cmd.split(maxsplit=2)
            if len(parts) > 2:
                lang, text = parts[1], parts[2]
                print(translate(lang, text))
            else:
                print("Kullanım: translate tr-en metin")
            continue

        # ----- GENİŞLETİLMİŞ DOSYA -----
        if cmd.startswith("copy"):
            parts = cmd.split(maxsplit=2)
            if len(parts) > 2:
                src = os.path.join(current_dir, parts[1])
                dst = os.path.join(current_dir, parts[2])
                shutil.copy(src, dst)
                print("Kopyalandı")
            continue

        if cmd.startswith("move"):
            parts = cmd.split(maxsplit=2)
            if len(parts) > 2:
                src = os.path.join(current_dir, parts[1])
                dst = os.path.join(current_dir, parts[2])
                shutil.move(src, dst)
                print("Taşındı")
            continue

        if cmd.startswith("find"):
            name = cmd[5:].strip()
            for root, dirs, files in os.walk(current_dir):
                for f in files + dirs:
                    if name in f:
                        print(os.path.join(root, f))
            continue

        if cmd.startswith("grep"):
            parts = cmd.split(maxsplit=2)
            if len(parts) > 2:
                word, file = parts[1], parts[2]
                path = os.path.join(current_dir, file)
                if os.path.exists(path):
                    with open(path, 'r', encoding='utf-8') as f:
                        for i, line in enumerate(f, 1):
                            if word in line:
                                print(f"{i}: {line.strip()}")
                else:
                    print("Dosya yok")
            continue

        # ----- EĞLENCE -----
        if cmd == "joke":
            print(get_joke())
            continue

        if cmd == "quote":
            print(get_quote())
            continue

        if cmd == "roll":
            print(f"Zar: {roll_dice()}")
            continue

        if cmd == "flip":
            print(flip_coin())
            continue

        if cmd == "ip":
            print(get_ip())
            continue

        if cmd.startswith("ping"):
            host = cmd[5:].strip()
            print(ping(host))
            continue

        if cmd.startswith("timer"):
            try:
                sec = int(cmd[6:].strip())
                print(f"{sec} saniye bekleniyor...")
                time.sleep(sec)
                print("Zaman doldu!")
            except:
                print("Geçersiz süre")
            continue

        if cmd == "stopwatch":
            input("Başlatmak için Enter'a bas...")
            start = time.time()
            input("Durdurmak için Enter'a bas...")
            elapsed = time.time() - start
            print(f"Geçen süre: {elapsed:.2f} saniye")
            continue

        if cmd == "beep":
            play_beep()
            continue

        if cmd == "fortune":
            print(get_fortune())
            continue

        if cmd == "calendar":
            print(calendar.month(datetime.date.today().year, datetime.date.today().month))
            continue

        print("Bilinmeyen komut")

    except Exception as e:
        print("Hata:", e)
