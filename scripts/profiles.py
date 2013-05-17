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

from BeautifulSoup import BeautifulStoneSoup as bss
import urllib2
import itertools
from wikitools import category as wtcat
import shelve #stores the pages we're interested in

import grantsbot_settings

wiki = wikitools.Wiki(grantsbot_settings.apiurl)
wiki.login(settings.username, grantsbot_settings.password)

class Page:
	"""A page on a wiki."""

	def __init__(self, title, namespace = grantsbot_settings.rootpage):
		"""
		Instantiates page-level variables.
		"""
		self.title = title
		self.namespace = namespace
		self.page_path = title + namespace

	def getText(self, section=False):
		"""
		Gets the raw text of a page or page section.
		"""
		if not section:
			section = ''
		url = self.sext_url % (self.namespace, self.title, section)
# 		url = urlEncode(url)
# 		print url
		usock = urllib2.urlopen(url)
		text = usock.read()
		usock.close()
		text = unicode(text, 'utf8')
		text = text.strip()

		return text

	def getSectionData(self, level):
		"""
		Returns the the section numbers and titles of all sections
		at a given level of the XML toc hierarchy.
		"""
		reps = {'_':'+', '/':'%2F', ' ':'+'}
		secs_list = []
		url = self.secs_url % (self.namespace, self.title)
		usock = urllib2.urlopen(url)
		sections = usock.read()
		usock.close()
		soup = bss(sections, selfClosingTags = ['s'])
		for x in soup.findAll('s',toclevel=level):
			secs_wanted = (x['index'], x['line'])
			secs_list.append(secs_wanted)

		return secs_list




class ProfilePage(Page):
	"""variables and functions related to working with profiles pages."""


classPropsalPage(Page):

class CategoryMembers:

	def getCategoryMembers(title):
		"""Get the members of a given category and its subcategories."""
		cat_pages = []
		cat_subcats = []
		cat_page = wtcat.Category(wiki, title)
		cat_pages = cat_page.getAllMembers(titleonly=True, namespace=[200,201]) #abstract
		subcat_count = len(cat_page.getAllMembers(titleonly=True, namespace=[14]))
		if len(subcat_count) > 0:

		cat_subcats = cat_page.getAllMembers(titleonly=True, namespace=[200,201])

	def getSubCatPages(cat_subcats):
		for subcat in cat_subcats:
			cat_page = wtcat.Category(wiki, title)










