# Lovisa Colérus
# 2015
# Creates rooms to be used in the Wumpus-game
class Room():
    def __init__(self, danger):
        self.danger = danger
        self.neighbours = dict()
    
    #links the rooms in lists
    def addNeighbour(self, riktning):
        return dict(riktning, Room)
        
    #checks if Wumpus is in the room
    def isWumpusInTheRoom(self):
        if (self.danger == 'Wumpus'):
            return True  
        return False
           
           