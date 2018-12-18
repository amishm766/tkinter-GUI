import tkinter
from tkinter import *
import pandas as pd
import RPi.GPIO as GPIO

from tkinter import messagebox

top = Tk()
top.title("Login page")
#top.geometry("250x100")

led_dict = {'led0' : 26, 'led1' : 12, 'led2' : 16, 'led3' : 20}
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
for pin in led_dict:
    GPIO.setup(led_dict[pin], GPIO.OUT)
button_dict = {0 : ('ON', 'OFF'), 1 : ('ON', 'OFF'), 2 : ('ON', 'OFF'), 3 : ('ON', 'OFF')}

def automation():
    if (E1.get() == 'a') and (E2.get() == 'p'):
        """ If the username and password matches """
        top.destroy()
        # Create a new window for automation        
        newTop = Tk()
        newTop.title("Automation")
        newTop.geometry("200x200")
        
        # Create labels for the appliances
        labels = []
        labelNames = ('labelLed0', 'labelLed1', 'labelLed2', 'labelLed3')
        
        for labelName in labelNames:
            labelName = Label(newTop, text = "LED {} ==>".format(labelName[-1]))
            labels.append(labelName)

        # Create a button for leds to turn ON
        buttonsOn = []
        buttonOnNames = ('led0ON', 'led1ON', 'led2ON', 'led3ON')
        
        for buttonOnName in buttonOnNames:
            buttonOnName = Button(newTop, text = "ON")
            buttonOnName.configure(command =lambda button = buttonOnName: ledAction(button))
            buttonsOn.append(buttonOnName)

        # Create a button for leds to turn OFF
        buttonsOff = []
        buttonOffNames = ('led0OFF', 'led1OFF', 'led2OFF', 'led3OFF')
        
        for buttonOffName in buttonOffNames:
            buttonOffName = Button(newTop, text = "OFF")
            buttonOffName.configure(command =lambda button = buttonOffName: ledAction(button))
            buttonsOff.append(buttonOffName)

        # Place all the labels at their positions
        i = 0
        for label in labels:
            label.grid(row = i, column = 0)
            i = i+1

        # Place all the ON buttons at their positions
        i = 0
        for buttonOn in buttonsOn:
            buttonOn.grid(row = i, column = 1)
            i = i+1
            
        # Place all the OFF buttons at their positions            
        i = 0
        for buttonOff in buttonsOff:
            buttonOff.grid(row = i, column = 2)
            i = i+1
        """

        i = 0
        for statusLabel in statusLabels:
            statusLabel.grid(row = i, column = 3)
            i = i+1
        """
        newTop.mainloop()
        
        #msg = messagebox.showinfo(title = "submit", message = "welcome")

def ledAction(button):

    """ If any button is pressed """
    gi=button.grid_info()
    x = gi['row']
    y = gi['column']
    appliance = 'led{}'.format(x)
    action = str(button_dict[x][y-1])
    actuator = int(led_dict[appliance])
    
    print("Turned {} {}".format(appliance, action))

    # Check which button was pressed and accordingly act
    if action == 'ON':
        GPIO.output(actuator, GPIO.HIGH)
    else :
        GPIO.output(actuator, GPIO.LOW)
    data = pd.DataFrame(led_dict, index = [0])
    pins = data.ix[0, :].get_values()
    data.ix[1,:] = [GPIO.input(pin) for pin in pins]
    data.ix[1, :] = data.ix[1, :].map({0 : 'OFF', 1 : 'ON'})
    status_list = data.ix[1,:].get_values()
    
    # Show a new flashing window to tell status
    msg = messagebox.showinfo(title = "Action", message = """LED0 {}
LED1 {}
LED2 {}
LED3 {}""".format(*status_list))
    
def login():
    global E1, E2
    L1 = Label(top, text = "Username")
    L2 = Label(top, text = "Password")

    L1.grid(row = 0, column = 0)
    L2.grid(row = 1, column = 0)
    E1 = Entry(top, bd = 5)
    E2 = Entry(top, bd = 5, show = '*')
    B1 = Button(top, text = 'submit', command = automation)

    E1.grid(row = 0, column = 1)
    E2.grid(row = 1, column = 1)
    B1.grid(row = 2, column = 1)
    top.mainloop()

if __name__ == '__main__' :
    try:
        login()
    except KeyboardInterrupt():
        pass
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()
