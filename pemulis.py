import csv
from scipy.stats import norm
import random

def assignElo(rating):
	for team in rating:
		if rating[team] > 0 and rating[team] < 100:
			sd = norm.ppf(rating[team]/100.0)
			rating[team] = (1500.0 + (2000/7.0)*sd)
		elif rating[team] == 100:
			sd = norm.ppf(0.997)
			rating[team] = (1500.0 + (2000/7.0)*sd)
		else:
			print "There was an error, check Elo ratings!"

def eloSim(team1, team2, rating1, rating2):
	# print rating1
	# print rating2
	expectedScore = 1.0/(1 + 10**((rating2-rating1)/400))
	# print expectedScore
	realScore = random.random()
	result = 10*(realScore-expectedScore)
	return result

def tournament(rateDict, teamOrder):
	teams = teamOrder
	ratings = []
	for team in teams:
		ratings.append(rateDict[team])
	while len(teams) > 1: # tournament loop
		print("Round of " + str(len(teams)))
		game = 0
		newTeams = []
		newRatings = []
		while game < len(teams): # round loop
			result = eloSim(teams[game], teams[game+1], ratings[game], ratings[game+1])
			if result < 0:
				score2 = random.randint(80,110)
				score1 = score2 + int(result**2) + 1
				print(teams[game] + " defeats " + teams[game+1] + " " + str(score1) + " to " + str(score2))
				newTeams.append(teams[game])
				newRatings.append(ratings[game])
			elif result > 0:
				score1 = random.randint(80,110)
				score2 = score1 + int(result**2) + 1
				print(teams[game+1] + " defeats " + teams[game] + " " + str(score2) + " to " + str(score1))
				newTeams.append(teams[game+1])
				newRatings.append(ratings[game+1])
			else:
				print "whoa a tie, too bad this will not work"
			game += 2
		teams = newTeams
		ratings = newRatings
		

		
with open('teams.csv', 'rb') as csvfile:
	readit = csv.reader(csvfile, delimiter=',')
	rating = {}
	teamOrder = []
	for row in readit:
		rating[row[0]] = float(row[1])
		teamOrder.append(row[0])
csvfile.close()

assignElo(rating)
for team, value in rating.iteritems():
	print("Team " + team + " has a rating of " + str(int(value)))
# eloSim(elo[1],elo[2])
tournament(rating, teamOrder)
