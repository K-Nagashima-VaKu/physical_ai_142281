"""Python 3.15 / standard-library-only Physical AI robot demo (~75 seconds)."""
import csv
import math
import tkinter as tk
from datetime import datetime
from pathlib import Path

W,H=960,620
DT=0.04
SCALE=100
DATA=[(0.10,'STOP'),(0.20,'STOP'),(0.35,'STOP'),(0.45,'STOP'),(0.55,'STOP'),(0.75,'GO'),(0.95,'GO'),(1.2,'GO'),(1.5,'GO'),(2.0,'GO'),(3.0,'GO'),(5.0,'GO')]

def predict(d):
    nearest=sorted(DATA,key=lambda item:abs(item[0]-d))[:3]
    stop=sum(label=='STOP' for _,label in nearest)
    return ('STOP' if stop>=2 else 'GO'),max(stop,3-stop)/3

class Demo:
    def __init__(self,root):
        self.root=root
        root.title('Physical AI Final Project - Multi-action robot demo (Python 3.15)')
        root.geometry(f'{W}x{H}')
        self.cv=tk.Canvas(root,width=W,height=485,bg='#f8fafc',highlightthickness=0)
        self.cv.pack()
        self.info=tk.StringVar(value='Ready - press START. Approx. 75 seconds.')
        tk.Label(root,textvariable=self.info,font=('Segoe UI',12),anchor='w',padx=20).pack(fill='x',pady=5)
        bar=tk.Frame(root);bar.pack(pady=6)
        tk.Button(bar,text='START / RESTART',width=20,command=self.start).pack(side='left',padx=8)
        tk.Button(bar,text='PAUSE / RESUME',width=18,command=self.pause).pack(side='left',padx=8)
        tk.Button(bar,text='QUIT',width=12,command=root.destroy).pack(side='left',padx=8)
        self.file=Path(__file__).with_name('events.csv')
        self.generation=0
        self.reset()
        self.draw()

    def reset(self):
        self.x=105.0;self.y=300.0;self.angle=0.0
        self.phase=0;self.elapsed=0.0;self.phase_time=0.0
        self.running=False;self.paused=False;self.done=False
        self.action='WAIT';self.conf=0.0;self.distance=0.0
        self.events=[]

    def log(self,name):
        with self.file.open('a',encoding='utf-8-sig',newline='') as f:
            w=csv.writer(f)
            if f.tell()==0:w.writerow(['timestamp','elapsed_s','event','x_px','y_px','distance_m'])
            w.writerow([datetime.now().isoformat(timespec='seconds'),f'{self.elapsed:.1f}',name,f'{self.x:.1f}',f'{self.y:.1f}',f'{self.distance:.2f}'])
        self.events.append(name)

    def start(self):
        self.generation+=1
        self.reset();self.running=True;self.log('START');self.schedule()

    def pause(self):
        if not self.running:return
        self.paused=not self.paused
        self.info.set('PAUSED' if self.paused else 'RESUMED')

    def advance(self,name):
        self.log(name)
        self.phase+=1;self.phase_time=0.0

    def schedule(self):
        token=self.generation
        self.root.after(int(DT*1000),lambda:self.tick(token))

    def tick(self,token):
        if token!=self.generation or not self.running:return
        if self.paused:self.schedule();return
        self.elapsed+=DT;self.phase_time+=DT
        # Phase 0: approach first obstacle. k-NN makes actual stop decision.
        if self.phase==0:
            self.distance=max(0,(650-(self.x+22))/SCALE)
            self.action,self.conf=predict(self.distance)
            if self.action=='STOP':self.advance('AI_STOP_1')
            else:self.x+=0.37*SCALE*DT
            label='1/6 AI approach: obstacle A'
        # Phase 1: hold the stop on screen for recording.
        elif self.phase==1:
            self.action='STOP';label='2/6 AI STOP at obstacle A'
            if self.phase_time>=5:self.advance('REVERSE_START')
        # Phase 2: reverse a fixed distance (ordinary control, not AI).
        elif self.phase==2:
            self.action='REVERSE';self.x-=0.24*SCALE*DT
            label='3/6 Reverse to safe position'
            if self.phase_time>=8:self.advance('TURN_START')
        # Phase 3: rotate left 90 degrees (ordinary control).
        elif self.phase==3:
            self.action='TURN LEFT';self.angle=min(math.pi/2,self.angle+(math.pi/2)/6*DT)
            label='4/6 Turn left 90 degrees'
            if self.phase_time>=6:self.advance('SECOND_APPROACH_START')
        # Phase 4: approach second obstacle northwards, again using k-NN.
        elif self.phase==4:
            self.distance=max(0,((self.y-22)-125)/SCALE)
            self.action,self.conf=predict(self.distance)
            if self.action=='STOP':self.advance('AI_STOP_2')
            else:self.y-=0.16*SCALE*DT
            label='5/6 AI approach: obstacle B'
        # Phase 5: hold final result for an extended demonstration.
        else:
            self.action='STOP';label='6/6 AI STOP at obstacle B - COMPLETE'
            if self.phase_time>=12:
                self.log('DEMO_COMPLETE');self.running=False;self.done=True
        self.info.set(f'{label} | {self.elapsed:.1f}s | AI/control: {self.action} | distance: {self.distance:.2f}m')
        self.draw()
        if self.running:self.schedule()

    def draw(self):
        c=self.cv;c.delete('all')
        c.create_text(24,25,text='AI Robot: Detect, Stop, Reverse, Turn, Detect Again',anchor='w',font=('Segoe UI',17,'bold'),fill='#193b58')
        c.create_text(24,57,text='AI: k-NN classification of virtual distance | Other actions: predefined wheel commands',anchor='w',font=('Segoe UI',11),fill='#586c7a')
        c.create_rectangle(30,82,930,405,fill='#e9eff3',outline='#bdcbd4',width=2)
        c.create_line(80,300,690,300,fill='#c3d0d8',width=3,dash=(9,8))
        c.create_line(490,300,490,112,fill='#c3d0d8',width=3,dash=(9,8))
        c.create_rectangle(650,258,700,342,fill='#d3534a',outline='#9d3029',width=2)
        c.create_text(675,298,text='A',font=('Segoe UI',18,'bold'),fill='white')
        c.create_rectangle(448,85,532,125,fill='#d3534a',outline='#9d3029',width=2)
        c.create_text(490,105,text='B',font=('Segoe UI',18,'bold'),fill='white')
        # robot top-down with rotating nose and side wheels
        x,y=self.x,self.y;a=self.angle
        c.create_oval(x-22,y-22,x+22,y+22,fill='#3185c1',outline='#164e78',width=3)
        nx=x+17*math.cos(a);ny=y-17*math.sin(a)
        c.create_line(x,y,nx,ny,fill='white',width=5,arrow=tk.LAST)
        for sign in (-1,1):
            wx=x+25*math.sin(a)*sign;wy=y+25*math.cos(a)*sign
            c.create_oval(wx-6,wy-6,wx+6,wy+6,fill='#333e48',outline='')
        c.create_text(x,y-42,text='ROBOT',font=('Segoe UI',10,'bold'),fill='#1b557d')
        c.create_text(24,435,text=f'Elapsed: {self.elapsed:.1f} s',anchor='w',font=('Segoe UI',12,'bold'),fill='#17324d')
        c.create_text(285,435,text=f'Decision: {self.action}',anchor='w',font=('Segoe UI',12,'bold'),fill='#ae4036' if self.action=='STOP' else '#24734f')
        c.create_text(605,435,text=f'AI confidence: {self.conf:.0%}',anchor='w',font=('Segoe UI',12,'bold'),fill='#17324d')
        if self.done:c.create_text(480,180,text='SUCCESS - TWO AI-TRIGGERED STOPS',font=('Segoe UI',18,'bold'),fill='#aa382f')

if __name__=='__main__':
    root=tk.Tk();Demo(root);root.mainloop()
