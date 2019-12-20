import arcade
import random
import os
import math
SW=600
SH=650
ST="DDD"
delta_time=0.01
directions=[[-1,0],[1,0],[0,-1],[0,1]]
file_list=['blue.png','red.png','green.png','ocean.png','dpurple.png','purple.png','orange.png','rainbow.png','brown.png','yellow.png','rose.png']
color_list=[arcade.load_texture(n) for n in file_list]
class MyGame(arcade.Window):
    def __init__(self):
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        super().__init__(SW,SH,ST)
        arcade.set_background_color(arcade.color.WHITE)
    def setup(self):
        self.PP=0
        self.time=60
        self.lico=arcade.color.GREEN
        self.board=[[None for _ in range(21)] for __ in range(21)]
        self.draob=[[None for _ in range(21)] for __ in range(21)]
        self.score=0
        back=arcade.load_texture('1.png')
        back.draw(300,300,600,600)
        for i in range(21):
            for j in range(21):
                if random.randint(1,10)>2:
                    qwq=random.randint(0,len(color_list)-1)
                    self.board[i][j]=color_list[qwq]
                    self.draob[i][j]=file_list[qwq]
             
    def on_draw(self):
        arcade.start_render()
        #print('dran')
        
        for i in range(21):
            arcade.draw_line(0,30*i,600,30*i,arcade.color.BLACK,1)
        for i in range(21):
            arcade.draw_line(30*i,0,30*i,600,arcade.color.BLACK,1)
        
        for i in range(21):
            for j in range(21):
                if self.board[i][j]!=None:
                    self.board[i][j].draw(30*i-15,30*j-15,20,20)
        arcade.draw_text('Score:',50,625,arcade.color.BLACK,20)
        arcade.draw_text(str(self.PP),120,625,arcade.color.BLACK,20)
        arcade.draw_line(200,625,200+(self.time*5),625,self.lico,40)
        self.lico=arcade.color.GREEN
    def update(self,delta_time):
        self.time-=delta_time
        
    def on_mouse_press(self,x,y,button,modifiers):
        
        if y<=600:
            tmp=True
            px=(x)//30+1
            py=(y)//30+1
            #print(px,py,self.board[px][py])
            if self.board[px][py]!=None:
                self.lico=arcade.color.RED
                self.time-=2
                return
            f=[]
            z=[]
            #print(px,py)
            for i in directions:
                x=px
                y=py
                while x>-1 and x<21 and y>-1 and y<21 and self.board[x][y]==None:
                    x+=i[0]
                    y+=i[1]
                if x<=0 or x>=21 or y<=-1 or y>=21:
                    continue
                f.append(self.draob[x][y])
                z.append((x,y))
            #print('ffffffffffff',f)
            
            colot=[]
            bk=False
            for color in file_list:
                #print('num',f.count(color))
                if f.count(color)>=2:
                    for c in range(len(f)):
                        if f[c] == color:
                            tmp=False
                            self.PP+=10
                            self.board[z[c][0]][z[c][1]]=None
                            self.draob[z[c][0]][z[c][1]]=None
                            #print('remove',z[c][0],z[c][1])
            if tmp:
                self.lico=arcade.color.RED
                self.time-=2
                            



                                
                    
            
                    
def main():
    print("Click on the empty grid to play the game!")
    window = MyGame()
    window.setup()
    arcade.run()

