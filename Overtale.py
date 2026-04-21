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
    
    def playervivos(self, i = 0):
        if i >= len(self.chosen):
            return False
        if self.chosen[i].estadovida():
            return True
        
        return self.playervivos(i + 1)
    
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
    
    def hollowvivos(self, i = 0):
        if i >= len(self.enemies):
            return False
        if self.chosen[i].estadovida():
            return True
        return self.hollowvivos(i + 1)

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

def turn(player, hollow, chosen):
    if not player.playervivos():
        return
    
    if not hollow.hollowvivos():
        return
    
    enemy = hollow.persact()

    if enemy is None:
        return
    
    attack(chosen, enemy)

    if not enemy.estadovida():
        hollow.loss(enemy)
        player.captura(enemy)
    else:
        attack(enemy, chosen)

        if not chosen.estadovida():
            player.loss(chosen)
            hollow.captura(chosen)

    turn(player, hollow, chosen)

def show_chara(characters):
    print("\n--- PERSONAJES DISPONIBLES")
    for chara, atr, in enumerate(characters):
        print(f"{chara}: {atr.name} | HP: {atr.maxhp} | ATK: {atr.attack} | DEF: {atr.defense}")

def selecta():
    avatars = ["Frisk", "Doggo", "Temmie"]
    print("\n--- AVATARES")
    for order, avatar in enumerate(avatars):
        print(order, "-", avatar)
    
    index = int(input("Elige avatar (0-2): "))
    return avatars[index]

def selectc(characters):
    chosen = []

    while len(chosen) < 3:

        print("\n--- ELIJA 3 PERSONAJES")
        for chara, name in enumerate(characters):
            if chara in chosen:
                status = "check"
            else:
                status = ""
            print(f"{chara}: {name.name} {status}")

        index = int(input("Seleccion indice: "))

        if index < 0 or index >= len(characters):
            print("No valido")
        elif characters[index] in chosen:
            print("Ya elegido")
        else:
            chosen.append(characters[index])
            print("Agregado ", characters[index].name)
    return chosen

def start():
    personajes = cargarpers()

    print("\n=== OVERTALE ===")

    nombre = input("Nombre de jugador: ")
    player = Jugador(nombre)

    avatar = selecta()

    player.chosen = selectc(personajes)

    print("\n--- RESUMEN ---")
    print("Jugador: ", player.name)
    print("Avatar:", avatar)
    print("\nPersonajes elegidos:")
    for chara in player.chosen:
        print("-", chara.name)
    return player, personajes

if __name__ == "__main__":
    player, personajes = start()
