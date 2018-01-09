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
                    'header template' : """<noinclude>[[Category:Learning_Pattern_Library]] {{mbox|text='''The list on this page is transcluded and updated daily by [[User:GrantsBot|GrantsBot]].''' Please make any edits to the actual pages listed, not here at the transclusion. If you have a question, or see an error that needs to be fixed, please post to the [[Grants_talk:Learning_patterns|Library talk page]]. You may also contact [[User:Jmorgan (WMF)|GrantsBot's maintainer]] directly.}}</noinclude>""",
                    'main namespace' : 0,
                    'output path' : 'Learning_patterns/',
                    'ignored pages' : [u'Sandbox:KHarold (WMF)/Education Toolkit/',u'KHarold (WMF) Sandbox/Education Toolkit/Dealing with Challenges',u'KHarold (WMF) Sandbox/Education Toolkit/Dealing with Challenges/Connectivity',],#had to make this a unicode string as a hack; should use unicode by default instead
                    'formatted fields' : ['problem'],
                    'edit summary' : 'Updating %s',
                    'all' :        {
                            'categories' : ['Learning_patterns',],
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
                            'categories' : ['IdeaLab/Ideas/Participants',],
                            'subpage' : 'Participants',
                            'time value' : 'timestamp',
                            },
                    'draft' :        {
                            'categories' : ['Project/Proposals/Draft', 'Rapid/Proposals/Draft', 'IdeaLab/Ideas/Proposal',],
                            'subpage' : 'Ideas/Drafts',
                            'time value' : 'timestamp',
                            },
                    'new' : {
                            'categories' : ['IdeaLab/Ideas/IdeaLab','IdeaLab/Ideas/Inspire',],
                            'subpage' : 'Ideas/New',
                            'time value' : 'created',
                            },
                    'all' : {
                            'categories' : ['IdeaLab/Ideas/IdeaLab','IdeaLab/Ideas/Inspire',],
                            'subpage' : 'Ideas/All',
                            'time value' : 'timestamp',
                            },
                    'inspire-all' : {
                            'categories' : ['IdeaLab/Ideas/Inspire/New_readers',],
                            'subpage' : 'Inspire/All',
                            'time value' : 'timestamp',
                            },
                    'inspire-draft' : {
                        'categories' : ['Project/Proposals/IdeaLab', 'Rapid/Proposals/Draft', 'IdeaLab/Ideas/Proposal',],
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
                    'header template' : """<noinclude>
[[Category:IdeaLab]]
{| class="infobox" style="width: 120px;" 
| colspan="2" | '''Can't find your profile?''' [[Grants:IdeaLab/Introductions/Archive|Check to archive]].
|}
</noinclude>""",
                    'main namespace' : 200,
                    'output path' : 'Grants:IdeaLab/',
                    'ignored pages' : ['Grants:IdeaLab/Preload',],
                    'formatted fields' : ['story', 'skills'],
                    'edit summary' : 'Updating %s',
                    'inspire-profiles' : {
                            'categories' : ['IdeaLab_members',],
                            'subpage' : 'Introductions',
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
                        'project_draft' : {
                            'action' : 4,
                            'category' : 'Project/Proposals/Draft',
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
                            'category' : 'IdeaLab/Ideas/Inspire/Knowledge_networks',
                            },
#                         'project draft' : {
#                             'action' : 4,
#                             'category' : 'Project/Proposals/Draft',
#                             },
#                         'rapid draft' : {
#                             'action' : 6,
#                             'category' : 'Rapid/Proposals/Draft',
#                             },                                                          
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
                        'number featured' : 4,
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
                            'page path' : '^\|\s*link\s*=',
                            'image' : '^\|\s*image\s*=',
                            'time' : '^\|\s*timestamp\s*=',
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


