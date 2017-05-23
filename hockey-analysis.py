#!/usr/bin/python
# -*- coding: latin-1 -*-

##
## Hockey Analysis
##
## Author: Simon Viel
## April 2013
## Modified April 2014:
##     New NHL playoff format
##

import codecs
from optparse import OptionParser


## Error functions

def usage():
    print 'Usage: python hockey-analysis.py year'
    exit()

def error(message):
    print message
    exit()


## Useful functions for generating the possible scenarios

def app(eq, scenario, other = None):
    scenario.append(eq[0])
    if other != None:
        other.append(eq)

def play(results, f, i, eq1, eq0, scenario, other = None):
    team = results[i]
    if team == eq1[0] or (team == 'x' and f[i]):
        app(eq1, scenario, other)
    elif team == eq0[0] or (team == 'x' and not f[i]):
        app(eq0, scenario, other)
    else:
        error( u"Error in results file, line %i"%(i+1) )


## Initial definitions

year = None

parser = OptionParser()
opt, args = parser.parse_args()

if len(args) > 0:
    if not args[0].isdigit():
        usage()
    else:
        year = args[0]
else:
    usage()

if len(args) > 1:
    usage()


poolfile = 'pool_%s.txt'%(year)
resultsfile = 'results_%s.txt'%(year)

n = 16  ## Number of teams participating in the playoffs


## Read in results data

try:
    lines = codecs.open(resultsfile, 'r', 'latin-1').read().splitlines()
except(IOError):
    error( u"Error reading results data: %s"%(resultsfile) )

init = []
east = []
west = []
results = []

j = 0

for line in lines:
    if not line:
        continue

    elif line.replace(' ','')[0].isalpha():
        team = line.split('\t')[0].replace(' ','')
        if team.startswith('x'):
            team = 'x'

        if j < n/2:
            init.append(team)
            east.append((team, j))
        elif j < n:
            init.append(team)
            west.append((team, j))
        else:
            results.append(team)
        j += 1

    else:
        error( u"Error: Incorrect results file format" )

if len(results) != n-1:
    error( u"Error: %i teams in results instead of %i"%(len(results), n-1) )


## Read in participants data
## Each participant's set of choices is called a "pool"

try:
    lines = codecs.open(poolfile, 'r', 'latin-1').read().splitlines()
except(IOError):
    error( u"Error reading participants data: %s"%(poolfile) )

pools = {}
score = {}
wins = {}

names = []
longestname = ''

for line in lines:
    if line.startswith('\t') or not line:
        continue

    elif line.replace(' ','')[0].isalpha():
        teams = line.split('\t')
        teams = filter(None, teams)
        for i, team in enumerate(teams):
            team = team.replace(' ','')
            if team not in init:
                error( u"Error: Non-participating team (%s) in pool by %s"%(team, names[i]) )
            else:
                pools[names[i]].append(team)

    elif line.startswith('#end') or line.startswith('$'):
        ## Verify the number of teams in each pool of the previous list
        if names:
            for name in names:
                if len(name) > len(longestname):
                    longestname = name
                if len(pools[name]) != n-1:
                    error( u"Error for participant %s: %i teams in the pool"%(name, len(pools[name])) )

        ## New list, if necessary
        if line.startswith('$'):
            names = line.replace('$ ','').split('\t')
            names = filter(None, names)
            for name in names:
                pools[name] = []
                score[name] = 0
                wins[name] = 0

        ## Otherwise, we are done reading the pools
        else:
            break

    else:
        error( u"Error: Incorrect participants data format" )


## Generate possible scenarios

Np = 2**(n-1)

scenarios = []

for p in xrange(Np):
    east2 = []
    west2 = []
    east3 = []
    west3 = []
    final = []

    scenario = []
    f = []

    for k in xrange(n-1):
        f.append((p / 2**k) % 2)


    ## Pre-2014 format
    if year < '2014':

        ## First round
        play(results, f, 0, east[0], east[7], scenario, east2)
        play(results, f, 1, east[1], east[6], scenario, east2)
        play(results, f, 2, east[2], east[5], scenario, east2)
        play(results, f, 3, east[3], east[4], scenario, east2)
        play(results, f, 4, west[0], west[7], scenario, west2)
        play(results, f, 5, west[1], west[6], scenario, west2)
        play(results, f, 6, west[2], west[5], scenario, west2)
        play(results, f, 7, west[3], west[4], scenario, west2)

        ## Re-sort teams in preparation for second round
        east2s = sorted(east2, key = lambda x:x[1])
        west2s = sorted(west2, key = lambda x:x[1])

        ## Second round
        play(results, f, 8, east2s[0], east2s[3], scenario, east3)
        play(results, f, 9, east2s[1], east2s[2], scenario, east3)
        play(results, f, 10, west2s[0], west2s[3], scenario, west3)
        play(results, f, 11, west2s[1], west2s[2], scenario, west3)

        ## Re-sort teams in preparation for third round
        east3s = sorted(east3, key = lambda x:x[1])
        west3s = sorted(west3, key = lambda x:x[1])

        ## Third round
        play(results, f, 12, east3s[0], east3s[1], scenario, final)
        play(results, f, 13, west3s[0], west3s[1], scenario, final)

        ## Final
        play(results, f, 14, final[0], final[1], scenario)


    ## Simplified NHL playoffs format, from 2014 onwards
    else:

        ## First round
        play(results, f, 0, east[0], east[1], scenario, east2)
        play(results, f, 1, east[2], east[3], scenario, east2)
        play(results, f, 2, east[4], east[5], scenario, east2)
        play(results, f, 3, east[6], east[7], scenario, east2)
        play(results, f, 4, west[0], west[1], scenario, west2)
        play(results, f, 5, west[2], west[3], scenario, west2)
        play(results, f, 6, west[4], west[5], scenario, west2)
        play(results, f, 7, west[6], west[7], scenario, west2)

        ## Second round
        play(results, f, 8, east2[0], east2[1], scenario, east3)
        play(results, f, 9, east2[2], east2[3], scenario, east3)
        play(results, f, 10, west2[0], west2[1], scenario, west3)
        play(results, f, 11, west2[2], west2[3], scenario, west3)

        ## Third round
        play(results, f, 12, east3[0], east3[1], scenario, final)
        play(results, f, 13, west3[0], west3[1], scenario, final)

        ## Final
        play(results, f, 14, final[0], final[1], scenario)
    

    if len(scenario) != n-1:
        error( u"Error: Incorrect number of teams in a scenario" )


    ## Verify that the scenario has not already been accounted for,
    ##     just to be sure (program is very fast anyway)

    if scenario in scenarios:
        continue
    else:
        scenarios.append(scenario)


    ## Calculate score for each participant in this scenario
    ## Correct guesses are worth:
    ##     1 point in the first round
    ##     1 point in the second round
    ##     2 points in the third round
    ##     4 points for the Stanley Cup winner

    for name, pool in pools.iteritems():
        score[name] = 0
        for i in xrange(0,8):
            if pool[i] in scenario[0:8]:
                score[name] += 1
        for i in xrange(8,12):
            if pool[i] in scenario[8:12]:
                score[name] += 1
        for i in xrange(12,14):
            if pool[i] in scenario[12:14]:
                score[name] += 2
        if pool[14] == scenario[14]:
            score[name] += 4


    ## Calculate the best score among participants for this scenario

    wscore = max(score.iteritems(), key = lambda x:x[1])[1]


    ## Award a victory point for each winning participant in this scenario

    wnames = []
    for name, s in score.iteritems():
        if s == wscore:
            wins[name] += 1
            wnames.append(name)

            ## Print winning scenario for this participant
            if name == u"Participant":
                print scenario
                print sorted(score.iteritems(), key = lambda x:-x[1])


    ## Test one particular scenario, based on binary pattern

    doTest = False

    if doTest and p == 0b001000100011101:
        print scenario
        print sorted(score.iteritems(), key = lambda x:-x[1])
        print wnames, wscore
        print '---'


## End scenarios loop


## Display results, sorted by remaining chances to win

out = 0
Ns = len(scenarios)

print
print '----------------------------------------------------------------'
print u"%i possible scenario%s out of %i"%(Ns, 's' if Ns > 1 else '', Np)
print

print "Percentage and number of winning scenarios for each participant"
print

for name, w in sorted(sorted(wins.iteritems()), key = lambda x:-x[1]):
    if w == 0:
        out += 1

    print ('%s\t%.1f%%\t%s'%(name, float(w)/Ns*100, w)).expandtabs(len(longestname)+5)

print
print u"Total: %i elimination%s out of %i participants"%(out, 's' if out > 1 else '', len(pools))
print '----------------------------------------------------------------'
print


