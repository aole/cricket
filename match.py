import numpy as np
import json
from copy import deepcopy

result_type = ['Wk','0', '1', '2', '3', '4', '6']
result_prob = [6,   35,  39,  18,  4,   13,   5]
result_prob = result_prob/np.sum(result_prob) # sum up to 1

matchid = 0
    
class Match:

    def __init__(self, teama=None, teamb=None):
        self.complete = False
        self.winner = None
        self.batsman_score = {}
        self.bowler_score = {}
        
        global matchid
        self.id = matchid
        matchid += 1
        
        self.init(teama, teamb)
        
    def init( self, teama, teamb ):
        if teama==None or teamb==None:
            return
            
        self.team1 = deepcopy( teama )
        self.team2 = deepcopy( teamb )
        
        coin = np.random.randint(0,2)
        if coin==1:
            self.team1, self.team2 = self.team2, self.team1
        
        self.toss = self.team2
        
    def __str__( self ):
        s = '#'+str(self.id)+' '
        if self.complete:
            if self.by_runs:
                s+=self.winner.name+ ' beat '+ self.looser.name+ ' by '+ str(self.by_runs)+' runs!'
            else:
                s+=self.winner.name+ ' beat '+ self.looser.name+ ' by '+ str(self.by_wickets)+' wickets!'
        else:
            s+=self.team1.name+ ' vs '+self.team2.name
        return s
    
    def __repr__( self ):
        return self.__str()
        
    def record( self, over, ball, runs, batsman, doubling, bowler, out=False):
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
        if batsman not in self.batsman_score:
            return -1, -1, None
        
        bw = self.batsman_score[batsman]['bowler']
        if bw:
            bw = 'b '+ bw
        else:
            bw = '*\t'
        return sum(self.batsman_score[batsman]['runs']), len(self.batsman_score[batsman]['runs']), bw
        
    def print_scoreboard(self):
        print( 'Match between', self.team1.name, 'and', self.team2.name )
        for team in [self.team1, self.team2]:
            print(team.name+'\'s inings...')
            for i in range(1, 12):
                p = team.get_batsman(i)
                bsr, bsb, bsbw = self.get_batsman_score( p )
                if bsr<0:
                    continue
                print( '   '+str(i)+'. '+p+'\t'+bsbw+'\t'+str(bsr)+' ('+str(bsb)+')' )
            
            print()
            
            for bowler, score in self.bowler_score.items():
                if score['team']==team:
                    continue
                bls = len(score['runs'])
                bo = bls//6
                bb = bls%6
                runs = sum(score['runs'])
                wkts = np.count_nonzero(score['wickets'])
                
                print( '   '+bowler+'\t'+str(bo)+'.'+str(bb)+' - '+str(runs)+' - '+str(wkts) )
                
            print()
            
            print('  '+team.name, 'scored', str(team.score)+'/'+str(team.wickets), 'in '+str(team.overs)+'.'+str(team.balls))
            
            print()
        
        print('  Man of the Match: '+self.mom[0]+'\t'+self.mom[1]+' ('+self.mom[2]+')')
        
        print ('  '+self.__str__())
        
        print()
        
    def play( self, verbose=True ):
        self.team1.score = self.team2.score = None
        
        for teambt, teambl in [[self.team1, self.team2],[self.team2, self.team1]]:
            teambt.score = 0
            teambt.wickets = 0
            
            batsman_facing = teambt.get_batsman(1)
            batsman_doubling = teambt.get_batsman(2)
            next_batsman_index = 3
            
            self.batsman_score[batsman_facing]={'team':teambt, 'runs':[],'out':False, 'bowler':None}
            self.batsman_score[batsman_doubling]={'team':teambt, 'runs':[],'out':False, 'bowler':None}
            
            for over in range(20):
                
                bowler = teambl.get_bowler(over+1)
                if bowler not in self.bowler_score:
                    self.bowler_score[bowler] = {'team':teambl, 'runs':[], 'wickets':[]}
                    
                for ball in range(1,7):
                    r = np.random.choice(result_type, p=result_prob)
                    
                    if r=='Wk':
                        teambt.wickets += 1
                        
                        self.record( over, ball, 0, batsman_facing, batsman_doubling, bowler, True )
                        
                        if teambt.wickets > 9:
                            break
                            
                        batsman_facing = teambt.get_batsman(next_batsman_index)
                        self.batsman_score[batsman_facing] = {'team':teambt, 'runs':[],'out':False, 'bowler':None}
                        
                        next_batsman_index += 1
                        
                    else:
                        r = int(r)
                        # add runs scored
                        teambt.score += r
                        
                        self.record( over, ball, r, batsman_facing, batsman_doubling, bowler )
                        
                        if teambl.score and teambt.score>teambl.score:
                            break
                        
                        # swap batsmen if odd runs
                        if r==1 or r==3:
                            batsman_facing, batsman_doubling = batsman_doubling, batsman_facing
                
                if teambt.wickets > 9:
                    break
            
                if teambl.score and teambt.score>teambl.score:
                    break
                
                # swap the batmen at the end of the over
                batsman_facing, batsman_doubling = batsman_doubling, batsman_facing
            
            teambt.overs = over if ball<6 else over+1
            teambt.balls = ball if ball<6 else 0
        
        # result
        
        self.complete = True
        if self.team1.score>self.team2.score:
            self.winner = self.team1
            self.looser = self.team2
            self.by_runs = self.team1.score-self.team2.score
            self.by_wickets = None
        # elif self.score[1] > self.score[0]:
        # TODO: Handle ties
        else:
            self.winner = self.team2
            self.looser = self.team1
            self.by_runs = None
            self.by_wickets = 10-self.team2.wickets
            
        # man of the match
        mm, mms, mmb = self.get_motm()
        self.mom = (mm, str(mms), str(mmb))
        
        if verbose:
            self.print_scoreboard()
        
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
        