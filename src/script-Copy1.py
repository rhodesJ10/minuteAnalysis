import json
import time
import pandas as pd

from model import GameStats, Players
from settings import DATA_PATH, OUTPUT_PATH


#Load data from file
def loadData():
    print("Loading data...")
    start = time.perf_counter()
    with open(DATA_PATH, "r") as json_data:
        for line in json_data:
            line = fr"{line}"

            break
        data = [json.loads(line) for line in json_data]
    
    finish = time.perf_counter()
    print("Data loaded in {:.6f}s".format(finish-start))
    return data


def transformData(data):
    print("Transforming data...")
    start = time.perf_counter()

    players = Players()
    players.generatePlayersData(data)

    gameStats = GameStats()
    gameStats.generateGameStats(data)

    finish = time.perf_counter()
    print("Data transformed in {:.6f}s".format(finish-start))
    return players, gameStats


def exportData(players: Players, gameStats: GameStats):
    print("Exporting data...")
    start = time.perf_counter()

    matchName = "2292823"
    data = []

    for playerKey in players.getPlayers():
        player = players.getPlayers()[playerKey]
        for periodKey in player.getPeriods():
            period = player.getPeriods()[periodKey]
            for clockKey in period:
                minuteData = period[clockKey]
                line = []
                line.append(matchName)
                line.append(periodKey)
                line.append(clockKey*60)
                line.append(clockKey)
                line.append(int(player.optaId))
                line.append(round(minuteData[player.KW_DISTANCE], 1))
                line.append(round(minuteData[player.KW_DISTANCEHS], 1))
                line.append(round(minuteData[player.KW_DISTANCESPR], 1))
                line.append(round(minuteData[player.KW_DISTANCEHI], 1))
                line.append(round(minuteData[player.KW_MAX_SPEED],1))
                line.append(round(minuteData[player.KW_AVG_SPEED],1))
                #line.append(minuteData[player.KW_ACCELERATION])
                #line.append(minuteData[player.KW_DECELERATION])
                #line.append(minuteData[player.KW_ACC_DEC_SUM])
                line.append(round(gameStats.getPeriods()[periodKey][clockKey][gameStats.KW_IN_PLAY], 1))
                line.append(round(gameStats.getPeriods()[periodKey][clockKey][gameStats.KW_HOME], 1))
                line.append(round(gameStats.getPeriods()[periodKey][clockKey][gameStats.KW_AWAY], 1))

                data.append(line)
        data.append([])

    dataFrame = pd.DataFrame(data, columns = ["matchId", "period", "gameClock", "minute", "optaid", "distance", "distanceHS", "distanceSPR", "distanceHI", "maxSpeed", "avgSpeed", 
                                              #"acceleration", "deceleration", "accDec", 
                                              "inPlay", "home", "away"])
    dataFrame.to_csv((matchName+"_output.csv"), #sheet_name = matchName
                      index = False)

    finish = time.perf_counter()
    print("Data exported in {:.6f}s".format(finish-start))


def main():
    data = loadData()
    players, gameStas = transformData(data)
    exportData(players, gameStas)

if __name__ == "__main__":
    main()