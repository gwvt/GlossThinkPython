#Gloss Think Python#

...as in, three verbs in a row.

After working through Allen Downey's excellent book _Think Python_, I wanted to build a tool to navigate the glossaries at the end of each chapter for reference and as a way to review concepts.

Here's a summary of the files:

* _GlossThinkPython-create-db.py_: scrapes the (open-license) HTML version of the book at <http://greenteapress.com/wp/think-python-2e/> and creates a SQLite database with columns for term, gloss, chapter, and order in chapter.
* _GlossThinkPython-db.sqlite_: The SQLite file created by the above script. Place in folder with _GlossThinkPython-main.py_ (or set absolute path).
* _GlossThinkPython-main.py_: presents a Tkinter GUI to navigate the database by search, listing by alphabetical order, and listing by chapter.

This was fun to build, and now nice to pull up when I'm working on Python... maybe others will find it useful.
