OBJ File Exporter for Surfaces
==============================

OBJ and MTL Files
-----------------

If the ability to manuver around an isosurface of your 3D simulation in 
`Sketchfab <http://sketchfab.com>`_ cost you a half a day of work (lets be 
honest, 2 days), prepare to be even less productive.  With a new  `OBJ file
<http://en.wikipedia.org/wiki/Wavefront_.obj_file>`_ exporter, you can now 
upload multiple surfaces of different transparencies in the same file.
The following code snippet produces two files in the current 
directory which contain the vertex info 
(surfaces.obj) and color/transparency info (surfaces.mtl) for a 3D 
galaxy simulation:

.. code-block:: python

   from yt.mods import *
   pf = load("/data/workshop2012/IsolatedGalaxy/galaxy0030/galaxy0030")
   rho = [2e-27, 1e-27]
   trans = [1.0, 0.5]
   filename = './surfaces'
   sphere = pf.h.sphere("max", (1.0, "mpc"))
   for i,r in enumerate(rho):
       surf = pf.h.surface(sphere, 'Density', r)
       surf.export_obj(filename, transparency = trans[i], 
                       color_field='Temperature', plot_index = i)

The calling sequence is fairly similar to the ``export_ply`` function 
`previously used <http://blog.yt-project.org/post/3DSurfacesAndSketchFab.html>`_ 
to export 3D surfaces.  However, one can now specify a transparency for each 
surface of interest and each is ennumerated in the OBJ files with the 
``plot_index``.  This means one could potentially add surfaces to a previously 
created file by setting ``plot_index`` to the number of previously written 
surfaces.  Behold the output of the above script:

.. raw:: html

   <iframe frameborder="0" height="480" width="854" allowFullScreen
   webkitallowfullscreen="true" mozallowfullscreen="true"
   src="http://skfb.ly/5k4j2fdca"></iframe>

One tricky thing: the header of the OBJ file points to the MTL file (with 
the header command ``mtllib``).  This means if you move one or both of the files 
you may have to change the headers to reflect their new directory location.

A Few More Options
------------------

There are a few extra inputs for formatting the surface files you may want to use.
(1) Put max and min of color field, and dist_fac

Uploading to SketchFab
----------------------

put ziping stuff and an example

Importing to MeshLab and Blender
--------------------------------

For meshlab: Put in info about how to trace colors to face.  Mention that transparency 
won't show up.

For blender, mention that now you see colors, and again, transparency doesn't show 
up until render.  

...One More Option
------------------

Mention emissivity, talk about the fact that what we are using is a modified form 
of the OBJ file format to include the emissivity of an object.

Include code snippet.

Mention that blender can use emissivity to do some lighting effects, but you 
have to modify the io_scene_obj reader.  Put where that file is located.

Put in modification code snippet, mention you have to turn on the right lighting 
in blender.  Say a more therow integration of yt and blender is in the works, so 
stay tuned!

