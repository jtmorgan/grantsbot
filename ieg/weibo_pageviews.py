#! /usr/bin/python2.7

# Copyright 2013 Jtmorgan

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import csv
from datetime import datetime, timedelta
import json
import numpy
import urllib2 as u2

pageview_path = 'http://stats.grok.se/json/zh/%s%s/%s'
null_dates = ["2012-02-29","2012-02-30","2012-02-31","2012-04-31","2012-06-31","2012-09-31","2012-11-31","2013-02-29","2013-02-30","2013-02-31","2013-04-31","2013-06-31","2013-09-31","2013-11-31"]

def readCSVdata():
	articles = []
	with open('/data/project/grantsbot/bot/data/weibo.csv','rb') as csvfile:
		sreader = csv.reader(csvfile)
		for row in sreader:
			try:
				article = {'title' : row[0], 'post date' : row[2].split(' ',1)[0], 'reposts' : row[3], 'weibo views' : row[4]}
				if len(article['post date']) == 10:
					articles.append(article)
				else:
					print "no date for article " + article['title']
			except:
				print "something went wrong here" + row[0]
# 		for article in articles:
# 			article['post date'] = datetime.strptime(article['post date'], "%m/%d/%Y")
		return articles

def getPageviews(articles):
	for article in articles:
		article['post date'] = datetime.strptime(article['post date'], "%m/%d/%Y")
		article['grokse url'] = pageview_path % (datetime.strftime(article['post date'], "%Y"),datetime.strftime(article['post date'], "%m"), article['title'])
# 		print pageview_url
# 		print article['post date']
		sock = u2.urlopen(article['grokse url'])
		views = sock.read()
		pv_data = json.loads(views)
		pv = pv_data['daily_views']
		article['daily views'] = [(datetime.strptime(key, "%Y-%m-%d"), float(value)) for key, value in pv.iteritems() if key not in [x for x in null_dates] and datetime.strptime(key, "%Y-%m-%d") >= article['post date'] - timedelta(days=3) and datetime.strptime(key, "%Y-%m-%d") < article['post date'] + timedelta(days=3)]
# 		print article['title']
# 		print article['daily views']
	return articles
# 		article['daily views'] = [{datetime.strptime(key, "%Y-%m-%d") : value} for key, value in pv.iteritems() if datetime.strptime(key, "%Y-%m-%d") < article['post date'] + timedelta(days=7)]

def getPrePostViews(articles):
	for article in articles:
		article['previous'] = [item[1] for item in article['daily views'] if item[0] < article['post date']]
		article['prev cnt'] =  len(article['previous'])
		article['prev sum'] =  sum(article['previous'])
		print numpy.mean(article['previous'])
		article['prev avg'] = numpy.mean(article['previous'])
# 		print numpy.mean(article['previous'])
		article['post'] = [item[1] for item in article['daily views'] if item[0] >= article['post date']]
		article['subs cnt'] =  len(article['post'])
		article['subs sum'] =  sum(article['post'])
		print numpy.mean(article['post'])
		article['subs avg'] = numpy.mean(article['post'])
# 		print article['previews']
# 		article['average previews'] = numpy.mean(item[1] for item in article['daily views'] if item[0] < article['post date'])
# 		print article['average previews']
# 		article['postviews'] = sum(int(v) for k,v in article['daily views'] if k >= article['post date'] < article['post date'] + timedelta(days=7))
	return articles

def dumpCSV(articles, f):
	writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC, dialect=csv.excel,)
	writer.writerow( ('article title', 'grokse url', 'post date', 'previous dates', 'previous sum', 'previous average', 'subsequent days', 'subsequent sum', 'subsequent average',) )
	for article in articles:
		try:
			writer.writerow( (article['title'], article['grokse url'], article['post date'], article['prev cnt'], article['prev sum'], article['prev avg'], article['subs cnt'], article['subs sum'], article['subs avg']) )
		except ValueError:
			writer.writerow( ("error!") )

##MAIN##
articles = readCSVdata()
articles = 	getPageviews(articles)
articles = getPrePostViews(articles)
output_path = '/data/project/grantsbot/bot/data/zh_weibo_views.csv'
f = open(output_path, 'wt')
dumpCSV(articles, f)
