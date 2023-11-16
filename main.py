import pygame as py
import math

class LineState:
    def __init__(self, x1, y1, x2, y2, colour):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.colour = colour

class TurtleState:
    def __init__(self):
        self.name = "Unknown"
        self.x = 640
        self.y = 360
        self.theta = 90.0
        self.pen_down = True
        self.colour = "black"

    def set_colour(self, colour):
        self.colour = colour

    def move(self, dist):
        th = math.radians(self.theta)
        self.x = self.x + dist * math.cos(th)
        self.y = self.y - dist * math.sin(th)

    def turn_left(self, angle):
        self.theta = self.theta + angle

    def turn_right(self, angle):
        self.theta = self.theta - angle

    def set_pen_up(self):
        self.pen_down = False

    def set_pen_down(self):
        self.pen_down = True

class TurtleGui:

    def __init__(self):
        py.init()
        self.screen = py.display.set_mode((1280, 720))
        self.clock = py.time.Clock()
        self.running = True

        self.turtles = {}
        self.lines = []

        self.last_turtle = ""

        self.bg_color = "white"
        self.screen.fill(self.bg_color)
        py.display.flip()

    def run(self):

        while self.running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in py.event.get():
                if event.type == py.QUIT:
                    self.running = False

            cmd = input('> ')
            cmd = cmd.strip()
            if cmd == "quit":
                break

            self.execute_cmd(cmd)

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill(self.bg_color)

            # draw the turtle
            for tname, tstate in self.turtles.items():
                self.draw_turtle(tstate)
                if self.last_turtle != "":
                    self.lines.append(self.last_line_state)

            for ls in self.lines:
                # print(ls.x1, ls.y1, ls.x2, ls.y2)
                py.draw.line(self.screen, ls.colour, (ls.x1, ls.y1), (ls.x2, ls.y2), 3)

            # flip() the display to put your work on screen
            py.display.flip()

            # add some delay
            self.clock.tick(60)  # limits FPS to 60

    def execute_cmd(self, cmd):
        cmd_tokens = cmd.split()
        self.last_turtle = ""
        match cmd_tokens[0]:
            case "turtle":
                if len(cmd_tokens) != 2:
                    print("Error: incorrect number of arguments")
                    return
                turtle_name = cmd_tokens[1]
                if turtle_name in self.turtles:
                    print("Error: turtle alreay exists")
                    return
                self.turtles[turtle_name] = TurtleState()
            case "colour":
                if len(cmd_tokens) != 3:
                    print("Error: incorrect number of arguments")
                    return
                turtle_name = cmd_tokens[1]
                if turtle_name not in self.turtles:
                    print("Error: no such turtle")
                    return
                c = cmd_tokens[2]
                self.turtles[turtle_name].set_colour(c)
            case "move":
                if len(cmd_tokens) != 3:
                    print("Error: incorrect number of arguments")
                    return
                turtle_name = cmd_tokens[1]
                if turtle_name not in self.turtles:
                    print("Error: no such turtle")
                    return
                dist = int(cmd_tokens[2])
                x1 = self.turtles[turtle_name].x
                y1 = self.turtles[turtle_name].y
                self.turtles[turtle_name].move(dist)
                x2 = self.turtles[turtle_name].x
                y2 = self.turtles[turtle_name].y
                self.last_line_state = LineState(x1, y1, x2, y2, self.turtles[turtle_name].colour)
                if self.turtles[turtle_name].pen_down:
                    self.last_turtle = turtle_name
            case "left":
                if len(cmd_tokens) != 3:
                    print("Error: incorrect number of arguments")
                    return
                turtle_name = cmd_tokens[1]
                if turtle_name not in self.turtles:
                    print("Error: no such turtle")
                    return
                th = int(cmd_tokens[2])
                self.turtles[turtle_name].turn_left(th)
            case "right":
                if len(cmd_tokens) != 3:
                    print("Error: incorrect number of arguments")
                    return
                turtle_name = cmd_tokens[1]
                if turtle_name not in self.turtles:
                    print("Error: no such turtle")
                    return
                th = int(cmd_tokens[2])
                self.turtles[turtle_name].turn_right(th)
            case "pen":
                if len(cmd_tokens) != 3:
                    print("Error: incorrect number of arguments")
                    return
                turtle_name = cmd_tokens[1]
                if turtle_name not in self.turtles:
                    print("Error: no such turtle")
                    return
                match cmd_tokens[2]:
                    case "up":
                        self.turtles[turtle_name].set_pen_up()
                    case "down":
                        self.turtles[turtle_name].set_pen_down()

    def draw_turtle(self, turtle):
        py.draw.circle(self.screen, turtle.colour, (turtle.x, turtle.y), 10)


if __name__ == '__main__':
    turtle_gui = TurtleGui()
    turtle_gui.run()
    py.quit()
