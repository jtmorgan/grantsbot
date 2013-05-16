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

class Page:
	"""A page on a wiki."""

	def __init__(self, title, namespace):
		"""
		Instantiates page-level variables.
		"""
# 		self.section = section
		self.title = title
		self.namespace = namespace
# 		self.level = level
		self.sext_url = u'http://meta.wikimedia.org/w/index.php?title=%s%s&action=raw&section=%s'
		self.secs_url = u'http://meta.wikipedia.org/w/api.php?action=parse&page=%s%s&prop=sections&format=xml'
		self.reps = {'_':'+', '/':'%%2F', ' ':'+'}


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


	def removeButtons(self, part2, part3):
		"""
		Removes particular button templates when it finds them in a page.
		This should be made more abstract.
		"""
		found = []
		edit = False
		rmv_list = []
		if part2 == 1:
			rmv_list.append("{{IEG/Proposals/Button/2}}")
		if part3 == 1:
			rmv_list.append("{{IEG/Proposals/Button/3}}")
		url = self.sext_url % (self.namespace, self.title, '')
		usock = urllib2.urlopen(url)
		text = usock.readlines()
		usock.close()
		for index, line in enumerate(text):
			for rmv in rmv_list:
				if rmv in line:
					found.append(text[index])
					del text[index]
		text = ''.join(text)
		if len(found) > 0:
			edit = True
		return (text, edit)
