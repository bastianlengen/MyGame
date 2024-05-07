class Data:
    def __init__(self, ui):
        # Private attributes
        self._ducks = 0
        self._health = 5

        # UI
        self.ui = ui 


    @property
    def ducks(self):
        return self._ducks

    @ducks.setter
    def ducks(self,value):
        self._ducks = value
        #self.ui.draw_ducks(self.ducks)

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = value
        #self.ui.draw_hearts(self.health)


