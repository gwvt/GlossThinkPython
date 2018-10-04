# Gloss Think Python
\* legacy code / my first Python project *

...as in three verbs in a row.

After working through Allen Downey's excellent book _Think Python_, I wanted to build a tool to navigate the glossaries at the end of each chapter for reference and as a way to review concepts.

Here's a summary of the files:

* __GlossThinkPython-create-db.py__: scrapes the (open-license) HTML version of the book at <http://greenteapress.com/wp/think-python-2e/> and creates a SQLite database with columns for term, gloss, chapter, and order in chapter.
* __GlossThinkPython-db.sqlite__: The SQLite file created by the above script. Place in folder with GlossThinkPython-main.py (or set absolute path).
* __GlossThinkPython-main.py__: presents a Tkinter GUI to navigate the database by search, listing by alphabetical order, and listing by chapter.

This was fun to build, and now nice to pull up when I'm working on Python... maybe others will find it useful.

![screenshot](https://github.com/gwvt/GlossThinkPython/blob/master/GlossThinkPython-screenshot.jpg)
