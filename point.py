
class Point:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ear = False
        self.name = -1
        self.next = None
        self.prev = None

    def ___str___(self):
        return self.name

    '''
    Compares this point to the given point. Only the x and y coordinates are compared.
    '''
    def equals(self, p):
        if p.x == self.x and p.y == self.y:
            return True
        return False

    '''
    Multiplies this point's x by k1 and y by k2.
    '''
    def scale(self, k1, k2):
        self.x = int(self.x * k1)
        self.y = int(self.y * k2)