# -*- coding: utf-8 -*-

from flask import Flask, url_for, render_template, request, redirect, flash, jsonify
app = Flask(__name__)
import re
from database_setup import Apt, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime


engine = create_engine('sqlite:///apts.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

elGoog = "600 Amphitheatre Pkwy, Mountain View, CA 94043"
testData = """
CL
SF bay area >
east bay >
housing >
apts/housing for rent
reply x prohibited[?]  Posted: 4 days ago print
favorite this post $1800 / 2br - 900ft2 - Charming 2 bedroom duplex apartment (oakland north / temescal) hide this posting
<
image 1 of 3
>
 1
 1 2 3


craigslist - Map data OpenStreetMap
Alcatraz at Shattuck
(google map)

2BR / 1Ba 900ft2 available now

open house dates
saturday 2016-05-21

duplex
w/d in unit
off-street parking

621 Alcatraz Avenue -This older approximately 900 sq ft 2bedroom duplex apartment with builtins has stove, refrigerator, washer and dryer. Living room and kitchen on ground floor, bedrooms and bath on upper floor, laundry room and garage on lower floor with large backyard. No Pets. No Smoking. Rent $1,800 Security Deposit $1,800. Open House Saturday, May 21, 2016 from 1 pm to 4 pm. BRE Realty 01223009
do NOT contact me with unsolicited services or offers
post id: 5593507265 posted: 2016-05-18 10:07pm updated: 2016-05-19 12:44pm email to friend ♥ best of [?]
Please flag discriminatory housing ads
Avoid scams, deal locally! DO NOT wire funds (e.g. Western Union), or buy/rent sight unseen
© 2016 craigslist help safety privacy feedback cl jobs terms about mobile
"""

@app.route('/')
@app.route('/main')
def mainPage():
	all_apts = session.query(Apt).all()
	return render_template("main.html", apts = all_apts)

@app.route('/JSON')
@app.route('/main/JSON')
def mainPageJSON():
	all_apts = session.query(Apt)
	return jsonify(Apt=[a.serialize for a in all_apts])

@app.route('/new', methods=['GET', 'POST'])
def newPage():
	if request.method == 'GET':
		return render_template("new.html")
	elif request.method == 'POST':
		pageContent, status = parsePageDump(request.form['datadump']);
		if pageContent and status:
			myRent = pageContent['rent']
			myAddr = pageContent['addr']
			myPosted = pageContent['posted']
			if 'lastupdate' in pageContent.keys():
				myUpdated = pageContent['lastupdate']
			else:
				myUpdated = datetime.now()
			myPostId = pageContent['postid']
		else:
			myRent = request.form['rent']
			myAddr = request.form['addr']
			myPosted = datetime.now()
			myUpdated = datetime.now()
			myPostId = 'DEADBEEF'

		if request.form['link']:
			link = request.form['link']
		elif 'link' in pageContent.keys():
			link = pageContent['link']
			print ("Link exists in keys"+pageContent['link'])
		else:
			link = ""
		prexists = None
		q = session.query(Apt).filter(Apt.link==link)
		for a in q:
			prexists = True
		# print q
		print "Link is: " + link
		if not prexists:
			new_apt = Apt(link=link, rent=myRent, addr=myAddr, posted = myPosted)
			session.add(new_apt)
			session.commit()
			return redirect(url_for('mainPage'))
		else:
			return render_template('new.html', already="Already exists!")

@app.route('/apts/<int:apt_id>/edit', methods = ['GET', 'POST'])
def editApt(apt_id):
	apt = session.query(Apt).filter_by(id=apt_id).one()
	print "Querying for apt id: %d"%apt_id
	# apt = [apt]
	if request.method == 'GET':
		return render_template('apt_view.html', apt=apt)
	elif request.method == 'POST':
		apt.addr = request.form['addr'];
		apt.rent = request.form['rent'];
		session.commit();
		return redirect(url_for('mainPage'));

@app.route('/apts/<int:apt_id>/delete', methods = ['GET', 'POST'])
def deleteApt(apt_id):
	apt = session.query(Apt).filter_by(id=apt_id).one()
	session.delete(apt)
	session.commit()
	return redirect(url_for('mainPage'))


def parsePageDump(page):
	pageContent = {'addr': elGoog, 'rent':'1000000'};
	status = False
	print "Parsing page data..."
	print page
	lines = page.split('\n')
	for i, l in enumerate(lines):
		# Search for rent
		m = re.search('\$(\d+)\s', l)
		if m and pageContent['rent'] == '1000000':
			pageContent['rent'] =  m.group(1)

		# Search for location
		m = re.search('SF bay area >', l)
		if m:
			if re.match(r'east bay', lines[i+1], re.I):
				pageContent['loc'] = 'eby'
			elif re.match(r'south bay', lines[i+1], re.I):
				pageContent['loc'] = 'sby'
			elif re.match(r'peninsula', lines[i+1], re.I):
				pageContent['loc'] = 'pen'
			elif re.match(r'san francisco', lines[i+1], re.I):
				pageContent['loc'] = 'sfc'


		# Search for addr
		m = re.search('craigslist - Map data.* OpenStreetMap', l)
		if m:
			pageContent['addr'] = lines[i+1]

		# Get post id
		m = re.search('post id:\s+?(\d+)\s', l)
		if m:
			pageContent['postid'] = m.group(1)

		# Get last updated
		m = re.search('updated:\s+?(\d+-\d+-\d+)\s', l)
		if m:
			pageContent['lastupdate'] = m.group(1)

		# Get last updated
		m = re.search('posted:\s+?(\d+-\d+-\d+)\s', l)
		if m:
			pageContent['posted'] = m.group(1)
			pageContent['posted'] = datetime.strptime(pageContent['posted'], "%Y-%m-%d")


		status = True

	pageContent['link'] = 'http://sfbay.craigslist.org/'+pageContent['loc']+'/apa/'+pageContent['postid']+'.html'

	if status:
		print pageContent
	return pageContent, status


	
if __name__ == '__main__':
	app.secret_key = 'my_foot_smells'
	app.debug = True
	app.run(host='0.0.0.0', port = 5000)