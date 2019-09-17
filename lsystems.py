from collections import Counter
import turtle

class Lsystem:

    '''
    Based on: https://repl.it/@ELC/Drawing-Koch-Snowflake-With-Python
    '''

    def __init__(self, axiom, rules):
        self.axiom = axiom
        self.rules = rules
        self.instructions = None

    def generate(self, iters):
        if iters == 0:
            self.instructions = self.axiom
        else:
            init_str = self.axiom[:]
            ter_str = ''
            for _ in range(iters):
                ter_str = "".join(self.rules[i] if i in self.rules else i for i in init_str)
                init_str = ter_str
            self.instructions = ter_str

    def turtle_draw(self, angle, distance):
        t = turtle.Turtle()
        t.speed(10)
        t.hideturtle()
        saved_positions = []
        saved_angles = []
        for cmd in self.instructions:
            if cmd == 'F':
                t.forward(distance)
            elif cmd == 'B':
                t.backward(distance)
            elif cmd == '+':
                t.right(angle)
            elif cmd == '-':
                t.left(angle)
            elif cmd == '[':
                saved_positions.append(t.position())
                saved_angles.append(t.heading())
            elif cmd == ']':
                t.up()
                t.goto(saved_positions.pop())
                t.setheading(saved_angles.pop())
                t.down()
            else:
                print('WARNING: Unrecognized instruction: %s' % cmd)

    def mpl_draw(self, angle, distance):
        pass
              
L = Lsystem('X', {'X':'F+[[X]-X]-F[-FX]+X', 'F':'FF'})
L.generate(iters=7)
L.turtle_draw(25, 3)
