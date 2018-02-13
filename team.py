import names

class Team:
    def __init__( self, name, data=None, players=None ):
        self.name = name
        if data:
            self.players = data[name]
        elif players:
            self.players = players
        else:
            self.players = []
            for i in range(11):
                name = names.get_full_name( gender='male' )
                self.players.append( name )
            
    def get_batsman( self, pos ): # 1 based index
        return self.players[pos-1]
    
    def get_bowler( self, over ):
        if over in [1,3,18,20]:
            return self.players[10]
        elif over in [2,4,17,19]:
            return self.players[9]
        elif over in [5,7,14,16]:
            return self.players[8]
        elif over in [6,8,10,12]:
            return self.players[7]
        else:
            return self.players[6]

    def add( self, name, pos ):
        self.players.insert(pos-1, name)
    
    def __str__( self ):
        '''
        s = self.name+'\n'
        s += '----\n'
        cnt=1
        for p in self.players:
            s += str(cnt)+'. '+p+'\n'
            cnt+=1
        '''
        return self.name
        
    def __repr__( self ):
        return self.__str__()
    
    def __hash__( self ):
        return hash( self.name )
    
    def __eq__( self, other ):
        return isinstance(other, Team) and self.name == other.name
        
    def __ne__( self, other ):
        return not( self == other )
        