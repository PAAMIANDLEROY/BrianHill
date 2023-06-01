# -*- coding: utf-8 -*-

import numpy as np
import math
import csv
import datetime
from scipy.spatial import distance
from sympy.solvers import solve
from sympy import Symbol

X = Symbol('x')


# Point de départ

def init():
# Vecteurs de résultats: objectif, nombre d'iteration et point elicité
    global objv,itv,betv,dzv,vhypo,phypo,vstop,az1,az2,dz1,dz2,az1h,az2h,maxiter,retrunOnlyAtLogs,sup_info,beforeMaxIter,useWhile,useReturn,returnAtEachBet
    objv = []
    itv = []
    betv = []
    dzv = []

    # Paramètre de calibration: nombre de point objectifs, voisinage de l'hypo et précision de l'élicitation sur l'hypo
    vhypo = 44  # voisinage de l'hypothenuse où on passe sur l'hypo
    phypo = 5  # distance d'arrêt sur l'hypothenuse
    vstop = 15  # distance euclidienne à partir de laquelle on stoppe l'algorithme

    az1 = []
    az2 = []
    dz1 = []
    dz2 = []
    az1h = []
    az2h = []
    maxiter = int(12/2)
    retrunOnlyAtLogs = True

    sup_info = [""]
    beforeMaxIter = [0]

    useWhile=False
    useReturn = not useWhile
    returnAtEachBet = not useWhile
#    return objv,itv,betv,dzv,vhypo,phypo,vstop,az1,az2,dz1,dz2,az1h,az2h,maxiter,retrunOnlyAtLogs,sup_info,beforeMaxIter,useWhile,useReturn,returnAtEachBet
#objv,itv,betv,dzv,vhypo,phypo,vstop,az1,az2,dz1,dz2,az1h,az2h,maxiter,retrunOnlyAtLogs,sup_info,beforeMaxIter,useWhile,useReturn,returnAtEachBet=init()
init()

def result(bet, finished=0, finishedBefMaxIter=None):
    sumlen = len(az1) + len(az2) + len(dz1) + len(dz2)
    nzdict = {"n_az1": len(az1), "n_az2": len(az2), "n_dz1": len(dz1), "n_dz2": len(dz2),
              "n_dz_tot": (len(dz1) + len(dz2))}
    initfinished = finished
    if (finishedBefMaxIter == None): finishedBefMaxIter = finished if useReturn else beforeMaxIter[0]
    if (returnAtEachBet and sumlen > maxiter): finished = 1
    finishedApartAlgo = int(initfinished == 0 and finished == 1)
    ccomments = sup_info[0]
    sup_info[0] = "";
    return (bet, finished, sumlen, nzdict, ccomments, finishedBefMaxIter, finishedApartAlgo, useReturn, useWhile)

def main(bet, opts):
    sup_info[0] = ""


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
    # print(argsv)




def zone(opts):
    if(opts==["A","B"]): czone="az1"
    elif(opts==["B","A"]): czone="az2"
    elif(opts==["B","B"]): czone="dz1"
    elif(opts==["A","A"]): czone="dz2"
    print('zone')
    print(opts)
    print(czone)
    return czone


