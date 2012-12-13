Particle Generators
===================


`Notebook Download <https://hub.yt-project.org/go/5o6k23>`_


In[12]:

.. sourcecode:: python

    from yt.mods import *
    from yt.utilities.particle_generator import *
    import yt.utilities.initial_conditions as ic
    import yt.utilities.flagging_methods as fm
    from yt.frontends.stream.api import refine_amr
    from yt.utilities.lib import CICDeposit_3
    
    def _pgdensity(field, data):
        blank = np.zeros(data.ActiveDimensions, dtype='float32')
        if data.NumberOfParticles == 0: return blank
        CICDeposit_3(data["particle_position_x"].astype(np.float64),
                     data["particle_position_y"].astype(np.float64),
                     data["particle_position_z"].astype(np.float64),
                     data["particle_gas_density"].astype(np.float32),
                     np.int64(data.NumberOfParticles),
                     blank, np.array(data.LeftEdge).astype(np.float64),
                     np.array(data.ActiveDimensions).astype(np.int32),
                     np.float64(data['dx']))
        return blank
    add_field("ParticleGasDensity", function=_pgdensity,
              validators=[ValidateGridType()], 
              display_name=r"$\mathrm{Particle}\/\mathrm{Gas}\/\mathrm{Density}$")
    
    def add_indices(npart, start_num) :
        return np.arange((npart)) + start_num

In[13]:

.. sourcecode:: python

    domain_dims = (128, 128, 128)
    dens = 0.1*np.random.random(domain_dims)
    fields = {"Density": dens}
    ug = load_uniform_grid(fields, domain_dims, 1.0)

.. parsed-literal::

    yt : [INFO     ] 2012-12-13 01:14:20,032 Parameters: current_time              = 0.0
    yt : [INFO     ] 2012-12-13 01:14:20,033 Parameters: domain_dimensions         = [128 128 128]
    yt : [INFO     ] 2012-12-13 01:14:20,033 Parameters: domain_left_edge          = [ 0.  0.  0.]
    yt : [INFO     ] 2012-12-13 01:14:20,034 Parameters: domain_right_edge         = [ 1.  1.  1.]
    yt : [INFO     ] 2012-12-13 01:14:20,035 Parameters: cosmological_simulation   = 0.0
    yt : [INFO     ] 2012-12-13 01:14:20,035 Parameters: current_time              = 0.0
    yt : [INFO     ] 2012-12-13 01:14:20,035 Parameters: domain_dimensions         = [128 128 128]
    yt : [INFO     ] 2012-12-13 01:14:20,036 Parameters: domain_left_edge          = [ 0.  0.  0.]
    yt : [INFO     ] 2012-12-13 01:14:20,037 Parameters: domain_right_edge         = [ 1.  1.  1.]
    yt : [INFO     ] 2012-12-13 01:14:20,037 Parameters: cosmological_simulation   = 0.0


In[14]:

.. sourcecode:: python

    num_particles1 = 10000
    field_list = ["particle_position_x","particle_position_y",
                  "particle_position_z","particle_gas_density"]
    x = np.random.uniform(low=0.0, high=0.5, size=num_particles1)
    y = np.random.uniform(low=0.0, high=0.5, size=num_particles1)
    z = np.random.uniform(low=0.0, high=0.5, size=num_particles1)
    pdata = {'particle_position_x':x,
             'particle_position_y':y,
             'particle_position_z':z}
    particles1 = FromListParticleGenerator(ug, num_particles1, pdata)
    particles1.assign_indices()
    particles1.apply_to_stream()

.. parsed-literal::

    yt : [INFO     ] 2012-12-13 01:14:20,048 Adding Density to list of fields
    yt : [INFO     ] 2012-12-13 01:14:20,051 Adding particle_position_z to list of fields
    yt : [INFO     ] 2012-12-13 01:14:20,051 Adding particle_index to list of fields
    yt : [INFO     ] 2012-12-13 01:14:20,052 Adding particle_position_x to list of fields
    yt : [INFO     ] 2012-12-13 01:14:20,052 Adding particle_position_y to list of fields


In[15]:

.. sourcecode:: python

    slc = SlicePlot(ug, 2, ["Density"], center=ug.domain_center)
    slc.set_cmap("Density","spring")
    slc.annotate_particles(0.2, p_size=10.0)
    slc.show()

.. parsed-literal::

    yt : [INFO     ] 2012-12-13 01:14:20,075 xlim = 0.000000 1.000000
    yt : [INFO     ] 2012-12-13 01:14:20,075 ylim = 0.000000 1.000000
    yt : [INFO     ] 2012-12-13 01:14:20,076 Making a fixed resolution buffer of (Density) 800 by 800
    yt : [INFO     ] 2012-12-13 01:14:20,084 xlim = 0.000000 1.000000
    yt : [INFO     ] 2012-12-13 01:14:20,084 ylim = 0.000000 1.000000
    yt : [INFO     ] 2012-12-13 01:14:20,087 Making a fixed resolution buffer of (Density) 800 by 800
    yt : [INFO     ] 2012-12-13 01:14:20,097 Making a fixed resolution buffer of (Density) 800 by 800
    yt : [INFO     ] 2012-12-13 01:14:20,896 Getting field particle_position_x from 1
    yt : [INFO     ] 2012-12-13 01:14:20,921 Getting field particle_position_y from 1


.. attachment-image:: ParticleGenerator_files/ParticleGenerator_ipynb_fig_00.png

In[16]:

.. sourcecode:: python

    pdims = np.array([10,10,10])
    ple = np.array([0.6,0.6,0.6])
    pre = np.array([0.9,0.9,0.9])
    particles2 = LatticeParticleGenerator(ug, pdims, ple, pre, field_list)
    particles2.assign_indices(function=add_indices, npart=np.product(pdims),
                              start_num=num_particles1)
    particles2.apply_to_stream()

.. parsed-literal::

    yt : [INFO     ] 2012-12-13 01:14:21,657 Adding particle_gas_density to list of fields


In[17]:

.. sourcecode:: python

    slc = SlicePlot(ug, 2, ["Density"], center=ug.domain_center)
    slc.set_cmap("Density","spring")
    slc.annotate_particles(0.2, p_size=10.0)
    slc.show()

.. parsed-literal::

    yt : [INFO     ] 2012-12-13 01:14:21,676 xlim = 0.000000 1.000000
    yt : [INFO     ] 2012-12-13 01:14:21,677 ylim = 0.000000 1.000000
    yt : [INFO     ] 2012-12-13 01:14:21,677 Making a fixed resolution buffer of (Density) 800 by 800
    yt : [INFO     ] 2012-12-13 01:14:21,686 xlim = 0.000000 1.000000
    yt : [INFO     ] 2012-12-13 01:14:21,686 ylim = 0.000000 1.000000
    yt : [INFO     ] 2012-12-13 01:14:21,688 Making a fixed resolution buffer of (Density) 800 by 800
    yt : [INFO     ] 2012-12-13 01:14:21,697 Making a fixed resolution buffer of (Density) 800 by 800
    yt : [INFO     ] 2012-12-13 01:14:22,534 Getting field particle_position_x from 1
    yt : [INFO     ] 2012-12-13 01:14:22,559 Getting field particle_position_y from 1


.. attachment-image:: ParticleGenerator_files/ParticleGenerator_ipynb_fig_01.png

In[18]:

.. sourcecode:: python

    indices = np.sort(np.int32(ug.h.all_data()["particle_index"]))
    print "All indices unique = ", np.all(np.unique(indices) == indices)

.. parsed-literal::

    yt : [INFO     ] 2012-12-13 01:14:51,545 Getting field particle_index from 1


.. parsed-literal::

    All indices unique =  True


In[19]:

.. sourcecode:: python

    fo = [ic.BetaModelSphere(1.0,0.1,0.5,[0.5,0.5,0.5],{"Density":(10.0)})]
    rc = [fm.flagging_method_registry["overdensity"](4.0)]
    pf = refine_amr(ug, rc, fo, 3)

.. parsed-literal::

    yt : [INFO     ] 2012-12-13 01:15:12,089 Refining another level.  Current max level: 0
    yt : [INFO     ] 2012-12-13 01:15:13,307 Parameters: current_time              = 0.0
    yt : [INFO     ] 2012-12-13 01:15:13,308 Parameters: domain_dimensions         = [128 128 128]
    yt : [INFO     ] 2012-12-13 01:15:13,308 Parameters: domain_left_edge          = [ 0.  0.  0.]
    yt : [INFO     ] 2012-12-13 01:15:13,309 Parameters: domain_right_edge         = [ 1.  1.  1.]
    yt : [INFO     ] 2012-12-13 01:15:13,310 Parameters: cosmological_simulation   = 0.0
    yt : [INFO     ] 2012-12-13 01:15:13,310 Parameters: current_time              = 0.0
    yt : [INFO     ] 2012-12-13 01:15:13,311 Parameters: domain_dimensions         = [128 128 128]
    yt : [INFO     ] 2012-12-13 01:15:13,311 Parameters: domain_left_edge          = [ 0.  0.  0.]
    yt : [INFO     ] 2012-12-13 01:15:13,312 Parameters: domain_right_edge         = [ 1.  1.  1.]
    yt : [INFO     ] 2012-12-13 01:15:13,313 Parameters: cosmological_simulation   = 0.0
    yt : [INFO     ] 2012-12-13 01:15:13,315 Adding Density to list of fields
    yt : [INFO     ] 2012-12-13 01:15:13,316 Refining another level.  Current max level: 1
    yt : [INFO     ] 2012-12-13 01:15:13,919 Parameters: current_time              = 0.0
    yt : [INFO     ] 2012-12-13 01:15:13,920 Parameters: domain_dimensions         = [128 128 128]
    yt : [INFO     ] 2012-12-13 01:15:13,920 Parameters: domain_left_edge          = [ 0.  0.  0.]
    yt : [INFO     ] 2012-12-13 01:15:13,921 Parameters: domain_right_edge         = [ 1.  1.  1.]
    yt : [INFO     ] 2012-12-13 01:15:13,922 Parameters: cosmological_simulation   = 0.0
    yt : [INFO     ] 2012-12-13 01:15:13,922 Parameters: current_time              = 0.0
    yt : [INFO     ] 2012-12-13 01:15:13,923 Parameters: domain_dimensions         = [128 128 128]
    yt : [INFO     ] 2012-12-13 01:15:13,923 Parameters: domain_left_edge          = [ 0.  0.  0.]
    yt : [INFO     ] 2012-12-13 01:15:13,924 Parameters: domain_right_edge         = [ 1.  1.  1.]
    yt : [INFO     ] 2012-12-13 01:15:13,925 Parameters: cosmological_simulation   = 0.0
    yt : [INFO     ] 2012-12-13 01:15:13,927 Adding Density to list of fields
    yt : [INFO     ] 2012-12-13 01:15:13,928 Refining another level.  Current max level: 2
    yt : [INFO     ] 2012-12-13 01:15:14,521 Parameters: current_time              = 0.0
    yt : [INFO     ] 2012-12-13 01:15:14,521 Parameters: domain_dimensions         = [128 128 128]
    yt : [INFO     ] 2012-12-13 01:15:14,522 Parameters: domain_left_edge          = [ 0.  0.  0.]
    yt : [INFO     ] 2012-12-13 01:15:14,523 Parameters: domain_right_edge         = [ 1.  1.  1.]
    yt : [INFO     ] 2012-12-13 01:15:14,524 Parameters: cosmological_simulation   = 0.0
    yt : [INFO     ] 2012-12-13 01:15:14,524 Parameters: current_time              = 0.0
    yt : [INFO     ] 2012-12-13 01:15:14,524 Parameters: domain_dimensions         = [128 128 128]
    yt : [INFO     ] 2012-12-13 01:15:14,525 Parameters: domain_left_edge          = [ 0.  0.  0.]
    yt : [INFO     ] 2012-12-13 01:15:14,526 Parameters: domain_right_edge         = [ 1.  1.  1.]
    yt : [INFO     ] 2012-12-13 01:15:14,526 Parameters: cosmological_simulation   = 0.0
    yt : [INFO     ] 2012-12-13 01:15:14,539 Adding Density to list of fields
    yt : [INFO     ] 2012-12-13 01:15:14,543 Adding particle_position_z to list of fields
    yt : [INFO     ] 2012-12-13 01:15:14,544 Adding particle_position_x to list of fields
    yt : [INFO     ] 2012-12-13 01:15:14,544 Adding particle_position_y to list of fields
    yt : [INFO     ] 2012-12-13 01:15:14,545 Adding particle_index to list of fields
    yt : [INFO     ] 2012-12-13 01:15:14,545 Adding particle_gas_density to list of fields


In[20]:

.. sourcecode:: python

    num_particles3 = 100000
    map_dict = {"Density": "particle_gas_density"}
    sphere = pf.h.sphere(pf.domain_center, (0.5, "unitary"))
    particles3 = WithDensityParticleGenerator(pf, sphere, num_particles3,
                                              field_list)
    particles3.assign_indices()
    particles3.map_grid_fields_to_particles(map_dict)
    particles3.apply_to_stream(clobber=True)

.. parsed-literal::

    yt : [INFO     ] 2012-12-13 01:15:31,256 Getting field x from 3
    yt : [INFO     ] 2012-12-13 01:15:31,740 Getting field Density from 3
    yt : [INFO     ] 2012-12-13 01:15:31,871 Getting field dx from 3
    yt : [INFO     ] 2012-12-13 01:15:32,012 Getting field dy from 3
    yt : [INFO     ] 2012-12-13 01:15:32,186 Getting field dz from 3
    yt : [INFO     ] 2012-12-13 01:15:32,393 Getting field dx from 3
    yt : [INFO     ] 2012-12-13 01:15:32,571 Getting field y from 3
    yt : [INFO     ] 2012-12-13 01:15:32,694 Getting field dy from 3
    yt : [INFO     ] 2012-12-13 01:15:32,879 Getting field z from 3
    yt : [INFO     ] 2012-12-13 01:15:33,009 Getting field dz from 3


In[21]:

.. sourcecode:: python

    slc = SlicePlot(pf, 2, ["Density","ParticleGasDensity"], center=pf.domain_center)
    slc.set_log("Density", True)
    slc.set_log("ParticleGasDensity", True)
    slc.set_cmap("all", "spring")
    slc.annotate_grids()
    slc.annotate_particles(0.01,p_size=3)
    slc.show()

.. parsed-literal::

    yt : [INFO     ] 2012-12-13 01:15:51,190 xlim = 0.000000 1.000000
    yt : [INFO     ] 2012-12-13 01:15:51,191 ylim = 0.000000 1.000000
    yt : [INFO     ] 2012-12-13 01:15:51,191 Making a fixed resolution buffer of (Density) 800 by 800
    yt : [INFO     ] 2012-12-13 01:15:51,200 Making a fixed resolution buffer of (ParticleGasDensity) 800 by 800
    yt : [INFO     ] 2012-12-13 01:15:51,211 xlim = 0.000000 1.000000
    yt : [INFO     ] 2012-12-13 01:15:51,211 ylim = 0.000000 1.000000
    yt : [INFO     ] 2012-12-13 01:15:51,214 Making a fixed resolution buffer of (ParticleGasDensity) 800 by 800
    yt : [INFO     ] 2012-12-13 01:15:51,222 Making a fixed resolution buffer of (Density) 800 by 800
    yt : [INFO     ] 2012-12-13 01:15:51,234 Making a fixed resolution buffer of (ParticleGasDensity) 800 by 800
    yt : [INFO     ] 2012-12-13 01:15:51,242 Making a fixed resolution buffer of (Density) 800 by 800
    yt : [INFO     ] 2012-12-13 01:15:54,010 Getting field particle_position_x from 3
    yt : [INFO     ] 2012-12-13 01:15:54,138 Getting field particle_position_y from 3
    yt : [INFO     ] 2012-12-13 01:15:54,504 Getting field particle_position_x from 3
    yt : [INFO     ] 2012-12-13 01:15:54,627 Getting field particle_position_y from 3


.. attachment-image:: ParticleGenerator_files/ParticleGenerator_ipynb_fig_02.png

.. attachment-image:: ParticleGenerator_files/ParticleGenerator_ipynb_fig_03.png

