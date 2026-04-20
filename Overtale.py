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
        character.recover()
        self.chosen.append(character)
        self.puntaje += 1
    
    def loss(self, character):
        if character in self.chosen:
            self.chosen.remove(character)
    
    def playervivos(self):
        for chara in self.chosen:
            if chara.estadovida():
                return True
        return False
    
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
        enemalive = []
        for chara in self.enemies:
            if chara.estadovida():
                enemalive.append(chara)
        
        if len(enemalive) == 0:
            return None
        else:
            return random.choice(enemalive)
    
    def hollowvivos(self):
        for chara in self.enemies:
            if chara.estadovida():
                return True
        return False

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
