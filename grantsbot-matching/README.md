grantsbot-matching
==================

GrantsBot/matching is a MediaWiki bot that runs in the
[IdeaLab](https://meta.wikimedia.org/wiki/Grants:IdeaLab), a collaborative
space that supports prospective grant applicants.

Ideas are tagged with categories denoting skills needed and topic; profiles are
tagged with skill and interest categories. GrantsBot/matching aids
discoverability by using these categories to select a relevant set of ideas for
each participant with a profile and posting them on the profile talk page, tagging
the participant so that they get an Echo notification.


## Getting started

To download with git:
```bash
$ git clone https://github.com/fhocutt/grantsbot-matching.git
```

Update `config.json` with your bot's login information and database
credentials, and make any other necessary changes (see
[Configuring GrantsBot/matching](#Configuring GrantsBot/matching)
for more information).

To create a database with the expected schema:
```bash
$ python path/to/grantsbot-matching/bin/createtable.py
```

To run the script manually:
```bash
$ python path/to/grantsbot-matching/matching/matching.py <path-to-config>
```
`<path-to-config>` defaults to `./matching/` if omitted.

GrantsBot/matching will not run if the directory specified in
`<path-to-config>` does not contain `config.json` and a `log/` folder.

### Running on Tool Labs
GrantsBot/matching is designed to be run on
[Tool Labs](https://wikitech.wikimedia.org/wiki/Help:Tool_Labs) with two
associated MySQL databases, one to log matches and one that lists the number of recent contributors to ideas in the IdeaLab.

Steps to get started:
* Make an account for your bot on the wiki you're running it on.
* Set up an account with database access on Tool Labs.
* Clone this repository.
* Edit `config.json` to include your bot's information (wiki and database logins).
* Set up a virtual environment with all necessary dependencies. Set up and activate your virtualenv with
```bash
path/to/virtualenv$ virtualenv .
path/to/virtualenv$ source bin/activate
```
and then use `pip` to install the needed dependencies:
```bash
$ pip install mysql-python
$ pip install sqlalchemy
$ pip install git+git://github.com/mwclient/mwclient.git
```
* Set up your database tables to log information on matches and track active ideas (see [Databases](#Databases) for details)
* If you want to set the bot up to run every five minutes, add the following line to your crontab in your Labs project account:
```
*/5 * * * * jsub /path/to/virtualenv/bin/python /path/to/grantsbot-matching/matching/matching.py /path/to/grantsbot-matching/matching/
```
This will use the `jsub` job scheduler on Tool Labs to run the bot using the virtualenv that you have set up previously.


## Dependencies
See `requirements.txt` for dependencies.

Notes:

* The development version of [mwclient](https://github.com/mwclient/mwclient)
  can be installed with pip:
```bash
$ pip install git+git://github.com/mwclient/mwclient.git
```
* SQLAlchemy depends on MySQLdb. On Tool Labs, if you are having a problem
  involving MySQLdb, try running `pip install mysql-python` from inside your
  virtualenv.


## How matches are made
GrantsBot/matching's category-based matching algorithm is as follows:

* Create a list of ideas which have been created recently and which are currently active
* List new and newly updated profiles, noting the skill and interest categories
* For each new (or newly updated) profile:
    * Find 5 active ideas which are categorized as looking for contributors with both an interest and a skill listed on the profile
    * If there are more than 5 such ideas, choose a random selection to post
    * If there are fewer than 5 such ideas, repeats the search with the match
      requirement loosened (topic *or* skill, not topic *and* skill)
    * If there are still fewer than 5 ideas in the list, add a random selection
      from the list of all ideas to make a list of 5 ideas (checking for duplicates in all cases)

GrantsBot/matching assumes that:

* Every IdeaLab participant will create their own profile page.
* Only sub-pages of the [IdeaLab](https://meta.wikimedia.org/wiki/Grants:IdeaLab)
  and its associated [talk pages](https://meta.wikimedia.org/Grants_talk:IdeaLab) are
  relevant to GrantsBot/matching's activity (queries or edits).
* Participants will correctly tag their profiles with the correct categories, whether
  via manual edits or through the profile page creation gadget.
* IdeaLab participants who do not want to receive automatic matches will manually
  add the opt-out category to their profile pages.


## Configuring GrantsBot/matching

GrantsBot/matching keeps user-configurable information (login and database
information, text of the greeting to post, relevant category titles, and
namespace/subpage information) in a configuration file.

To change these settings, use a text editor to edit `config.json`. You should
add `config.json` to your `.gitignore` file to avoid accidentally uploading
your bot's credentials to your code repository. A sample configuration file is
provided (`config.json.sample`).

JSON quirks:
* JSON expects no comma after the last item in a list. If you are getting
  mysterious JSON-related errors, check your lists.
* Only use double quotation marks, `"`.

### Configurable settings
#### Categories (`categories`):
As described in [How matches are made](#How matches are made), GrantsBot/matching
uses the presence or absence of categories on IdeaLab profile pages to select
the ideas most likely to be of interest. An IdeaLab participant may opt out of
receiving matches by adding the opt-out category to their profile page. A
participant declares their skills and interests by adding one or more of the
associated categories to their IdeaLab profile.

All categories should include the "Category:" prefix.

Categories are divided between `ideas` and `people` and should be added to
Idea pages and profile pages, respectively.

* `ideas`:
    * all: category containing all IdeaLab ideas
    * skills: list of skills that may be useful in carrying out an idea
    * topics: list of high-level topics of interest

* `people`:
    * all: category containing all IdeaLab participants
    * optout: category for participants who do not wish to receive match messages
    * skills: list of skills participants have to offer
    * topics: list of high-level topics of interest (e.g. for Inspire campaigns, the campaign topic)

There may be any number of skills or topics in these lists, but
there *must* be the same number in the respective `ideas` and `people` lists and each pair of lists
*must* be in the same order.


#### Database information (`dbinfo`):

* `dbname`, `host`: Database name and host for the MySQL database you are using
  to log matches and record idea activity (see [Logging](#Logging)).
* `username`, `password`: Username and password for the MySQL database; distinct
  from the bot's wiki username and password.


#### Messages (`greetings`):
GrantsBot/matching edits IdeaLab profile talk pages to deliver a list of five ideas of possible interest, using the text provided in this section.

* `section`: Section header for normal talk pages. Also used as the edit summary.
* `greeting`: Text of the section contents. This will generate an Echo notification for the participant.
     * `{0}`: The user name of the participant
     * `{1}`: The list of five ideas

*NOTE:* All `{N}`-type text listed above *must* be included in your messages,
no matter what other changes you make to the message text. For example, a
`nomatchgreeting` string that does not contain "`{0}`" is not valid and will
lead to errors that prevent the message from being posted.


#### Login information (`login`)

* `username`, `password`: Your bot's username and password on the wiki it runs on.
* `protocol`: `http` or `https`. `https` is more secure and is recommended if
  the wiki supports it.
* `site`: the URL of the wiki the bot runs on (for instance, `meta.wikimedia.org`
  for [Meta-Wiki](https://meta.wikimedia.org))
* `useragent`: Information about your bot. When running on WMF-run wikis, it
  must contain your bot's user name and a way to contact the person responsible
  for running it. For more information, see the [User-agent policies](http://meta.wikimedia.org/wiki/User-Agent_policy).


#### Namespace/root page/prefixes (`pages`):
GrantsBot/matching operates on sub-pages of the main IdeaLab page and of its associated talk
page.

* `main`: Title of the main page. All IdeaLab profile pages are sub-pages of this
  page.
* `talk`: Title of the main talk page. All IdeaLab profile talk pages are sub-
  pages of this page.


## Logging
GrantsBot/matching logs information every time it is run. All log files are stored in
`path/to/grantsbot-matching/matching/log/`; the database of matches and active ideas is stored
on Tool Labs.

### Run logs
Information about each time the bot runs is logged to the `matching.log` text
file: the date and time the script was run, whether the script successfully
edited one or more pages, successfully logged information on one or more
matches to the associated relational database, and whether any errors were
handled while the script ran.

Example line in `matching.log`:
```
INFO 2015-01-01 01:00:45.650401 Edited: False Wrote DB: False Errors: False
```
To cap the size of these files, a new log file is started every 30 days. Two
backup logs are kept, each for 60 days.

### Databases
GrantsBot/matching's record of recently created and active ideas and log of
matches posted are both backed by a MySQL database on
[Tool Labs](https://wikitech.wikimedia.org/wiki/Help:Tool_Labs).

#### Active ideas (`idealab_ideas`)
GrantsBot/matching identifies recently active ideas (recently created, and with
a certain number of userids posting on the idea page and talk page) so that the
bot does not recommend inactive ideas. It gets this information from the 
`idealab_ideas` table in the project database. It has the following structure:

```sql
> SHOW COLUMNS FROM idealab_ideas;
+---------------------+------------------+------+-----+---------+----------------+
| Field               | Type             | Null | Key | Default | Extra          |
+---------------------+------------------+------+-----+---------+----------------+
| id                  | int(11) unsigned | NO   | PRI | NULL    | auto_increment |
| idea_id             | int(11)          | YES  | UNI | NULL    |                |
| idea_title          | varbinary(255)   | YES  |     | NULL    |                |
| idea_talk_id        | int(11)          | YES  |     | NULL    |                |
| idea_creator        | varbinary(255)   | YES  |     | NULL    |                |
| idea_created        | datetime         | YES  |     | NULL    |                |
| idea_endorsements   | int(11)          | YES  |     | NULL    |                |
| idea_recent_editors | int(11)          | YES  |     | NULL    |                |
| ignore              | tinyint(1)       | YES  |     | 0       |                |
+---------------------+------------------+------+-----+---------+----------------+
```

Running `$ python bin/ideaDBcreation.py` should create this table.

This table can be regularly updated by running the following script:
[Update idea table](https://github.com/jtmorgan/grantsbot/blob/master/idealab/update_idea_table.py)
The `ignore` column defaults to `0` and is not automatically updated. Manually
setting the `ignore` flag to 1 will prevent the bot from adding that idea to
any lists to be posted.

#### Matches (`matches`)
Information about matches posted is logged to the `matches` table, which has the following
structure:

```sql
> SHOW COLUMNS FROM matches;

+--------------------+-------------+------+-----+---------+----------------+
| Field              | Type        | Null | Key | Default | Extra          |
+--------------------+-------------+------+-----+---------+----------------+
| id                 | int(11)     | NO   | PRI | NULL    | auto_increment |
| participant_userid | int(11)     | YES  |     | NULL    |                |
| p_profile_pageid   | int(11)     | YES  |     | NULL    |                |
| p_interest         | varchar(75) | YES  |     | NULL    |                |
| p_skill            | varchar(75) | YES  |     | NULL    |                |
| request_time       | datetime    | YES  |     | NULL    |                |
| match_time         | datetime    | YES  |     | NULL    |                |
| match_revid        | int(11)     | YES  |     | NULL    |                |
| idea_pageid        | int(11)     | YES  |     | NULL    |                |
| run_time           | datetime    | YES  |     | NULL    |                |
+--------------------+-------------+------+-----+---------+----------------+
```

Methods to create this table are in `bin/sqlcreateinsert.py`.

Help on Tool Labs is available on the `#wikimedia-labs` IRC channel on
Freenode.

### Errors
When possible, GrantsBot/matching simply logs errors and allows the script to continue.
Errors are logged to `matching_errors.log`. They include a stack trace for
all exceptions raised, including ones that are logged and handled so
GrantsBot/matching can finish running.

The `matching_errors.log` file is not automatically rotated. If the file becomes
inconveniently large, you can compress it or delete it.
