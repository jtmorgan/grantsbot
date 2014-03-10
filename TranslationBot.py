#   -*- coding: utf-8  -*-


import wikipedia
import time, sys, codecs
import re
from datetime import datetime, timedelta

class TranslateBot:
  def __init__(self):
    self.site = wikipedia.getSite(fam='meta', code='meta', user='GrantsBot') # although it can be used directly on other wikis, but this is the default.


  def addTranslate(self):
    title = u"Grants:Learning & Evaluation/About"
    page = wikipedia.Page(self.site, title)


    try:
      pageText = page.get()
      pagetitle = page.title()
    except wikipedia.NoPage:
      wikipedia.output("Page does not exist!")
      return
    except KeyboardInterrupt:
      raise KeyboardInterrupt
    except:
      wikipedia.output("Unknown error!")
      return

    page_text = "<!-- Translation tags were added automatically by GrantsBot. Templates and tables are excluded. Please tag them manually if necessary.-->\n<translate>" + pageText
    page_text = page_text + "</translate>"

    page_text = re.sub(r"\[\[([Ff]ile.*thumb.*\|)(.*?)\]\]", r"</translate>[[\1<!--X--><translate>\2</translate>]]<translate>",page_text)     # deals with files (not the best way to do it)
    page_text = re.sub(r"\[\[([Ff]ile:.*?[^X].*?)\]\]", r"</translate>[[\1]]<translate>",page_text)                                             # deals with files without thumbs


    regex = re.compile(r"\{\|(.*?)\|\}", re.DOTALL)
    page_text = re.sub(regex, r"</translate>\n{|\1|}\n<translate>",page_text)              # deals with tables

    regexTemplate = re.compile(r"\{\{(.*?)\}\}", re.DOTALL)
    page_text = re.sub(regexTemplate, r"</translate>\n{{\1}}\n<translate>",page_text)     # deals with templates

    page_text = re.sub(r"\[\[([Cc]ategory.*?)\]\]", r"</translate>[[\1]]<translate>",page_text)     # deals with Categories

    page_text = re.sub(r"__(.*?)__", r"</translate>__\1__<translate>",page_text)     # deals with Magic Words



    page_text = re.sub(r"\n\n\}\}", r"\n}}",page_text)     # deals with templates
    page_text = re.sub(r"\n\n\|", r"\n|",page_text)     # deals with templates


    page_text = re.sub(r"<translate>(\n*?)</translate>", r"\1",page_text)               # deals with redundunt tags
    page_text = page_text.replace(u"<!--X-->", u"")                                     # removes marks from thumb files



    wikipedia.output("S0")

    OutTitle =  u"User:Haithams/" + title
    OutPage = wikipedia.Page(self.site, OutTitle)
    wikipedia.output("S1")

    summary = u"Test - Translation tags"
    OutPage.put(page_text, summary)
    wikipedia.output("S2")

if __name__ == '__main__':
  try:
    bot = TranslateBot()
    bot.addTranslate()
  finally:
    wikipedia.stopme()

