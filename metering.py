#!/usr/bin/env python3

from third_party.pyserial.serial import *
from time import *
from threading import Thread
import ac
import acsys
from third_party.sim_info import *

appName = "Metering"
width, height = 1 , 1 

simInfo = SimInfo()
s = Serial('COM11')
deltaTimer = 0
maxRpm = 0

def acMain(ac_version):
    global appWindow
    appWindow = ac.newApp(appName)
    ac.setTitle(appWindow, appName)
    ac.setSize(appWindow, width, height)
    ac.addRenderCallback(appWindow, appGL)
    return appName

def appGL(deltaT):
    pass

def acUpdate(deltaT):
    global deltaTimer
    global thread
    global maxRpm
    deltaTimer += deltaT
    if deltaTimer > 0.05:
        deltaTimer = 0
        blink=0
        rpmValue = ac.getCarState(0, acsys.CS.RPM)
        gearValue = ac.getCarState(0, acsys.CS.Gear)
        if rpmValue > maxRpm: maxRpm = rpmValue
        if rpmValue > maxRpm*0.94: blink=1
        d=str(int(rpmValue))+','+str(gearValue-1)+','+str(blink)+'\n'
        print(d)
        try:
            s.write(str.encode(d))
            s.flush()
        except Exception as e:
            print(e)
            s.close()
            s.open()







