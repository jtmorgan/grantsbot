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

class Params:
	"""
	output parameters for building various kinds of profiles and their values
	"""

	def __init__(self):
		self.output_params = {
			'featured idea' : {
				'summary' : '^\|\s*summary\s*=',
				'output path' : 'Grants:IdeaLab/Ideas/Featured/',
				'edit summary' : '**TeSt** updating %s profile',
				'number featured' : 2,
				'participants' : {
					'category' : 'IEG/Proposals/Participants',
					'action' : 3,
					'first subpage' : 1,
					},
				'draft' :	{
					'category' : 'IEG/Proposals/Draft/IdeaLab',
					'action' : 4,
					'first subpage' : 3,
					},
				'new' : {
					'category' : 'IEG/Proposals/IdeaLab',
					'action' : 1,
					'first subpage' : 5,
					},
				},
			'featured person' : {
				'summary' : '| story',
				'output path' : 'Grants:IdeaLab/Introductions/Featured/',
				'edit summary' : '**TeSt** updating %s profile',
				'number featured' : 6,
				'main page' : 'Grants:IdeaLab/Introductions',
				'image' : '| image =',
				'recent' : {
					'action' : 5,
					'first subpage' : 3,
					},
				'active' : {
					'action' : 5,
					'first subpage' : 1,
					},
				},
			'idea profile' : {
				'summary' : '^\|\s*summary\s*=',
				'creator' : '^\|\s*creator\s*=',
				'output path' : 'Grants:IdeaLab/Ideas/',
				'edit summary' : '**TeSt** updating %ss',
				'participants' : {
					'category' : 'IEG/Proposals/Participants',
					'subpage' : 'Participants',
					},
				'draft' :	{
					'category' : 'IEG/Proposals/Draft/IdeaLab',
					'subpage' : 'Drafts',
					},
				'new' : {
					'category' : 'IEG/Proposals/IdeaLab',
					'subpage' : 'New',
					},
				'ineligible' : {
					'category' : 'IEG/Proposals/Ineligible',
					'subpage' : 'Ineligible',
					},
				'all' : {
					'category' : 'IEG/Proposals/IdeaLab',
					'subpage' : 'All',
					},
				},
			'participant profile' : {
				'output path' : 'Grants:IdeaLab/Introductions',
				'edit summary' : 'Reordering %ss, putting recently active collaborators at the top',
				},
			}

	def getParams(self, prfl_type):
		try:
			tp = self.output_params[prfl_type]
			return tp
		except:
			print "unrecognized profile type " + prfl_type

