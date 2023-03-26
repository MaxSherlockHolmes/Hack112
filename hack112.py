from cmu_graphics import *
from PIL import Image
import os, pathlib

class Screen:
    def __init__(self):
        pass

class Platform:
    platformList=[]
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        Platform.platformList.append(self)
    
    def drawPlatform(self):
        drawRect(self.x,self.y,self.width,self.height,align='center',fill='lightBlue',border='blue')

class Character:
    def __init__(self,speed,jump,width,height):
        self.speed = speed
        self.jump = jump
        self.width = width
        self.height = height
    
    
    
#Kosbie and Taylor around 30x55 and Scotty around 40x30

class Wall:
    wallList=[]
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        Wall.wallList.append(self)

def checkCollision(x,width,y,height):   
    for platform in Platform.platformList:
        if (platform.x-platform.width/2)<= (x+width/2):
            if (x-width/2) <=(platform.x+platform.width/2):
                if ((platform.y-platform.height/2)<= (y+height/2) <=(platform.y+platform.height/2)):
                    return True
    return False

def checkWallCollision(x,width,y,height):
    for platform in Wall.wallList:
        if (platform.x-platform.width/2)<= (x+width/2):
            if (x-width/2) <=(platform.x+platform.width/2):
                if ((platform.y-platform.height/2)<= (y+height/2) <=(platform.y+platform.height/2)):
                    return True
    return False    

def onAppStart(app):
    app.kosbieImage=Image.open(os.path.join(pathlib.Path(__file__).parent,"Untitled_Artwork (1).png"))
    app.kosbieImageFlipped = app.kosbieImage.transpose(Image.FLIP_LEFT_RIGHT)
    app.kosbieImage=CMUImage(app.kosbieImage)
    app.kosbieImageFlipped=CMUImage(app.kosbieImageFlipped)

    app.taylorImage=Image.open(os.path.join(pathlib.Path(__file__).parent,"Untitled_Artwork 2 (1).png"))
    app.taylorImageFlipped = app.taylorImage.transpose(Image.FLIP_LEFT_RIGHT)
    app.taylorImage=CMUImage(app.taylorImage)
    app.taylorImageFlipped=CMUImage(app.taylorImageFlipped)

    app.cmuBackground = Image.open(os.path.join(pathlib.Path(__file__).parent,"New Project.png"))
    app.cmuBackground = CMUImage(app.cmuBackground)

    app.chee = Image.open(os.path.join(pathlib.Path(__file__).parent,"ZChee.png"))
    app.chee = CMUImage(app.chee)
    reset(app)

def reset(app):
    app.startScreen=True
    app.menuScreen=False
    app.controlScreen=False
    app.levelScreen=False
    app.playerScreen=False
    app.gameScreen=False
    app.pause = False
    app.gameOver = False
    app.player0Won = False
    app.player1Won = False

    app.level=None

    app.player0X=100
    app.player0Y=100
    app.player1X=app.width-100
    app.player1Y=100
    app.player0Jumping = False
    app.vel0 = 0
    app.jumpCounter0 = 0
    app.player1Jumping = False
    app.vel1 = 0
    app.jumpCounter1 = 0
    app.player0Health = 100
    app.player1Health = 100

    app.player0holdLeft = False
    app.player0holdRight = False
    app.player0holdUp = False
    app.player0holdDown = False
    app.player1holdLeft = False
    app.player1holdRight = False
    app.player1holdUp = False
    app.player1holdDown = False

    app.Kosbie=Character(1,1,30,55)
    app.Taylor=Character(1.3,1,30,55)

    app.player0=app.Kosbie
    app.player1=app.Taylor
    
    app.p0p=Platform(app.width//2,400,700,50)
    app.p1=Platform(150,200,200,25)
    app.p2=Platform(750,200,200,25)
    app.p0f=Wall(app.width//2,400,700,50)

    ##storing Projectiles
    app.projectileList = []
    app.shotABullet = False
    app.player0dir = "right"
    app.count = 0

    ##storing sword
    app.player1dir = "left"
    app.player1dirOp = "right"
    app.swordA = False          #sword anim starts
    app.swordI = False          #sword exists
    app.swordL = 5              #sword length
    app.swordG = False          #sword growth
    app.swordCount = 0

def redrawAll(app):
    if not app.gameOver:
        if app.startScreen:
            drawLabel("The 15-112 Battle Royale!",450,100,font='cinzel',fill='green',size=40,bold=True)
            msg="It's time to see which 15-112 Lecture is superior, Dr. Kosbie vs Professor Taylor!"
            msg1="Dr. Kosbie is a projectile fighter, uses WASD to move, and 'C' to shoot"
            msg2="Prof. Taylor is a melee fighter, uses the Arrow Keys to move, 'O' to attack"
            drawLabel(msg,450,200,size=20,bold=True)
            drawLabel(msg1,450,250,size=20,bold=True)
            drawLabel(msg2,450,300,size=20,bold=True)
            #drawRect(0,0,app.width,app.height,fill='lightGreen',opacity=25)
            drawPolygon(0,0,0,app.height,app.width,app.height,fill='green',opacity=25)
            drawPolygon(app.width,0,0,0,app.width,app.height,fill='blue',opacity=25)
        elif app.gameScreen: 
            drawImage(app.cmuBackground,0,0)
            drawRect(app.player0X,app.player0Y,app.player0.width,app.player0.height,align="center",fill=None)
            if app.player0dir == 'right':
                drawImage(app.kosbieImage, app.player0X, app.player0Y, align="center")
            elif app.player0dir == 'left':
                drawImage(app.kosbieImageFlipped, app.player0X, app.player0Y, align="center")
            if app.player1dir == 'left':
                drawImage(app.taylorImage, app.player1X, app.player1Y, align="center")
            elif app.player1dir == 'right':
                drawImage(app.taylorImageFlipped, app.player1X, app.player1Y, align="center")
            drawRect(app.player1X,app.player1Y,app.player1.width,app.player1.height,align="center",fill=None)
            app.p0p.drawPlatform()
            app.p1.drawPlatform()
            app.p2.drawPlatform()
            #if app.pause==True:

            ##drawing Projectile
            for bullet in app.projectileList:
                bulletcx, bulletcy = bullet[0], bullet[1]
                drawRect(bulletcx,bulletcy,25,10,fill="white",align="center")
                drawLabel("FUCK", bulletcx, bulletcy, fill = "red", size = 10, bold = True)
        
        ##drawing sword
            if app.swordI == True and app.swordA == True:
                drawImage(app.chee,app.player1X,app.player1Y,align=app.player1dirOp)
                drawRect(app.player1X, app.player1Y, app.swordL, 65, align = app.player1dirOp,fill=None)

            drawHealth(app)
    else:
        drawGameOver(app)

def drawGameOver(app):
    if app.player0Won:
        drawLabel('KOSBIE WINS',450,300,size=40,bold=True)
        drawLabel("Press 'r' to play again!",450,350,size=20)
    elif app.player1Won:
        drawLabel('TAYLOR WINS',450,300,size=40,bold=True)
        drawLabel("Press 'r' to play again!",450,350,size=20)

def drawHealth(app):
    drawRect(175,537.5,200,100,align='center',fill="white",border="black")
    drawRect(725,537.5,200,100,align='center',fill="white",border="black")
    drawLabel("Kosbie Health",175,525,size=24,bold=True)
    drawLabel(f'{app.player0Health}',175,550,size=24,bold=True)
    drawLabel("Taylor Health",725,525,size=24,bold=True)
    drawLabel(f'{app.player1Health}',725,550,size=24,bold=True)

def onKeyPress(app, key):
    if key=='r' and app.gameOver:
        reset(app)
    if app.pause==False:
        if key == "c" and not app.shotABullet:
            app.projectileList.append([app.player0X, app.player0Y, app.player0dir])
            app.shotABullet = True
        if key == "v":
            if app.player0holdLeft:
                pass
            if app.player0holdRight:
                pass
            if app.player0holdUp:
                pass
            if app.player0holdDown:
                pass
            pass
        if key == "o":
            if app.swordI==False:
                app.swordA = True
                app.swordI = True
                app.swordG = True
            pass
        if key == "p":
            if app.player1holdLeft:
                pass
            if app.player1holdRight:
                pass
            if app.player1holdUp:
                pass
            if app.player1holdDown:
                pass
            pass
        if key == "a":
            app.player0dir = "left"
        if key == "d":
            app.player0dir = "right"
        if key == "left":
            app.player1dir = "left"
            app.player1dirOp = "right"
        if key == "right":
            app.player1dir = "right"
            app.player1dirOp = "left"
    if key == "escape":
        app.pause = not app.pause
    if key == 'w' and app.jumpCounter0 < 2:
        app.jumpCounter0 += 1
        app.player0Jumping = True
        app.vel0 = -15
    if key == 'up' and app.jumpCounter1 < 2:
        app.jumpCounter1 += 1
        app.player1Jumping = True
        app.vel1 = -15

def onKeyHold(app, keys):
    #Player 0 controls
    if app.pause==False:
        if 'a' in keys:
            app.player0X-=3*app.player0.speed
            # if checkCollision(app.player0X,app.player0.width,app.player0Y,app.player0.height):
            #     app.player0X+=3
            app.player0holdLeft = True
        if 's' in keys:
            app.player0Y+=3
            # if checkCollision(app.player0X,app.player0.width,app.player0Y,app.player0.height):
            #     app.player0Y-=3
            app.player0holdDown = True
        if 'd' in keys:
            app.player0X+=3*app.player0.speed
            # if checkCollision(app.player0X,app.player0.width,app.player0Y,app.player0.height):
            #     app.player0X-=3
            app.player0holdRight = True
        
    #Player 1 controls
        if 'left' in keys:
            app.player1X-=3*app.player1.speed
            # if checkCollision(app.player1X,app.player1.width,app.player1Y,app.player1.height):
            #     app.player1X+=3
        if 'down' in keys:
            app.player1Y+=3
            # if checkCollision(app.player1X,app.player1.width,app.player1Y,app.player1.height):
            #     app.player1Y-=3
        if 'right' in keys:
            app.player1X+=3*app.player1.speed
            # if checkCollision(app.player1X,app.player1.width,app.player1Y,app.player1.height):
            #     app.player1X-=3


def onKeyRelease(app, key):
    if app.pause==False:
        if key == "w":
            app.player0holdUp = False
        if key == "a":
            app.player0holdLeft = False
        if key == "s":
            app.player0holdDown = False
        if key == "d":
            app.player0holdRight = False
        if key == "up":
            app.player1holdUp = False
        if key == "left":
            app.player1holdLeft = False
        if key == "down":
            app.player1holdDown =  False
        if key == "right":
            app.player1holdRight = False

def onMousePress(app,mouseX,mouseY):    
    if app.startScreen: 
        app.startScreen=False
        app.gameScreen=True

def onStep(app):
    if not app.pause:
        takeStep(app)

def takeStep(app):
    doGravity(app)
    
    ##projectileAmountLimiter
    if app.shotABullet:
        app.count += 1
    if app.count == 20:
        app.shotABullet = False
        app.count = 0
    

    #sword growth
    if app.swordI==True:
        if app.swordG==True:
            if app.swordL<65:
                app.swordL+=10
            elif app.swordL>=35:
                app.swordG=False
        elif app.swordG==False:
            if app.swordL>5:
                app.swordL-=10
            elif app.swordL<=5:
                app.swordL=5
                app.swordA=False
    if app.swordI==True:
        app.swordCount += 1
    if app.swordCount == 30:
        app.swordI = False
        app.swordCount = 0

    ##projectile moving
    for projectile in app.projectileList:
        if projectile[2] == "left":
            projectile[0] -= 10
        elif projectile[2] == "right":
            projectile[0] += 10
        elif projectile[2] == "up":
            projectile[1] -= 10
        elif projectile[2] == "down":
            projectile[1] += 10
    
    checkProjHitbox(app)
    checkSwordHit(app)
    checkGameOver(app)

def checkGameOver(app):
    if app.player0Health == 0 or app.player1Health == 0 or checkOffMap(app.player0X,app.player0Y) or checkOffMap(app.player1X,app.player1Y):
        app.gameOver = True
        if app.player1Health == 0 or checkOffMap(app.player1X,app.player1Y):
            app.player0Won = True
        elif app.player0Health == 0 or checkOffMap(app.player0X,app.player1X):
            app.player1Won = True

def checkOffMap(x,y):
    width = 30
    height = 55
    if y-55/2 > 600:
        return True
    return False

def checkProjHitbox(app):
    i = 0
    while i < len(app.projectileList):
        projcx, projcy = app.projectileList[i][0]+5, app.projectileList[i][1]+5
        if (projcx < -5) or (projcx > app.width) or (projcy < -5) or (projcy > app.height):
            app.projectileList.pop(i)
        elif (app.player1X - app.player1.width/2 <= projcx <=app.player1X + app.player1.width/2) and (app.player1Y - app.player1.height/2 <= projcy <= app.player1Y + app.player1.width/2):
            app.projectileList.pop(i)
            app.player1Health -= 5
        else:
            i += 1
        
def checkSwordHit(app):
    if app.swordA == True:
        if app.player1dir == "left":
            swordLeft = app.player1X - app.swordL
            swordRight = app.player1X
            swordMiddle = app.player1Y
            if ((app.player0X-app.player0.width/2<=swordLeft<=app.player0X+app.player0.width)or(app.player0X-app.player0.width/2<=swordRight<=app.player0X+app.player0.width))and(app.player0Y-32/2<=swordMiddle<=app.player0Y+32):
                app.player0Health -= 10
                app.swordA = False
        elif app.player1dir == "right":
            swordLeft = app.player1X
            swordRight = app.player1X + app.swordL
            swordMiddle = app.player1Y
            if ((app.player0X-app.player0.width/2<=swordLeft<=app.player0X+app.player0.width)or(app.player0X-app.player0.width/2<=swordRight<=app.player0X+app.player0.width))and(app.player0Y-32/2<=swordMiddle<=app.player0Y+32):
                app.player0Health -= 10
                app.swordA = False


def doGravity(app):
    if not checkCollision(app.player0X,app.player0.width,app.player0Y,app.player0.height) or app.player0Jumping:
        acc = 1
        app.player0Y = nextPos(app.player0Y,app.vel0)
        app.vel0 = nextVel(app.vel0,acc)
        if checkCollision(app.player0X,app.player0.width,app.player0Y,app.player0.height) and app.vel0>0:
            app.player0Jumping = False
            app.vel0 = 0
            app.jumpCounter0 = 0
    if not checkCollision(app.player1X,app.player1.width,app.player1Y,app.player1.height) or app.player1Jumping:
        acc = 1
        app.player1Y = nextPos(app.player1Y,app.vel1)
        app.vel1 = nextVel(app.vel1,acc)
        if checkCollision(app.player1X,app.player1.width,app.player1Y,app.player1.height) and app.vel1>0:
            app.player1Jumping = False
            app.vel1 = 0
            app.jumpCounter1 = 0
    if checkCollision(app.player0X,app.player0.width,app.player0Y,app.player0.height):
        distSunk0 = correctCollision(app.player0Y,app.player0.height)
        app.player0Y -= distSunk0
    if checkCollision(app.player1X,app.player1.width,app.player1Y,app.player1.height):
        distSunk1 = correctCollision(app.player1Y,app.player1.height)
        app.player1Y -= distSunk1

def correctCollision(y,height):
    currPlat = None
    for platform in Platform.platformList:
        if ((platform.y-platform.height/2)<= (y+height/2) <=(platform.y+platform.height/2)):
            currPlatY = platform.y-platform.height/2
    return (y+height/2) - currPlatY

def nextPos(y,vel):
    return y + vel

def nextVel(vel,acc):
    return vel + acc

def main():
    runApp(width=900,height=600)



main()
cmu_graphics.run()
