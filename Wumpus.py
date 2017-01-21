import random
import Room

# Lovisa Colérus
# 2015
# Text-based game where you hunt Wumpus



class Wumpus():
    def __init__(self):
        self.nTurns = 0
        self.name = ''
        self.roomList = []
        self.room = None
        self.nArrow = 0
        self.difficulty = ''
        self.numbersOfRooms = 20
        
    #players name that will be seen in the highscore
    def playerName():
        name = input("Skriv in ditt namn: ")
        return name

    #Takes input about how hard the game will be
    def chooseDifficulty():
        while(True):
            difficulty = input('Välj svårighetsgrad (Lätt, Medel, Svår): ')
            if (difficulty.lower() == 'lätt'):
                return 'Lätt'
            #lowers the possibility for dangers in the rooms
                break
            elif (difficulty.lower() == 'medel'):
                return 'Medel'
                break
            #normal
            elif (difficulty.lower() == 'svår'):
                return 'Svår'
            #Wumpus moves
                break
            else:
                print('Skriv in godkänt kommando (Lätt, Medel, Svår)')
    


               
            
        
        
    #random danger that will be assigned to a room
    #Depening on the choice of level of the game, the propabilities of dangers differs
    def randomDanger(self):
        if(self.difficulty == 'Lätt'):
            bat = 20
            hole = 30
        else:
            bat = 30
            hole = 50
        danger = random.randint(1,100)
        if (danger <= bat):
            danger = 'bat'
        elif ((bat+1) <= danger <= hole):
            danger = 'hole'
        return danger
            
            
    #creates a list of 20 rooms
    #Puts Wumpus in a random room
    #makes one random room the starting room without a danger
    def createRooms(self):
        roomList = []
        for i in range(0,self.numbersOfRooms):
            danger = Wumpus.randomDanger(self)
            roomList.append(Room.Room(danger))
        wumpusRoom = random.randint(0,(self.numbersOfRooms-1))
        roomList[wumpusRoom].danger = 'Wumpus'
        
        while(True):
            startingRoom = random.randint(0, (self.numbersOfRooms-1))
            if(startingRoom != wumpusRoom):
                roomList[startingRoom].danger = 'startingpoint'
                self.room = roomList[startingRoom]
                break
        self.roomList = roomList
        
        
        
    #shuffles roomList twice and adds Neighbours in every direction for each room in roomList
    def createNeighbours(self):
        roomList = self.roomList
        random.shuffle(roomList)
        for i in range(len(roomList)):
            roomList[i].neighbours['V'] = roomList[(i-1)]
            if i == (self.numbersOfRooms-1):
                roomList[i].neighbours['Ö'] = roomList[0]
            else:
                roomList[i].neighbours['Ö'] = roomList[(i+1)]
        random.shuffle(roomList)
        for j in range(len(roomList)):
            roomList[j].neighbours['N'] = roomList[(j-1)]
            if j == (self.numbersOfRooms-1):
                roomList[j].neighbours['S'] = roomList[0]
            else:
                roomList[j].neighbours['S'] = roomList[(j+1)]        
        
        
        
        
        
    #moved Wumpus if the choice is to play in Hard-mode
    #Wumpus moves into a neighbouring room that does not have a danger in it
    def moveWumpus(self):
        if(self.difficulty == 'Svår'):
            i = 0
            while(True):
                if(self.roomList[i].danger == 'Wumpus'):
                    self.roomList[i].danger = None
                    neighbours = list(self.room.neighbours.values())
                    random.shuffle(neighbours)
                    for j in neighbours:
                        if (j.danger != 'bat' or j.danger != 'hole'):
                            j.danger = 'Wumpus'
                            break
                            
                if(i < (self.numbersOfRooms-1)):    
                    i = i+1
                else:
                    break        
        
    #if player dies it ends the game and saves the highscore
    def death(self):
        print('Du dog')
        exit(0)
        
    # saves the players highscore to a file that is sorted, highest to lowest
    # shows top 3 highscore
    def saveToHighscore(self):
        scoreSet = []
        file = open('Highscore.txt', 'r')
        for i in file:
            part =  i.split(' ')
            iscore = part.pop()
            iname = ' '.join(part)
            iscore = iscore.strip()
            scoreSet.append((iname, iscore))
        file.close()
        scoreSet.append((self.name, self.nTurns))
        scoreSet = sorted(scoreSet, key = lambda x: int(x[1]))
        file = open('Highscore.txt', 'w')
        for j in scoreSet:
            file.write(str(j[0]) + ' ' + str(j[1]) + '\n')
        
        print('\n' + 'Topp tre highscore: ' + '\n')
        for i in range(0,3):    
            print(str(scoreSet[i][0]) + ' ' + str(scoreSet[i][1]))
        
        
        file.close()        
        
    #checks dangers in the room and executes them
    def playerInDanger(self):
        if (self.room.isWumpusInTheRoom()):
            print('Wumpus åt dig')
            self.death()
        elif (self.room.danger == 'bat'):
            roomNumber = random.randint(0,(self.numbersOfRooms-1))
            print('Du känner fladdermusvingar mot kinden och lyfts uppåt. Efter en kort flygtur '+
            'släpper fladdermössen ner dig i rum %i' % (roomNumber+1) + '\n')
            self.room = self.roomList[roomNumber]
        elif (self.room.danger == 'hole'):
            print('Du klev ner i ett bottenlöst hål')
            self.death()
        return None


        
       

    #Writes which dangers are in the neighbouring rooms 
    def playerNearDanger(self):
        bat = False
        Wumpus = False
        hole = False
        roomList = self.room.neighbours.values()
        for j in roomList:
            if (j.danger == 'bat'):
                bat = True
            elif (j.danger == 'Wumpus'):
                Wumpus = True
            elif (j.danger == 'hole'):
                hole = True              
        if(bat):
            print('Jag hör fladdermusvingar!')
        if(hole):
            print('Jag känner vinddraget från ett avgrundshål')
        if(Wumpus):
            print('Jag känner stanken av Wumpus')
        
        
        
    #prints which other room you can move to (might be one room more than once)    
    def moveOptions(self):
        neighbourList = list(self.room.neighbours.values())
        roomNumbers = []
        for j in neighbourList:
            roomNumbers.append(self.roomList.index(j))
        print('Härifrån kan man ta sig till följande rum: %i %i %i %i' % ((roomNumbers[0]+1), (roomNumbers[1]+1), (roomNumbers[2]+1), (roomNumbers[3]+1)) + '\n')
        
    #asks which direction and handling wrong inputs 
    def direction():
        while(True):
            direction = input('Vilken riktning? (N, S, V, Ö) \n')
            if (direction.upper() == 'N' or direction.upper() == 'S' or direction.upper() == 'V' or direction.upper() == 'Ö'):   
                return direction.upper()
                break
            else:
                print('Ge ett godkänt kommando (N, S, V, Ö) \n')
           
    #Moves the playes to the next room   
    def movement(self):
        direction = ''
        self.nTurns = self.nTurns + 1
        direction = Wumpus.direction()      
        self.room = self.room.neighbours[direction]
        


    
    #if player decides to shoot this will let the arrow go through 3 rooms
    #player chooses direction through every room
    #if Wumpus is shot, player wins the game
    def shoot(self):
        self.nArrow = self.nArrow + 1
        self.nTurns = self.nTurns + 1
        room = self.room
        count = 0
        direction = ''
        #shows how the arrow moves. Checks if the player shoots themselves
        while(count<3):
            print('Pilen lämnar rum nr %i ' % (count+1))
            direction = Wumpus.direction()
              
            room = room.neighbours[direction]
            if(room == self.room):
                print('Du skjöt dig själv')
                Wumpus.death(self)
            if(room.isWumpusInTheRoom()):
                print('Wumpus är död! Du vinner!')
                self.saveToHighscore()
                exit(0)
           
            count= count + 1        
        
    #checks dangers of the room
    #asks if player want to shoot or move
    def playerInNewRoom(self):
        Wumpus.playerInDanger(self)
        print('\n' + 'Du är nu i rum %i' % (self.roomList.index(self.room)+1))        
        Wumpus.playerNearDanger(self)
        Wumpus.moveOptions(self)
        if(self.nArrow < 6):
            while(True):
                action = input('Vill du förflytta dig, skjuta eller avsluta? (F, S, A) ')
                if(action.upper() == 'S'):
                    self.shoot()
                elif(action.upper() == 'F'):
                    Wumpus.movement(self)
                    break
                elif(action.upper() == 'A'):
                    print('Spelet avslutas')
                    exit(0)
                else:
                    print('Ge ett godkänt kommando (F, S, A) ')
        else:
            print('Du har inga pilar kvar!')
            Wumpus.movement(self)
        Wumpus.moveWumpus(self)
        return self.room
           



        


        
#runs the game            
def mainProgram():
    game = Wumpus()
    game.name = Wumpus.playerName()
    game.difficulty = Wumpus.chooseDifficulty()
    Wumpus.createRooms(game)
    Wumpus.createNeighbours(game)
   
    print('Du befinner dig i kulvertarna under CSC, där den glupske Wumpus bor.\n'+
        'För att undvika att bli uppäten måste du skjuta Wumpus med din pil\n'+
        'och båge. Kulvertarna har 20 rum som är förenade med smala gångar.\n'+
        'Du kan röra dig åt norr, öster, söder eller väster från ett rum till\n'+
        'ett annat.\n'+
        'Här finns dock faror som lurar. I vissa rum finns bottenlösa hål. Kliver\n'+
        'du ner i ett sådant dör du omedelbart. I andra rum finns fladdermöss\n'+
        'som lyfter upp dig, flyger en bit och släpper dig i ett godtyckligt\n'+
        'rum. I ett av rummen finns Wumpus, och om du vågar dig in i det rummet\n'+ 
        'blir du genast uppäten. Som tur är kan du från rummen bredvid känna\n'+
        'vinddraget från ett avgrundshål eller lukten av Wumpus. Du får också\n'+
        'i varje rum reda på vilka rum som ligger intill.\n'+
        'För att vinna spelet måste du skjuta Wumpus. När du skjuter iväg en\n'+
        'pil förflyttar den sig genom tre rum - du kan styra vilken riktning\n'+
        'pilen ska välja i varje rum. Glöm inte bort att tunnlarna vindlar sig\n'+
        'på oväntade sätt. Du kan råka skjuta dig själv...\n'+
        'Du har fem pilar. Lycka till! \n')
        
    while(True):    
        game.playerInNewRoom()
    
        
mainProgram()