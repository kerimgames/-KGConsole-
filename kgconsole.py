import os
os.system("title KGConsole v1.0")


import os  
import webbrowser
import getpass
import shutil

# ------------------ AYARLAR ------------------
VERSION = "1.0"
START_DIR = os.path.join(os.path.expanduser("~"), "Desktop")
ALIASES = {}
HISTORY = []
CONFIRM_DELETE = True

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

/sistem
history
!N                   → geçmişten çalıştır
alias k=komut
unalias k
whoami
about
clear
exit

/internet
http:site.com
https:site.com
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

        print("Bilinmeyen komut")

    except Exception as e:
        print("Hata:", e)
