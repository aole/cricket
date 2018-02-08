import numpy as np
from match import Match
import json

class Tournament:
    def __init__(self, teams=None):
        with open('data.txt') as f:
            data = json.load(f)

        if teams is None:
            teams = data['Teams']
            
        self.scores = {}
        
        self.teams = list(teams)
        np.random.shuffle(self.teams)
        self.init()
        
    def init(self):
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
        
    def collect_score(self, team, scores):
        for n,s in scores.items():
            if n not in self.scores:
                self.scores[n] = {'team':team,'score':[]}
            self.scores[n]['score'].extend(s)
            
    def play_match(self, match):
        winner = match.play()
        
        self.collect_score( match.team1, match.batsmen1_score )
        self.collect_score( match.team2, match.batsmen2_score )
        
        return winner
        
    def play(self):
        print('\n____ Quaterfinals...')
        self.print_fixture()
        ts1 = self.play_match( self.q1 )
        ts2 = self.play_match( self.q2 )
        self.s1.init(ts1,ts2)
        ts3 = self.play_match( self.q3 )
        ts4 = self.play_match( self.q4 )
        self.s2.init(ts3,ts4)
            
        print('\n____ Semifinals...')
        self.print_fixture()
        tf1 = self.play_match( self.s1 )
        tf2 = self.play_match( self.s2 )
        self.final.init(tf1, tf2)
            
        print('\n____ Finals...')
        self.print_fixture()
        res = self.play_match( self.final )
            
        self.print_fixture()
        
        # man of the match
        print(res, 'won the tournament!')
        
        team, mm, mms = self.get_mots()
        print('Man of the Series: '+team+'\'s '+mm+'\t'+str(sum(mms))+' ('+str(len(mms))+')')
        
    def print_fixture( self ):
        print('--------------------')
        print(self.q1.team1)
        w = '\tW: ' + self.q1.winner if self.q1.complete else ''
        print(self.q1.team2, w)
        
        if self.s1.complete:
            print('\t\t\tW:', self.s1.winner)
        else:
            print()
        
        w = '\tW: ' + self.q2.winner if self.q2.complete else ''
        print(self.q2.team1, w)
        print(self.q2.team2)
        
        if self.final.complete:
            print('\t\t\t\tW:', self.final.winner)
        else:
            print()
        
        print(self.q3.team1)
        w = '\tW: ' + self.q3.winner if self.q3.complete else ''
        print(self.q3.team2, w)
        
        if self.s2.complete:
            print('\t\t\tW:', self.s2.winner)
        else:
            print()
        
        w = '\tW: ' + self.q4.winner if self.q4.complete else ''
        print(self.q4.team1, w)
        print(self.q4.team2)
        print('--------------------')