import names

class Batsman:
    def __init__(self, team, name=None, prob=[6,   35,  39,  18,  4,   13,   5]):
        self.team = team
        self.prob = prob
        if name==None:
            name = names.get_full_name(gender='male')
        self.name = name

        self.score = {}
        
    def add_match(self, match, runs, is_out=False):
        out = 0 if is_out else 1
        self.score[match] = (runs,out)
    
    def get_total_runs(self):
        t = 0
        for m, s in self.score.items():
            t += sum(s[0])
        return t
    
    def get_average(self):
        t = 0
        w = 0
        for m, s in self.score.items():
            t += sum(s[0])
            w += s[1]
        
        if w==0:
            return -1
        else:
            return t/w
    
    def get_strikerate(self):
        t = 0
        b = 0
        for m, s in self.score.items():
            t += sum(s[0])
            b += len(s[0])
        
        if b==0:
            return -1
        else:
            return round((t/b)*100, 2)
    
if __name__ == '__main__':
    b = Batsman('Abc')
    print(b.name)
    