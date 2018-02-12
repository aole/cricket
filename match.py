import numpy as np
import json

result_type = ['Wk','0', '1', '2', '3', '4', '6']
result_prob = [6,   35,  39,  18,  4,   13,   5]
result_prob = result_prob/np.sum(result_prob) # sum up to 1

class Match:
    def __init__(self, teama=None, teamb=None):
        self.complete = False
        self.winner = None
        self.batsman_score = {}
        self.bowler_score = {}
        self.init(teama, teamb)
        
    def init( self, teama, teamb ):
        if teama==None or teamb==None:
            return
            
        self.team1 = teama
        self.team2 = teamb
        
        coin = np.random.randint(0,2)
        if coin==1:
            self.team1, self.team2 = self.team2, self.team1
        
    def record( self, over, ball, runs, batsman, bowler, out=False):
        assert batsman in self.batsman_score, batsman
        assert bowler in self.bowler_score, bowler
        
        self.batsman_score[batsman]['runs'].append( runs )
        self.bowler_score[bowler]['runs'].append( runs )
        if out:
            self.batsman_score[batsman]['out'] = True
            self.batsman_score[batsman]['bowler'] = bowler
            self.bowler_score[bowler]['wickets'].append( batsman )
        else:
            self.bowler_score[bowler]['wickets'].append( '' )
        
    def get_batsman_score( self, batsman ):
        assert batsman in self.batsman_score
        
        bw = self.batsman_score[batsman]['bowler']
        if bw:
            bw = 'b '+ bw
        else:
            bw = '*\t'
        return sum(self.batsman_score[batsman]['runs']), len(self.batsman_score[batsman]['runs']), bw
            
    def play( self ):
        print( 'Match between', self.team1.name, 'and', self.team2.name )
        
        self.score = [0,0]
        self.wickets = [0,0]
        
        batsman_facing = self.team1.get_batsman(1)
        batsman_doubling = self.team1.get_batsman(2)
        next_batsman_index = 3
        
        self.batsman_score[batsman_facing]={'team':self.team1, 'runs':[],'out':False, 'bowler':None}
        self.batsman_score[batsman_doubling]={'team':self.team1, 'runs':[],'out':False, 'bowler':None}
        
        # first inings
        print(self.team1.name, 'innings...')
        for over in range(20):
            
            bowler = self.team2.get_bowler(over+1)
            if bowler not in self.bowler_score:
                self.bowler_score[bowler] = {'team':self.team2, 'runs':[], 'wickets':[]}
                
            for ball in range(1,7):
                r = np.random.choice(result_type, p=result_prob)
                
                if r=='Wk':
                    self.wickets[0] += 1
                    
                    self.record( over, ball, 0, batsman_facing, bowler, True )
                    
                    if self.wickets[0] > 9:
                        break
                        
                    batsman_facing = self.team1.get_batsman(next_batsman_index)
                    self.batsman_score[batsman_facing] = {'team':self.team1, 'runs':[],'out':False, 'bowler':None}
                    
                    next_batsman_index += 1
                    
                else:
                    r = int(r)
                    # add runs scored
                    self.score[0] += r
                    
                    self.record( over, ball, r, batsman_facing, bowler )
                    
                    # swap batsmen if odd runs
                    if r==1 or r==3:
                        batsman_facing, batsman_doubling = batsman_doubling, batsman_facing
            
            if self.wickets[0] > 9:
                break
        
            # swap the batmen at the end of the over
            batsman_facing, batsman_doubling = batsman_doubling, batsman_facing
        
        for i in range(1, next_batsman_index):
            p = self.team1.get_batsman(i)
            bsr, bsb, bsbw = self.get_batsman_score( p )
            assert bsr!=None, str(i)+':'+p+':'+str(self.batsman_score)
            print( '   '+str(i)+'. '+p+'\t'+bsbw+'\t'+str(bsr)+' ('+str(bsb)+')' )
        
        print()
        
        for bowler, score in self.bowler_score.items():
            if score['team']==self.team1:
                continue
            bls = len(score['runs'])
            bo = bls//6
            bb = bls%6
            runs = sum(score['runs'])
            wkts = np.count_nonzero(score['wickets'])
            
            print( '   '+bowler+'\t'+str(bo)+'.'+str(bb)+' - '+str(runs)+' - '+str(wkts) )
            
        print()
        
        print('  '+self.team1.name, 'scored', str(self.score[0])+'/'+str(self.wickets[0]), 'in '+str(over if ball<6 else over+1)+'.'+str((ball if ball<6 else '')))
        
        print()
        
        # second inings
        batsman_facing = self.team2.get_batsman(1)
        batsman_doubling = self.team2.get_batsman(2)
        next_batsman_index = 3
        
        self.batsman_score[batsman_facing]={'team':self.team2, 'runs':[],'out':False, 'bowler':None}
        self.batsman_score[batsman_doubling]={'team':self.team2, 'runs':[],'out':False, 'bowler':None}
        
        print(self.team2.name, 'innings...')
        for over in range(20):
            
            bowler = self.team1.get_bowler(over+1)
            if bowler not in self.bowler_score:
                self.bowler_score[bowler] = {'team':self.team1, 'runs':[], 'wickets':[]}
            
            for ball in range(1,7):
                r = np.random.choice(result_type, p=result_prob)
                
                if r=='Wk':
                    self.wickets[1] += 1
                    
                    self.record( over, ball, 0, batsman_facing, bowler, True )
                    
                    if self.wickets[1] > 9:
                        break
                        
                    batsman_facing = self.team2.get_batsman(next_batsman_index)
                    self.batsman_score[batsman_facing] = {'team':self.team2, 'runs':[],'out':False, 'bowler':None}
                    
                    next_batsman_index += 1
                else:
                    r = int(r)
                    # add runs scored
                    self.score[1] += r
                    
                    self.record( over, ball, r, batsman_facing, bowler )
                    
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
        
        for i in range(1, next_batsman_index):
            p = self.team2.get_batsman(i)
            bsr, bsb, bsbw = self.get_batsman_score( p )
            assert bsr!=None, str(i)+':'+p+':'+str(self.batsman_score)
            print( '   '+str(i)+'. '+p+'\t'+bsbw+'\t'+str(bsr)+' ('+str(bsb)+')' )
        
        print()
        
        for bowler, score in self.bowler_score.items():
            if score['team']==self.team2:
                continue
            bls = len(score['runs'])
            bo = bls//6
            bb = bls%6
            runs = sum(score['runs'])
            wkts = np.count_nonzero(score['wickets'])
            
            print( '   '+bowler+'\t'+str(bo)+'.'+str(bb)+' - '+str(runs)+' - '+str(wkts) )
            
        print()
        
        print('  '+self.team2.name, 'scored', str(self.score[1])+'/'+str(self.wickets[1]), 'in '+str(over if ball<6 else over+1)+'.'+str((ball if ball<6 else '')))
        
        # result
        self.complete = True
        if self.score[0] > self.score[1]:
            print ('  '+self.team1.name, 'beat', self.team2.name, 'by', str(self.score[0]-self.score[1]),'runs!')
            self.winner = self.team1
        # elif self.score[1] > self.score[0]:
        # TODO: Handle ties
        else:
            print ('  '+self.team2.name, 'beat', self.team1.name, 'by', str(10-self.wickets[1]),'wickets!')
            self.winner = self.team2
            
        # man of the match
        mm, mms, mmb = self.get_motm()
        print('  Man of the Match: '+mm+'\t'+str(mms)+' ('+str(mmb)+')')
        
        print()
        
        return self.winner

    def get_motm(self):
        maxn = None
        maxs = 0
        maxb = 0
        for n, b in self.batsman_score.items():
            r, bl, _ = self.get_batsman_score( n )
            if r>maxs:
                maxn = n
                maxs = r
                maxb = bl
            elif r==maxs and bl<maxb:
                maxn = n
                maxs = r
                maxb = bl
                
        return maxn, maxs, maxb
        