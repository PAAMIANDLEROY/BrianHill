#Import Part
import yaml #beug with streamlit. Need correction
import matplotlib.pyplot as plt
import matplotlib as mpl
import base64
import numpy as np
from pywaffle import Waffle as Wf
#import class_range_slider as crs
#
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb
import streamlit as st

import mpld3
#import fonction and Script
import time
import math
import csv
import datetime
from scipy.spatial import distance
from sympy.solvers import solve
from sympy import Symbol
import pandas as pd
X = Symbol('x')

def set_config(name_variable,value_init=[]):
    if name_variable not in st.session_state:
        st.session_state[name_variable]=value_init
def update_value(name_variable,value):
    st.session_state[name_variable]=value
# Point de départ
liste_variable=['objv','itv','betv','dzv','vhypo','phypo','vstop','az1','az2','dz1','dz2','az1h','az2h','maxiter','retrunOnlyAtLogs','sup_info','beforeMaxIter','useWhile','useReturn','returnAtEachBet']
def init():
    for var in liste_variable:
        st.session_state[var]=[]


    # Paramètre de calibration: nombre de point objectifs, voisinage de l'hypo et précision de l'élicitation sur l'hypo
    update_value('vhypo',44)  # voisinage de l'hypothenuse où on passe sur l'hypo
    update_value('phypo',5)  # distance d'arrêt sur l'hypothenuse
    update_value('vstop',15)  # distance euclidienne à partir de laquelle on stoppe l'algorithme
    update_value('maxiter',int(12/2))
    update_value('retrunOnlyAtLogs',True)
    update_value('sup_info',[""])
    update_value('beforeMaxIter',[0])
    update_value('useWhile',False)
    update_value('useReturn',not st.session_state['useWhile'])
    update_value('returnAtEachBet',not st.session_state['useWhile'])

def zone(opts):
    if(opts==["A","B"]): czone="az1"
    elif(opts==["B","A"]): czone="az2"
    elif(opts==["B","B"]): czone="dz1"
    elif(opts==["A","A"]): czone="dz2"
    return czone




def result(bet, finished=0, finishedBefMaxIter=None):
    for var in liste_variable:
        set_config(var,value_init=[])
        exec(var+"=st.session_state[var]")
    sumlen = len(az1) + len(az2) + len(dz1) + len(dz2)
    nzdict = {"n_az1": len(az1), "n_az2": len(az2), "n_dz1": len(dz1), "n_dz2": len(dz2),
              "n_dz_tot": (len(dz1) + len(dz2))}
    initfinished = finished
    if (finishedBefMaxIter == None): finishedBefMaxIter = finished if useReturn else beforeMaxIter[0]
    if (returnAtEachBet and sumlen > maxiter): finished = 1
    finishedApartAlgo = int(initfinished == 0 and finished == 1)
    ccomments = sup_info[0]
    sup_info[0] = "";
    for var in liste_variable:
        update_value(var,eval(var))
    return (bet, finished, sumlen, nzdict, ccomments, finishedBefMaxIter, finishedApartAlgo, useReturn, useWhile)

def algo_main(bet, opts):
    for var in liste_variable:
        set_config(var,value_init=[])
        exec("global "+var+"; "+var+"=st.session_state['"+var+"']")
    # Critère d'arrêt de l'algo à 12 questions
    mainCondition = (len(az1) + len(az2) + len(dz1) + len(dz2) < maxiter)
    while mainCondition:
        mainCondition = (len(az1) + len(az2) + len(dz1) + len(dz2) < maxiter)

        ####Algo ####

#Reprendre phase 1
# Verifier critere darret
# Tester

        # Phase 1:
        if dz1 == [] and dz2 == []:

                    # Phase 1.4

            # Procedure in AZ1 on hypo
            if zone(opts) == "az1" and minc(az2, bet) != "Empty" and m(bet[0], bet[1]) >= vhypo:
                az1.append(bet)
                az1h.append(bet)
                bet = [x((alphamax1(az2, bet[0], bet[1]) + alpha(bet[0], bet[1])) / 2, 50),
                       y((alphamax1(az2, bet[0], bet[1]) + alpha(bet[0], bet[1])) / 2, 50)]
                log("az114", bet)
                if (returnAtEachBet): return result(bet, 0)

            # Procedure in AZ2 on hypo
            if zone(opts) == "az2" and minc(az1, bet) != "Empty" and m(bet[0], bet[1]) >= vhypo:
                az2.append(bet)
                az2h.append(bet)
                bet = [x((alphamin1(az1, bet[0], bet[1]) + alpha(bet[0], bet[1])) / 2, 50),
                        y((alphamin1(az1, bet[0], bet[1]) + alpha(bet[0], bet[1])) / 2, 50)]
                log("az214", bet)
                if (returnAtEachBet): return result(bet, 0)

            # Procedure d'arret sur l'hypo
                if m(bet[0], bet[1]) == 50 and az2h != [] and az1h != [] and \
                    az1h[np.argmin([az1h[i][0] for i in range(len(az1h))])][0] - \
                    az2h[np.argmax([az2h[i][0] for i in range(len(az2h))])][0] < phypo:
                    if (useReturn): return result(bet, 1)  # sumlen>=maxiter
                    if (not useReturn):
                        beforeMaxIter[0] = 1
                        break

            # Phase 1.1
            # Procedure in AZ1 if AZ2,m is empty
            if zone(opts) == "az1" and minc(az1, bet) != "Empty" and minc(az2, bet) == "Empty":
                az1.append(bet)
                bet = step2az1(bet[0], bet[1])
                log("az111", bet)
                if (returnAtEachBet): return result(bet, 0)

            # Procedure in AZ2 if AZ1,m is empty
            if zone(opts) == "az2" and minc(az2, bet) != "Empty" and minc(az1, bet) == "Empty":
                az2.append(bet)
                bet = step2az2(bet[0], bet[1])
                log("az211", bet)
                if (returnAtEachBet): return result(bet, 0)

            # Phase 1.2

            # Procedure in AZ1 if AZ2,m  is NOT empty
            if zone(opts) == "az1" and minc(az2, bet) != "Empty" and m(bet[0], bet[1]) < vhypo:
                az1.append(bet)
                bet = step1az1(bet[0], bet[1])
                log("az112", bet)
                if (returnAtEachBet and not retrunOnlyAtLogs):
                    return result(bet, 0)
                if (returnAtEachBet): return result(bet, 0)

            # Procedure in AZ2 if AZ1,m is NOT empty
            if zone(opts) == "az2" and minc(az1, bet) != "Empty" and m(bet[0], bet[1]) < vhypo:
                az2.append(bet)
                bet = step1az2(bet[0], bet[1])
                log("az212", bet)
                if (returnAtEachBet and not retrunOnlyAtLogs):
                    return result(bet, 0)
                if (returnAtEachBet): return result(bet, 0)

            # Phase 1.3

            # Procedure in AZ1 if no other point has the same m
            if zone(opts) == "az1" and minc(az1, bet) == "Empty" and minc(az2, bet) == "Empty":
                az1.append(bet)
                bet = [x((alpha(bet[0], bet[1]) + alphamax(az2))/2, m(bet[0], bet[1])), y((alpha(bet[0], bet[1]) + alphamax(az2))/2, m(bet[0], bet[1]))]
                log("az113", bet)
                if (returnAtEachBet): return result(bet, 0)

            # Procedure in AZ2 if no other point has the same m
            if zone(opts) == "az2" and minc(az1, bet) == "Empty" and minc(az2, bet) == "Empty":
                az2.append(bet)
                bet = [x((alpha(bet[0], bet[1]) + alphamin(az1))/2, m(bet[0], bet[1])), y((alpha(bet[0], bet[1]) + alphamin(az1))/2, m(bet[0], bet[1]))]
                log("az213", bet)
                if (returnAtEachBet): return result(bet, 0)


            # Procedure in DZ2
            if zone(opts) == "dz2":
                dz2.append(bet)
                bet = [(3*bet[0]+100-bet[1]) / 4, (100-bet[0]+3*(bet[1])) / 4]
                log("dz211", bet)
                if (returnAtEachBet): return result(bet, 0)
            # Procedure in DZ1
            if zone(opts) == "dz1":
                dz1.append(bet)
                if bet[0] - bet[1] > 0:
                    bet = [(2 * bet[0] - bet[1]) / 2, bet[1] / 2]
                elif bet[0] - bet[1] <= 0:
                    bet = [bet[0] / 2, (2 * bet[1] - bet[0]) / 2]
                log("dz111", bet)
                if (returnAtEachBet): return result(bet, 0)

        # Phase 2.1 DZ1 non vide:
        if dz1 != [] and dz2 == []:
            # Procedure in AZ1: case 1
            if zone(opts) == "az1":
                az1.append(bet)
                bet = [x((alpha(bet[0], bet[1]) + ralpha(m(bet[0], bet[1]), minbb(dz1))) / 2, m(bet[0], bet[1])),
                       y((alpha(bet[0], bet[1]) + ralpha(m(bet[0], bet[1]), minbb(dz1))) / 2, m(bet[0], bet[1]))]
                log("az121", bet)
                if (returnAtEachBet): return result(bet, 0)
            # Procedure in AZ2 : case 1
            if zone(opts) == "az2":
                az2.append(bet)
                bet = [x((alpha(bet[0], bet[1]) + balpha(m(bet[0], bet[1]), minb(dz1))) / 2, m(bet[0], bet[1])),
                       y((alpha(bet[0], bet[1]) + balpha(m(bet[0], bet[1]), minb(dz1))) / 2, m(bet[0], bet[1]))]
                log("az221", bet)
                # if  m(bet[0],bet[1]) < 0 or  m(bet[0],bet[1]) > 100:
                #	print "PROB"
                #	break
                if (returnAtEachBet): return result(bet, 0)

            # Procedure in DZ2
            if zone(opts) == "dz2":
                dz2.append(bet)
                bet = [(bet[0] + minb(dz1)[0]) / 2, (bet[1] + minb(dz1)[1]) / 2]
                log("dz221", bet)
                if distance.euclidean(minbb(dz1), maxbb(dz2)) < vstop:
                    betf = [(minbb(dz1)[0] + maxbb(dz2)[0]) / 2, (minbb(dz1)[1] + maxbb(dz2)[1]) / 2]
                    log(betf, "c3")
                    return result(betf, 1, 0)
                    break
                elif (returnAtEachBet):
                    return result(bet, 0)
                #if (returnAtEachBet): return result(bet, 0)
            # Procedure dans DZ1
            if zone(opts) == "dz1":
                dz1.append(bet)
                if bet[0] - bet[1] > 0:
                    bet = [(2 * bet[0] - bet[1]) / 2, bet[1] / 2]
                elif bet[0] - bet[1] <= 0:
                    bet = [bet[0] / 2, (2 * bet[1] - bet[0]) / 2]
                log("dz121", bet)
                if min(minbb(dz1)[0], minbb(dz1)[1]) < vstop:
                    betf = minbb(dz1)
                    log(betf, "c2.1")
                    return result(betf, 1, 0)
                    break
                elif (returnAtEachBet):
                    return result(bet, 0)
                #if (returnAtEachBet): return result(bet, 0)

            # Critre d'arret en phase 2.1



        # Phase 2.2 DZ2 non vide:
        if dz1 == [] and dz2 != []:
            # Procedure in AZ1:
            if zone(opts) == "az1":
                az1.append(bet)
                bet = [x((alpha(bet[0], bet[1]) + balpha(m(bet[0], bet[1]), maxb(dz2))) / 2, m(bet[0], bet[1])),
                       y((alpha(bet[0], bet[1]) + balpha(m(bet[0], bet[1]), maxb(dz2))) / 2, m(bet[0], bet[1]))]
                log("az122", bet)
                if (returnAtEachBet): return result(bet, 0)
            # Procedure in AZ2 :
            if zone(opts) == "az2":
                az2.append(bet)
                bet = [x((alpha(bet[0], bet[1]) + ralpha(m(bet[0], bet[1]), maxbb(dz2))) / 2, m(bet[0], bet[1])),
                       y((alpha(bet[0], bet[1]) + ralpha(m(bet[0], bet[1]), maxbb(dz2))) / 2, m(bet[0], bet[1]))]
                log("az222", bet)
                if (returnAtEachBet): return result(bet, 0)

            # Procedure in DZ2
            if zone(opts) == "dz2":
                dz2.append(bet)
                bet = [(3*bet[0]+100-bet[1]) / 4, (100-bet[0]+3*(bet[1])) / 4]
                log("dz222", bet)
                if 100 - maxbb(dz2)[0] - maxbb(dz2)[1] < vstop:
                    betf = maxbb(dz2)
                    log(betf, "c2.2")
                    return result(betf, 1, 0)
                    break
                elif (returnAtEachBet):
                    return result(bet, 0)
                #if (returnAtEachBet): return result(bet, 0)
            # Procedure dans DZ1
            if zone(opts) == "dz1":
                dz1.append(bet)
                bet = [(bet[0] + maxb(dz2)[0]) / 2, (bet[1] + maxb(dz2)[1]) / 2]
                log("dz122", bet)
                if distance.euclidean(minbb(dz1), maxbb(dz2)) < vstop:
                    betf = [(minbb(dz1)[0] + maxbb(dz2)[0]) / 2, (minbb(dz1)[1] + maxbb(dz2)[1]) / 2]
                    log(betf, "c3")
                    return result(betf, 1, 0)
                    break
                elif (returnAtEachBet):
                    return result(bet, 0)
                #if (returnAtEachBet): return result(bet, 0)




        # Phase 3:
        if dz1 != [] and dz2 != []:
            # Procedure in DZ1:
            if zone(opts) == "dz1":
                dz1.append(bet)
                bet = [(bet[0] + maxb(dz2)[0]) / 2, (bet[1] + maxb(dz2)[1]) / 2]
                log("dz131", bet)
                if distance.euclidean(minbb(dz1), maxbb(dz2)) < vstop:
                    betf = [(minbb(dz1)[0] + maxbb(dz2)[0]) / 2, (minbb(dz1)[1] + maxbb(dz2)[1]) / 2]
                    log(betf, "c3")
                    return result(betf, 1, 0)
                    break
                elif (returnAtEachBet):
                    return result(bet, 0)
                #if (returnAtEachBet): return result(bet, 0)
            # Procedure in DZ2:
            if zone(opts) == "dz2":
                dz2.append(bet)
                bet = [(bet[0] + minb(dz1)[0]) / 2, (bet[1] + minb(dz1)[1]) / 2]
                log("dz231", bet)
                if distance.euclidean(minbb(dz1), maxbb(dz2)) < vstop:
                    betf = [(minbb(dz1)[0] + maxbb(dz2)[0]) / 2, (minbb(dz1)[1] + maxbb(dz2)[1]) / 2]
                    log(betf, "c3")
                    return result(betf, 1, 0)
                    break
                elif (returnAtEachBet):
                    return result(bet, 0)
                #if (returnAtEachBet): return result(bet, 0)

            # Procedure in AZ1:
            if zone(opts) == "az1":
                az1.append(bet)
                bet = [x((alpha(bet[0], bet[1]) + max(ralpha(m(bet[0], bet[1]), minbb(dz1)),
                                                      balpha(m(bet[0], bet[1]), maxb(dz2)))) / 2,
                         m(bet[0], bet[1])), y((alpha(bet[0], bet[1]) +  max(ralpha(m(bet[0], bet[1]), minbb(dz1)),
                                                      balpha(m(bet[0], bet[1]), maxb(dz2)))) / 2,
                                               m(bet[0], bet[1]))]
                log("az13", bet)
                if (returnAtEachBet): return result(bet, 0)
            # Procedure in AZ2 :
            if zone(opts) == "az2":
                az2.append(bet)
                bet = [x((alpha(bet[0], bet[1]) + min(balpha(m(bet[0], bet[1]), minb(dz1)),
                                                      ralpha(m(bet[0], bet[1]), maxbb(dz2)))) / 2,
                         m(bet[0], bet[1])), y((alpha(bet[0], bet[1]) + min(balpha(m(bet[0], bet[1]), minb(dz1)),
                                                      ralpha(m(bet[0], bet[1]), maxbb(dz2)))) / 2,
                                               m(bet[0], bet[1]))]
                log("az23", bet)
                if (returnAtEachBet): return result(bet, 0)




        if (useReturn): return result(bet, 0)
    if (not useReturn or not mainCondition):

        # Point retenu
        if dz1 == [] and dz2 == [] and m(bet[0], bet[1]) < vhypo:  # Point retenu phase 1.2, 1.3
            bet = [(minbb(az2)[0] + maxbb(az1)[0]) / 2, (minbb(az2)[1] + maxbb(az1)[1]) / 2]
            log(bet, "c1")
            if (returnAtEachBet): return result(bet, 1, 0)
        if m(bet[0], bet[1]) == 50 and az2h != [] and az1h != [] and \
                az1h[np.argmin([az1h[i][0] for i in range(len(az1h))])][0] - \
                az2h[np.argmax([az2h[i][0] for i in range(len(az2h))])][
                    0] < phypo:  # Point retenu sur l'hypo phase 1
            bet = [(az2h[np.argmax([az2h[i][0] for i in range(len(az2h))])][0] +
                    az1h[np.argmin([az1h[i][0] for i in range(len(az1h))])][0]) / 2, (
                               az2h[np.argmax([az2h[i][0] for i in range(len(az2h))])][1] +
                               az1h[np.argmin([az1h[i][0] for i in range(len(az1h))])][1]) / 2]
            log(bet, "ch")
            if (returnAtEachBet): return result(bet, 1, 0)
        if dz1 != [] and dz2 == []:  # Point retenu phase 2.1
            bet = minbb(dz1)
            log(bet, "c2.1")
            if (returnAtEachBet): return result(bet, 1, 0)
        if dz1 == [] and dz2 != []:  # Point retenu phase 2.2
            bet = maxbb(dz2)
            log(bet, "c2.2")
            if (returnAtEachBet): return result(bet, 1, 0)
        if dz1 != [] and dz2 != []:  # Point retenu phase 3
            bet = [(minbb(dz1)[0] + maxbb(dz2)[0]) / 2, (minbb(dz1)[1] + maxbb(dz2)[1]) / 2]
            log(bet, "c3")
            if (returnAtEachBet): return result(bet, 1, 0)

        log(len(az1), len(az2), len(dz1), len(dz2), bet)
        if (not useReturn): finalZone = zone(opts)
        return result(bet, 1, 0)


# Résultats: nombre moyen d'itération par point obj, distance moyenne du point élicité au point obj

# log( np.mean(itv), np.mean(dzv), np.mean([math.sqrt(v[0]**2 + v[1]**2) for i,v in enumerate(betv - np.array(objv))]))

# def algo2(*algovars):

#def runAlgo():
#Point de départ

# bet = [30,30]

#bet[0] -> blue
#bet[1] -> red

#Vecteurs de résultats: objectif, nombre d'iteration et point elicité

# objv = []
# itv = []
# betv = []
# dzv = []

# Paramètre de calibration: nombre de point objectifs, voisinage de l'hypo et précision de l'élicitation sur l'hypo

# d= 1
# vhypo = 44
# phypo = 2


#Tirage aléatoire d'un vecteur de points objectifs

#low = np.random.randint(low=0, high=100+1, size=d)

#for i in range(d):
	# obj = [low[i],np.random.randint(low=0, high=100 - low[i] + 1, size=1)[0]]
	# objv.append(obj)


	# az1 = []
	# az2 = []
	# dz1 = []
	# dz2 = []
	# az1h = []
	# az2h = []

	# Droites d'indifférence

	# cb1 = np.random.randint(low=1, high=10+1, size=1)
	# cb2 = obj[1] - cb1*obj[0]
	# 
	# cr1 = np.random.randint(low=1, high=cb1+1, size=1)
	# cr2 = obj[1] - cr1*obj[0]
	
	# opts = ["B","B"]

	#print(obj)
	#print(cb1)
	#print(cb2)
	#print(cr1)
	#print(cr2)
  

	# algo_fun=algo(False,"print") #"logfile.txt" instead of "print" in order to write to a log file
	# algo_fun(bet,zone)
  
#print(np.mean(itv), np.mean(dzv), np.mean([math.sqrt(v[0]**2 + v[1]**2) for i,v in enumerate(betv - np.array(objv))]))

def step1az2(a, b):
    if m(a, b) <= vhypo:
        return [x((alphamin1(az1, a, b) + alpha(a, b)) / 2, (m(a, b) + 50) / 2),
                y((alphamin1(az1, a, b) + alpha(a, b)) / 2, (m(a, b) + 50) / 2)]
    elif m(a, b) > vhypo:  # if bet is close to hypo
        return [x((alphamin1(az1, a, b) + alpha(a, b)) / 2, 50),
                y((alphamin1(az1, a, b) + alpha(a, b)) / 2, 50)]

def step1az1(a, b):
    if m(a, b) <= vhypo:
        return [x((alphamax1(az2, a, b) + alpha(a, b)) / 2, (m(a, b) + 50) / 2),
                y((alphamax1(az2, a, b) + alpha(a, b)) / 2, (m(a, b) + 50) / 2)]
    elif 50 >= m(a, b) > vhypo:  # if bet is close to hypo
        return [x((alphamax1(az2, a, b) + alpha(a, b)) / 2, 50),
                y((alphamax1(az2, a, b) + alpha(a, b)) / 2, 50)]

def step2az2(a, b):
    if m(a, b) <= vhypo:
        return [x((1 + alpha(a, b)) / 2, (m(a, b) + 50) / 2),
                y((1 + alpha(a, b)) / 2, (m(a, b) + 50) / 2)]
    elif m(a, b) > vhypo:  # if bet is close to hypo
        return [x((1 + alpha(a, b)) / 2, 50),
                y((1 + alpha(a, b)) / 2, 50)]

def step2az1(a, b):
    if m(a, b) <= vhypo:
        return [x(alpha(a, b) / 2, (m(a, b) + 50) / 2),
                y(alpha(a, b) / 2, (m(a, b) + 50) / 2)]
    elif 50 >= m(a, b) > vhypo:  # if bet is close to hypo
        return [x(alpha(a, b) / 2, 50),
                y(alpha(a, b) / 2, 50)]



def alpha(a, b):
    if a < b:
        return 0.5 * (1 - float(b - a) / 100)
    if a >= b:
        return float(a - b) / 200 + 0.5

def m(a, b):  # distance a l'origine
    if a == 100:
        return 50
    if b == 100:
        return 50
    if a < b:
        return float(100 * a) / (a - b + 100)
    if a >= b:
        return float(b * 100) / (b + 100 - a)

def x(al, m):
    if al < 0.5:
        return float(2 * al * m)
    if al >= 0.5:
        return float(200 * (al - 0.5) + (1 - 2 * (al - 0.5)) * m)

def y(al, m):
    if al < 0.5:
        return float(2 * al * m + (1 - 2 * al) * 100)
    if al >= 0.5:
        return float((1 - 2 * (al - 0.5)) * m)

def ralpha(m, r):  # returns the alpha of the intersection of a r line and of a m line
    r = r[1]
    #c = solve(2 * X * m + (1 - 2 * X) * 100 - r)[0]
    # d = solve((1 - 2 * (X - 0.5)) * m - r)[0]
    c = (100-r)/(2*(100-m))
    d = 1 - (r/(2*m))
    if r >= m:
        return c
    if r < m:
        return d

def balpha(m, b):  # returns the alpha of the intersection of a b line and of a m line
    b = b[0]
    #c = solve(2 * X * m - b)[0]
    #d = solve(200 * (X - 0.5) + (1 - 2 * (X - 0.5)) * m - b)[0]
    c = b/(2*m)
    d = (b + 100 - 2*m)/(2*(100 - m))
    if b <= m:
        return c
    if b > m:
        return d

def alphamax(az):  # returns the biggest alpha in a zone
    if az == []:
        return 0
    elif az != []:
        return max([alpha(v[0], v[1]) for i, v in enumerate(az)])

def alphamin(az):  # returns the smallest alpha in a zone
    if az == []:
        return 1
    elif az != []:
        return min([alpha(v[0], v[1]) for i, v in enumerate(az)])

def alphamax1(az, a, b):  # returns the biggest alpha in a zone which has the same m than a given point (a,b)
    if az == []:
        return 0
    if az != []:
        l = []
        for i, v in enumerate(az):
            if np.abs(m(v[0], v[1]) - m(a, b)) < 0.05:
                l.append(alpha(v[0], v[1]))
        if l == []:
            return 0
        if l != []:
            return max(l)

def alphamin1(az, a, b):  # returns the smallest alpha in a zone which has the same m than a given point (a,b)
    if az == []:
        return 1
    if az != []:
        l = []
        for i, v in enumerate(az):
            if np.abs(m(v[0], v[1]) - m(a, b)) < 0.05:
                l.append(alpha(v[0], v[1]))
        if l == []:
            return 1
        if l != []:
            return min(l)

def indicmin(dz):  # returns the point in a zone with the minimum a+b coordinates
    return dz[np.argmin([dz[i][0] + dz[i][1] for i in range(len(dz))])]

def indicmax(dz):  # returns the point in a zone with the maximum a+b coordinates
    return dz[np.argmax([dz[i][0] + dz[i][1] for i in range(len(dz))])]

def minb(dz):  # returns the point in a zone with the minimum first coordinate
    return dz[np.argmin([dz[i][0] for i in range(len(dz))])]

def maxb(dz):  # returns the point in a zone with the maximum first coordinate
    return dz[np.argmax([dz[i][0] for i in range(len(dz))])]

def minbb(dz):  # returns the point in a zone with the minimum second coordinate
    return dz[np.argmin([dz[i][1] for i in range(len(dz))])]

def maxbb(dz):  # returns the point in a zone with the maximum second coordinate
    return dz[np.argmax([dz[i][1] for i in range(len(dz))])]


def minc(az, bet):  # returns the points in a zone which have the same m than a given point bet
    minaz = []
    for i, v in enumerate(az):
        if np.abs(m(v[0], v[1]) - m(bet[0], bet[1])) < 5:
            minaz.append(v)
    if minaz == []:
        return "Empty"
    else:
        return minaz

def log(*argsv):
    if (len(argsv) > 0):
        if True :#(argsv[0] == "print"):
            print(argsv)
        else:
            try:
                with open(algovars[0], 'a') as csvfile:
                    delimiter = ","
                    w = csv.writer(csvfile, delimiter=delimiter)
                    w.writerow([str(datetime.datetime.now())] + list(argsv))
            except  Exception as inst:
                print("Log entry non written on " + str(datetime.datetime.now()), inst)
    else:
        sup_info[0] += "; " if sup_info[0] != "" else ""
        sup_info[0] += str(','.join(map(lambda x: str(x), argsv)))



#Config
st.set_page_config(
    page_title="Brian Hill", layout="wide", page_icon="images/flask.png"
)
if 'finish' not in st.session_state:
    st.session_state.finish=0
if 'config' not in st.session_state:
    st.session_state.config={}
if 'cmpt_page' not in st.session_state:
    st.session_state.cmpt_page=-3
if 'cmpt_exp' not in st.session_state:
    st.session_state.cmpt_exp=0
if 'save_bet' not in st.session_state:
    st.session_state.save_bet=[]
if 'all_save_bet' not in st.session_state:
    st.session_state.all_save_bet=[]
if 'new_bet' not in st.session_state:
    st.session_state.new_bet=[30,30]
if 'histo' not in st.session_state:
    st.session_state.histo=[]
if 'histo_opts' not in st.session_state:
    st.session_state.histo_opts=[]
if 'slider_value' not in st.session_state:
    st.session_state.slider_value=[30,30]
if 'save_exp' not in st.session_state:
    st.session_state.save_exp=[]

color_Green='#54cc33'
color_Yellow='#e4e805'
color_Red='#ff0000'
color_Blue='#0000ff'
color_Grey='#b3b3b3'
color_White='#ffffff'
def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))




#Useful function
def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

def up_cmpt():
    st.session_state.cmpt_page+=1


def label(xy, text):
    y = xy[1] - 0.15  # shift y-value for label so that it's below the artist
    plt.text(xy[0], y, text, ha="center", family='sans-serif', size=14)
def validation(values,opts):
    st.session_state.histo.append(values)
    bet, finished, sumlen, nzdict, ccomments, finishedBefMaxIter, finishedApartAlgo, useReturn, useWhile=algo_main(values,opts)
    bet=[int(bet[0]),int(bet[1])]
    
    return bet, finished, sumlen, nzdict, ccomments, finishedBefMaxIter, finishedApartAlgo, useReturn, useWhile




####################################################block 1 => ###########################



def front_choice_bias(Winning_amount,Number_of_ball,Freq_green):
    blue=st.session_state.new_bet[1]
    red=st.session_state.new_bet[0]
    grey=100-blue-red
    values_recup=st.session_state.slider_value
    col1,col3, col2 = st.columns([2,1,2])
    with col1:
        
        col1a,col1b=st.columns([2.3,3])#COL1A;COL1B
        with col1a:
            st.subheader("  ")
            st.write(str(Number_of_ball)+" draws were made, with "+str(int(Number_of_ball*Freq_green))+" green balls.")
            st.write("The others were yellow")
            fig3 = plt.figure(
                FigureClass=Wf,
                rows=int(math.sqrt(Number_of_ball)),
                #columns=10,  # Either rows or columns could be omitted
                values=[int(Number_of_ball*Freq_green), Number_of_ball-int(Number_of_ball*Freq_green)],
                colors=[color_Green,color_Yellow],
                characters='⬤',
                font_size=20)
            st.pyplot(fig3)
        with col1b:
            st.subheader("  ")
            st.subheader("Option A")
            fig1, ax1=plt.subplots()#figsize=(4,4))
            x1,y1 = ([0,-0.1,0], [-0.1,0,0.1])
            line1 = mpl.lines.Line2D(x1,y1, lw=10., alpha=0.9)
            value_money=st.session_state.cmpt_page%2*Winning_amount
            plt.text(0.1, 0.1, "Green: "+str(value_money)+"€", ha="center", family='sans-serif', size=30)
            plt.text(0.1, -0.1, "Yellow: "+str(20-value_money)+"€", ha="center", family='sans-serif', size=30)
            ax1.add_line(line1)
            plt.axis('equal')
            plt.axis('off')
            plt.tight_layout()
            st.pyplot(fig1)
    with col3:
        st.subheader("  ")
        st.subheader("Experiment number "+str(st.session_state.cmpt_exp+1))
        st.subheader("  ")
        choice=st.radio("Which option do you choose ?",('Option A', 'Option B'),horizontal=True,index=np.random.randint(2))
        choice='A' if choice=='Option A' else 'B'
        button_val=st.button('Validation',key='val1')
        if button_val:
            button_val=False
            up_cmpt()
            st.session_state.save_bet.append([red,blue])
            st.session_state.histo_opts.append(choice)
            if st.session_state.cmpt_page%2==0:
                opts=st.session_state.histo_opts[-2:]
                bet, finished, sumlen, nzdict, ccomments, finishedBefMaxIter, finishedApartAlgo, useReturn, useWhile=validation([red,blue],opts)
                list_save=[time.strftime("%Y/%m/%d %Hh%M")]+st.session_state.pers_info+[int(st.session_state.cmpt_exp),finished,int(st.session_state.cmpt_page),list(st.session_state.save_bet),list(st.session_state.histo_opts),nzdict]
                st.session_state.save_exp.append(list_save)
                st.session_state.new_bet=bet
                if finished:
                    st.session_state.all_save_bet.append(st.session_state.save_bet)
                    st.session_state.save_bet=[]
                    st.session_state.histo_ops=[]
                    st.session_state.new_bet=[30,30]
                    st.session_state.cmpt_exp+=1
                    init()
                    st.session_state.cmpt_page=0
                    st.write("It's finished, we will send the results")
            st.experimental_rerun()
    with col2:
        
        col2a,col2b=st.columns([3,2.3])
        with col2b:
            st.subheader("  ")
            st.subheader("Option B")
            fig4 = plt.figure(
                FigureClass=Wf,
                rows=10,
                columns=10,  # Either rows or columns could be omitted
                values=[red,grey,blue],
                colors=[color_Red,color_Grey,color_Blue],
                characters='⬤',
                font_size=20,
                )
            st.pyplot(fig4)
        with col2a:
            st.subheader("  ")
            st.subheader("  ")
            st.subheader("  ")
            fig3, ax3=plt.subplots()#figsize=(4,4))
            x3,y3 = ([0,0.1,0], [-0.1,0,0.1])
            line3 = mpl.lines.Line2D(x3,y3, lw=10., alpha=0.9)
            value_money=st.session_state.cmpt_page%2*Winning_amount
            plt.text(-0.1, 0.1, "Red: "+str(value_money)+"€", ha="center", family='sans-serif', size=30)
            plt.text(-0.1, -0.1, "Blue: "+str(20-value_money)+"€", ha="center", family='sans-serif', size=30)
            ax3.add_line(line3)
            plt.axis('equal')
            plt.axis('off')
            plt.tight_layout()
            st.pyplot(fig3)    
    return 0

################################################<=block1###############block 2 => ############################################################################

def front_choice_unbias(Winning_amount,Number_of_ball,Freq_green):
    blue=st.session_state.new_bet[1]
    red=st.session_state.new_bet[0]
    grey=100-blue-red
    values_recup=st.session_state.slider_value
    col1,col3, col2 = st.columns([2,1,2])
    with col1:
        
        col1a,col1b=st.columns([2.3,3])#COL1A;COL1B
        with col1a:
            st.subheader("  ")
            fig3 = plt.figure(
                FigureClass=Wf,
                rows=int(math.sqrt(Number_of_ball)),
                #columns=10,  # Either rows or columns could be omitted
                values=[int(Number_of_ball*Freq_green), Number_of_ball-int(Number_of_ball*Freq_green)],
                colors=[color_Green,color_Yellow],
                characters='⬤',
                font_size=20)
            st.pyplot(fig3)
            st.write(str(Number_of_ball)+" draws were made, with "+str(int(Number_of_ball*Freq_green))+" green balls.")
            st.write("The others were yellow")
        with col1b:
            st.subheader("  ")
            st.subheader("Option A")
            fig1, ax1=plt.subplots()#figsize=(4,4))
            x1,y1 = ([0,-0.1,0], [-0.1,0,0.1])
            line1 = mpl.lines.Line2D(x1,y1, lw=10., alpha=0.9)
            value_money=st.session_state.cmpt_page%2*Winning_amount
            plt.text(0.1, 0.1, "Green: "+str(value_money)+"€", ha="center", family='sans-serif', size=30)
            plt.text(0.1, -0.1, "Yellow: "+str(20-value_money)+"€", ha="center", family='sans-serif', size=30)
            ax1.add_line(line1)
            plt.axis('equal')
            plt.axis('off')
            plt.tight_layout()
            st.pyplot(fig1)
    with col3:
        if not st.session_state.finish:
            st.subheader("  ")
            st.subheader("Experiment number "+str(st.session_state.cmpt_exp+1))
            st.subheader("  ")
            choice=st.radio("Which option do you choose ?",('Option A', 'Option B'),horizontal=True,index=np.random.randint(2))
            choice='A' if choice=='Option A' else 'B'
            button_val=st.button('Validation',key='val1')
            if button_val:
                button_val=False
                up_cmpt()
                st.session_state.save_bet.append([red,blue])
                st.session_state.histo_opts.append(choice)
                if st.session_state.cmpt_page%2==0:
                    opts=st.session_state.histo_opts[-2:]
                    bet, finished, sumlen, nzdict, ccomments, finishedBefMaxIter, finishedApartAlgo, useReturn, useWhile=validation(st.session_state.slider_value,opts)
                    list_save=[time.strftime("%Y/%m/%d %Hh%M")]+st.session_state.pers_info+[int(st.session_state.cmpt_exp),finished,int(st.session_state.cmpt_page),list(st.session_state.save_bet),list(st.session_state.histo_opts),nzdict]
                    st.session_state.save_exp.append(list_save)
                    st.session_state.new_bet=bet##a verifier
                    st.session_state.finish=finished
                    st.experimental_rerun()
                else:
                    st.experimental_rerun()
                    #st.session_state.save_bet=bet

        if st.session_state.finish:
            st.subheader("")
            st.subheader("  ")
            st.subheader("")
            if [red,blue]!=st.session_state.slider_value:
                if red!=st.session_state.slider_value[0]:
                    choice=st.radio("Which option do you choose ?",('Option A', 'Option B'),horizontal=True,index=0)
                else:
                    choice=st.radio("Which option do you choose ?",('Option A', 'Option B'),horizontal=True,index=1)
            else:
                choice=st.radio("Which option do you choose ?",('Option A', 'Option B'),horizontal=True,index=1)
            choice='A' if choice=='Option A' else 'B'
            st.write("Option "+str(choice)+" is selected")
            st.write("Experiment number "+str(st.session_state.cmpt_exp+1))
       
    with col2:
        
        col2a,col2b=st.columns([3,2.3])
        with col2b:
            st.subheader("  ")
            st.subheader("Option B")
            fig4 = plt.figure(
                FigureClass=Wf,
                rows=10,
                columns=10,  # Either rows or columns could be omitted
                values=[red,grey,blue],
                colors=[color_Red,color_Grey,color_Blue],
                characters='⬤',
                font_size=20,
                )
            st.pyplot(fig4)
        with col2a:
            st.subheader("  ")
            st.subheader("  ")
            st.subheader("  ")
            fig3, ax3=plt.subplots()#figsize=(4,4))
            x3,y3 = ([0,0.1,0], [-0.1,0,0.1])
            line3 = mpl.lines.Line2D(x3,y3, lw=10., alpha=0.9)
            value_money=st.session_state.cmpt_page%2*Winning_amount
            plt.text(-0.1, 0.1, "Red: "+str(value_money)+"€", ha="center", family='sans-serif', size=30)
            plt.text(-0.1, -0.1, "Blue: "+str(Winning_amount-value_money)+"€", ha="center", family='sans-serif', size=30)
            ax3.add_line(line3)
            plt.axis('equal')
            plt.axis('off')
            plt.tight_layout()
            st.pyplot(fig3)
    if st.session_state.finish:
        values_recup=finish_part(red,blue,grey)
    return 0
def finish_part(red,blue,grey):
    fig4b = plt.figure(figsize=(10,0.8))
    ax4b = fig4b.add_axes([0.05, 0.475, 0.9, 0.15])
    cmap = mpl.colors.ListedColormap([color_White,color_Blue])
    bounds = [0,red+grey,100]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    cb4b = mpl.colorbar.ColorbarBase(ax4b, cmap=cmap,
                                    norm=norm,
                                    ticks=bounds,  # optional
                                    spacing='proportional',
                                    orientation='horizontal')
    ax4b.axis('off')
    st.pyplot(fig4b)
    fig4a = plt.figure(figsize=(10,0.8))
    ax4a = fig4a.add_axes([0.05, 0.475, 0.9, 0.15])
    cmap = mpl.colors.ListedColormap([color_Red,color_White])
    bounds = [0,red,100]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    cb4a = mpl.colorbar.ColorbarBase(ax4a, cmap=cmap,
                                    norm=norm,
                                    ticks=bounds,  # optional
                                    spacing='proportional',
                                    orientation='horizontal')
    ax4a.axis('off')
    st.pyplot(fig4a)
            
    options=list(range(101))
    st.write('Option A')
    values_recup = st.select_slider(' ',options, value = (red,100-blue),format_func=lambda x:'')#on_change=_update_slider
    values_recup=list(values_recup)
    values_recup[1]=100-values_recup[1]
    st.session_state.slider_value=values_recup
    colR,colW, colB = st.columns([1.6,2,1])
    with colR:
        st.write('The Red value is equal to '+str(values_recup[0]))
    with colW:
        st.write("The Red value can't inferior than "+str(red)+". The Blue value can't inferior than "+str(blue))
        st.write("You can change only one color")
        button_val_rez=st.button('Validation result')
        if button_val_rez:
            if values_recup[0]<red:
                st.write('red is too low')
            elif values_recup[1]<blue:
                st.write('blue is too low')
            elif values_recup[1]!=blue and values_recup[0]!=red:
                st.write('You can move only one handles')
            else:
                finished=1
                list_save=[time.strftime("%Y/%m/%d %Hh%M")]+st.session_state.pers_info+[int(st.session_state.cmpt_exp),finished,int(st.session_state.cmpt_page),list(st.session_state.save_bet),list(st.session_state.histo_opts),{}]
                st.session_state.save_exp.append(list_save)
                st.session_state.histo.append(st.session_state.histo_opts)
                st.session_state.all_save_bet.append(st.session_state.save_bet)
                st.session_state.save_bet=[]
                st.session_state.histo_opts=[]
                st.session_state.finish=0
                init()
                st.session_state.new_bet=[30,30]
                st.session_state.cmpt_exp+=1
                st.session_state.cmpt_page=0
                st.write("It's finished, we will send the results")
                st.experimental_rerun()
    with colB:
        st.write('The Blue value is equal to '+str(values_recup[1]))
    ColorMinMax = st.markdown(''' <style> div.stSlider > div[data-baseweb = "slider"] > div[data-testid="stTickBar"] > div {
    background: rgb(1 1 1 / 0%); } </style>''', unsafe_allow_html = True)
    Slider_Cursor = st.markdown(''' <style> div.stSlider > div[data-baseweb="slider"] > div > div > div[role="slider"]{
    background-color: rgb(14, 38, 74); box-shadow: rgb(14 38 74 / 20%) 0px 0px 0px 0.2rem;} </style>''', unsafe_allow_html = True)
    #background: linear-gradient(to right, rgba(151, 166, 195, 0.25) 0%, rgba(151, 166, 195, 0.25) 20%, rgb(255, 75, 75) 20%, rgb(255, 75, 75) 70%, rgba(151, 166, 195, 0.25) 70%, rgba(151, 166, 195, 0.25) 100%);
    #st.write(values_recup[0],values_recup[1],t)
    r,g,b = int(values_recup[0]),100-int(values_recup[0])-int(values_recup[1]),int(values_recup[1])
    #red_rgb=str(hex_to_rgb(color_Red))
    #blue_rgb=str(hex_to_rgb(color_Blue))
    col1 = f''' <style> div.stSlider > div[data-baseweb = "slider"] > div > div{{
    background: linear-gradient(90deg, red 0% {r}%, 
                            grey {r}% {100-b}%, 
                            blue {100-b}% 100%); }} </style>'''#rgb'''+red_rgb+''' 
    ColorSlider = st.markdown(col1, unsafe_allow_html = True)
    st.write('Option B')
    fig2a = plt.figure(figsize=(10,0.8))
    ax2a = fig2a.add_axes([0.05, 0.475, 0.9, 0.15])
    cmap = mpl.colors.ListedColormap([color_Blue,color_White])
    bounds = [0,red+grey,100]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    cb4a = mpl.colorbar.ColorbarBase(ax4a, cmap=cmap,
                                    norm=norm,
                                    ticks=bounds,  # optional
                                    spacing='proportional',
                                    orientation='horizontal')
    ax2a.axis('off')
    st.pyplot(fig4a)
    fig2b = plt.figure(figsize=(10, 0.8))
    ax2b = fig2b.add_axes([0.05, 0.475, 0.9, 0.15])
    cmap = mpl.colors.ListedColormap([color_White,color_Red])
    bounds = 100-np.array([0,red,100])
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    cb2b = mpl.colorbar.ColorbarBase(ax2b, cmap=cmap,
                                    norm=norm,
                                    ticks=bounds,  # optional
                                    spacing='proportional',
                                    orientation='horizontal')
    ax2b.axis('off')
    st.pyplot(fig2b)


    return values_recup


#############################################<=block2###################block 3=> ###############################################

def front_choice_stated(Winning_amount,Number_of_ball,Freq_green):
    blue=st.session_state.new_bet[1]
    red=st.session_state.new_bet[0]
    grey=100-blue-red
    values_recup=st.session_state.slider_value
    col1,col3, col2 = st.columns([2,1,2])
    with col1:
        col1a,col1b=st.columns([2.3,3])#COL1A;COL1B
        with col1a:
            st.subheader("  ")
            st.subheader("Option A")
            st.subheader(str(Number_of_ball)+" draws were made, with "+str(int(Number_of_ball*Freq_green))+" green balls.")
            st.subheader("The others were yellow")
##            fig3 = plt.figure(
##                FigureClass=Wf,
##                rows=int(math.sqrt(Number_of_ball)),
##                #columns=10,  # Either rows or columns could be omitted
##                values=[int(Number_of_ball*Freq_green), Number_of_ball-int(Number_of_ball*Freq_green)],
##                colors=[color_Green,color_Yellow],
##                characters='⬤',
##                font_size=20)
##            st.pyplot(fig3)
        with col1b:
            st.subheader("  ")
            st.subheader("Option A")
            fig1, ax1=plt.subplots()#figsize=(4,4))
            x1,y1 = ([0,-0.1,0], [-0.1,0,0.1])
            line1 = mpl.lines.Line2D(x1,y1, lw=10., alpha=0.9)
            value_money=st.session_state.cmpt_page%2*Winning_amount
            plt.text(0.1, 0.1, "Green: "+str(value_money)+"€", ha="center", family='sans-serif', size=30)
            plt.text(0.1, -0.1, "Yellow: "+str(20-value_money)+"€", ha="center", family='sans-serif', size=30)
            ax1.add_line(line1)
            plt.axis('equal')
            plt.axis('off')
            plt.tight_layout()
            st.pyplot(fig1)
    with col3:
        st.subheader("  ")
        st.subheader("Experiment number "+str(st.session_state.cmpt_exp+1))
        st.subheader("  ")
        choice=st.radio("Which option do you choose ?",('Option A', 'Option B'),horizontal=True,index=np.random.randint(2))
        choice='A' if choice=='Option A' else 'B'
        button_val=st.button('Validation')
        if button_val:
            button_val=False
            up_cmpt()
            st.session_state.save_bet.append([red,blue])
            st.session_state.histo_opts.append(choice)
            if st.session_state.cmpt_page%2==0:
                opts=st.session_state.histo_opts[-2:]
                bet, finished, sumlen, nzdict, ccomments, finishedBefMaxIter, finishedApartAlgo, useReturn, useWhile=validation([red,blue],opts)
                list_save=[time.strftime("%Y/%m/%d %Hh%M")]+st.session_state.pers_info+[int(st.session_state.cmpt_exp),finished,int(st.session_state.cmpt_page),list(st.session_state.save_bet),list(st.session_state.histo_opts),nzdict]
                st.session_state.save_exp.append(list_save)
                st.session_state.new_bet=bet
                #st.session_state.save_bet=bet
                if finished:
                    init()
                    st.session_state.histo.append(st.session_state.histo_opts)
                    st.session_state.all_save_bet.append(st.session_state.save_bet)
                    st.session_state.save_bet=[]
                    st.session_state.histo_opts=[]
                    st.session_state.new_bet=[30,30]
                    init()
                    st.session_state.cmpt_exp+=1
                    st.session_state.cmpt_page=0
                    st.write("It's finished, we will send the results")
            st.experimental_rerun()
    with col2:
        col2a,col2b=st.columns([3,2.3])
        with col2b:
            st.subheader("  ")
            st.subheader("Option B")
            st.subheader("In this urn, you have "+str(red)+" red balls, "+str(blue)+" blue balls and "+str(grey)+" blue or red.")
##            fig4 = plt.figure(
##                FigureClass=Wf,
##                rows=10,
##                columns=10,  # Either rows or columns could be omitted
##                values=[red,grey,blue],
##                colors=[color_Red,color_Grey,color_Blue],
##                characters='⬤',
##                font_size=20,
##                )
##            st.pyplot(fig4)
        with col2a:
            st.subheader("  ")
            st.subheader("  ")
            st.subheader("  ")
            fig3, ax3=plt.subplots()#figsize=(4,4))
            x3,y3 = ([0,0.1,0], [-0.1,0,0.1])
            line3 = mpl.lines.Line2D(x3,y3, lw=10., alpha=0.9)
            value_money=st.session_state.cmpt_page%2*Winning_amount
            plt.text(-0.1, 0.1, "Red: "+str(value_money)+"€", ha="center", family='sans-serif', size=30)
            plt.text(-0.1, -0.1, "Blue: "+str(20-value_money)+"€", ha="center", family='sans-serif', size=30)
            ax3.add_line(line3)
            plt.axis('equal')
            plt.axis('off')
            plt.tight_layout()
            st.pyplot(fig3)    

##    if st.session_state.cmpt_page>=2:
##
##        fig4b = plt.figure(figsize=(10,1))
##        ax4b = fig4b.add_axes([0.05, 0.475, 0.9, 0.15])
##        cmap = mpl.colors.ListedColormap([color_White,color_Blue])
##        bounds = [0,red+grey,100]
##        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
##        cb4b = mpl.colorbar.ColorbarBase(ax4b, cmap=cmap,
##                                        norm=norm,
##                                        ticks=bounds,  # optional
##                                        spacing='proportional',
##                                        orientation='horizontal')
##        ax4b.axis('off')
##        st.pyplot(fig4b)
##        fig4a = plt.figure(figsize=(10,1))
##        ax4a = fig4a.add_axes([0.05, 0.475, 0.9, 0.15])
##        cmap = mpl.colors.ListedColormap([color_Red,color_White])
##        bounds = [0,red,100]
##        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
##        cb4a = mpl.colorbar.ColorbarBase(ax4a, cmap=cmap,
##                                        norm=norm,
##                                        ticks=bounds,  # optional
##                                        spacing='proportional',
##                                        orientation='horizontal')
##        ax4a.axis('off')
##        st.pyplot(fig4a)
##                
##        options=list(range(101))
##        st.write('Option A')
##        values_recup = st.select_slider(' ',options, value = (red,100-blue),format_func=lambda x:'')#on_change=_update_slider
##        values_recup=list(values_recup)
##        values_recup[1]=100-values_recup[1]
##        st.session_state.slider_value=values_recup
##        colR,colW, colB = st.columns([1.6,2,1])
##        with colR:
##            st.write('The Red value is equal to '+str(values_recup[0]))
##        with colW:
##            st.write("The Red value can't superior than "+str(red)+". The Blue value can't superior than "+str(blue))
##        with colB:
##            st.write('The Blue value is equal to '+str(values_recup[1]))
##        ColorMinMax = st.markdown(''' <style> div.stSlider > div[data-baseweb = "slider"] > div[data-testid="stTickBar"] > div {
##        background: rgb(1 1 1 / 0%); } </style>''', unsafe_allow_html = True)
##        Slider_Cursor = st.markdown(''' <style> div.stSlider > div[data-baseweb="slider"] > div > div > div[role="slider"]{
##        background-color: rgb(14, 38, 74); box-shadow: rgb(14 38 74 / 20%) 0px 0px 0px 0.2rem;} </style>''', unsafe_allow_html = True)
##        #background: linear-gradient(to right, rgba(151, 166, 195, 0.25) 0%, rgba(151, 166, 195, 0.25) 20%, rgb(255, 75, 75) 20%, rgb(255, 75, 75) 70%, rgba(151, 166, 195, 0.25) 70%, rgba(151, 166, 195, 0.25) 100%);
##        #st.write(values_recup[0],values_recup[1],t)
##        r,g,b = int(values_recup[0]),100-int(values_recup[0])-int(values_recup[1]),int(values_recup[1])
##        #red_rgb=str(hex_to_rgb(color_Red))
##        #blue_rgb=str(hex_to_rgb(color_Blue))
##        col1 = f''' <style> div.stSlider > div[data-baseweb = "slider"] > div > div{{
##        background: linear-gradient(90deg, red 0% {r}%, 
##                                grey {r}% {100-b}%, 
##                                blue {100-b}% 100%); }} </style>'''#rgb'''+red_rgb+''' 
##        ColorSlider = st.markdown(col1, unsafe_allow_html = True)
##        st.write('Option B')
##        fig2a = plt.figure(figsize=(10,1))
##        ax2a = fig2a.add_axes([0.05, 0.475, 0.9, 0.15])
##        cmap = mpl.colors.ListedColormap([color_Blue,color_White])
##        bounds = [0,red+grey,100]
##        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
##        cb4a = mpl.colorbar.ColorbarBase(ax4a, cmap=cmap,
##                                        norm=norm,
##                                        ticks=bounds,  # optional
##                                        spacing='proportional',
##                                        orientation='horizontal')
##        ax2a.axis('off')
##        st.pyplot(fig4a)
##        fig2b = plt.figure(figsize=(10, 1))
##        ax2b = fig2b.add_axes([0.05, 0.475, 0.9, 0.15])
##        cmap = mpl.colors.ListedColormap([color_White,color_Red])
##        bounds = 100-np.array([0,red,100])
##        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
##        cb2b = mpl.colorbar.ColorbarBase(ax2b, cmap=cmap,
##                                        norm=norm,
##                                        ticks=bounds,  # optional
##                                        spacing='proportional',
##                                        orientation='horizontal')
##        ax2b.axis('off')
##        st.pyplot(fig2b)
##        if st.button('to_result'):
##            st.session_state.cmpt_exp+=1
##            st.experimental_rerun()
##    else:
##        pass
##
##    return 0

#############################################<=block3############################################################################


         
        
def process(Winning_amount):
    if st.session_state.cmpt_page==-3:
##        Nb_group=st.number_input('Number of group?',value=1)
        id_number=st.text_input('What is your ID?')
        name=st.text_input('What is your first and last name?')
        subject=st.text_input('Subject')
        age=st.number_input('What is your age?',value=0)
        gender=st.radio("What is your gender?",('Men','Female','Other'),index=2)
##        Freq_green_input=st.number_input("number of green ball",0,100,value=int(Freq_green*100))
##        Freq_green=Freq_green_input/100
##        Winning_amount=st.number_input("Winning_amount",value=Winning_amount)
        if st.button('Validation'):
            if st.session_state.cmpt_page==-3:
                st.session_state.pers_info=[id_number,name,subject,age,gender]
            up_cmpt()
            st.experimental_rerun()
    elif st.session_state.cmpt_page==-2:
        tirage_groupe=0#np.random.randint(6)
        st.session_state.config=load_config(tirage_groupe)
        st.write(tirage_groupe+1)
        st.write('inserer une vidéo')
        st.video("https://www.youtube.com/watch?v=0lROkD7pVz0")
        st.write('inserer une vidéo')
        st.video("https://www.youtube.com/watch?v=P-km9ksZkyg")
        if st.button('Validation'):
            up_cmpt()
            st.experimental_rerun()
    elif st.session_state.cmpt_page==-1:
        text_input_option=st.text_input('If you want, you can write something here')
        init()
        if st.button('Validation'):
            up_cmpt()
            st.experimental_rerun()
    elif st.session_state.cmpt_page==-5:
        st.write("Thank you")
        st.write("Add tirage session")
        if st.button('To dropbox'):
            to_dropbox(st.session_state.save_exp)
            st.write('File uploaded !')
        st.write('Owner : Brian Hill')
        st.write('Contributor : Pierre-Antoine Amiand-Leroy')
        st.write('Thanks to Hi! PARIS')
        st.subheader('Thanks for your participation')
    elif st.session_state.cmpt_page>=0 and st.session_state.cmpt_exp<=len(st.session_state.config)-1:
        config_exp=st.session_state.config[st.session_state.cmpt_exp]
        if config_exp[0][:-1]=='Choice_bias':
            front_choice_bias(Winning_amount,config_exp[1],config_exp[2])
        elif config_exp[0][:-1]=='Choice_unbias':
            front_choice_unbias(Winning_amount,config_exp[1],config_exp[2])
        elif config_exp[0][:-1]=='Choice_stated':
            front_choice_stated(Winning_amount,config_exp[1],config_exp[2])
    else:
        st.session_state.cmpt_page=-5
        st.experimental_rerun()

def to_dropbox(list_of_list):
    import dropbox

    filename = "argument.csv"
    pddf=pd.DataFrame(list_of_list)
    to_send=pddf.to_csv("argument.csv",sep=';',encoding='utf-8')
    # Create a dropbox object using an API v2 key
    token=st.secrets['DB_token'] 
    dbx = dropbox.Dropbox(token)
    dbx.files_upload(
        f=to_send,
        path='/Brian_Hill_experiment/'+str(int(time.time()))+'.csv',
        mode=dropbox.files.WriteMode.overwrite
    )
    
    return print('File uploaded !')

def load_yaml():
    with open('parameter.yml', 'r', encoding='utf8') as file:
        data = yaml.safe_load(file)
    return data
def sent_to_csv(list_of_list):
    pddf=pd.DataFrame(list_of_list)
    pddf.to_csv("argument.csv",sep=';',encoding='utf-8')
def load_config(tirage_groupe):
    data=load_yaml()
    liste_option=["A1","A2","B1","B2","C1","C2"]
    option=liste_option[tirage_groupe]
    config=data[option]
    list_key=list(config.keys())
    config_list=[[key]+config[key] for key in list_key]
    return config_list
    
    

def main():
    #data=load_yaml()#beug with streamlit. Need correction 
    if 'pers_info' not in st.session_state:
      st.session_state.pers_info=[]

    def hide_header_footer():
        hide_streamlit_style = """
                    <style>
                    footer {visibility: hidden;}
                    </style>
                    """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    #hide_header_footer()
    #st.header("# Brian Hill 🖥")
##    st.subheader(
##        """
##        Decision  🧪
##        """
##    )
##    experiment_front()
    data=load_yaml()
    Winning_amount=data['Winning_Amount']
    process(Winning_amount)



if __name__=='__main__':
    main()

#st.markdown(" ")
#st.markdown("### HEC Researcher Brian Hill " )
#st.image(['images/1.png'], width=230,caption=["Vadim Malvone"])

#st.markdown('# Made by Hi!Paris')
#images = Image.open('./images/hi-paris.png')
#st.image(images, width=250)
#st.write('    ')
#st.markdown('# Contributors:')
#PA=Image.open('./images/PA.jpg')
#Pierre=Image.open('./images/Pierre.jpg')
#GAE=Image.open('./images/gaetan.png')
#st.image([PA,GAE,Pierre],width=110)





def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))


def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)


def layout(*args):

    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;background - color: white}
     .stApp { bottom: 80px; }
    </style>
    """
    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        color="black",
        text_align="center",
        height="auto",
        opacity=1,

    )

    style_hr = styles(
        display="block",
        margin=px(8, 8, "auto", "auto"),
        border_style="inset",
        border_width=px(2)
    )

    body = p()
    foot = div(
        style=style_div
    )(
        hr(
            style=style_hr
        ),
        body
    )

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)
