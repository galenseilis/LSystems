from collections import Counter
import numpy as np
import turtle
import matplotlib.pyplot as plt
import random

class Lsystem:

    '''
    [ Push position
    ] Pop position
    ( Push angle
    ) Pop angle
    { Push distance
    } Pop distance
    D Increase distance increment
    d Decrease distance increment
    M Move forward (no drawing)
    + Turn left by angle
    - Turn right by angle
    A Increase angle increment
    a Decrease angle increment
    F Draw forward
    Q Switch to queu behaviour
    q Switch to stack behaviour

    Sources:
        https://repl.it/@ELC/Drawing-Koch-Snowflake-With-Python
    '''

    def __init__(self, axiom, rules):
        self.alphabet = (list('[](){}DdM+-AaFQq!'))
        self.axiom = axiom
        self.rules = rules
        self.instructions = None

    def shuffle_rules(self):
        '''
        Sources:
        https://stackoverflow.com/questions/19895028/randomly-shuffling-a-dictionary-in-python
        '''
        L = list(self.rules.items())
        random.shuffle(L)
        self.rules = dict(L)
        

    def generate(self, iters):
        if iters == 0:
            self.instructions = self.axiom
        else:
            init_str = self.axiom[:]
            ter_str = ''
            for _ in range(iters):
                self.shuffle_rules()
                ter_str = "".join(self.rules[i] if i in self.rules else i for i in init_str)
                init_str = ter_str
            self.instructions = ter_str

    def mpl_draw(self, angle, distance, cmap=plt.cm.nipy_spectral):
        plt.style.use('dark_background')
        plt.figure(figsize=(1.920, 1.080), dpi=100)
        plt.axis('off')
        colors = cmap(np.linspace(0,1,len(self.instructions)))
        current_position = [0, 0]
        current_angle = 0
        turn_meaning = 1
        saved_positions = []
        saved_angles = []
        c = 0
        for i, cmd in enumerate(self.instructions):
            print(i, cmd, (i+1) / len(self.instructions) * 100)
            if cmd == 'F':
                # Move and draw forward
                old_position = current_position[:]
                current_position[0] += distance * np.cos(current_angle)
                current_position[1] += distance * np.sin(current_angle)
                plt.plot([old_position[0],
                          current_position[0]],
                         [old_position[1],
                          current_position[1]],
                         linewidth=0.1,
                         c=colors[i])
                plt.savefig('step_{}.png'.format(str(c).zfill(len(str(len(self.instructions))))),
                        dpi=1000)
                c += 1
            elif cmd == 'M':
                # Move forward but not draw
                old_position = current_position[:]
                current_position[0] += distance * np.cos(current_angle)
                current_position[1] += distance * np.sin(current_angle)
                c += 1
            elif cmd == '+':
                if turn_meaning:
                    current_angle -= angle
                else:
                    current_angle += angle
            elif cmd == '-':
                if turn_meaning:
                    current_angle += angle
                else:
                    current_angle -= angle
            elif cmd == '[':
                saved_positions.append(current_position[:])
            elif cmd == ']':
                current_position = saved_positions.pop()
            elif cmd == '(':
                saved_angles.append(current_angle)
            elif cmd == ')':
                current_angle = saved_angles.pop()
            elif cmd == '!':
                if turn_meaning == 1:
                    turn_meaning -= 1
                else:
                    turn_meaning += 1

L = Lsystem('++FX', {'X':'[(-FX)]+FX'})
L.generate(11)
print(len(L.instructions))
L.mpl_draw(np.pi/8, 1, cmap=plt.cm.hsv)
