import numpy as np
from match import Match
from tournament import Tournament
import json

with open('data.txt') as f:
    data = json.load(f)
    teams = data['Teams']
    
def cmd_teams(arg):
    idx=0
    for team in teams:
        idx += 1
        print(str(idx)+'.',team)
    
def cmd_match(arg):
    args = arg.split()
    teama = teams[int(args[1])-1]
    teamb = teams[int(args[2])-1]
    m = Match( teama, teamb )
    m.play()
    
def cmd_tournament(arg):
    t = Tournament()
    t.play()
    
def cmd_help(arg):
    print('Commands..')
    for k in commands.keys():
        print(k)
        
commands = { 'teams':cmd_teams, 'match':cmd_match, 'tournament':cmd_tournament, 'help':cmd_help }

while True:
    print('cmd>',end=' ')
    cmd = input()
    if cmd=='quit' or cmd=='exit':
        break
    
    func = cmd.split(' ',1)[0]
    if func not in commands:
        print('Command \''+func+'\' '+'not found! Type \'help\' to get list of commands.')
    else:
        commands[func](cmd)
        