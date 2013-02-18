#! /usr/bin/env python

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

import sys; sys.path.append('/home/jtmorgan/local/lib/python2.7/site-packages/')
from BeautifulSoup import BeautifulStoneSoup as bss
import urllib2
import itertools

#instantiates page variables. Level and section are optional parameters.
class Page:
	def __init__(self, title, namespace, level=False, section=False):
		self.section = section
		self.title = title
		self.namespace = namespace
		self.level = level
		self.sext_url = u'http://meta.wikimedia.org/w/index.php?title=%s%s&action=raw&section=%s'
		self.secs_url = u'http://meta.wikipedia.org/w/api.php?action=parse&page=%s%s&prop=sections&format=xml'
		self.reps = {'_':'+', '/':'%%2F', ' ':'+'}

	#gets the raw text of a page or a page section	
	def getText(self):
		url = self.sext_url % (self.namespace, self.title, self.section)
		url = urlEncode(url)
# 		print url
		usock = urllib2.urlopen(url)
		text = usock.read()
		usock.close()
		text = unicode(text, 'utf8')
		text = text.strip()	
		return text

	#gets the titles of all sections at a given level of the XML toc hierarchy.	
	def getSectionData(self):
		reps = {'_':'+', '/':'%2F', ' ':'+'}
		sec_list = []
		url = self.secs_url % (self.namespace, self.title)						
		usock = urllib2.urlopen(url)
		sections = usock.read()
		usock.close()
		soup = bss(sections, selfClosingTags = ['s'])
		for x in soup.findAll('s',toclevel=self.level):
			secs_wanted = x['line']
			sec_list.append(secs_wanted)	
		return sec_list	
	
	#removes particular button templates when it finds them in a page. This could be more abstract.	
	def removeButtons(self, part2, part3):
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
		