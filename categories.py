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
import wikitools
import grantsbot_settings

class Categories:
	"""A category on a wiki."""

	def __init__(self, title, namespace = False, type = "page", action = False): #should be more agnostic about namespace param
		"""
		Instantiate basic variables for the category you're interested in.
		"""
		self.cat_title = "Category:" + title
		self.supercat = "Category:IdeaLab/Ideas/Active"
		self.mem_type = type
		if action:
			self.action = action
# 		print self.type
		if namespace:
			self.mem_namespace = namespace
		else:
			self.mem_namespace = ""	
		self.wiki = wikitools.Wiki(grantsbot_settings.apiurl)
		self.wiki.login(grantsbot_settings.username, grantsbot_settings.password)

	def getCatMembers(self):
		"""
		Get the members of the specified category and their metadata.
		Example: http://meta.wikimedia.org/w/api.php?action=query&list=categorymembers&cmtype=page&cmtitle=Category:IEG/Proposals/IdeaLab&cmnamespace=200&cmprop=title|timestamp|ids&cmsort=timestamp&cmdir=desc&format=jsonfm
		will return a dict like {'page id' : 'someid', 'page path' : 'somepath', 'datetime added' : 'sometimestamp'}
		"""
		if self.mem_type == 'page':
			query_params = {
			'action': 'query',
			'list': 'categorymembers',
			'cmtitle' : self.cat_title,
			'cmtype': self.mem_type,
			'cmnamespace' : self.mem_namespace,
			'cmprop' : 'title|timestamp|ids',
			'cmsort' : 'timestamp',
			'cmdir' : 'desc'
			}
			req = wikitools.APIRequest(self.wiki, query_params)
			response = req.query()
			mem_list = [{'page id' : str(x['pageid']), 'page path' : x['title'], 'timestamp' : x['timestamp']} for x in response['query']['categorymembers']]
			for mem in mem_list:
				mem = self.getPageMetaData(mem)
			return mem_list
		else: 
			print "not set up to get " + self.mem_type + " category members yet"

	def getPageMetaData(self, mempage):
		"""
		Gets some additional metadata about each page. Currently just the local talkpage id or subjectid and the full url. Need to make this a call to profiles.py.
		"""
		params = {
			'action': 'query',
			'titles': mempage['page path'],
			'prop': 'info',
			'inprop' : 'talkid|subjectid|url'
		}
		req = wikitools.APIRequest(self.wiki, params)
		response = req.query()
		pageid = str(mempage['page id'])
		try:
			mempage['talkpage id'] = str(response['query']['pages'][pageid]['talkid'])
		except KeyError:
			mempage['talkpage id'] = "" #probably not necessary anymore, if I add these default params in to every one anyway.
		return mempage


#this was some 'supercat' that was below for mem in mem_list:
# 				print mem['talkpage id']
# 			if self.cat_title == "Category:IdeaLab/Ideas/Participants":
# 				print "participants FTW"
# 				query_params['cmtitle'] = self.supercat
# 				req = wikitools.APIRequest(self.wiki, query_params)
# 				response = req.query()
# 				super_list = [{'page id' : x['pageid'], 'page path' : x['title'], 'datetime added' : x['timestamp']} for x in response['query']['categorymembers']]
# 				active_pages = [x['page id'] for x in super_list]
# 				mem_list = [x for x in mem_list if x['page id'] in active_pages]
# 			else:
# 				pass


#other stuff I could be getting
# 		mempage['subject id'] = response['query']['pages'][pageid]['subjectid']
# 		mempage['url'] = response['query']['pages'][pageid]['fullurl']


