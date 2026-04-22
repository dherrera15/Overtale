import random

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

class Jugador:
    def __init__(self, name):
        self.name = name
        self.chosen = []
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
        chosen = enemyturn_aux(player.chosen)
    
    if chosen is None:
        return chosen, currenemy
    
    return chosen, currenemy

def enemyturn_aux(chosenlist, chara = 0):
    if chara >= len(chosenlist):
        return None
    
    if chosenlist[chara].estadovida():
        return chosenlist[chara]
    
    return enemyturn_aux(chosenlist, chara + 1)

def showchosen(player, i = 0):
    if i >= len(player.chosen):
        return
    
    chara = player.chosen[i]
    status = "VIVO"
    print(f"{i}: {chara.name} ({status})")

    showchosen(player, i + 1)

def selectingame(player):
    print("\n--- YOUR TEAM")
    showchosen(player)

    index = int(input("Choose the one to fight: "))

    if index < 0 or index >= len(player.chosen):
        print("Not valid")
        return selectingame(player)
    
    return player.chosen[index]

def batalla(player, hollow, chosen, currenemy):
    if not player.playervivos():
        print("You lost")
        return
    
    if not hollow.hollowvivos():
        print("You won, the hollow is defeated!")
        return
    
    print("\nYour turn:")
    print("1: Attack")
    print("2: Change character")

    act = input("Elige: ")

    if act == "1":
        if currenemy is None:
            return batalla(player, hollow, chosen, currenemy)
        attack(chosen, currenemy)

        if not currenemy.estadovida():
            hollow.loss(currenemy)
            player.captura(currenemy)
            currenemy = hollow.persact()
    elif act == "2":
        newchosen = selectingame(player)

        if newchosen != chosen:
            print(f"Changed to {newchosen.name}")
            chosen = newchosen
    
    chosen, currenemy = enemyturn(player, hollow, chosen, currenemy)

    return batalla(player, hollow, chosen, currenemy)

def show_chara(characters):
    print("\n--- AVAILABLE CHARACTERS")
    for chara, atr, in enumerate(characters):
        print(f"{chara}: {atr.name} | HP: {atr.maxhp} | ATK: {atr.attack} | DEF: {atr.defense}")

def selecta():
    avatars = ["Frisk", "Doggo", "Temmie"]
    print("\n--- AVATARS")
    for order, avatar in enumerate(avatars):
        print(order, "-", avatar)
    
    index = int(input("Elige avatar (0-2): "))
    return avatars[index]

def selectc(characters):
    chosen = []

    while len(chosen) < 3:
        print("\n--- CHOOSE 3 CHARACTERS")
        for chara, name in enumerate(characters):
            if characters[chara] in chosen:
                status = "check"
            else:
                status = ""
            print(f"{chara}: {name.name} {status}")

        index = int(input("Index selection: "))

        if index < 0 or index >= len(characters):
            print("Not valid")
        elif characters[index] in chosen:
            print("Already chosen")
        else:
            chosen.append(characters[index])
            print("Added ", characters[index].name)
    
    return chosen

def start():
    personajes = cargarpers()

    print("\n=== OVERTALE ===")

    nombre = input("Player name: ")
    player = Jugador(nombre)

    avatar = selecta()

    player.chosen = selectc(personajes)

    print("\n--- SUMMARY ---")
    print("Player: ", player.name)
    print("Avatar:", avatar)
    print("\nChosen characters:")
    for chara in player.chosen:
        print("-", chara.name)
    return player, personajes

if __name__ == "__main__":
    player, personajes = start()