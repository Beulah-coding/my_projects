import FA
import time
import math

fa=FA.Create()
fa.ComClose()
fa.ComOpen(3)


### Hyper Parameters
gain = 10  ##angle step
d = 10  ##Distance
X = 0   #X origin
Y = 0   ##Y origin
A = 0   ##Starting angle
move = '' 
delay = 0  ##delay time
black = 70 ##Black colour threshold

xP = X
yP = Y
state = ''
RefDirection = 'Right'

prev_a =  0 + A
new_a = prev_a
prev_X = X
prev_Y = Y
new_X = X
new_Y = Y

end_X = 530
end_Y = 65
LLimit = 10
ULimit = 50

##Function to determine the X and Y position of the robot
def compute(a_p,d, x_p, y_p):
    if a_p == 360:
        a_p = 0
    elif a_p > 360:
        a_p = 360 - a_p
    if state == 'forward':
        x_n = x_p + d*math.sin(math.radians(a_p))
        y_n = y_p + d*math.cos(math.radians(a_p))
    return  x_p + d*math.sin(math.radians(a_p)), y_p + d*math.cos(math.radians(a_p))
    
##Move Foward    
def MoveForward(aP,xP,yP):
    state = 'forward'
    fa.Forwards(d)
    xN, yN = compute(aP,d,xP,yP)
    xP = xN
    yP = yN
    time.sleep(1)
    return aP, xN, yN
    
##Move Backward 
def MoveBackward(aP,xP,yP):
    state = 'backward'
    fa.Forwards(d)
    xN, yN = compute(aP,d,xP,yP)
    time.sleep(1)
    return aP, xN, yN

##Turn Left
def TurnLeft(aP):
    fa.Left(gain) 
    aN = aP - gain
    time.sleep(1)
    return aN

##Turn Right    
def TurnRight(aP):
    fa.Right(gain)
    aN = aP + gain
    time.sleep(1)
    return aN

###Read value for line detector
def read_line_sensor():
    left_sensor =[]
    right_sensor = []
    for i in range (10):
        a =fa.ReadLine(0)
        b =fa.ReadLine(1)
        left_sensor.append(a)
        right_sensor.append(b)
    return max(left_sensor), max(right_sensor)


###Keep last five moves
left = []
right = []
moves = []

def last_five(a, n):
    if len(a) >= 5:
        a.pop(0)
        a.append(n)
    else:
        a.append(n)
    return a

### Have you reached your goals?
def goal_checker(finalX,finalY):
    if ((end_X - LLimit) <= finalX <= (end_X + ULimit) and ( end_Y- LLimit) <= finalY <= (end_Y + ULimit)):
        goal = 'done'
        return goal

##Start command    
def Start_command():
    time.sleep(3)
    fa.LCDBacklight(100)    ##Print starting Message on screen
    fa.LCDClear()
    fa.LCDPrint (0, 10, '  Ready to Start   ' )
    time.sleep(2)
    fa.LCDClear()
    fa.LCDPrint (0, 10, '  Waiting to Start  ' )
    time.sleep(3)
    #fa.LCDBacklight(0)
    fa.LCDClear()
    fa.LCDPrint (0, 10, '    On Track    ' )
    fa.PlayNote(65, 1000)  ###Play the sound
    for i in range(1,8):   ###Turn on LED
        fa.LEDOn(i)
        time.sleep(.5)

## Ending Command
def end_command():
    #fa.LCDBacklight(100)
    notes = [65, 175, 220, 494, 698] #Plays note to sound alarm
    for note in notes:
        fa.PlayNote(note, 100)
    for note in reversed(notes):
        fa.PlayNote(note, 100)
    fa.LCDClear()
    fa.LCDPrint (0, 10, '  Cycle Completed   ' ) ##Print end message on screen
    time.sleep(2)
    fa.LCDClear()
    fa.LCDPrint (0, 10, 'Going to Sleep mode' )
    time.sleep(3)
    fa.LCDBacklight(0)
    fa.Left(180) 
    fa.PlayNote(65, 1000)
    fa.LCDBacklight(0)
    fa.LCDClear()
    for i in range(1,8):   ###Turn on LED
        fa.LEDOff(i)
        time.sleep(.5)
    
    
    
## Detect and Avoid obstacle
def avoid_obstacle():
    # Read the distance sensors
    left_sensor = fa.ReadIR(0)
    front_sensor = fa.ReadIR(1)
    right_sensor = fa.ReadIR(2)
    
    '''##Full automation mode
    while True:
        if (fa.ReadIR(2) > 200) or (fa.ReadIR(1)>200) or (fa.ReadIR(0) > 200):
            fa.PlayNote(65, 1000)
            for i in range(1,8):   ###Turn off LED
                fa.LEDOff(i)
            fa.PlayNote(65, 1000)
            for i in range(1,8):   ###Turn on LED
                fa.LEDOn(i)
        else:
            break'''

    ##Semi-automation mode        
    if (fa.ReadIR(2) > 50) or (fa.ReadIR(1)>50) or (fa.ReadIR(0) > 50):
        while True:
            sw_L = fa.ReadSwitch(0)
            sw_R = fa.ReadSwitch(1)
            fa.PlayNote(65, 1000)
            for i in range(1,8):   ###Turn off LED
                fa.LEDOff(i)
            fa.PlayNote(65, 1000)
            for i in range(1,8):   ###Turn on LED
                fa.LEDOn(i)
            if sw_L > 0 or sw_R > 0: # If left push button is pressed, move forward when obstacle is removed
                time.sleep(1)
                break 
    else:
        pass
        

## Main


Start_command()
start_time = time.time()
while True:
    
    avoid_obstacle()
    
    # Read the line sensors
    left_sensor, right_sensor = read_line_sensor()  
    
    ### Keep record of last move
    ##left = last_five(left, left_sensor)
    ##right = last_five(right, right_sensor)
    
    if left_sensor <= black and right_sensor <= black:
        new_a, new_X, new_Y = MoveForward(prev_a, prev_X, prev_Y)
        prev_X = new_X
        prev_Y = new_Y
        print("[info] Robot position -- Angle: {}°, X:{}, Y:{}".format(new_a, round(new_X,1), round(new_Y,2)))         
        move = 'forward'
        moves = last_five(moves, move)
        time.sleep(delay)
    

    elif left_sensor <= black and right_sensor > black:

        new_a = TurnLeft(prev_a)
        prev_a = new_a
        move = 'left'
        moves = last_five(moves, move)
        time.sleep(delay)

    elif left_sensor >black and right_sensor <= black:
        new_a = TurnRight(prev_a)
        prev_a = new_a
        move = 'right'
        moves = last_five(moves, move)
        time.sleep(delay)

    else:
              
        print('Just passing by')
        time.sleep(.5)
              
              
    move = goal_checker(new_X, new_Y)
    if move == 'done':
        end_command()          
        #duration = time.time() - start_time()
        print("Total time of travel is:", time.time() - start_time())    
        break

fa.ComClose()
