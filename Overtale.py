import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

window = tk.Tk()
window.title("Overtale")
window.geometry("1280x720")

def clear():
    for widget in window.winfo_children():
        widget.destroy()

class Personaje:
    def __init__(self, name, hp, atk, df):
        self.name = name
        self.maxhp = hp
        self.currhp = hp
        self.attack = atk
        self.defense = df
        self.ko = False
    
    def dano(self, damage):
        self.currhp = self.currhp - damage
        
        if self.currhp <= 0:
            self.currhp = 0
            self.ko = True
    
    def recover(self):
        self.currhp = self.maxhp
        self.ko = False
    
    def estadovida(self):
        return not self.ko
    
    def separate(self):
        return Personaje(self.name, self.maxhp, self.attack, self.defense)

class Jugador:
    def __init__(self, name):
        self.name = name
        self.chosen = []
        self.team = []
        self.puntaje = 0
    
    def captura(self, character):
        if character not in self.chosen:
            character.recover()
            self.chosen.append(character)
            self.puntaje += 1
    
    def loss(self, character):
        if character in self.chosen:
            self.chosen.remove(character)
    
    def playervivos(self, chara = 0):
        if chara >= len(self.chosen):
            return False
        if self.chosen[chara].estadovida():
            return True
        
        return self.playervivos(chara + 1)
    
class Hollow:
    def __init__(self, name, characters):
        self.name = name
        self.enemies = characters

    def captura(self, character):
        if character not in self.enemies:
            character.recover()
            self.enemies.append(character)
    
    def loss(self, character):
        if character in self.enemies:
            self.enemies.remove(character)
    
    def persact(self):
        enemalive = self.persact_aux()
        
        if len(enemalive) == 0:
            return None
        else:
            return random.choice(enemalive)
    
    def persact_aux(self, i = 0, alive = None):
        if alive is None:
            alive = []

        if i >= len(self.enemies):
            return alive
        
        if self.enemies[i].estadovida():
            alive.append(self.enemies[i])
        
        return self.persact_aux(i + 1, alive)
    
    def hollowvivos(self, chara = 0):
        if chara >= len(self.enemies):
            return False
        if self.enemies[chara].estadovida():
            return True
        return self.hollowvivos(chara + 1)

def cargarpers():
    personajes = []
    archivo = open("personajes.txt", "r")
    for fila in archivo:
        atributo = fila.strip().split(",")
        name = atributo[0]
        hp = int(atributo[1])
        atk = int(atributo[2])
        df = int(atributo[3])
        chara = Personaje(name, hp, atk, df)
        personajes.append(chara)

    archivo.close()
    return personajes

def hollowtypes(personajes):
    return [
        Hollow("Ruins", [p.separate() for p in personajes[0:3]]),
        Hollow("Snowdin", [p.separate() for p in personajes[3:6]]),
        Hollow("Waterfall", [p.separate() for p in personajes[6:9]]),
        Hollow("Hotland", [p.separate() for p in personajes[9:12]]),
        Hollow("Castle", [p.separate() for p in personajes[12:15]])
    ]

def attack(atkr, dfdr):
    dmg = atkr.attack - dfdr.defense

    if dmg <= 0:
        dmg = 1

    dfdr.dano(dmg)

def enemyturn(player, hollow, chosen, currenemy):
    if currenemy is None:
        return chosen, currenemy
    
    prob = 0.3
    pos = hollow.persact_aux()

    if len(pos) <= 1:
        act = "attack"
    else:
        if random.random() < prob:
            act = "change"
        else:
            act = "attack"
    
    if act == "change":
        newen = random.choice(pos)

        if newen != currenemy:
            print(f"Hollow changes to {newen.name}")
            return chosen, newen
    
    print(f"{currenemy.name} attacks!")

    attack(currenemy, chosen)

    if not chosen.estadovida():
        player.loss(chosen)
        hollow.captura(chosen)
        chosen = pepejuana(player.team)
    
    if chosen is None:
        return chosen, currenemy
    
    return chosen, currenemy

def pepejuana(chosenlist, chara = 0):
    if chara >= len(chosenlist):
        return None
    
    if chosenlist[chara].estadovida():
        return chosenlist[chara]
    
    return pepejuana(chosenlist, chara + 1)

# PANTALLAS TKINTER
def endwindow(player):
    clear()

    tk.Label(window, text="CONGRATULATIONS!!! YOU SAVED THE STORY", font=("Arial", 20)).pack()
    tk.Label(window, text=f"Total points: {player.puntaje}", font=("Arial", 14)).pack()

    tk.Button(window, text="Go back to start", command=startwindow).pack()

def startwindow():
    clear()
    personajes = cargarpers()

    bkgnd = Image.open("images/backgrounds/start.png")
    bkgnd = bkgnd.resize((1280, 720))
    bkgnd = ImageTk.PhotoImage(bkgnd)
    bglabel = tk.Label(window, image=bkgnd)
    bglabel.image = bkgnd
    bglabel.place(x=0, y=0, relwidth = 1, relheight = 1)
    
    tk.Label(window, text="OVERTALE", font=("Arial", 28, "bold"), bg="black", fg="white").pack(pady=10)

    tk.Label(window, text="Name:", bg="black", fg="white").pack()
    name_entry = tk.Entry(window, font=("Arial", 12))
    name_entry.pack()

    avatar_var = tk.StringVar()
    avatar_var.set("")
    tk.Label(window, text="Choose avatar", font=("Arial", 14), bg="black", fg="white").pack()

    avatars = {
        "Frisk": "images/avatars/frisk.png",
        "Doggo": "images/avatars/doggo.png",
        "Temmie": "images/avatars/temmie.png"
    }

    avatarframe = tk.Frame(window, bg="black")
    avatarframe.pack(pady=10)
    
    for a, path in avatars.items():
        img = Image.open(path)
        img = img.resize((120, 120))
        img = ImageTk.PhotoImage(img)

        rb = tk.Radiobutton(
            avatarframe, text=a, image=img, compound="top",
            variable=avatar_var, value=a, bg="black",
            fg="white", selectcolor="gray"
        )
        rb.image = img
        rb.pack(side="left", padx=15)

    tk.Label(window, text="Choose 3 characters", font=("Arial", 14), bg="black", fg="white").pack()

    container = tk.Frame(window, bg="black")
    container.pack(pady=10)

    canvas = tk.Canvas(container, bg="black", highlightthickness=0, width=900, height=300)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)

    scrollframe = tk.Frame(canvas, bg="black")
    scrollframe.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((450,0), window=scrollframe, anchor="n")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    chara_vars = []

    for i, chara in enumerate(personajes):
        var = tk.IntVar()

        img = Image.open(f"images/characters/{chara.name.lower()}.png")
        img = img.resize((90,90))
        img = ImageTk.PhotoImage(img)

        cb = tk.Checkbutton(
            scrollframe, text=chara.name, image=img, compound="top",
            variable=var, bg="black", fg="white", selectcolor="gray"
        )

        cb.image = img
        cb.grid(row=i//4, column=i%4, padx=15, pady=12)

        chara_vars.append((var, chara))
    
    def startgame():
        chosen = [c for v, c in chara_vars if v.get()==1]

        if name_entry.get().strip() == "":
            messagebox.showwarning(
                "Name Required!",
                "Please enter your name."
            )
            return

        if avatar_var.get() == "":
            messagebox.showwarning(
                "Avatar Required!",
                "Please choose an avatar."
            )
            return

        if len(chosen) != 3:
            messagebox.showwarning(
                "Non-valid Team!",
                "You must choose exactly 3 characters."
            )
            return
        
        player = Jugador(name_entry.get())
        player.chosen = chosen
        player.team = chosen.copy()
        player.hollowdefeat = []

        mapwindow(player, personajes)
    
    tk.Button(
        window, text="START GAME", font=("Arial", 16, "bold"),
        bg="white", fg="black", command=startgame
    ).pack(pady=20)

def mapwindow(player, personajes):
    clear()

    if len(player.hollowdefeat) == 5:
        endwindow(player)
        return
    
    bkgnd = Image.open("images/backgrounds/map.png")
    bkgnd = bkgnd.resize((1280, 720))
    bkgnd = ImageTk.PhotoImage(bkgnd)

    bglabel = tk.Label(window, image=bkgnd)
    bglabel.image = bkgnd
    bglabel.place(x=0, y=0, relwidth=1, relheight=1)


    tk.Label(
        window, text="WORLD MAP", font=("Arial", 22, "bold"),
        bg="black", fg="white"
    ).place(x=20, y=20)

    tk.Label(
        window, text=f"Score: {player.puntaje}", font=("Arial", 16, "bold"),
        bg="black", fg="white"
    ).place(x=20, y = 75)

    hollows = hollowtypes(personajes)

    positions = {
        "Ruins": (120, 550),
        "Snowdin": (350, 500),
        "Waterfall":(850, 520),
        "Hotland": (900, 350),
        "Castle": (530, 250)
    }

    
    
    for h in hollows:
        if h.name in player.hollowdefeat:
            text = h.name + "DEFEATED"
            color = "gray"
        else:
            text = h.name
            color = "white"

        def enterhollow(hollow=h):
            if hollow.name in player.hollowdefeat:
                return
            prebattleselectwindow(player, hollow, personajes)

        x,y = positions[h.name]

        tk.Button(
            window, text=text, font=("Arial", 14, "bold"),
            bg=color, fg="black", width=10, command=enterhollow
        ).place(x=x, y=y)

def prebattleselectwindow(player, hollow, personajes):
    clear()

    tk.Label(window, text="Choose 3 characters").pack()

    varslist = []

    for chara in player.chosen:
        var = tk.IntVar()
        tk.Checkbutton(window, text=chara.name, variable=var).pack()
        varslist.append((var, chara))

    def confirmteam():
        selected = [c for v, c in varslist if v.get() == 1]

        if len(selected) != 3:
            tk.Label(window, text="Must choose 3", fg="red").pack()
            return

        player.team = selected
        battlewindow(player, hollow, personajes)   
    
    tk.Button(window, text="BATTLE!", command=confirmteam).pack()

def battlewindow(player, hollow, personajes, chosen=None):
    clear()

    if chosen is None:
        chosen = pepejuana(player.team)
    
    enemy = hollow.persact()

    texto = tk.Label(window, font=("Arial", 12))
    texto.pack()

    labelpoint = tk.Label(window, font=("Arial", 12))
    labelpoint.pack()

    frame = tk.Frame(window)
    frame.pack()

    def update():
        if enemy is None:
            return
        
        texto.config(
            text=f"{chosen.name} HP: {chosen.currhp}\n"
                 f"{enemy.name} HP: {enemy.currhp}"
        )

        labelpoint.config(text=f"Puntaje: {player.puntaje}")
    
    def enemturntk():
        nonlocal chosen, enemy
        chosen, enemy = enemyturn(player, hollow, chosen, enemy)

        if chosen is None:
            startwindow()
            return
        
        update()
    
    def attacktk():
        nonlocal chosen, enemy

        if enemy is None:
            return
        
        attack(chosen, enemy)

        if not enemy.estadovida():
            hollow.loss(enemy)
            player.captura(enemy)
            enemy = hollow.persact()

            if enemy is None:
                player.hollowdefeat.append(hollow.name)

                for chara in player.chosen:
                    chara.recover()
                    
                mapwindow(player, personajes)
                return
        
        enemturntk()
    
    def changetk():
        clear()

        tk.Label(window, text="Choose character").pack()

        for chara in player.team:
            def chooseinbattle(newchosen=chara):
                battlewindow(player, hollow, personajes, newchosen)
            tk.Button(window, text=chara.name, command=chooseinbattle).pack()
    
    tk.Button(frame, text="Attack", command=attacktk).pack()
    tk.Button(frame, text="Change", command=changetk).pack()

    update()

if __name__ == "__main__":
    startwindow()
    window.mainloop()