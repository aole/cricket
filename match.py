import numpy as np
import json

with open('data.txt') as f:
    data = json.load(f)
    
result_type = ['Wk','0', '1', '2', '3', '4', '6']
result_prob = [6,   35,  39,  18,  4,   13,   5]
result_prob = result_prob/np.sum(result_prob) # sum up to 1

class Match:
    def __init__(self, teama=None, teamb=None):
        self.complete = False
        self.winner = None
        self.init(teama, teamb)
        
    def init( self, teama, teamb ):
        if teama==None or teamb==None:
            return
            
        self.team1 = teama
        self.team2 = teamb
        
        coin = np.random.randint(0,2)
        if coin==1:
            self.team1, self.team2 = self.team2, self.team1
        
        self.batsmen1 = data[self.team1]
        assert len(self.batsmen1)>10
        self.batsmen2 = data[self.team2]
        assert len(self.batsmen2)>10
        
    def play( self ):
        print('Match between', self.team1, 'and', self.team2)
        
        self.score = [0,0]
        self.wickets = [0,0]
        
        team1_balls = []
        batsmen1_score = { self.batsmen1[0]:[], self.batsmen1[1]:[] }
        batsman_facing = self.batsmen1[0]
        batsman_doubling = self.batsmen1[1]
        next_batsman_index = 2
        
        # first inings
        print(self.team1, 'innings...')
        for o in range(20):
            for b in range(6):
                r = np.random.choice(result_type, p=result_prob)
                team1_balls.append(r)
                
                if r=='Wk':
                    self.wickets[0] += 1
                    if self.wickets[0] > 9:
                        break
                    batsmen1_score[batsman_facing].append(0) # wicket is also a ball faced
                    batsmen1_score[self.batsmen1[next_batsman_index]] = []
                    batsman_facing = self.batsmen1[next_batsman_index]
                    next_batsman_index += 1
                else:
                    r = int(r)
                    # add runs scored
                    self.score[0] += r
                    batsmen1_score[batsman_facing].append(r)
                    
                    # swap batsmen if odd runs
                    if r==1 or r==3:
                        batsman_facing, batsman_doubling = batsman_doubling, batsman_facing
            
            if self.wickets[0] > 9:
                break
        
            # swap the batmen at the end of the over
            batsman_facing, batsman_doubling = batsman_doubling, batsman_facing
        
        self.batsmen1_score = batsmen1_score
        # print(batsmen1_score)
        for i in range(next_batsman_index):
            print('   '+self.batsmen1[i]+'\t'+str(sum(batsmen1_score[self.batsmen1[i]]))+' ('+str(len(batsmen1_score[self.batsmen1[i]]))+')')
            
        print('  '+self.team1, 'scored', str(self.score[0])+'/'+str(self.wickets[0]), 'in '+str(o if b<5 else o+1)+'.'+str((b+1 if b<5 else '')))
        # print(team1_balls)
        
        # second inings
        team2_balls = []
        batsmen2_score = { self.batsmen2[0]:[], self.batsmen2[1]:[] }
        batsman_facing = self.batsmen2[0]
        batsman_doubling = self.batsmen2[1]
        next_batsman_index = 2
        
        print(self.team2, 'innings...')
        for o in range(20):
            for b in range(6):
                r = np.random.choice(result_type, p=result_prob)
                team2_balls.append(r)
                
                if r=='Wk':
                    self.wickets[1] += 1
                    if self.wickets[1] > 9:
                        break
                    batsmen2_score[batsman_facing].append(0)
                    batsmen2_score[self.batsmen2[next_batsman_index]] = []
                    batsman_facing = self.batsmen2[next_batsman_index]
                    next_batsman_index += 1
                else:
                    r = int(r)
                    # add runs scored
                    self.score[1] += r
                    batsmen2_score[batsman_facing].append(r)
            
                    if self.score[1]>self.score[0]:
                        break
                    
                    # swap batsmen if odd runs
                    if r==1 or r==3:
                        batsman_facing, batsman_doubling = batsman_doubling, batsman_facing
                        
            if self.wickets[1] > 9:
                break
            elif self.score[1]>self.score[0]:
                break
            
            # swap the batsmen at the end of the over
            batsman_facing, batsman_doubling = batsman_doubling, batsman_facing
        
        self.batsmen2_score = batsmen2_score
        for i in range(next_batsman_index):
            print('   '+self.batsmen2[i]+'\t'+str(sum(batsmen2_score[self.batsmen2[i]]))+' ('+str(len(batsmen2_score[self.batsmen2[i]]))+')')
            
        print('  '+self.team2, 'scored', str(self.score[1])+'/'+str(self.wickets[1]), 'in '+str(o if b<5 else o+1)+'.'+str((b+1 if b<5 else '')))
        # print(team2_balls)
        
        # result
        self.complete = True
        if self.score[0] > self.score[1]:
            print ('  '+self.team1, 'beat', self.team2, 'by', str(self.score[0]-self.score[1]),'runs!')
            self.winner = self.team1
        # elif self.score[1] > self.score[0]:
        # TODO: Handle ties
        else:
            print ('  '+self.team2, 'beat', self.team1, 'by', str(10-self.wickets[1]),'wickets!')
            self.winner = self.team2
            
        # man of the match
        mm, mms = self.get_motm()
        print('  Man of the Match: '+mm+'\t'+str(sum(mms))+' ('+str(len(mms))+')')
        
        return self.winner

    def get_motm(self):
        maxn = None
        maxs = []
        for n, s in self.batsmen1_score.items():
            if sum(s)>sum(maxs):
                maxn = n
                maxs = s
            elif sum(s)==sum(maxs) and len(s)<len(maxs):
                maxn = n
                maxs = s
                
        for n, s in self.batsmen2_score.items():
            if sum(s)>sum(maxs):
                maxn = n
                maxs = s
            elif sum(s)==sum(maxs) and len(s)<len(maxs):
                maxn = n
                maxs = s
                
        return maxn, maxs
        