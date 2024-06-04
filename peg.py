class Peg():

    def __init__(self, x, y, in_play, row, column):
        # x position of peg
        self._x = x

        # y position of peg
        self._y = y

        # 1 if in play, else 0
        self._in_play = in_play

        # row peg is in (0 indexed)
        self._row = row

        # column peg is in (0 indexed)
        self._column = column

    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, y):
        self._y = y

    @property
    def in_play(self):
        return self._in_play
    
    @in_play.setter
    def in_play(self, in_play):
        self._in_play = in_play

    @property
    def row(self):
        return self._row
    
    @row.setter
    def row(self, row):
        self._row = row

    @property
    def column(self):
        return self._column
    
    @column.setter
    def column(self, column):
        self._column = column