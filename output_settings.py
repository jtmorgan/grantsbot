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
            'pattern_guide' : {
                    'infobox params' : {
                        'summary' : '^\|\s*problem\s*=',
                        'image' : '^\|\s*image\s*=',
                        },
                    'header template' : """<noinclude>[[Category:Learning_Pattern_Library]] {{mbox|text='''This page is updated daily by [[User:GrantsBot|GrantsBot]].''' Edits made by others may be inadvertently overwritten the next time the bot runs. If you have a question, or see an error that needs to be fixed, please post to the [[Grants_talk:Learning_patterns|Library talk page]]. You may also contact [[User:Jmorgan (WMF)|GrantsBot's maintainer]] directly.}}</noinclude>""",
                    'main namespace' : 200,
                    'output path' : 'Grants:Learning_patterns/',
                    'ignored pages' : ['Grants:IdeaLab/Preload',], #more ignored pages for inspire?
                    'edit summary' : 'Updating %s',
                    'all' :        {
                            'category' : 'Learning_patterns',
                            'subpage' : 'All',
                            'time value' : 'timestamp',
                            },
                    },
            'idealab_guide' : {
                    'infobox params' : {
                        'summary' : '^\|\s*summary\s*=',
                        'image' : '^\|\s*image\s*=',
                        },
                    'header template' : """<noinclude>[[Category:IdeaLab]]</noinclude>""",
                    'main namespace' : 200,
                    'output path' : 'Grants:IdeaLab/',
                    'ignored pages' : ['Grants:IdeaLab/Preload',],
                    'formatted fields' : ['summary',],
                    'edit summary' : 'Updating %s',
                    'participants' : {
                            'category' : 'IdeaLab/Ideas/Participants',
                            'subpage' : 'Participants',
                            'time value' : 'timestamp',
                            },
                    'draft' :        {
                            'category' : 'IEG/Proposals/Draft',
                            'subpage' : 'Ideas/Drafts',
                            'time value' : 'timestamp',
                            },
                    'new' : {
                            'category' : 'IdeaLab/Ideas/IdeaLab',
                            'subpage' : 'Ideas/New',
                            'time value' : 'created',
                            },
                    'all' : {
                            'category' : 'IdeaLab/Ideas/IdeaLab',
                            'subpage' : 'Ideas/All',
                            'time value' : 'timestamp',
                            },
                    'inspire-all' : {
                            'category' : 'IdeaLab/Ideas/Inspire',
                            'subpage' : 'Inspire/All',
                            'time value' : 'timestamp',
                            },
                    'inspire-draft' : {
                            'category' : 'IdeaLab/Ideas/Proposal',
                            'subpage' : 'Inspire/Drafts',
                            'time value' : 'timestamp',
                            },
                    },
            'idealab_profile_guide' : {
                    'infobox params' : {
                        'story' : '^\|\s*story\s*=',
                        'image' : '^\|\s*image\s*=',
                        'skills' : '^\|\s*skills\s*=',
                        },
                    'header template' : """<noinclude>[[Category:IdeaLab]]</noinclude>""",
                    'main namespace' : 200,
                    'output path' : 'Grants:IdeaLab/',
                    'ignored pages' : ['Grants:IdeaLab/Preload',],
                    'formatted fields' : ['story', 'skills'],
                    'edit summary' : 'Updating %s',
                    'inspire-profiles' : {
                            'category' : 'IdeaLab_members',
                            'subpage' : 'Inspire/Profiles',
                            'time value' : 'created',
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
            'inspire_feed' : { #needs update
                    'output path' : 'Grants:IdeaLab/Inspire/Activity',
                    'ignored pages' : ['Grants:IdeaLab/Preload',], #others?
                    'number featured' : 6,
                    'main page' : 'Grants:IdeaLab/Inspire/Activity',
                    'main namespace' : 200,
                    'username' : '',
                    'output section' : '',
                    'edit summary' : 'Updating %s entries',
                    'header template' : """<noinclude>[[Category:IdeaLab]]</noinclude>""",
                    'activity' : {
                        'new idea' : {
                            'action' : 1,
                            'category' : 'IdeaLab/Ideas/Inspire',
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
            'idealab_intro' : {
                'output path' : 'Grants:IdeaLab/Introductions',
                'output page id' : 2101758,
                'main namespace' : 200,
                'talk namespace' : 201,
                'edit summary' : 'Reordering %ss, putting recently active participants at the top',
                },
            'profile defaults' : ['action','badge','datetime','image','page id','page path','participants', 'problem', 'summary', 'create date', 'talkpage id','time','timestamp','title','title link','username','item', 'name', ]
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


