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
        self.captured = []
    
    def captura(self, character):
        if self.duplicados(character.name):
            return
        
        new = character.separate()
        new.recover()
        self.chosen.append(new)
        self.team.append(new)
        self.puntaje += 1
    
    def duplicados(self, name, i=0):
        if i >= len(self.chosen):
            return False
        
        if self.chosen[i].name == name:
            return True
        
        return self.duplicados(name, i + 1)
    
    def loss(self, character):
        if character in self.team:
            self.team.remove(character)
        if character not in self.captured:
            self.captured.append(character)
    
class Hollow:
    def __init__(self, name, characters):
        self.name = name
        self.enemies = characters

    def captura(self, character):
        new = character.separate()
        new.recover()
        self.enemies.append(new)
    
    def loss(self, character):
        if character in self.enemies:
            self.enemies.remove(character)
    
    def persact(self):
        enemalive = self.persact_aux(self.enemies)
        
        if len(enemalive) == 0:
            return None
        else:
            return random.choice(enemalive)
    
    def persact_aux(self, lista, i = 0):

        if i >= len(lista):
            return []
        
        if lista[i].estadovida():
            return [lista[i]] + self.persact_aux(lista, i+1)
        
        return self.persact_aux(lista, i + 1)

def cargarpers():
    archivo = open("personajes.txt", "r")
    personajes = cargarpers_aux(archivo, [])
    archivo.close()
    return personajes

def cargarpers_aux(archivo, lista):
    fila = archivo.readline()

    if fila == "":
        return lista
    
    atributo = fila.strip().split(",")
    name = atributo[0]
    hp = int(atributo[1])
    atk = int(atributo[2])
    df = int(atributo[3])
    chara = Personaje(name, hp, atk, df)
    lista.append(chara)

    return cargarpers_aux(archivo, lista)

def hollowtypes(personajes):
    return [
        Hollow("Ruins", hollowtypes_aux(personajes, 0, 3, 0)),
        Hollow("Snowdin", hollowtypes_aux(personajes, 3, 6, 0)),
        Hollow("Waterfall", hollowtypes_aux(personajes, 6, 9, 0)),
        Hollow("Hotland", hollowtypes_aux(personajes, 9, 12, 0)),
        Hollow("Castle", hollowtypes_aux(personajes, 12, 15, 0))
    ]

def hollowtypes_aux(personajes, desde, hasta, i):
    if desde + i >= hasta:
        return []
    
    chara = personajes[desde + i].separate()
    return [chara] + hollowtypes_aux(personajes, desde, hasta, i + 1)

def attack(atkr, dfdr):
    dmg = atkr.attack - dfdr.defense

    if dmg <= 0:
        dmg = 1

    dfdr.dano(dmg)
    return dmg

def enemyturn(player, hollow, chosen, currenemy):
    if currenemy is None:
        return chosen, currenemy
    
    prob = 0.3
    pos = hollow.persact_aux(hollow.enemies)

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
            return chosen, newen
    
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

    bkgnd = Image.open("images/backgrounds/start.png")
    bkgnd = bkgnd.resize((1280, 720))
    bkgnd = ImageTk.PhotoImage(bkgnd)

    bglabel = tk.Label(window, image=bkgnd)
    bglabel.image = bkgnd
    bglabel.place(x=0, y=0, relwidth=1, relheight=1)

    frame = tk.Frame(window, bg="black")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(
        frame, text="CONGRATULATIONS!!! YOU SAVED THE STORY", 
        font=("Arial", 20, "bold"), fg="white", bg="black"
    ).pack(pady=10)

    tk.Label(
        frame, text=f"Total points: {player.puntaje}", font=("Arial", 14),
        fg="white", bg="black"
    ).pack(pady=10)

    tk.Button(
        frame, text="Go back to start",
        font=("Arial", 12, "bold"), command=startwindow
    ).pack(pady=20)

def startwindow():
    clear()

    def aboutpage():
        try:
            archivo = open("about.txt", "r", encoding="utf-8")
            lines = archivo.read()
            archivo.close()
        except:
            lines = "About file not found."
        
        messagebox.showinfo("About Overtale", lines)

    personajes = cargarpers()

    bkgnd = Image.open("images/backgrounds/start.png")
    bkgnd = bkgnd.resize((1280, 720))
    bkgnd = ImageTk.PhotoImage(bkgnd)
    bglabel = tk.Label(window, image=bkgnd)
    bglabel.image = bkgnd
    bglabel.place(x=0, y=0, relwidth = 1, relheight = 1)
    
    tk.Label(window, text="OVERTALE", font=("Arial", 28, "bold"), bg="black", fg="white").pack(pady=10)

    tk.Button(
        window, text="About...", font=("Arial", 12, "bold"),
        command=aboutpage, bg="white", fg="black"
    ).place(x=10, y=10)

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
    canvas.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    chara_vars = []

    for i, chara in enumerate(personajes[15:30]):
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
        player.hollows = hollowtypes(personajes)

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

    hollows = player.hollows

    positions = {
        "Ruins": (120, 550),
        "Snowdin": (360, 490),
        "Waterfall":(850, 520),
        "Hotland": (920, 340),
        "Castle": (530, 250)
    }

    for h in hollows:
        if h.name in player.hollowdefeat:
            text = h.name + " DEFEATED"
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
            bg=color, fg="black", command=enterhollow
        ).place(x=x, y=y)

def prebattleselectwindow(player, hollow, personajes):
    clear()

    bkgnd = Image.open("images/backgrounds/battle.png")
    bkgnd = bkgnd.resize((1280, 720))
    bkgnd = ImageTk.PhotoImage(bkgnd)
    bglabel = tk.Label(window, image=bkgnd)
    bglabel.image = bkgnd
    bglabel.place(x=0, y=0, relwidth = 1, relheight = 1)

    tk.Label(
        window, text=f"{hollow.name} - Choose team",
        font=("Arial", 22, "bold"), bg="black", fg="white"
    ).pack(pady=20)

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
    canvas.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    chara_vars = []

    for i, chara in enumerate(player.team):
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
    
    def confirmteam():
        selected = [c for v, c in chara_vars if v.get() == 1]

        if len(selected) != 3:
            messagebox.showwarning(
                "Invalid Team",
                "You must choose exactly 3 characters"
            )
            return
        
        player.team = selected
        battlewindow(player, hollow, personajes)
    
    tk.Button(
        window, text="START BATTLE", font=("Arial", 16, "bold"),
        bg="white", fg="black", command=confirmteam
    ).pack(pady=20)

def battlewindow(player, hollow, personajes, chosen=None, enemy=None, msg=None):
    clear()

    bkgnd = Image.open("images/backgrounds/battle.png")
    bkgnd = bkgnd.resize((1280, 720))
    bkgnd = ImageTk.PhotoImage(bkgnd)
    bglabel = tk.Label(window, image=bkgnd)
    bglabel.image = bkgnd
    bglabel.place(x=0, y=0, relwidth=1, relheight=1)

    if chosen is None:
        chosen = pepejuana(player.team)

    if enemy is None:
        enemy = hollow.persact()

    if enemy is None:
        mapwindow(player, personajes)
        return
    
    tk.Label(
        window, text=f"Score: {player.puntaje}", font=("Arial", 16, "bold"),
        bg="black", fg="white"
    ).place(x=20, y = 75)

    playerimg = ImageTk.PhotoImage(Image.open(f"images/characters/{chosen.name.lower()}.png").resize((250, 250)))
    enemyimg = ImageTk.PhotoImage(Image.open(f"images/characters/{enemy.name.lower()}.png").resize((250, 250)))

    playerlabel = tk.Label(window, image=playerimg, bg="black")
    playerlabel.image = playerimg
    playerlabel.place(x=150, y=200)

    enemylabel = tk.Label(window, image=enemyimg, bg="black")
    enemylabel.image = enemyimg
    enemylabel.place(x=880, y=200)

    playerinfo = tk.Label(window, font=("Arial", 14, "bold"), bg="black", fg="white")
    playerinfo.place(x=150, y=470)

    enemyinfo = tk.Label(window, font=("Arial", 14, "bold"), bg="black", fg="white")
    enemyinfo.place(x=880, y=470)

    starttext = msg if msg else "The battle has started."

    actions = tk.Label(
        window, text=starttext, font=("Arial", 14),
        bg="black", fg="white", width=40,
        height=10, wraplength=400, justify="center"
    )
    actions.place(x=420, y=250)

    buttonframe = tk.Frame(window, bg="black")
    buttonframe.place(x=450, y=550)

    def update():
        playerinfo.config(text=f"{chosen.name}\nHP: {chosen.currhp}/{chosen.maxhp}")
        enemyinfo.config(text=f"{enemy.name}\nHP: {enemy.currhp}/{enemy.maxhp}")

    def enemturntk():
        if not playerlabel.winfo_exists() or not enemylabel.winfo_exists():
            return

        nonlocal chosen, enemy

        prevhp = chosen.currhp
        oldenemy = enemy
        oldchosen = chosen

        chosen, enemy = enemyturn(player, hollow, chosen, enemy)

        prevalive = prevhp > 0

        if chosen is None:
            messagebox.showinfo("Game Over", "You lost.")
            startwindow()
            return
        
        newplayerimg = ImageTk.PhotoImage(
            Image.open(f"images/characters/{chosen.name.lower()}.png").resize((250,250))
        )
        playerlabel.config(image=newplayerimg)
        playerlabel.image = newplayerimg

        if enemy != oldenemy:
            actions.config(text=f"The Hollow changed to {enemy.name}")
            newimg = ImageTk.PhotoImage(Image.open(f"images/characters/{enemy.name.lower()}.png").resize((250, 250)))
            enemylabel.config(image=newimg)
            enemylabel.image = newimg
        else:
            dmg = abs(prevhp - chosen.currhp)

            if prevalive and not oldchosen.estadovida():
                actions.config(
                    text=f"{enemy.name} attacks!\nDamage: {dmg}\n{oldchosen.name} was captured!"
                )
            else:
                actions.config(text=f"{enemy.name} attacks!\nDamage: {dmg}")

        update()

    def attacktk():
        nonlocal chosen, enemy

        dmg = attack(chosen, enemy)
        actions.config(text=f"{chosen.name} attacks!\nDamage: {dmg}")

        if not enemy.estadovida():
            actions.config(text=f"{enemy.name} defeated!")

            hollow.loss(enemy)
            player.captura(enemy)
            enemy = hollow.persact()

            if enemy is None:
                player.hollowdefeat.append(hollow.name)

                for c in player.chosen:
                    c.recover()

                player.team = player.chosen.copy()

                player.captured.clear()

                messagebox.showinfo("Victory!", f"{hollow.name} defeated!")
                mapwindow(player, personajes)
                return

            newimg = ImageTk.PhotoImage(Image.open(f"images/characters/{enemy.name.lower()}.png").resize((250, 250)))
            enemylabel.config(image=newimg)
            enemylabel.image = newimg

        update()
        window.after(800, enemturntk)

    def changetk():
        clear()

        bkgnd2 = ImageTk.PhotoImage(Image.open("images/backgrounds/battle.png").resize((1280, 720)))
        bglabel2 = tk.Label(window, image=bkgnd2)
        bglabel2.image = bkgnd2
        bglabel2.place(x=0, y=0, relwidth=1, relheight=1)

        tk.Label(window, text="Choose character", font=("Arial", 20, "bold"),
                 bg="black", fg="white").pack(pady=20)

        def show(i=0):
            if i >= len(player.team):
                return
            
            chara = player.team[i]

            if chara.estadovida():
                def chooseinbattle(newchosen=chara):
                    battlewindow(player, hollow, personajes, newchosen, enemy, msg=f"You changed to {newchosen.name}.")

                tk.Button(
                    window,
                    text=f"{chara.name} (HP: {chara.currhp})",
                    font=("Arial", 14),
                    command=chooseinbattle
                ).pack(pady=5)
            
            show(i+1)
        
        show()

    tk.Button(buttonframe, text="ATTACK", font=("Arial", 16, "bold"),
              bg="red", fg="white", width=10, command=attacktk).pack(side="left", padx=20)

    tk.Button(buttonframe, text="CHANGE", font=("Arial", 16, "bold"),
              bg="blue", fg="white", width=10, command=changetk).pack(side="left", padx=20)

    update()

    if msg:
            window.after(800, enemturntk)

if __name__ == "__main__":
    startwindow()
    window.mainloop()