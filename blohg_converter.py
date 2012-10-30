"""
This module creates a converter to the particular ReST format that works best
with the Blohg (blohg.org) blogging engine
"""

import os
import copy
import nbconvert as nb
import argparse
import shutil
from yt.utilities.minimal_representation import MinimalNotebook

class BlohgConverter(nb.ConverterRST):

    def __init__(self, post_name, infile):
        self.infile = infile
        self.infile_dir, infile_root = os.path.split(infile)
        if post_name is None: post_name = infile_root
        self.post_name = post_name
        infile_root = os.path.splitext(infile_root)[0]
        sanitized_root = infile_root.replace(" ", "_")
        files_dir = os.path.join("content", "attachments", sanitized_root + '_files')
        if not os.path.isdir(files_dir):
            os.mkdir(files_dir)
        self.infile_root = sanitized_root
        self.files_dir = files_dir
        self.outbase = os.path.join("content", "post", sanitized_root)
        # Now we copy the entire notebook source over
        outfile = os.path.join("content", "attachments",
                               sanitized_root + ".ipynb")
        shutil.copyfile(self.infile, outfile) # Store a backup here
        mn = MinimalNotebook(self.infile, self.post_name)
        rv = mn.upload()
        self.hub_url = rv['url']

    def render_code(self, cell):
        if not cell.input:
            return []

        lines = ['In[%s]:' % cell.prompt_number, '']
        lines.extend(nb.rst_directive('.. sourcecode:: python', cell.input))

        for output in nb.coalesce_streams(cell.outputs):
            conv_fn = self.dispatch(output.output_type)
            lines.extend(conv_fn(output))

        return lines

    def _img_lines(self, img_file):
        prefix = "content/attachments/"
        if img_file.startswith(prefix):
            img_file = img_file[len(prefix):]
        return ['.. attachment-image:: %s' % img_file, '']

    def optional_header(self):
        header = [self.post_name + "\n" + "=" * len(self.post_name)]
        header += ["", "", "`Notebook Download <%s>`_\n\n" % (self.hub_url)]
        return header

if __name__ == '__main__':
    cwd = os.getcwd()
    if not os.path.exists("content"):
        raise RuntimeError
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs=1)
    parser.add_argument('-p', '--post-name', default=None,
                        dest = "post_name", help="The name of the blog post")
    args = parser.parse_args()
    converter = BlohgConverter(args.post_name, args.infile[0])
    converter.render()
