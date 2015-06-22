#! /usr/bin/env python2.7

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

# from wikitools import category as wtcat
from datetime import datetime, timedelta
import dateutil.parser
from dateutil.relativedelta import relativedelta
import wikitools
import grantsbot_settings
import MySQLdb
import output_settings
import templates
import operator
import queries
import re
import time

class Profiles:
	"""Operations you might want to perform on and with profiles."""

	def __init__(self, path, id = False, settings = False):
		"""
		Instantiate page-level variables for building a set of profiles.
		"""
		self.page_path = path
		if id:
			self.page_id = str(id)
		if settings:
			self.profile_settings = settings
		self.tools = Toolkit()
		self.wiki = wikitools.Wiki(grantsbot_settings.apiurl)
		self.wiki.login(grantsbot_settings.username, grantsbot_settings.password)

	def getPageSectionData(self, level = False):
		"""
		Returns the section titles and numbers for a given page.
		Level arg can be used to return only sections of a given indentation level.
		Sample request: http://meta.wikimedia.org/w/api.php?action=parse&page=Grants:IdeaLab/Introductions&prop=sections&format=jsonfm
		"""
		params = {
			'action': 'parse',
			'page': self.page_path,
			'prop': 'sections',
		}
		req = wikitools.APIRequest(self.wiki, params)
		response = req.query()
		if level:
			secs_list = [{'title' : unicode(x['line']), 'index' : x['index']} for x in response['parse']['sections'] if x['toclevel'] == level]
		else:
			secs_list = [{'title' : unicode(x['line']), 'index' : x['index']} for x in response['parse']['sections']]
		return secs_list

	def getPageText(self, section = False):
		"""
		Gets the raw text of a page or page section.
		Sample: http://meta.wikimedia.org/w/api.php?action=query&prop=revisions&titles=Grants:Learning_patterns/Repeat_events&rvprop=content&rvsection=0&format=jsonfm&rawcontinue=1
		"""
		params = {
			'action': 'query',
			'prop': 'revisions',
			'titles': self.page_path,
			'rvprop' : 'content',
			'rvsection' : '',
			'rawcontinue' : '1',
		}
		if section:
			params['rvsection'] = section
		req = wikitools.APIRequest(self.wiki, params)
		response = req.query()
		text = response['query']['pages'][self.page_id]['revisions'][0]['*']
		return text

# 		Retrieve latest revision metadata.
# 		Sample: http://meta.wikimedia.org/w/api.php?action=query&prop=info&titles=Grants:IEG/GIS_and_Cartography_in_Wikimedia&format=jsonfm
# 		latest_rev = response['query']['pages'][self.page_id]['lastrevid']

	def getPageEditInfo(self, sort_dir="older", page = False, rvstart = False, rvend = False): #should just be 'getPageRecentRevs'
		"""
		Returns a list of values for revision properties you specify. Can use the page id associated with the current profiles object, or another one specified through the page arg.
		Example: http://meta.wikimedia.org/w/api.php?action=query&prop=revisions&pageids=2101758&rvdir=newer&rvstart=20130601000000&rvprop=comment|ids|timestamp|user|userid&rvlimit=50&format=jsonfm&rawcontinue=1
		"""
		if page:
			page_id = page
		else:
			page_id = self.page_id

		params = {
				'action': 'query',
				'prop': 'revisions',
				'pageids': page_id,
				'rvprop' : 'comment|ids|timestamp|user|userid',
				'rvlimit' : 'max',
				'rvdir' : sort_dir,
    			'rawcontinue' : '1',
					}
		if rvstart:
			params['rvstart'] = rvstart
		if rvend:
			params['rvend'] = rvend
		req = wikitools.APIRequest(self.wiki, params)
		response = req.query()
		try:
			revs = response['query']['pages'][page_id]['revisions']
		except:
			revs = []
		return revs

	def getUserRecentEditInfo(self, user_name, edit_namespace = False): #rename
		"""
		Get edits by a user in a given namespace within the past month
		(or whatever range recentchanges is set to on your wiki).
		Sample: http://meta.wikimedia.org/w/api.php?action=query&list=recentchanges&rcnamespace=200&rcuser=Jmorgan_(WMF)&rclimit=500&format=jsonfm&rawcontinue=1
		"""
		params = {
				'action': 'query',
				'list': 'recentchanges',
				'rcuser': user_name,
				'rcnamespace': edit_namespace,
    			'rawcontinue' : '1',
		}
		req = wikitools.APIRequest(self.wiki, params)
		response = req.query()
		recent_edits = len(response['query']['recentchanges'])
		return recent_edits

	def getRecentIntros(self, rvend): #should generalize this a bit, like getPageEditInfo
		"""
		Gets recent profiles added to a page. Example:
http://meta.wikimedia.org/w/api.php?action=query&prop=revisions&pageids=2101758&rvdir=older&rvend=20131001000000&rvprop=comment|ids|timestamp|user|userid&rvlimit=50&format=jsonfm&rawcontinue=1
		"""
		params = {
				'action': 'query',
				'prop': 'revisions',
				'pageids': self.page_id,
				'rvprop' : 'comment|ids|timestamp|user',
				'rvend' : rvend,
				'rvlimit' : 100, #arbitrarily high
				'rvdir' : 'older',
    			'rawcontinue' : '1',
					}
		intro_list = []
		suffix = "new section"
		req = wikitools.APIRequest(self.wiki, params)
		response = req.query()
		revs = response['query']['pages'][self.page_id]['revisions']
		for r in revs:
			if r['comment'].endswith(suffix):
				intro = {'username' : r['user'], 'timestamp' : r['timestamp'], 'page path' : self.page_path, 'page id' : self.page_id}
				intro_list.append(intro)
		return intro_list

	def scrapeInfobox(self, member, infobox, redict = False, trans_tag = False):
		"""
		Method for grabbing the values of parameters from an infobox.
		Regexes for each infobox param are specified in the settings for the profile object.
		You can also pass a custom dict of regex strings to look for, via redict.
		Translate tags ('<translate>') and other tags that push
		the param value to the next line can be specified by passing the tag string
		in the optional trans_tag argument.
		"""
		if redict:
			re_types = redict #this is now very inconsistent, because of the away I'm storing these regexes. Fix!
		else:
			re_types = self.profile_settings[self.profile_settings['subtype']]['infobox params']
		second_line = False #used to test for translate tags
		for k,v in re_types.iteritems():	#params are loaded when the profile object is created
			for line in infobox.split('\n'):
				if second_line:
					try:
						member[k] = re.sub('(<[^>]+>)+', '', line)
					except:
						pass
						# print "can't capture the second line"
					second_line = False
					break #we found the value below the param, let's move on to another param
				else:
					if re.search(v, line): #can I just search for the key?
						if (trans_tag and trans_tag in line):
							second_line = True
							continue
						else:
							try:
								member[k] = re.search('(?<=\=)(.*?)(?=<|\||$)',line).group(1) #am I ignoring HTML comments?
							except:
								pass
# 								print "can't find this param in the infobox"
					else:
						continue #should I ignore profiles that don't have, say summaries?
		return member

	def formatProfile(self, val):
		"""
		Takes in a dictionary of parameter values and plugs them
		into the specified template by matching keys.
		"""
		page_templates = templates.Template()
		tmplt = page_templates.getTemplate(self.profile_settings['type'])
		tmplt = tmplt.format(**val).encode('utf-8')
		return tmplt

	def publishProfile(self, val, path, edit_summ, sb_page = False, edit_sec = False):
		"""
		Publishes a profile or set of concatenated profiles to a page on a wiki.
		"""
		if sb_page:
			path += str(sb_page)
# 		print path
# 		print val
# 		print edit_summ
# 		print edit_sec
		output = wikitools.Page(self.wiki, path)
		if edit_sec:
			output.edit(val, section=edit_sec, summary=edit_summ, bot=1)
		else:
			output.edit(val, summary=edit_summ, bot=1)

class Toolkit:
	"""
	Handy ready-to-use methods.
	You don't need to create an object beforehand to use these.
	"""

	def addDefaults(self, member_list):
		"""
		Adds pre-specified set of default (null) fields to a dictionary.
		"""
		params = output_settings.Params()
		mem_defaults = dict.fromkeys(params.getParams('profile defaults'), "")
		for m in member_list:
			for k,v in mem_defaults.iteritems():
				if k not in m.keys():
					m[k] = v
		return member_list

	def setTimeValues(self, member_list, val="timestamp"):
		"""
		Adds a python date object and a pretty formatted date string
		to each dict in a list of dicts.
		Requires that dict contains a 'timestamp' key with a
		a 12-digit date string (like rev_timestamp from MediaWiki database)
		or an ISO 8601 date string (like MediaWiki API timestamp)
		"""
		for m in member_list:
			try:
				m['datetime'] = dateutil.parser.parse(m[val])
				m['time'] = datetime.strftime(m['datetime'], '%d %B %Y')
			except:
				pass
# 				print "no timestamp available for " + m['title']
		return member_list


	def getSubDate(self, day_interval):
		"""
		Returns the date a specified number of days before the current date
		as an API and database-friendly 14-digit timestamp string.
		"""
		today = datetime.utcnow()
		sd_datetime = today - relativedelta(days=day_interval)
		sd_datetime = datetime.utcnow().replace(tzinfo=dateutil.tz.tzutc())-timedelta(days=day_interval)
		sd_string = sd_datetime.strftime('%Y%m%d%H%M%S')
		subdate = (sd_datetime, sd_string)
		return subdate

	def titleFromPath(self, path):
		"""
		Get the title of the lowest subpage from a long path.
		Example: "IdeaLab/Ideas/My_great_idea" returns "My great idea".
		"""
		title = re.search('([^/]+$)', path).group(1).replace("_", " ")
		return title

	def titleFromComment(self, comment):
		"""
		Gets the title of a page section from an edit comment
		that contains the section title.
		Example: "\*How do I edit a section?*\reply"
		returns "How do I edit a section?"
		"""
		title = re.search('\*(.*?)\*', comment).group(1)
		for sub in ['* ', ' *']:
			if sub in title:
				title.replace(sub,"")
		return title

	def formatSummaries(self, text): #need to be able to pass in a custom dict here, like in scrapeInfobox above
		"""
		Cleans markup from strings of profile summary text.
		"""
		text = text.strip()
		text = re.sub("(\[\[)(.*?)(\|)","",text)
		text = re.sub("\]","",text)
		text = re.sub("\[","",text)
		text = text + "..."
# 		text = (text[:200] + '...') if len(text) > 200 else text
		return text

	def dedupeMemberList(self, mem_list, sort_val, dict_val):
		"""
		Sort and remove duplicates from a list of dicts
		based on a specified key/value pair.
		"""
		mem_list.sort(key=operator.itemgetter(sort_val), reverse=True)
		seen_list = []#why is this here?
		unique_list = []
		for mem in mem_list:
			t = mem[dict_val]
			if t not in seen_list:
				seen_list.append(t)
				unique_list.append(mem)
			else:
				pass
		return unique_list

	def compareDates(self, date_one, date_two):
		"""
		Compares two date objects and returns the most recent one.
		"""
		if date_one >= date_two:
			return date_one
		else:
			return date_two

	def queryDB(self, query_type):
		"""
		MySQL queries for the evaluation portal.
		"""
		conn = MySQLdb.connect(host = grantsbot_settings.host, db = grantsbot_settings.dbname, read_default_file = grantsbot_settings.defaultcnf, use_unicode=True, charset="utf8")
		cursor = conn.cursor()
		q = queries.Query()
		query = q.getQuery(query_type)
		cursor.execute(query)
		rows = cursor.fetchall()
		return rows

	def pprintDict(self, d, indent=0):
		"""
		Pretty prints a nested dictionary to make it easier
		to spot-check structure and content.
		"""
		for key, value in d.iteritems():
		  print '\t' * indent + str(key)
		  if isinstance(value, dict):
			 pretty(value, indent+1)
		  else:
			 print '\t' * (indent+1) + str(value)

	def excludeSubpages(self, mem_list, path_key, depth=1, skip_list=False):
		"""
		Takes a list of dictionaries that contains data about a bunch of wiki-pages,
		including the page path. Removes dicts from the list
		if their page depth ("/") is greater than the defined value.
		"""
		depth_constrained_list = []
		for mem in mem_list:
			if (skip_list and mem[path_key] in skip_list):
				depth_constrained_list.append(mem)
			else:
				path_comps = [p for p in mem[path_key].split('/') if p] #rmvs empty strings if path starts or ends in '/'
				if len(path_comps) == depth:
					depth_constrained_list.append(mem)
				else:
					pass

		return depth_constrained_list






