This is the repository that the yt Project's blog is held in.

How to Add a Blog Entry
=======================

Simply create a new .rst file in ``content/post/``, with the extension
``.rst``.  The file doesn't need to have any prefixes; the old blog entries do
simply because that helped organize them.

Then, submit a pull request.

How to Add an IPython Notebook
==============================

First, download the nbconvert repository from the IPython project.  Place that
directory in your path.

Then, from the root of this blohg directory, run::

   python2.7 blohg_converterer.py --post-name "Your Post Name" /path/to/notebook.ipynb

This will upload a copy of your notebook to the Hub as well as converting it to
ReST, along with all of its attachments.  Then to add it to the blog, with its
files::

   hg ci -A

which will add any new files that are found in the repository's path.

What Manages The Blog
=====================

This blog is managed by the software ``blohg`` ( blohg.org ) which handles
versioning in a mercurial repository.  On top of that, it uses Shining Panda
and Amazon's S3 to automatically publish new entries that get pushed to the
main repository.

How Do I View My Blog Locally
=============================

First, ensure you have blohg installed::

   pip install -U blohg

Once you have committed your new file to the repository, run::

   blohg runserver

and go to the URL it spits out.  This will show you your new blog entry.
