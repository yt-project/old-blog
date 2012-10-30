Simple Grid Refinement.ipynb
============================


`Notebook Download <https://hub.yt-project.org/go/65ik8c>`_


Grid refinement
---------------

In yt, you can now generate very simple initial conditions:

In[1]:

.. sourcecode:: python

    from yt.mods import *
    from yt.frontends.stream.api import load_uniform_grid
    from yt.frontends.gdf.api import *
    from yt.utilities.grid_data_format.writer import write_to_gdf
    
    class DataModifier(object):
        pass
    
    class TophatSphere(DataModifier):
        def __init__(self, fields, radius, center):
            self.fields = fields
            self.radius = radius
            self.center = center
        
        def apply(self, grid, container):
            r = ((grid['x'] - self.center[0])**2.0
             +   (grid['y'] - self.center[1])**2.0
             +   (grid['z'] - self.center[2])**2.0)**0.5
            for field in self.fields:
                grid[field][r < self.radius] = self.fields[field]
    
    data = na.random.random((256, 256, 256))
    ug = load_uniform_grid({'Density': data}, [256, 256, 256], 1.0)

.. parsed-literal::

    yt : [INFO     ] 2012-10-30 18:11:48,715 Loading plugins from /home/mturk/.yt/my_plugins.py
    yt : [INFO     ] 2012-10-30 18:11:49,025 Parameters: current_time              = 0.0
    yt : [INFO     ] 2012-10-30 18:11:49,026 Parameters: domain_dimensions         = [256 256 256]
    yt : [INFO     ] 2012-10-30 18:11:49,026 Parameters: domain_left_edge          = [ 0.  0.  0.]
    yt : [INFO     ] 2012-10-30 18:11:49,027 Parameters: domain_right_edge         = [ 1.  1.  1.]
    yt : [INFO     ] 2012-10-30 18:11:49,028 Parameters: cosmological_simulation   = 0.0
    yt : [INFO     ] 2012-10-30 18:11:49,028 Parameters: current_time              = 0.0
    yt : [INFO     ] 2012-10-30 18:11:49,028 Parameters: domain_dimensions         = [256 256 256]
    yt : [INFO     ] 2012-10-30 18:11:49,029 Parameters: domain_left_edge          = [ 0.  0.  0.]
    yt : [INFO     ] 2012-10-30 18:11:49,029 Parameters: domain_right_edge         = [ 1.  1.  1.]
    yt : [INFO     ] 2012-10-30 18:11:49,030 Parameters: cosmological_simulation   = 0.0


In[2]:

.. sourcecode:: python

    spheres = []
    spheres.append(TophatSphere({"Density": 2.0}, 0.1, [0.2,0.3,0.4]))
    spheres.append(TophatSphere({"Density": 20.0}, 0.05, [0.7,0.4,0.75]))
    for sp in spheres: sp.apply(ug.h.grids[0], ug)

.. parsed-literal::

    yt : [INFO     ] 2012-10-30 18:11:49,035 Adding Density to list of fields


In[3]:

.. sourcecode:: python

    p = ProjectionPlot(ug, "x", "Density")
    p.show()

.. parsed-literal::

    Initializing tree  0 /  0  0% |                               | ETA:  --:--:-- 
    Initializing tree  0 /  0100% ||||||||||||||||||||||||||||||||| Time: 00:00:00 
    Projecting  level  0 /  0   0% |                              | ETA:  --:--:-- 
    Projecting  level  0 /  0 100% |||||||||||||||||||||||||||||||| Time: 00:00:01 
    yt : [INFO     ] 2012-10-30 18:11:53,889 Projection completed
    yt : [INFO     ] 2012-10-30 18:11:53,894 xlim = 0.000000 1.000000
    yt : [INFO     ] 2012-10-30 18:11:53,894 ylim = 0.000000 1.000000
    yt : [INFO     ] 2012-10-30 18:11:53,895 Making a fixed resolution buffer of (Density) 800 by 800
    yt : [INFO     ] 2012-10-30 18:11:53,914 xlim = 0.000000 1.000000
    yt : [INFO     ] 2012-10-30 18:11:53,915 ylim = 0.000000 1.000000
    yt : [INFO     ] 2012-10-30 18:11:53,915 Making a fixed resolution buffer of (Density) 800 by 800
    yt : [INFO     ] 2012-10-30 18:11:53,934 Making a fixed resolution buffer of (Density) 800 by 800


.. attachment-image:: Simple_Grid_Refinement_files/Simple_Grid_Refinement_fig_00.png

We can even save them out to disk!

In[4]:

.. sourcecode:: python

    !rm /home/mturk/test.gdf

In[5]:

.. sourcecode:: python

    write_to_gdf(ug, "/home/mturk/test.gdf")

In[6]:

.. sourcecode:: python

    pf = GDFStaticOutput("/home/mturk/test.gdf")

.. parsed-literal::

    yt : [INFO     ] 2012-10-30 18:11:56,370 Parameters: current_time              = 0.0
    yt : [INFO     ] 2012-10-30 18:11:56,371 Parameters: domain_dimensions         = [256 256 256]
    yt : [INFO     ] 2012-10-30 18:11:56,371 Parameters: domain_left_edge          = [ 0.  0.  0.]
    yt : [INFO     ] 2012-10-30 18:11:56,372 Parameters: domain_right_edge         = [ 1.  1.  1.]
    yt : [INFO     ] 2012-10-30 18:11:56,373 Parameters: cosmological_simulation   = 0.0


In[7]:

.. sourcecode:: python

    p2 = ProjectionPlot(pf, "x", "Density")
    p2.show()

.. parsed-literal::

    Initializing tree  0 /  0  0% |                               | ETA:  --:--:-- 
    Initializing tree  0 /  0100% ||||||||||||||||||||||||||||||||| Time: 00:00:00 
    Projecting  level  0 /  0   0% |                              | ETA:  --:--:-- 
    Projecting  level  0 /  0 100% |||||||||||||||||||||||||||||||| Time: 00:00:01 
    yt : [INFO     ] 2012-10-30 18:11:57,908 Projection completed
    yt : [INFO     ] 2012-10-30 18:11:57,914 xlim = 0.000000 1.000000
    yt : [INFO     ] 2012-10-30 18:11:57,914 ylim = 0.000000 1.000000
    yt : [INFO     ] 2012-10-30 18:11:57,915 Making a fixed resolution buffer of (Density) 800 by 800
    yt : [INFO     ] 2012-10-30 18:11:57,934 xlim = 0.000000 1.000000
    yt : [INFO     ] 2012-10-30 18:11:57,935 ylim = 0.000000 1.000000
    yt : [INFO     ] 2012-10-30 18:11:57,935 Making a fixed resolution buffer of (Density) 800 by 800
    yt : [INFO     ] 2012-10-30 18:11:57,954 Making a fixed resolution buffer of (Density) 800 by 800


.. attachment-image:: Simple_Grid_Refinement_files/Simple_Grid_Refinement_fig_01.png

Over time, this functionality will expand to include cell-flagging,
refinement, and much more interesting modifications to grid values.
