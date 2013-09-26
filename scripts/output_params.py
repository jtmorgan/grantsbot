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
			'featured_idea' : {
				'summary' : '^\|\s*summary\s*=',
				'output path' : 'Grants:IdeaLab/Ideas/Featured/',
				'edit summary' : 'Updating %s profile',
				'image' : '^\|\s*image\s*=',
				'number featured' : 2,
				'participants' : {
					'category' : 'IdeaLab/Ideas/Participants',
					'action' : 3,
					'first subpage' : 1,
					},
				'draft' :	{
					'category' : 'IEG/Proposals/Draft',
					'action' : 4,
					'first subpage' : 3,
					},
				'new' : {
					'category' : 'IdeaLab/Ideas/Active',
					'action' : "",
					'first subpage' : 5,
					},
				},
			'featured_person' : {
				'summary' : '^\|\s*story\s*=',
				'output path' : 'Grants:IdeaLab/Introductions/Featured/',
				'edit summary' : 'Updating %s profile',
				'number featured' : 6,
				'main page' : 'Grants:IdeaLab/Introductions',
				'image' : '^\|\s*image\s*=',
				'badge' : '^\|\s*badge\s*=',
				'recent' : {
					'action' : 5,
					'first subpage' : 3,
					},
				'active' : {
					'action' : 5,
					'first subpage' : 1,
					},
				},
			'idea_profile' : {
				'summary' : '^\|\s*summary\s*=',
				'creator' : '^\|\s*creator\s*=',
				'image' : '^\|\s*image\s*=',
				'output path' : 'Grants:IdeaLab/Ideas/',
				'edit summary' : 'Updating %ss',
				'participants' : {
					'category' : 'IdeaLab/Ideas/Participants',
					'subpage' : 'Participants',
					},
				'draft' :	{
					'category' : 'IEG/Proposals/Draft',
					'subpage' : 'Drafts',
					},
				'new' : {
					'category' : 'IdeaLab/Ideas/Active',
					'subpage' : 'New',
					},
				'ineligible' : {
					'category' : 'IEG/Proposals/Ineligible', #ineligible ideas?
					'subpage' : 'Ineligible',
					},
				'all' : {
					'category' : 'IdeaLab/Ideas/IdeaLab',
					'subpage' : 'All',
					},
				},
			'participant_profile' : {
				'output path' : 'Grants:IdeaLab/Introductions',
				'edit summary' : 'Reordering %ss, putting recently active collaborators at the top',
				},
			'activity_feed' : {
				'output path' : 'Grants:IdeaLab/Ideas/Activity',
				'number featured' : 6,
				'main page' : 'Grants:IdeaLab/',
				'creator' : 'creator',
				'edit summary' : 'Updating %s',
				'header template' : '<noinclude>{{IdeaLab/Categories/Template}}</noinclude>\n',
				'people' : {
					'action' : 5,
					'subpage' : 'Introductions',
					},
				'new' : {
					'action' : 1,
					'category' : 'IdeaLab/Ideas/Active',
					'subpage' : 'Ideas/All',
					},
				'draft' : {
					'action' : 4,
					'category' : 'IEG/Proposals/Draft',
					'subpage' : 'Ideas/Drafts',
					},
				'participants' : {
					'action' : 3,
					'category' : 'IdeaLab/Ideas/Participants',
					'subpage' : 'Ideas/Participants',
					},
				},
			'ieg_proposal' : {
				'button header' : 'Part 2:',
				'button template' : '{{IEG/Proposals/Button/2}}',
				'edit summary' : 'Removing button templates from %ss',
				'draft' :	{
					'category' : 'IEG/Proposals/Draft',
					},
				'proposed' :	{
					'category' : 'IEG/Proposals/Proposed',
					},
				'withdrawn' :	{
					'category' : 'IEG/Proposals/Withdrawn',
					},
				'ineligible' : {
					'category' : 'IEG/Proposals/Ineligible',
					},
				},
			'evaluation_activity_feed' : { #fixme
				'output path' : 'Grants:IdeaLab/Ideas/Activity',
				'number featured' : 6,
				'main page' : 'Grants:IdeaLab/',
				'creator' : 'creator',
				'edit summary' : 'Updating %s',
				'header template' : '<noinclude>{{IdeaLab/Categories/Template}}</noinclude>\n',
				'people' : {
					'action' : 5,
					'subpage' : 'Introductions',
					},
				'new' : {
					'action' : 1,
					'category' : 'IdeaLab/Ideas/Active',
					'subpage' : 'Ideas/All',
					},
				'draft' : {
					'action' : 4,
					'category' : 'IEG/Proposals/Draft',
					'subpage' : 'Ideas/Drafts',
					},
				'participants' : {
					'action' : 3,
					'category' : 'IdeaLab/Ideas/Participants',
					'subpage' : 'Ideas/Participants',
					},
				},
			'evaluation_resource_profile' : { #fixme
				'summary' : '^\|\s*summary\s*=',
				'creator' : '^\|\s*creator\s*=',
				'image' : '^\|\s*image\s*=',
				'output path' : 'Grants:IdeaLab/Ideas/',
				'edit summary' : 'Updating %ss',
				'participants' : {
					'category' : 'IdeaLab/Ideas/Participants',
					'subpage' : 'Participants',
					},
				'draft' :	{
					'category' : 'IEG/Proposals/Draft',
					'subpage' : 'Drafts',
					},
				'new' : {
					'category' : 'IdeaLab/Ideas/Active',
					'subpage' : 'New',
					},
				'ineligible' : {
					'category' : 'IEG/Proposals/Ineligible', #ineligible ideas?
					'subpage' : 'Ineligible',
					},
				'all' : {
					'category' : 'IdeaLab/Ideas/IdeaLab',
					'subpage' : 'All',
					},
				},
			'evaluation_featured_resource' : { #fixme
				'summary' : '^\|\s*summary\s*=',
				'output path' : 'Grants:IdeaLab/Ideas/Featured/',
				'edit summary' : 'Updating %s profile',
				'image' : '^\|\s*image\s*=',
				'number featured' : 2,
				'participants' : {
					'category' : 'IdeaLab/Ideas/Participants',
					'action' : 3,
					'first subpage' : 1,
					},
				'draft' :	{
					'category' : 'IEG/Proposals/Draft',
					'action' : 4,
					'first subpage' : 3,
					},
				'new' : {
					'category' : 'IdeaLab/Ideas/Active',
					'action' : "",
					'first subpage' : 5,
					},
				},
			'evaluation_featured_person' : { #fixme
				'summary' : '^\|\s*story\s*=',
				'output path' : 'Grants:IdeaLab/Introductions/Featured/',
				'edit summary' : 'Updating %s profile',
				'number featured' : 6,
				'main page' : 'Grants:IdeaLab/Introductions',
				'image' : '^\|\s*image\s*=',
				'badge' : '^\|\s*badge\s*=',
				'recent' : {
					'action' : 5,
					'first subpage' : 3,
					},
				'active' : {
					'action' : 5,
					'first subpage' : 1,
					},
				},
			'evaluation_participant_profile' : { #fixme
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

