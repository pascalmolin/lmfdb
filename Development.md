Conventions
===========

Template
--------

A template has several variables:
 * title - that appears on several places
 * properties - right hand bar, see below
 * bread - breadcumb hierarchy, i.e. [ ('name', 'url'), ... ]
 * sidebar - additional sidebar entries, datastructure is
   [ ('topic', [ ('text', 'url'), ...]), ... ]
   ** info.downloads, info.friends, info.learnmore have the same strucutre,
      names might change sometimes.
 * credit - small credits note at the bottom
 * support - either a default or a line that says who has supported this. 

For more details read templates/homepage.html


The idea is to extend "homepage.html" and replace the content block:
{% block content %}
   ... your stuff ...
{% endblock %}


Code Organization / Blueprints
------------------------------

Each part of the website should be a Python module [1] and a
proper flask Blueprint [2]. Look at how /knowledge/ is done,
especially knowledge/__init__.py and knowledge/main.py. 
Also, templates and static files specific to the module
should be in their respective "templates" and "static"
folders, e.g. /knowledge/templates/. 

[1] http://docs.python.org/tutorial/modules.html
[2] http://flask.pocoo.org/docs/blueprints/

Basic Orga / Editorial Board
----------------------------

Behind the Scenes:
 * Backend: Harald Schilly
 * Server: Jonathan Bober
 * Data Management: Ralf Furmaniak

Sections:
 * Hilbert MF: John Voight
 * Elliptic Curves: John Cremona
 * L-functions: Stefan Lemurell
 * Siegeld MF: Nils Skoruppa
 * Elliptic MFs: Nathan Ryan
 * Maass Fs: Fredrik Stromberg
 * Number Fields / Galois Groups: John Jones
 * Artin Repos: Paul-Olivier Dehaye
 * Dirichlet Characters: Pascal Molin
 * Zeroes: Jonathan Bober

Code Attribution
----------------
Each file should begin with a short copyright information,
mentioning the people who are mainly involved in coding
this particular python file. 

Pro Tipp: Debugging
-------------------
Just add

  import pdb; pdb.set_trace()

somewhere (e.g. protected inside a sensible if) this magic
line and you will end up inside the interactive python
debugger. there, you can check for the local variables with dir()
you can execute python code (e.g. to introspect objects)
and use "pp <var name>" to pretty print variables and 
to continue executing code use the "n" command.
When you get lost, the command "bt" shows you exactly where you
are and "up" helps you to get on step up on the stack.
Of course, "help [<command>]" will tell you more...

Git Tipps
=========

```
[alias]
        st=status
        aliases=!git config --get-regexp 'alias.*' | colrm 1 6 | sed 's/[ ]/ = /'
        ci=commit
        br=branch
        co=checkout
        df=diff
        who=shortlog -s --
        ll = log --oneline --graph --decorate -25
        lla = log --oneline --graph --decorate --all -25
        wdiff=diff --word-diff=color
[color]
    ui = auto
    branch = auto
    diff = auto
    interactive = auto
    status = auto
```

List-table should always be like
--------------------------------

<table class="ntdata">
  <thead><tr><td>...</td></tr></thead>

  <tbody>
   <tr class="odd"> <td>...</td></tr>
   <tr class="even"><td>...</td></tr>
   <tr class="odd"> <td>...</td></tr>
   ...
  </tbody>
</table>

... we might also switch to CSS3's nth-element selector and forget about this.

Properties
----------
the table on the right renders Strings formatted in the following datastructure:
prop = [ ( '<description>', [ '<value 1>', '<value 2>', ...] ), ... ]
or
prop = [ ( '<description>', '<value>'), ('<description>', '<value>'), ... ]
you can mix list or non-list.

LaTeX Macros
------------

The following extra macros may be used in LaTeX on the site:
  \Z for the rational integers
  \Q for the rational numbers
  \R for the real numbers
  \C for the complex numbers
  \F for finite fields, as in $\F_5$
Each produces the corresponding letter in blackboard bold.

One should use the following macros for names of algebraic groups:
  \GL, \SL, \PGL, \PSL, \Sp, \GSp
Each produces the group name in upright font.

The convention for indicating the size is $\GL(2)$ or $\GL(2,\Q)$ where
appropriate instead of $\GL_2$ and $\GL_2(\Q)$.

Mercurial
---------

You can tell Mercurial about your password and nickname other repositories.
Open .hg/hgrc and edit it like this:

[paths]
default = !!! ENTER YOUR URL, https://... !!!
master  = http://lmfdb.googlecode.com/hg
beta = https://code.google.com/r/jwbober-lmfdb-beta

# infrastructure
jonathan = http://jwbober-lmfdb.googlecode.com/hg
harald = http://haraldschilly-content.googlecode.com/hg

# l-functions
stefan = http://sj-lmfdb2.googlecode.com/hg
gagan = http://gagandsekhon-lmdb.googlecode.com/hg

# maass forms
fredrik = http://fredrik314-classicalandmaassforms.googlecode.com/hg

dk = http://dkhuynhms-lmfdb.googlecode.com/hg
cremona = http://johncremona-lmfdb.googlecode.com/hg
voight = http://jvoight-lmfdb.googlecode.com/hg
nils = http://nilsskoruppa-lmfdb.googlecode.com/hg
rishi = http://rishikes-lmfdb.googlecode.com/hg
nathan = http://nathancryan-lmfdb.googlecode.com/hg
sally = http://koutslts-lmfdb.googlecode.com/hg
michael = http://michaelorubinstein-lmfdb.googlecode.com/hg

[auth]
default.username = !!! ENTER YOUR GOOGLE ID EMAIL !!!
default.password = !!! YOUR SPECIAL GOOGLE CODE/PROFILE/SETTINGS PASSWORD !!!

Server Hook
-----------
This is in the `hooks/post-receive` in the bare Git repo:

```
#!/bin/sh
# update the lmfdb-git-beta or -prod server depending on the branc
# this is based on http://stackoverflow.com/a/13057643/54236

restart() {
    echo "updating $1" 
    export GIT_WORK_TREE=/home/lmfdbweb/lmfdb-git-$1
    git checkout $1 -f
    echo 'git HEAD now at' `git rev-parse HEAD`
    bash ~/restart-$1
}

while read oldrev newrev refname
do
    branch=$(git rev-parse --symbolic --abbrev-ref $refname)
    case $branch in
        prod) restart $branch
              ;;

        beta) restart $branch
              ;;
    esac
done
```
