import numpy as np
from match import Match
from tournament import Tournament
import json
import names

with open('data.txt') as f:
    data = json.load(f)
    teams = data['Teams']

default_team = None
    
def all_teams(arg):
    idx=0
    for team in teams:
        idx += 1
        print(str(idx)+'.',team)
    
def cmd_match(arg):
    args = arg.split()
    teama = teams[int(args[1])-1]
    teamb = teams[int(args[2])-1]
    m = Match( data, teama, teamb )
    m.play()
    
def cmd_tournament(arg):
    t = Tournament(data, default_team=default_team)
    t.play()
    
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
    
while True:
    print('cmd>',end=' ')
    cmd = input()
    if cmd=='quit' or cmd=='exit':
        break
    
    exec( cmd, globals() )
    