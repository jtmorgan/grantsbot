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
			'evalportal_gallery' : {
					'edit summary' : 'Updating %s profiles',
					'header template' : '<noinclude>[[Category:Evaluation portal]]</noinclude>',
					'learning_pattern' : {
						'output path' : 'Grants:Evaluation/Library/Featured/',
						'action' : 1,
						'input page path' : 'Grants:Learning_patterns',
						'input page id' : 2344400,
						'profile toclevel' : 2,
						'first subpage' : 1,
						'number featured' : 4,
						'infobox params' : {
							'summary' : '^\|\s*summary\s*=',
							'image' : '^\|\s*image\s*=',
							'page path' : '^\|\s*title link\s*=',
							'time' : '^\|\s*time\s*=',
							},
						},
					'case_study' : {
						'output path' : 'Grants:Evaluation/Library/Featured/',
						'action' : 3,
						'input page path' : 'Grants:Evaluation/Library/Case_studies',
						'input page id' : 2344401,
						'first subpage' : 5,
						'number featured' : 1,
						'profile toclevel' : 2,
						'infobox params' : {
							'summary' : '^\|\s*summary\s*=',
							'image' : '^\|\s*image\s*=',
							'page path' : '^\|\s*title link\s*=',
							'time' : '^\|\s*time\s*=',
							},
						},
					'learning_module' : {
						'output path' : 'Grants:Evaluation/Library/Featured/',
						'action' : 2, #not ready for this yet
						'input page path' : 'Grants:Evaluation/Library/Learning_modules',
						'input page id' : 2344399,
						'first subpage' : 6,
						'number featured' : 1,
						'profile toclevel' : 2,
						'infobox params' : {
							'summary' : '^\|\s*summary\s*=',
							'image' : '^\|\s*image\s*=',
							'page path' : '^\|\s*title link\s*=',
							'time' : '^\|\s*time\s*=',
							},
						},
					'intro' : {
						'output path' : 'Grants:Evaluation/Parlor/Featured/',
						'action' : 5,
						'input page path' : 'Grants:Evaluation/Parlor/Introductions',
						'input page id' : 2344396,
						'first subpage' : 1,
						'number featured' : 3,
						'profile toclevel' : 2,
						'infobox params' : {
							'summary' : '^\|\s*story\s*=',
							'name' : '^\|\s*name\s*=',
							'image' : '^\|\s*image\s*=',
							},
						},
					'question' : {
						'output path' : 'Grants:Evaluation/Parlor/Featured/',
						'action' : 4,
						'input page path' : 'Grants:Evaluation/Parlor/Questions',
						'input page id' : 2344395,
						'first subpage' : 4,
						'number featured' : 3,
						'profile toclevel' : 1,
						'infobox params' : {
							'summary' : '^\|\s*summary\s*=',
							'image' : '^\|\s*image\s*=',
							'page path' : '^\|\s*title link\s*=',
							'time' : '^\|\s*time\s*=',
							},
						},
					},
			'guide' : {
					'output path' : 'Grants:Learning_patterns',
					'output section' : 1,
					'edit summary' : 'Updating %s',
					'patterns' : {
						'infobox params' : {
							'summary' : '^\|\s*problem\s*=',
							'endorse' : '^\|\s*endorse\s*=',
							'image' : '^\|\s*image\s*=',
							},

						'header template' : """== Patterns ==\n</noinclude>""",
						'category' : 'Learning patterns',
						'subpage' : '',
						'query' : 'list patterns',
						'namespace' : 'Grants:',
						},
					},
			'feed' : { #fixme
					'output path' : 'Grants:Evaluation/Activity',
					'number featured' : 6,
					'main page' : 'Grants:Evaluation',
					'username' : '',
					'output section' : '',
					'edit summary' : 'Updating %s entries',
					'header template' : '<noinclude>[[Category:Evaluation portal]]</noinclude>\n__NOTOC__\n',
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
					'ignored pages' : ['Grants:IdeaLab/Preload',],
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
							'category' : 'IdeaLab/Ideas/IdeaLab',
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
					'ignored pages' : ['Grants:IdeaLab/Preload',],
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
						'participants wanted' : {
							'action' : 3,
							'category' : 'IdeaLab/Ideas/Participants',
							},
						'joined' : {
							'action' : 5,
							},
						},
					},
			'idealab_gallery' : {
					'edit summary' : 'Updating %s profiles',
					'header template' : '<noinclude>[[Category:IdeaLab]]</noinclude>',
					'new_idea' : {
						'output path' : 'Grants:IdeaLab/Ideas/Featured/',
						'action' : 1,
						'input page path' : 'Grants:IdeaLab/Ideas/New',
						'input page id' : 2289291,
						'profile toclevel' : 1,
						'first subpage' : 1,
						'number featured' : 2,
						'infobox params' : {
							'summary' : '^\|\s*summary\s*=',
							'image' : '^\|\s*image\s*=',
							'page path' : '^\|\s*idea link\s*=',
							'time' : '^\|\s*time\s*=',
							},
						},
					'participants_wanted' : {
						'output path' : 'Grants:IdeaLab/Ideas/Featured/',
						'action' : 3,
						'input page path' : 'Grants:IdeaLab/Ideas/Participants',
						'input page id' : 2294498,
						'first subpage' : 3,
						'number featured' : 2,
						'profile toclevel' : 1,
						'infobox params' : {
							'summary' : '^\|\s*summary\s*=',
							'image' : '^\|\s*image\s*=',
							'page path' : '^\|\s*idea link\s*=',
							'time' : '^\|\s*time\s*=',
							},
						},
					'ieg_draft' : {
						'output path' : 'Grants:IdeaLab/Ideas/Featured/',
						'action' : 4,
						'input page path' : 'Grants:IdeaLab/Ideas/Drafts',
						'input page id' : 2294500,
						'first subpage' : 5,
						'number featured' : 2,
						'profile toclevel' : 1,
						'infobox params' : {
							'summary' : '^\|\s*summary\s*=',
							'image' : '^\|\s*image\s*=',
							'page path' : '^\|\s*idea link\s*=',
							'time' : '^\|\s*time\s*=',
							},
						},
					'intro' : {
						'output path' : 'Grants:IdeaLab/Introductions/Featured/',
						'action' : 5,
						'input page path' : 'Grants:IdeaLab/Introductions',
						'input page id' : 2101758,
						'first subpage' : 1,
						'number featured' : 6,
						'profile toclevel' : 1,
						'infobox params' : {
							'summary' : '^\|\s*story\s*=',
							'name' : '^\|\s*name\s*=',
							'image' : '^\|\s*image\s*=',
							'badge' : '^\|\s*badge\s*=',
							},
						},
					},
			'evalportal_intro' : {
				'output path' : 'Grants:Evaluation/Parlor/Introductions',
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
			'profile defaults' : ['action','badge','datetime','image','page id','page path','participants','summary', 'create date', 'talkpage id','time','timestamp','title','title link','username','item', 'name', ]
			,
			'learning reports' : {
				'output path' : 'Grants:Evaluation/Boiler room/Grants lessons 2012',
				'header template' : '<noinclude>[[Category:Evaluation portal]]</noinclude>\n',
				'edit summary' : 'adding lessons learned sections of grant reports',
				},
			}

	def getParams(self, profile_type):
		tp = self.output_params[profile_type]
		return tp


