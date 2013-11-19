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
	output parameters for building various kinds of profiles and their values and settings.
	"""

	def __init__(self):
		self.output_params = {
			'gallery' : { #fixme
					'summary' : '^\|\s*summary\s*=',
					'output path' : 'Programs:Evaluation portal/',
					'edit summary' : 'Updating %s profile',
					'image' : '^\|\s*image\s*=',
					'header template' : '<noinclude>[[Category:Evaluation portal]]</noinclude>',					
					'number featured' : 2,
					'infobox params' : {
						'summary' : '^\|\s*problem\s*=',
						'endorse' : '^\|\s*endorse\s*=',
						'image' : '^\|\s*image\s*=',
						},												
					'sub page' : 'Parlor/Featured/',
					'featured' : { 
						'pattern' : {
							'namespace' : 'Grants:',
							'action' : 1,
							'first subpage' : 1,
							'query' : 'list patterns',
							},
						'question' :	{
							'namespace' : 'Programs:',
							'action' : 4,
							'first subpage' : 3,
							'query' : 'recent questions',
							},
						'intro' : {
							'action' : 5,
							'first subpage' : 5,
							'query' : 'recent intros',
							'namespace' : 'Programs:',
							},
						},	
					},
			'guide' : { 
					'output path' : 'Programs:Evaluation portal/Library/',
					'output section' : 5,				
					'edit summary' : 'Updating list of: %ss',
					'patterns' : {
						'infobox params' : {
							'summary' : '^\|\s*problem\s*=',
							'endorse' : '^\|\s*endorse\s*=',
							'image' : '^\|\s*image\s*=',
							},	
						'header template' : """== Learning patterns ==
					\n</noinclude>\n""",												
						'category' : 'Learning patterns',
						'subpage' : 'Learning patterns',
						'query' : 'list patterns',
						'namespace' : 'Grants:',
						},
					},
			'feed' : { #fixme
					'output path' : 'Programs:Evaluation portal/Activity',
					'number featured' : 6,
					'main page' : 'Programs:Evaluation portal',
					'username' : '',
					'output section' : '',
					'edit summary' : 'Updating %s entries',
					'header template' : '<noinclude>[[Category:Evaluation portal]]</noinclude>\n',
					'activity' : {
						'intro' : {
							'action' : 5,
							'query' : 'recent intros',
							'namespace' : 'Programs:',
							},
						'pattern' : {
							'action' : 1,
							'query' : 'recent patterns',
							'namespace' : 'Grants:',
							},
						'endorse' : {
							'action' : 3,
							'query' : 'recent endorsements',
							'namespace' : 'Grants:',
							},
						'question' : {
							'action' : 2,
							'query' : 'recent questions',
							'namespace' : 'Programs:',
							},					
						},
					},
			'idealab_guide' : {
					'infobox params' : {			
						'summary' : '^\|\s*summary\s*=',
						'image' : '^\|\s*image\s*=',
						},
					'header template' : """<noinclude>[[Category:IdeaLab]]</noinclude>""",	
					'main namespace' : 200,				
					'output path' : 'Grants:IdeaLab/Ideas/',
					'edit summary' : 'Updating %s',
					'participants' : {
							'category' : 'IdeaLab/Ideas/Participants',
							'subpage' : 'Participants',
							'time value' : 'timestamp',							
							},
					'draft' :        {
							'category' : 'IEG/Proposals/Draft',
							'subpage' : 'Drafts',
							'time value' : 'timestamp',							
							},
					'new' : {
							'category' : 'IdeaLab/Ideas/Active',
							'subpage' : 'New',
							'time value' : 'created',
							},
					'ineligible' : {
							'category' : 'IEG/Proposals/Ineligible', #ineligible ideas?
							'subpage' : 'Ineligible',
							'time value' : 'timestamp',														
							},
					'all' : {
							'category' : 'IdeaLab/Ideas/IdeaLab',
							'subpage' : 'All',
							'time value' : 'timestamp',														
							},
					},	
			'idealab_feed' : { #fixme
					'output path' : 'Grants:IdeaLab/Ideas/Activity',
					'number featured' : 6,
					'main page' : 'Grants:IdeaLab/Ideas/Activity',
					'main namespace' : 200,
					'username' : '',
					'output section' : '',
					'category' : 'IdeaLab/Ideas/All',					
					'edit summary' : 'Updating %s entries',
					'header template' : """<noinclude>[[Category:IdeaLab]]</noinclude>""",
					'activity' : {
						'new idea' : {
							'action' : 1,
							'category' : 'IdeaLab/Ideas/Active',							
							},
						'ieg' : {
							'action' : 4,
							'category' : 'IEG/Proposals/Draft',	
							},						
						'joined' : {
							'action' : 5,
							},					
						},
					},											
			'evalportal_intro' : {
				'output path' : 'Programs:Evaluation portal/Parlor/Introductions',
				'output page id' : 2344396,
				'profile toclevel' : 2,
				'output section' : 1,
				'edit summary' : 'Reordering %ss, putting recently active participants at the top',
				},
			'idealab_intro' : {
				'output path' : 'Grants:IdeaLab/Introductions',
				'output page id' : 2101758,
				'main namespace' : 200,
				'talk namespace' : 201,
				'edit summary' : 'Reordering %ss, putting recently active participants at the top',
				},				
			'profile defaults' : ['action','badge','datetime','image','page id','page path','participants','summary', 'create date', 'talkpage id','time','timestamp','title','title link','username','item',]
			,
			'learning reports' : {
				'output path' : 'Programs:Evaluation portal/Boiler room/Grants lessons 2012',
				'header template' : '<noinclude>[[Category:Evaluation portal]]</noinclude>\n',				
				'edit summary' : 'adding lessons learned sections of grant reports',
				},														
			}

	def getParams(self, profile_type):
		tp = self.output_params[profile_type]
		return tp		


