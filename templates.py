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
		'pattern_guide' : u"""
===<noinclude>{title}</noinclude>===
{{{{Evaluation/Resource/Summary
| time= {time}
| title = {title}
| title link= {page path}
| summary= {summary}
| creator= {username}
| image = {image}
}}}}""",
'idealab_guide' : u"""
==<noinclude>{title}</noinclude>==
{{{{IdeaLab/Idea/Summary
| time= {time}
| idea= {title}
| idea link= {page path}
| summary= {summary}
| creator= {username}
| image = {image}
}}}}""",
'idealab_profile_guide' : u"""
==<noinclude>{title}</noinclude>==
{{{{IdeaLab/Inspire/Profile
| title= {title}
| link= {page path}
| story= {story}
| skills= {skills}
| image = {image}
| timestamp = {time}
}}}}""",
'idealab_feed' :u"""
{{{{IdeaLab/Activity/Entry
| time = {time}
| username = {username}
| number of people = {participants}
| action = {action}
| idea = {title}
| idea link = {page path}
}}}}""",
'inspire_feed' :u"""
{{{{IdeaLab/Activity/Entry
| time = {time}
| username = {username}
| number of people = {participants}
| action = {action}
| idea = {title}
| idea link = {page path}
}}}}""",
'idealab_gallery' :u"""
{{{{IdeaLab/Feature
| time = {time}
| image = {image}
| name = {name}
| username = {username}
| number of people = {participants}
| action = {action}
| idea = {title}
| idea link = {page path}
| summary = {summary}
}}}}""",
	'idealab_intro' : u"""<noinclude><div style="font-family: Helvetica Neue, Helvetica, arial, sans-serif; line-height: 1.5em; background-color: #ffffff; color: #{{{{IEG/Color/Gray}}}}; min-width: 810px; margin-top: -60px; padding: 40px 0 20px">
<div style="margin:0 15%">
<span style="font-size: 3em; color: #{{{{IEG/Color/Light blue}}}};">'''IdeaLab'''</span>
<div style="margin:1em 0">
<span style="font-size: 3em; color: #{{{{IEG/Color/Light blue}}}};">introductions</span></div>
<div style="margin:3em 0">If you've made any corrections to your introduction and you are finished, [[Grants:IdeaLab|return to the IdeaLab]].</div>
</div>
</div></noinclude>
{profiles}""",
}

	def getTemplate(self, member):
		"""
		Select a profile template that matches the passed template name.
		"""
		tmplt = self.profile_templates[member]
		return tmplt

