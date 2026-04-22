import random
import tkinter as tk

window = tk.Tk()
window.title("Overtale")
window.geometry("700x700")

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
    
    tk.Label(window, text="OVERTALE", font=("Arial", 20)).pack()

    tk.Label(window, text="Name:").pack()
    name_entry = tk.Entry(window)
    name_entry.pack()

    avatar_var = tk.StringVar()
    tk.Label(window, text="Choose Avatar").pack()

    for a in ["Frisk", "Doggo", "Temmie"]:
        tk.Radiobutton(window, text=a, variable=avatar_var, value=a).pack()

    tk.Label(window, text="Choose 3 characters").pack()

    chara_vars = []
    for chara in personajes:
        var = tk.IntVar()
        tk.Checkbutton(window, text=chara.name, variable=var).pack()
        chara_vars.append((var, chara))
    
    def startgame():
        chosen = [c for v, c in chara_vars if v.get()==1]

        if len(chosen) != 3:
            print("You must choose 3 characters")
            return
        
        player = Jugador(name_entry.get())
        player.chosen = chosen
        player.team = chosen.copy()
        player.hollowdefeat = []

        mapwindow(player, personajes)
    
    tk.Button(window, text="Start Game", command=startgame).pack()

def mapwindow(player, personajes):
    clear()

    tk.Label(window, text="MAPA", font=("Arial", 16)).pack()
    tk.Label(window, text=f"Puntaje: {player.puntaje}", font=("Arial", 12)).pack()

    hollows = hollowtypes(personajes)

    if len(player.hollowdefeat) == 5:
        endwindow(player)
        return
    
    for h in hollows:
        if h.name in player.hollowdefeat:
            status = "DONE"
        else:
            status = ""
        def enterhollow(hollow=h):
            if hollow.name in player.hollowdefeat:
                return
            prebattleselectwindow(player, hollow, personajes)
        
        tk.Button(window, text=h.name + status, command=enterhollow).pack()

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