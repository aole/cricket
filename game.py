import numpy as np
from match import Match
from tournament import Tournament
from team import Team
import json
import names

def all_teams(arg):
    idx=0
    for team in teams:
        idx += 1
        print(str(idx)+'.',team)
    
def play_match(teama=None, teamb=None):
    if not teamb:
        teamb = teams[2]
    if not teama:
        teama = teams[0]
        
    m = Match( teama, teamb )
    m.play()
    
    global last_match
    last_match = m
    
def play_tournament():
    t = Tournament( teams, default_team=default_team )
    t.play()
    
    global last_tournament, last_match
    last_tournament = t
    last_match = t.final
    
def create_team( team ):
    '''
    Create a team.
    11 random players will be added.
    this will become the default team of the Coach.
    '''
    global default_team
    
    teams.append(team)
    default_team = team
    
    players=[]
    for i in range(11):
        name = names.get_full_name(gender='male')
        players.append(name)
    data[team]=players
    
    print_team( team )
    
def add_player( pos, name, team=None ):
    '''
    add new player to the default team at a specific position
    '''
    if not team:
        team = default_team
        
    data[team].insert(pos-1, name)
    
    print_team( team )
    
def print_team(team=None):
    if not team:
        team = default_team
        
    print('Team', team+':')
    cnt=1
    for p in data[team]:
        print(str(cnt)+'. '+p)
        cnt+=1

with open('data.txt') as f:
    data = json.load(f)
    # teams = data['Teams']
    teams = []
    for team in data['Teams']:
        teams.append( Team(team, data=data) )

default_team = None
last_match = None
last_tournament = None

while True:
    print('cmd>',end=' ')
    cmd = input()
    if cmd=='quit' or cmd=='exit':
        break
    
    exec( cmd, globals() )
    