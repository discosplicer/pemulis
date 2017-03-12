import csv
from scipy.stats import norm
import random

def readTeams(filename):
	f = open( filename, "r" )
	return f.read().splitlines()

def assignElo(rating):
	mutable = {}
	for team in rating:
		mutable[team] = float(rating[team])
		if mutable[team] > 0 and mutable[team] < 100:
			sd = norm.ppf(mutable[team]/100.0)
			mutable[team] = (1500.0 + (2000/7.0)*sd**2)
		elif mutable[team] == 100:
			sd = norm.ppf(0.995)
			mutable[team] = (1500.0 + (2000/7.0)*sd**2)
		else:
			print "There was an error, check Elo ratings!"
			print mutable
	return mutable

def eloSim(team1, team2, rating1, rating2):
	# print rating1
	# print rating2
	expectedScore = 1.0/(1 + 10**((rating2-rating1)/400))
	# print expectedScore
	realScore = random.random()
	result = 10*(realScore-expectedScore)
	return result

def playin(rateDict, playins):
	teams = playins
	ratings = []
	lines = []
	for team in teams:
		ratings.append(rateDict[team])
	playinWinners = []
	game = 0
	if len(playinWinners) >= 1:
		lines.append("Playins <br>")
	while game < len(teams): # round loop
		result = eloSim(teams[game], teams[game+1], ratings[game], ratings[game+1])
		diff = min(int(result**2), 30)
		if result < 0:
			score2 = random.randint(45,70)
			score1 = score2 + diff + 1
			lines.append("<b>" + teams[game] + "</b> defeats <b>" + teams[game+1] + "</b> " + str(score1) + " to " + str(score2))
			playinWinners.append(teams[game])
		elif result > 0:
			score1 = random.randint(45,70)
			score2 = score1 + diff + 1
			lines.append("<b>" + teams[game+1] + "</b> defeats <b>" + teams[game] + "</b> " + str(score2) + " to " + str(score1))
			playinWinners.append(teams[game+1])
		else:
			print "whoa a tie, too bad this will not work"
		game += 2
		lines.append("<br>")
	return (playinWinners, lines)
	
def tournament(rateDict, teamOrder, playins):
	playinTuple = playin(rateDict, playins)
	playinWinners = playinTuple[0]
	lines = playinTuple[1]
	teams = []
	i = 0
	upsets = 0
	upsetRating = 0
	for team in teamOrder:
		if team == "Playin":
			teams.append(playinWinners[i])
			i+= 1
		else:
			teams.append(team)
	ratings = []
	for team in teams:
		ratings.append(rateDict[team])
	while len(teams) > 1: # tournament loop
		lines.append("Round of " + str(len(teams)) + "<br>")
		game = 0
		newTeams = []
		newRatings = []
		while game < len(teams): # round loop
			result = eloSim(teams[game], teams[game+1], ratings[game], ratings[game+1])
			diff = min(int(result**2), 30)
			if result < 0:
				if ratings[game] < ratings[game+1]: # upset check
					upsets += 1
					upsetRating += ratings[game+1] - ratings[game]
				score2 = random.randint(45,70)
				score1 = score2 + diff + 1
				lines.append("<b>" + teams[game] + "</b> defeats <b>" + teams[game+1] + "</b> " + str(score1) + " to " + str(score2))
				newTeams.append(teams[game])
				newRatings.append(ratings[game])
			elif result > 0:
				if ratings[game] > ratings[game+1]: # upset check
					upsets += 1
					upsetRating += ratings[game] - ratings[game+1]
				score1 = random.randint(45,70)
				score2 = score1 + diff + 1
				lines.append("<b>" + teams[game+1] + "</b> defeats <b>" + teams[game] + "</b> " + str(score2) + " to " + str(score1))
				newTeams.append(teams[game+1])
				newRatings.append(ratings[game+1])
			else:
				print "whoa a tie, too bad this will not work"
			game += 2
		teams = newTeams
		ratings = newRatings
		lines.append("<br>")
	# lines.append("<b> Upsets:</b> " + str(upsets) + ", <b>Upset Score:</b> " + str(int(round(upsetRating))))
	return lines

