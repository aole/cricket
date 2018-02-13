import numpy as np
from match import Match
import operator
import json
from team import Team

class Tournament:
    KO8 = 1
    BIG8 = 2
    
    def __init__(self, teams, default_team=None, type=None):
        self.scores = {}
        
        self.teams = list(teams)
        
        # if there is a default team remove a random team and include this
        if default_team!=None:
            r = np.random.randint(8)
            self.teams[r] = default_team
            
        np.random.shuffle(self.teams)
        
        if not type:
            type=self.KO8
        self.type = type
        self.init()
        
    def init(self):
        if self.type==self.BIG8:
            self.g1pts = {self.teams[0]:0,self.teams[1]:0,self.teams[2]:0,self.teams[3]:0}
            self.g1m1 = Match(self.teams[0], self.teams[1])
            self.g1m2 = Match(self.teams[2], self.teams[3])
            self.g1m3 = Match(self.teams[0], self.teams[2])
            self.g1m4 = Match(self.teams[1], self.teams[3])
            self.g1m5 = Match(self.teams[0], self.teams[3])
            self.g1m6 = Match(self.teams[1], self.teams[2])
            
            self.g2pts = {self.teams[4]:0,self.teams[5]:0,self.teams[6]:0,self.teams[7]:0}
            self.g2m1 = Match(self.teams[4], self.teams[5])
            self.g2m2 = Match(self.teams[6], self.teams[7])
            self.g2m3 = Match(self.teams[4], self.teams[6])
            self.g2m4 = Match(self.teams[5], self.teams[7])
            self.g2m5 = Match(self.teams[4], self.teams[7])
            self.g2m6 = Match(self.teams[5], self.teams[6])
        elif self.type==self.KO8:
            self.q1 = Match(self.teams[0], self.teams[1])
            self.q2 = Match(self.teams[2], self.teams[3])
            self.q3 = Match(self.teams[4], self.teams[5])
            self.q4 = Match(self.teams[6], self.teams[7])
        
        self.s1 = Match()
        self.s2 = Match()
        self.final = Match()
        
    def get_mots(self):
        maxn = None
        maxs = []
        team = None
        for n, s in self.scores.items():
            if sum(s['score'])>sum(maxs):
                maxn = n
                maxs = s['score']
                team = s['team']
            elif sum(s['score'])==sum(maxs) and len(s['score'])<len(maxs):
                maxn = n
                maxs = s['score']
                team = s['team']
                
        return team, maxn, maxs
        
    def collect_score(self, scores):
        for n,s in scores.items():
            if n not in self.scores:
                self.scores[n] = {'team':s['team'],'score':[]}
            self.scores[n]['score'].extend(s['runs'])
            
    def play_match(self, match):
        winner = match.play()
        
        self.collect_score( match.batsman_score )
        
        return winner
        
    def play(self):
        if self.type==self.BIG8:
            print('____ Group Stage ____')
            # play league matches
            g1m1w = self.play_match( self.g1m1 )
            self.g1pts[g1m1w] += 1
            print( self.g1m1.summary() )
            
            g2m1w = self.play_match( self.g2m1 )
            self.g2pts[g2m1w] += 1
            print( self.g2m1.summary() )
            
            g1m2w = self.play_match( self.g1m2 )
            self.g1pts[g1m2w] += 1
            print( self.g1m2.summary() )
            
            g2m2w = self.play_match( self.g2m2 )
            self.g2pts[g2m1w] += 1
            print( self.g2m2.summary() )
            
            g1m3w = self.play_match( self.g1m3 )
            self.g1pts[g1m3w] += 1
            print( self.g1m3.summary() )
            
            g2m3w = self.play_match( self.g2m3 )
            self.g2pts[g2m3w] += 1
            print( self.g2m3.summary() )
            
            g1m4w = self.play_match( self.g1m4 )
            self.g1pts[g1m4w] += 1
            print( self.g1m4.summary() )
            
            g2m4w = self.play_match( self.g2m4 )
            self.g2pts[g2m4w] += 1
            print( self.g2m4.summary() )
            
            g1m5w = self.play_match( self.g1m5 )
            self.g1pts[g1m5w] += 1
            print( self.g1m5.summary() )
            
            g2m5w = self.play_match( self.g2m5 )
            self.g2pts[g2m5w] += 1
            print( self.g2m5.summary() )
            
            g1m6w = self.play_match( self.g1m6 )
            self.g1pts[g1m6w] += 1
            print( self.g1m6.summary() )
            
            g2m6w = self.play_match( self.g2m6 )
            self.g2pts[g2m6w] += 1
            print( self.g2m6.summary() )
            
            
            g1 = sorted( self.g1pts.items(), key=operator.itemgetter(1), reverse=True )
            g2 = sorted( self.g2pts.items(), key=operator.itemgetter(1), reverse=True )
            
            self.s1.init( g1[0][0], g2[1][0] )
            self.s2.init( g2[0][0], g1[1][0] )
            
        elif self.type==self.KO8:
            print('\n____ Quaterfinals ____')
            self.print_fixture()
            ts1 = self.play_match( self.q1 )
            ts2 = self.play_match( self.q2 )
            self.s1.init(ts1,ts2)
            
            ts3 = self.play_match( self.q3 )
            ts4 = self.play_match( self.q4 )
            self.s2.init(ts3,ts4)
            
        print('\n____ Semifinals ____')
        self.print_fixture()
        tf1 = self.play_match( self.s1 )
        print( self.s1.summary() )
            
        tf2 = self.play_match( self.s2 )
        print( self.s2.summary() )
            
        self.final.init(tf1, tf2)
            
        print('\n____ Finals ____')
        self.print_fixture()
        winner = self.play_match( self.final )
        print( self.final.summary() )
            
        self.print_fixture()
        
        # man of the match
        print(winner.name, 'won the tournament!')
        
        team, mm, mms = self.get_mots()
        print('Man of the Series: '+team.name+'\'s '+mm+'\t'+str(sum(mms))+' ('+str(len(mms))+')')
        
    def print_fixture( self ):
        print('--------------------')
        if self.type==self.KO8:
            print(self.q1.team1.name)
            w = '\tW: ' + self.q1.winner.name if self.q1.complete else ''
            print(self.q1.team2.name, w)
        
        if self.s1.complete:
            print('\t\t\tW:', self.s1.winner.name)
        else:
            print()
        
        if self.type==self.KO8:
            w = '\tW: ' + self.q2.winner.name if self.q2.complete else ''
            print(self.q2.team1.name, w)
            print(self.q2.team2.name)
        
        if self.final.complete:
            print('\t\t\t\tW:', self.final.winner.name)
        else:
            print()
        
        if self.type==self.KO8:
            print(self.q3.team1.name)
            w = '\tW: ' + self.q3.winner.name if self.q3.complete else ''
            print(self.q3.team2.name, w)
        
        if self.s2.complete:
            print('\t\t\tW:', self.s2.winner.name)
        else:
            print()
        
        if self.type==self.KO8:
            w = '\tW: ' + self.q4.winner.name if self.q4.complete else ''
            print(self.q4.team1.name, w)
            print(self.q4.team2.name)
        print('--------------------')

if __name__ == '__main__':
    with open('data.txt') as f:
        data = json.load(f)
        teams = []
        for team in data['Teams']:
            teams.append( Team(team, data=data) )

    Tournament( teams ).play()
    #Tournament( teams, type=Tournament.BIG8 ).play()
    