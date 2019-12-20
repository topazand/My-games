from math import sin,cos
import numpy as np
from scipy.integrate import odeint
import time

g = 9.8
len1=100
len2=100
l1tag=False
l2tag=False
class DoublePendulum(object):
    def __init__(self, m1, m2, l1, l2):
        self.m1, self.m2, self.l1, self.l2 = m1, m2, l1, l2
        self.init_status = np.array([np.pi/2,np.pi/2,0.0,0.0])
        
    def equations(self, w, t):
        """
        微分方程公式
        """
        m1, m2, l1, l2 = self.m1, self.m2, self.l1, self.l2
        th1, th2, v1, v2 = w
        dth1 = v1
        dth2 = v2
        
        #eq of th1
        a = l1*l1*(m1+m2)  # dv1 parameter
        b = l1*m2*l2*cos(th1-th2) # dv2 paramter
        c = l1*(m2*l2*sin(th1-th2)*dth2*dth2 + (m1+m2)*g*sin(th1))
        
        #eq of th2
        d = m2*l2*l1*cos(th1-th2) # dv1 parameter
        e = m2*l2*l2 # dv2 parameter
        f = m2*l2*(-l1*sin(th1-th2)*dth1*dth1 + g*sin(th2))
        
        dv1, dv2 = np.linalg.solve([[a,b],[d,e]], [-c,-f])
        
        return np.array([dth1, dth2, dv1, dv2])
        
def double_pendulum_odeint(pendulum, ts, te, tstep):
    t = np.arange(ts, te, tstep)
    track = odeint(pendulum.equations, pendulum.init_status, t)
    th1_array, th2_array = track[:,0], track[:, 1]
    l1, l2 = pendulum.l1, pendulum.l2
    x1 = l1*np.sin(th1_array)
    y1 = -l1*np.cos(th1_array)
    x2 = x1 + l2*np.sin(th2_array)
    y2 = y1 - l2*np.cos(th2_array)
    pendulum.init_status = track[-1,:].copy() 
    return [x1, y1, x2, y2]


def drag1(x,y):
        global the1
        global t1
        global l1
        global l2
        global t2
        global done
        global len1
        global len2
        global l1tag
        done[0]=True
        delt=t2.position()-t1.position()
        if not l1tag:
            if y<0:
                the=np.arctan(x/-y)
            elif y!=0:
                the=np.arctan(x/-y)+np.pi
            else:
                the=np.pi/2
            the1=the
            x=len1*sin(the)
            y=-len1*cos(the)
        else:
            len1=np.sqrt(x**2+y**2)
            if y<0:
                the=np.arctan(x/-y)
            elif y!=0:
                the=np.arctan(x/-y)+np.pi
            else:
                the=np.pi/2
            the1=the
        t1.goto(x,y)
        l1.undo()
        l1.undo()
        l2.undo()
        l2.undo()
        l1.pu()
        l1.home()
        l1.pd()
        l1.setpos(x,y)
        l2.pu()
        l2.setpos(x,y)
        l2.pd()
        l2.setpos(t1.position()+delt)
        t2.goto(t1.position()+delt)
        turtle.update()
def drag2(x,y):
        global the2
        global l2
        global t2
        global t1
        global done
        global len1
        global len2
        global l2tag
        done[1]=True
        if not l2tag:
            x-=t1.position()[0]
            y-=t1.position()[1]
            
            if y<0:
                the=np.arctan(x/-y)
            elif y!=0:
                the=np.arctan(x/-y)+np.pi
            else:
                
                the=np.pi/2
            the2=the
            x=len2*sin(the)
            y=-len2*cos(the)
        else:
            x-=t1.position()[0]
            y-=t1.position()[1]
            len2=np.sqrt(x**2+y**2)
            if y<0:
                the=np.arctan(x/-y)
            elif y!=0:
                the=np.arctan(x/-y)+np.pi
            else:
                the=np.pi/2
            the2=the
        l2.undo()
        l2.undo()
        l2.pu()
        l2.setpos(t1.position())
        l2.pd()
        l2.setpos(x+t1.position()[0],y+t1.position()[1])
        t2.goto(x+t1.position()[0],y+t1.position()[1])
        turtle.update()
def click1():
    global l1
    global l1tag
    l1.undo()
    l1.undo()
    if l1tag:
        l1tag=False
        l1.pencolor("red")
        l1.fd(0)
        l1.fd(0)

        drag1(t1.position()[0],t1.position()[1])
    else:
        l1tag=True
        l1.pencolor("green")
        l1.fd(0)
        l1.fd(0)
        drag1(t1.position()[0],t1.position()[1])
    print(l1.pencolor())
def click2():
    global l2
    global l2tag
    l2.undo()
    l2.undo()
    if l2tag:
        l2tag=False
        l2.pencolor("red")
        l2.fd(0)
        l2.fd(0)

        drag2(t2.position()[0],t2.position()[1])
    else:
        l2tag=True
        l2.pencolor("green")
        l2.fd(0)
        l2.fd(0)
        drag2(t2.position()[0],t2.position()[1])
def start():
        global t1
        global t2
        global l1
        global l2
        global len1
        global len2
        if done[0] and done[1]:
            t1.ondrag(None)
            t2.ondrag(None)
            l1.undo()
            l2.undo()
            l1.pencolor('black')
            l2.pencolor('black')
            print(t2.position())
            pendulum = DoublePendulum(10, 5, len1, len2)
            pendulum.init_status[0]=the1
            pendulum.init_status[1]=the2
            x1, y1, x2, y2 = double_pendulum_odeint(pendulum, 0, 10000, 0.2)
           
            t1.pu()
            t2.pu()
            t1.setpos(x1[0],y1[0])
            t2.setpos(x2[0],y2[0])
            t1.pd()
            t2.pd()
            l1.pu()
            l2.pu()
            l1.home()
            l2.setpos(x1[0],y1[0])
            l1.pd()
            l2.pd()
            l1.fd(0)
            l2.fd(0)
            l2.fd(0)
            l1.fd(0)
            for i in range(10000):
                time.sleep(0.03)
                l1.undo()
                l1.undo()
                l2.undo()
                l2.undo()
                l1.pu()
                l1.home()
                l1.pd()
                l1.setpos(x1[i],y1[i])
                l2.pu()
                l2.setpos(x1[i],y1[i])
                l2.pd()
                l2.setpos(x2[i],y2[i])
                
                t1.goto(x1[i],y1[i])
                t2.goto(x2[i],y2[i])
                '''
                time.sleep(0.03)
                '''
                turtle.update()
def main():
    print("drag the two objects(move both of them)\npress 1 and 2 to lock/unlock the length\npress space to start time(calculation may take some time)")
    import turtle
    global t1,t2,l1,l2,c,done,the1,the2,turtle
    drag=False
    the1=-3*np.pi/5
    the2=-np.pi/9+np.pi
    done=[False,False]                
    c=turtle.Turtle()
    t1=turtle.Turtle()
    t2=turtle.Turtle()
    l1=turtle.Turtle()
    l2=turtle.Turtle()
    l1.pencolor('red')
    l2.pencolor('red')
    l2.pu()
    t1.pu()
    t2.pu()
    c.pu()
    c.ht()
    l1.ht()
    l2.ht()
    t1.setpos(len1,0)
    t2.setpos(len1+len2,0)
    l1.pu()
    l1.home()
    l1.pd()
    l1.setpos(len1,0)
    l2.pu()
    l2.setpos(len1,0)
    l2.pd()
    l2.setpos(len1+len2,0)
    c.dot(10,"blue")
    t1.pencolor("red")
    t2.pencolor("green")
    print('sha')
    t1.shape("circle")
    t2.shape("circle")
    
    t1.ondrag(drag1)
    t2.ondrag(drag2)
    turtle.onkey(click1,"1")
    turtle.onkey(click2,"2")
    turtle.onkey(start,"space")
    turtle.tracer(0,0)

    turtle.listen()

    turtle.mainloop()
    turtle.done()
