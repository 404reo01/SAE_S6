class CalculerGerme:
    def __init__(self, points):
        self.points = points

    def plus_proche(self, coin_x, coin_y) : 
        res = 0
        nb_PPP = len(self.points)
        for i in range(nb_PPP) : 
            xres = self.points[res][0]
            yres = self.points[res][1]
            xi = self.points[i][0]
            yi = self.points[i][1]
            if((coin_x-xres)**2+(coin_y-yres)**2>(coin_x-xi)**2+(coin_y-yi)**2) : res = i
        return res