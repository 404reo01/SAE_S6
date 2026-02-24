
class LirePoints:
    def __init__(self, chemin):
        self.chemin = chemin

    def get_Points(self) :
        PPP = []
        with open(self.chemin , 'r') as f:
            for couple in f.readlines() :
                PPP.append(tuple(map(float, couple.strip().split(','))))
        return PPP