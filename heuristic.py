import random
import math
import ast
import time
from datetime import datetime as dt
#                                                                    +---------+
#                                                                    | BASICS: |
#                                                                    +---------+
# this script learns the correct actions to take when it faces corresponding scenarios, each scenario has its own action. changing scenario amount will thus also change action amount
# NOTE: functions are used in reverse order, because functions must be defined before they are called and the functions call each other.
# NOTE 2: score represents the stats and ID of each action/scenario combination, that is why it's used as a central list.
# NOTE 3: reset must be true on initial execution if you want to execute with a custom amount of scenarios. Default is 2.
reset= True  # if False, progress is saved in a .txt ; if True, progress is reset. set to True when changing scenario_amount or old values will still be used
insights = False # if true, prints extra stats and lists
scenario_amount = 10 # defines amount of scenarios
repeat = "inf" # number of attempts that should be executed, if int: loop will be executed {repeat} times. setting it to "inf" will make the script repeat infinitely
cooldown = 0.25 # time (in seconds) inbetween each attempt
formatcharacter = "-" # customizes the character used to format reports
formatlength = 25 # customizes length of reports
timestamp = True # displays each attempt's timestamp, duh
#
#                                                                    +-------+
#                                                                    | CODE: |
#                                                                    +-------+
#
score=[] # basic strucure: (0,"green/green", 0, 0),(1,"green/red", 0, 0),(2,"red/green", 0, 0), (3,"red/red", 0,0)
scenarios=[]
actions=[]

#recompiling the score list, consisting of tuples: (index: int, "action/scenario": str, tries: int, successes: int)
for i in range(scenario_amount):
    scenarios.append(f"scenario{i+1}")
    actions.append(f"action{i+1}")
for i in range(len(actions)):
    for u in range(len(scenarios)):
        score.append((len(score), f"{actions[i]}/{scenarios[u]}",0,0))
if insights:
    print(f"score list length: {len(score)}")
#checking if reset is set to True, if so, contents of the txt are wiped and replaced with previously recompiled score contents
if reset:
    with open("score.txt","w",encoding="utf-8") as file:
        file.write(str(score))
        print("score reset")

# changes current selected scenario to a random one from score; .split("/") is used because action and scenario are formated in a single string ("action/scenario")
def randomScenario():
    dec = random.randint(0,len(score)-1)
    return score[dec][1].split("/")[1]

#after each attempt, saves current score in the txt
def save():
    with open("score.txt","w",encoding="utf-8") as file:
        file.write(str(score))
    if insights:
        print(score)

# function that executes/evaluates the attempt. if successful tries +1 and successes +1 , else tries +1
def execute(index,state):
    action = state.split("/")[0]
    scenario = state.split("/")[1]
    templist = list(score[index])
    templist[2] +=1
    now= dt.now()
    currentTime = now.strftime("%H:%M:%S")
    messageFormater = lambda x: (x - (len(action)+len(scenario))) * formatcharacter
    if action[6:] ==scenario[8:]:
        print(f"{currentTime if timestamp else ""} chose {action} if {scenario} {messageFormater(formatlength)} CORRECT")
        templist[3] +=1
    else:
        print(f"{currentTime if currentTime else ""} chose {action} if {scenario} {messageFormater(formatlength - 1)} INCORRECT")
    score[index] = tuple(templist)
    save()

# decides which action is the best to take in the current scenario. this is mainly being calculated with successes / tries * math.log(tries) ; successes / tries calculates the success rate and log(tries) prevents cases like tries=1,successes=1,successrate=1.0 by reducing the values of rates with few attempts and increasing rates for those who have many attempts and are still successful
def decideAction():
    currentScenario=randomScenario()
    comparisonList=[]
    for index,state, tries, successes in score:
        if state.split("/")[1] == currentScenario:
            comparisonList.append((index,state,tries,successes))
    highestEntry = 0.0
    otherRates=[]
    badRates=[]
    for index,state,tries,successes in comparisonList:
        if tries:
            calculatedRate=successes / tries * math.log(tries)
            if calculatedRate > highestEntry and calculatedRate > 1:
                highestEntry = calculatedRate
                highestEntryState = state
                highestEntryIndex = index
        if not tries > successes:
            otherRates.append((index,state,tries,successes))
        else:
            badRates.append((index,state,tries,successes))
    if highestEntry > 0.0:
        execute(highestEntryIndex,highestEntryState)
    elif len(otherRates) > 0:
        exeIndex, exeState, ennie, meenie = otherRates[random.randint(0, len(otherRates) - 1)] if len(otherRates) > 1 else otherRates[0]
        execute(exeIndex,exeState)
    else:
        exeIndex, exeState, ennie, meenie = badRates[random.randint(0, len(badRates) - 1)] if len(badRates) > 1 else badRates[0]
        execute(exeIndex,exeState)
    if insights:
        print(highestEntry)

# import score from the txt
def importScore():
    with open("score.txt","r",encoding="utf-8") as file:
        global score
        contents = file.read()
        score =ast.literal_eval(contents)
        decideAction()

#repeating the functions
if repeat == "inf":
  while True:
      importScore()
      time.sleep(cooldown)
elif isinstance(repeat, int):
  for i in range(repeat):
    importScore()
    time.sleep(cooldown)
