from flask import render_template, flash, redirect, request, Markup
from app import app
from .pemulis import *

playins = readTeams("app/static/playin.txt")
teams = readTeams("app/static/teams.txt")

@app.route('/')
@app.route('/index', methods=['GET','POST'])
def index():
	return render_template('ratings.html',
							teams=teams,
							playins=playins)


@app.route('/rating', methods=['POST'])
def rating():
	rating = request.form
	mutableRating = assignElo(rating)
	brackets = []
	for i in range(10):
		brackets.append(tournament(mutableRating, teams, playins))
	return render_template('base.html', lines = brackets)
