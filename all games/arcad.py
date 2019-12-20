import arcade
import numpy
import copy
import random
import time

score=0

class MyGame(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height, title,block,time,score):
        super().__init__(width, height, title)
        self.block=block
        self.time=time
        arcade.set_background_color(arcade.color.WHITE)
        self.fall=False
        self.score=score
        # If you have sprite lists, you should create them here,
        # and set them to None

    def setup(self):
        # Create your sprites and sprite lists here\
        global lis
        global nex
        lis=[[[0,0],[0,-1],[1,-1],[1,-2],(0, 106, 78)],[[0,0],[0,-1],[0,-2],[0,-3],(132, 27, 45)],
             [[0,0],[0,-1],[0,-2],[1,-1],(2, 222, 205)],[[0,0],[0,-1],[1,0],[1,-1],(61, 29, 31)],
             [[0,0],[0,-1],[-1,-1],[-1,-2],(86, 130, 3)],[[0,0],[0,-1],[0,-2],[1,0],(148, 0, 211)],
             [[0,0],[1,0],[1,-1],[1,-2],(253, 63, 146)]]
        nex=lis[random.randint(0,len(lis)-1)].copy()

    def on_draw(self):
        time.sleep(0.25)
        """
        Render the screen.
        """
        global falling
        global initpos
        global lastpos
        global lastfall
        global score
        global nex
        #last- to clear the blocks from last frame
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()
        for i in range(0,601,20):
            arcade.draw_commands.draw_line(0,i,400,i,arcade.color.BLACK,1)
        for i in range(0,401,20):
            arcade.draw_commands.draw_line(i,0,i,600,arcade.color.BLACK,1)
        
        if not self.fall:
            falling=nex.copy()
            nex=lis[random.randint(0,len(lis)-1)].copy()
            initpos=[random.randint(5,15),29]
            lastpos=initpos.copy()
            lastfall=falling.copy()
            self.fall=True
            # Call draw() on all your sprite lists below
        else:
            initpos[1]-=1
        for i in range(len(lastfall)-1):
                self.block[(lastpos[0]+lastfall[i][0])%20][lastpos[1]+lastfall[i][1]]=0
        tmp=False
        for i in range(len(falling)-1):
                self.block[(initpos[0]+falling[i][0])%20][initpos[1]+falling[i][1]]=falling[-1]
                if initpos[1]+falling[i][1]==0:
                    tmp=True
                if [falling[i][0],falling[i][1]-1] not in falling:
                    if self.block[(initpos[0]+falling[i][0])%20][initpos[1]+falling[i][1]-1]!=0:
                        tmp=True
        if tmp:
            self.fall=False
            for i in self.block:
                if i[-1]!=0:
                    arcade.draw_text('YOU LOSE',100,200,arcade.color.RED,100)
        lastpos=copy.deepcopy(initpos)
        lastfall=copy.deepcopy(falling)
        for a in range(len(self.block)):
            for b in range(len(self.block[a])):
                if self.block[a][b]==0:
                    continue
                else:
                    arcade.draw_commands.draw_rectangle_filled(10.5+a*20,10.5+b*20,19,19,self.block[a][b],0)
        tpp=10
        for b in range(30):
            tmp=True
            for a in range(20):
                if self.block[a][b]==0:
                    tmp=False
                    break
            if tmp:
                score+=tpp
                tpp*=2
                for k in range(b,29):
                    for c in range(20):
                        self.block[c][k]=copy.deepcopy(self.block[c][k+1])
                print(score)
        arcade.draw_text(str(score),20,625,arcade.color.BLACK,25)
        arcade.draw_text('NEXT',230,615,arcade.color.BLACK,25)
        for i in range(len(falling)):
            a=nex[i][0]
            b=nex[i][1]
            arcade.draw_commands.draw_rectangle_filled(10.5+15*(21+a),10.5+(33+b)*20,19,19,nex[-1],0)

    def update(self, delta_time):    
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        pass

    def on_key_press(self, key, key_modifiers):
        global initpos
        global falling
        tmp=falling.copy()
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        if initpos[1]<30:
            if key==97:
                initpos[0]-=1
                dp=False
                for i in range(len(falling)-1):
                        if self.block[(initpos[0]+falling[i][0]-1)%20][initpos[1]+falling[i][1]]!=0 and [falling[i][0]-1,falling[i][1]] not in tmp:
                            dp=True
                if dp:
                    initpos[0]+=1
                    dp=False
            if key==100:
                initpos[0]+=1
                dp=False
                for i in range(len(falling)-1):
                        if self.block[(initpos[0]+falling[i][0]+1)%20][initpos[1]+falling[i][1]]!=0 and [falling[i][0]+1,falling[i][1]] not in tmp:
                            dp=True
                if dp:
                    initpos[0]-=1
                    dp=False
            if key==119:
                
                falling[0]=[falling[0][1],-falling[0][0]]
                falling[1]=[falling[1][1],-falling[1][0]]
                falling[2]=[falling[2][1],-falling[2][0]]
                falling[3]=[falling[3][1],-falling[3][0]]
                dp=False
                for i in range(len(falling)-1):
                        if self.block[(initpos[0]+falling[i][0])%20][initpos[1]+falling[i][1]]!=0 and [falling[i][0],falling[i][1]] not in tmp:
                            dp=True
                if dp:
                    falling=copy.deepcopy(tmp)
                    dp=False
            if key==115:
                falling[0]=[-falling[0][1],falling[0][0]]
                falling[1]=[-falling[1][1],falling[1][0]]
                falling[2]=[-falling[2][1],falling[2][0]]
                falling[3]=[-falling[3][1],falling[3][0]]
                dp=False
                for i in range(len(falling)-1):
                        if self.block[(initpos[0]+falling[i][0])%20][initpos[1]+falling[i][1]]!=0 and [falling[i][0],falling[i][1]] not in tmp:
                            dp=True
                if dp:
                    falling=copy.deepcopy(tmp)
                    dp=False
            if key==32:
                tp=False
                while not tp:
                    tp=False
                    for i in range(len(falling)-1):
                            if initpos[1]+falling[i][1]==0:
                                tp=True
                            if [falling[i][0],falling[i][1]-1] not in falling:
                                if self.block[(initpos[0]+falling[i][0])%20][initpos[1]+falling[i][1]-1]!=0:
                                    tp=True
                    initpos[1]-=1
                initpos[1]+=2
    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass
def main():
    block=[]
    for a in range(20):
        block.append([0,0,0,0,0,0,0,0,0,0,0,0,0,(123,142,75),0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    SCREEN_WIDTH = 400
    SCREEN_HEIGHT = 681
    SCREEN_TITLE = "Starting Template"
    print("Use WASD and space to control")
    game= MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE,block,0,0)
    game.setup()
    arcade.run()
