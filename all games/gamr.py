import random
import arcade
import os
import math
# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = 0.2
COIN_COUNT = 100
hard=5
rang=100
number=100
health=10
tear=4
speed=3
Shot_List=[arcade.key.UP,arcade.key.DOWN,arcade.key.LEFT,arcade.key.RIGHT]
Move_List=[arcade.key.W, arcade.key.A, arcade.key.S, arcade.key.D]
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Sprite Collect Coins Example"
'''
class Item(arcade.sprite):
    def __init(self,filename,factor):
        pass
'''
class Bullet(arcade.Sprite):
    def __init__(self,filename,factor,rang):
        super().__init__(filename,factor)
        self.change_x=0
        self.change_y=0
        self.rang=rang
    def update(self):
        if self.left < 0:
            self.kill()

        if self.right > SCREEN_WIDTH:
            self.kill()

        if self.bottom < 0:
            self.kill()

        if self.top > SCREEN_HEIGHT:
            self.kill()
        self.center_x+=self.change_x
        self.center_y+=self.change_y
        self.rang-=1
        if self.rang<=0:
            self.kill()
class MyGame(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)


        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)


        self.player_list = None
        self.coin_list = None
        self.bullet_list=None
        self.all_sprites_list = None
        self.player_sprite = None
        self.score = 0
        self.health=health
        self.tear=tear
        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.AMAZON)
        self.heart=arcade.load_texture('heart.png')
        self.hurt=0
    def setup(self):
        """ Set up the game and initialize the variables. """
        #setting
        # Sprite lists
        self.bullet_list=arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.bullet_list=arcade.SpriteList()
        self.all_sprites_list = arcade.SpriteList()
        # Score
        self.score = 0
        self.player_sprite = arcade.Sprite("character.png", SPRITE_SCALING_PLAYER,)
        self.player_sprite.center_x= 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)
        self.all_sprites_list.append(self.player_sprite)
        self.player_sprite.last_x=self.player_sprite.center_x
        self.player_sprite.last_y=self.player_sprite.center_y
        # Create the coins
        for i in range(number):

            coin = arcade.Sprite("coin.png", SPRITE_SCALING_COIN)

            # Position the coin
            wid=random.randrange(SCREEN_WIDTH)
            hei=random.randrange(SCREEN_HEIGHT)
            coin.center_x = wid
            coin.center_y = hei

            # Add the coin to the lists
            self.coin_list.append(coin)
            self.all_sprites_list.append(coin)

    def on_draw(self):
        """ Draw everything """
        arcade.start_render()
        self.all_sprites_list.draw()
    
        # Put the text on the screen.
        output = f"Score: {round(self.score,2)}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)
        for i in range(self.health):
            self.heart.draw(150+50*i,20,60,60)

    def update(self, delta_time):
        """ Movement and game logic """
        #print('updated')
        #stats change
        if self.tear!=0:
            self.tear-=1
        if self.hurt!=0:
            self.hurt-=1
        self.coin_list.update()
        self.bullet_list.update()
        self.player_sprite.update()

        coins_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
        '''
        for coin in self.coin_list:
            coin.center_x+=hard*(random.random()-0.5)
            coin.center_x%=SCREEN_WIDTH
            coin.center_y+=hard*(random.random()-0.5)
            coin.center_y%=SCREEN_HEIGHT
        '''
        for coin in self.coin_list:
            dis=hard*(random.random())/math.sqrt(abs(self.player_sprite.center_x-coin.center_x)**2+abs(self.player_sprite.center_y-coin.center_y)**2)
            coin.center_x+=(self.player_sprite.center_x-coin.center_x)*dis+hard*5*(random.random()-0.5)
            coin.center_x%=SCREEN_WIDTH
            coin.center_y+=(self.player_sprite.center_y-coin.center_y)*dis+hard*5*(random.random()-0.5)
            coin.center_y%=SCREEN_HEIGHT
        # Loop through each colliding sprite, remove it, and add to the score.
        if len(coins_hit_list)!=0 and self.hurt==0:
            self.health-=1
            self.hurt=100
            if self.health==0:
                self.player_sprite.kill()
                exit()
        for bullet in self.bullet_list:
            coins_kill_list=arcade.check_for_collision_with_list(bullet, self.coin_list)
            for coin in coins_kill_list:
                self.score+=1
                coin.kill()
            if len(coins_kill_list)!=0:
                bullet.kill()
    def on_key_press(self, key, modifiers):
        if key in Shot_List and self.tear==0:
            self.tear=tear
            if key==arcade.key.UP:#w
                
                bullet=Bullet("bullet1.png",0.2,rang)
                bullet.center_x,bullet.center_y=self.player_sprite.center_x,self.player_sprite.center_y
                bullet.change_x=self.player_sprite.change_x
                bullet.change_y=self.player_sprite.change_y+5
                self.all_sprites_list.append(bullet)
                self.bullet_list.append(bullet)
            elif key==arcade.key.LEFT:#a
                bullet=Bullet("bullet3.png",0.2,rang)
                bullet.center_x,bullet.center_y=self.player_sprite.center_x,self.player_sprite.center_y
                bullet.change_x=self.player_sprite.change_x-5
                bullet.change_y=self.player_sprite.change_y
                self.all_sprites_list.append(bullet)
                self.bullet_list.append(bullet)
            elif key==arcade.key.DOWN:#s
                bullet=Bullet("bullet4.png",0.2,rang)
                bullet.center_x,bullet.center_y=self.player_sprite.center_x,self.player_sprite.center_y
                bullet.change_x=self.player_sprite.change_x
                bullet.change_y=self.player_sprite.change_y-5
                self.all_sprites_list.append(bullet)
                self.bullet_list.append(bullet)
            elif key==arcade.key.RIGHT:#d
                bullet=Bullet("bullet2.png",0.2,rang)
                bullet.center_x,bullet.center_y=self.player_sprite.center_x,self.player_sprite.center_y
                bullet.change_x=self.player_sprite.change_x+5
                bullet.change_y=self.player_sprite.change_y
                self.all_sprites_list.append(bullet)
                self.bullet_list.append(bullet)
        if key in Move_List:
            if key==arcade.key.W:
                self.player_sprite.change_y=speed
            if key==arcade.key.A:
                self.player_sprite.change_x=-speed
            if key==arcade.key.S:
                self.player_sprite.change_y=-speed
            if key==arcade.key.D:
                self.player_sprite.change_x=speed
    def on_key_release(self, key, modifiers):
        if key in Move_List:
            if key==arcade.key.W:
                self.player_sprite.change_y=0
            if key==arcade.key.A:
                self.player_sprite.change_x=0
            if key==arcade.key.S:
                self.player_sprite.change_y=0
            if key==arcade.key.D:
                self.player_sprite.change_x=0
def main():
    """ Main method """
    print("Use WASD to move\nUse arrow keys to fire")
    window = MyGame()
    window.setup()
    arcade.run()

