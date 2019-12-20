import arcad
import time
import turtlependulum
import gamr
import q1
try:
    import arcade
except:
    print("please install arcade library(pip install arcade)")
    exit()
print("...")
print("THE GAME WINDOW MAY APPEAR BEHIND THIS WINDOW!")
while True:
    a=int(input('Which game do you want to Play?\n1.Tetris\n2.double pendulum\n3.another game\n4.a strange game\n'))
    if a==1:
        arcad.main()
    if a==2:
        try:
            turtlependulum.main()
        except Exception:
            pass
        print("Ignore these error messages")
    if a==3:
        gamr.main()
    if a==4:
        q1.main()
        

