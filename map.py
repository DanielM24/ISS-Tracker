from turtle import Turtle, Screen


class Map:
    def __init__(self):
        self.screen = Screen()
        self.screen.setup(width=1200, height=600)
        self.screen.title('ISS Tracker')
        self.screen.setworldcoordinates(-180, -90, 180, 90)

        self.screen.register_shape('images/home.gif')
        self.screen.register_shape('images/iss.gif')

        self.iss = Turtle()
        self.iss.penup()

        self.home = Turtle()
        self.home.penup()

    def choose_background(self, map_type):
        if map_type == 'day':
            self.screen.bgpic("images/world_day.png")
        elif map_type == 'night':
            self.screen.bgpic("images/world_night.png")

    def position_home(self, user_cord: tuple):
        self.home.shape('images/home.gif')
        self.home.speed('fastest')
        self.home.goto(user_cord[0], user_cord[1])

    def position_iss(self, iss_cord: tuple):
        self.iss.shape('images/iss.gif')
        self.iss.speed('fastest')
        self.iss.goto(iss_cord[0], iss_cord[1])
