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

class Template:
	"""templates of profiles for wiki pages"""
	def __init__(self):
		self.profile_templates = {
		'gallery' : u"""
{{{{Evaluation/Feature
| time = {time}
| image = {image}
| title = {title}
| action = {action}
| title link = {page path}
| summary = {summary}
}}}}""",
		'guide' : u"""
===<noinclude>{title}</noinclude>===
{{{{Evaluation/Resource/Summary
| time= {time}
| title = {title}
| title link= {page path}
| summary= {summary}
| image = {image}
}}}}""",
		'feed' :u"""
==<noinclude>{item}</noinclude>==
{{{{Evaluation/Activity/Entry
| time = {time}
| username = {username}
| action = {action}
| title = {title}
| title link = {page path}
}}}}"""	,
	'intro' : u"""<noinclude>{{{{Evaluation/Header
|page summary=Thanks for making your profile! {{{{Evaluation/Link/Dark_background|top text=|top color=F7F6F1|top wikilink=Programs:Evaluation_portal/Parlor|line color=F7F6F1}}}}
|links=
|more content=<div style="color: #2E2C2C; text-align:center">{{{{Evaluation/People/Button}}}}</div>
}}}}
</noinclude>
{profiles}""",
	'learning reports' :u"""
=={title}==
{{{{main|{page path}}}}}

{lessons}

""",
}

	def getTemplate(self, member):
		tmplt = self.profile_templates[member]
		return tmplt

