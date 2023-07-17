from math import ceil
from statistics import mean
from matplotlib import pyplot as plt
from settings import TIME_FRAME, INTERVAL_SECONDS

import numpy as np


class Player:
    KW_DISTANCE = "distance"
    KW_DISTANCEHS = "distanceHS"
    KW_DISTANCESPR = "distanceSPR"
    KW_DISTANCEHI = "distanceHI"
    KW_MAX_SPEED = "maxSpeed"
    KW_AVG_SPEED = "avgSpeed"
    #KW_ACCELERATION = "Acceleration"
    #KW_DECELERATION = "Deceleration"
    KW_ACC_DEC_SUM = "Acc+Dec"

    def __init__(self, optaId):
        self.optaId = optaId
        self.periods = {
            1: {},
            2: {}
        }

        # Data to compute accel decel
        self.rawSpeed = []
        self.rawTime = []
        #self.accelDecel = None
        #self.acc_counts = None
        #self.dec_counts = None
        #self.acceleration = None
    
    def getPeriods(self):
        return self.periods
    
    def getOptaId(self):
        return self.optaId
    
    def addInstant(self, speed, periodName, gameClock):
        period = self.periods[periodName]
        minute = ceil(gameClock/INTERVAL_SECONDS)
        if minute == 0:
            return
        
        #Create the time period if it doesn't exist
        if minute not in period.keys():
            period[minute] = {
                self.KW_DISTANCE: 0,
                self.KW_DISTANCEHS: 0,
                self.KW_DISTANCESPR: 0,
                self.KW_DISTANCEHI: 0,
                self.KW_MAX_SPEED: 0,
                self.KW_AVG_SPEED: 0,
                #self.KW_ACCELERATION: [],
                #self.KW_DECELERATION: [],
                #self.KW_ACC_DEC_SUM: 0
            } 
        distance = speed * TIME_FRAME
        distanceHS = distance if speed >= 5.5 and speed < 7 else 0
        distanceSPR = distance if speed >= 7 else 0
        distanceHI = distance if speed >= 5.5 else 0
        

        period[minute][self.KW_DISTANCE] += distance
        period[minute][self.KW_DISTANCEHS] += distanceHS
        period[minute][self.KW_DISTANCESPR] += distanceSPR
        period[minute][self.KW_DISTANCEHI] += distanceHI
        period[minute][self.KW_MAX_SPEED] = max(speed, period[minute][self.KW_MAX_SPEED])
        period[minute][self.KW_AVG_SPEED] = np.average(speed)
        
        # Add raw speed to player
        self.rawSpeed.append(speed)
        self.rawTime.append([periodName, gameClock])

        


class Players:
    def __init__(self):
        self.players = {}

    def getPlayer(self, optaId):
        if optaId not in self.players.keys():
            self.players[optaId] = Player(optaId)

        return self.players[optaId]

    def getPlayers(self):
        return self.players

    def addTimestamp(self, timestamp):
        period = timestamp["period"]
        gameClock = timestamp["gameClock"]
        allPlayersInstant = timestamp["homePlayers"] + timestamp["awayPlayers"]
        
        for playerInstant in allPlayersInstant:
            self.getPlayer(playerInstant["optaId"]).addInstant(playerInstant["speed"], period, gameClock)
    
    ############################################################
    #   MAIN FUNTION                                           #
    ############################################################
    def generatePlayersData(self, data):
        for timestamp in data[1:-1]:
            self.addTimestamp(timestamp)
        
        


class GameStats:
    KW_IN_PLAY = "InPlay"
    KW_OUT_PLAY = "OutPlay"
    KW_HOME = "home"
    KW_AWAY = "away"

    periods = {
            1: {},
            2: {}
        }

    def getPeriods(self):
        return self.periods

    def addTimestamp(self, timestamp):
        period = timestamp["period"]
        gameClock = timestamp["gameClock"]
        minute = ceil(gameClock/INTERVAL_SECONDS)
        if gameClock > 59:
            pass

        if minute not in self.periods[period].keys():
            self.periods[period][minute] = {
                self.KW_IN_PLAY: 0,
                self.KW_OUT_PLAY: 0,
                self.KW_HOME: 0,
                self.KW_AWAY: 0
            }
        
        self.periods[period][minute][self.KW_IN_PLAY] += 0.04 if timestamp["live"] else  0
        self.periods[period][minute][self.KW_OUT_PLAY] += 0.04 if timestamp["live"] == False else  0
        self.periods[period][minute][self.KW_HOME] += 0.04 if timestamp["live"] and timestamp["lastTouch"] == "home" else  0
        self.periods[period][minute][self.KW_AWAY] += 0.04 if timestamp["live"] and timestamp["lastTouch"] == "away" else  0

    
    def generateGameStats(self, data):
        for timestamp in data[1:-1]:
            self.addTimestamp(timestamp)

    