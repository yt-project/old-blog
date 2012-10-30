Enzo 2.0 and Inline yt
======================

.. author: Matthew Turk <matthewturk@gmail.com>

.. date: 1285895136

Enzo 2.0 has just been released to its new `Google Code website
<http://enzo.googlecode.com/>`_.  This release features preliminary support for
inline Python analysis, using yt.

In the Enzo documentation there's a `brief
section <http://docs.enzo.googlecode.com/hg/user_guide/EmbeddedPython.html>`_ on
how to use yt for inline analysis.  As it stands, many features are not fully
functional, but things like phase plots, profiles, derived quantities and slices
all work.  This functionality is currently untested at large (> 128)
processors, but for small runs -- particularly debugging runs! -- it works
nicely.  (Projections do not work yet, `but they will <http://blog.enzotools.org
/quad-tree-projections>`_.) 

Email the mailing list or leave a comment here if you run into any trouble, or
if you want to share success stories!

