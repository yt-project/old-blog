Particle Generators
===================


`Notebook Download <https://hub.yt-project.org/go/i483hp>`_


In[1]:

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

In[2]:

.. sourcecode:: python

    domain_dims = (128, 128, 128)
    dens = 0.1*np.random.random(domain_dims)
    fields = {"Density": dens}
    ug = load_uniform_grid(fields, domain_dims, 1.0)

.. parsed-literal::

    yt : [INFO     ] 2012-12-13 02:55:15,381 Parameters: current_time              = 0.0
    yt : [INFO     ] 2012-12-13 02:55:15,381 Parameters: domain_dimensions         = [128 128 128]
    yt : [INFO     ] 2012-12-13 02:55:15,382 Parameters: domain_left_edge          = [ 0.  0.  0.]
    yt : [INFO     ] 2012-12-13 02:55:15,383 Parameters: domain_right_edge         = [ 1.  1.  1.]
    yt : [INFO     ] 2012-12-13 02:55:15,383 Parameters: cosmological_simulation   = 0.0
    yt : [INFO     ] 2012-12-13 02:55:15,384 Parameters: current_time              = 0.0
    yt : [INFO     ] 2012-12-13 02:55:15,384 Parameters: domain_dimensions         = [128 128 128]
    yt : [INFO     ] 2012-12-13 02:55:15,385 Parameters: domain_left_edge          = [ 0.  0.  0.]
    yt : [INFO     ] 2012-12-13 02:55:15,385 Parameters: domain_right_edge         = [ 1.  1.  1.]
    yt : [INFO     ] 2012-12-13 02:55:15,386 Parameters: cosmological_simulation   = 0.0


In[3]:

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

    yt : [INFO     ] 2012-12-13 02:55:15,397 Adding Density to list of fields
    yt : [INFO     ] 2012-12-13 02:55:15,400 Adding particle_position_z to list of fields
    yt : [INFO     ] 2012-12-13 02:55:15,401 Adding particle_index to list of fields
    yt : [INFO     ] 2012-12-13 02:55:15,401 Adding particle_position_x to list of fields
    yt : [INFO     ] 2012-12-13 02:55:15,402 Adding particle_position_y to list of fields


In[4]:

.. sourcecode:: python

    slc = SlicePlot(ug, 2, ["Density"], center=ug.domain_center)
    slc.set_cmap("Density","spring")
    slc.annotate_particles(0.2, p_size=10.0)
    slc.show()

.. parsed-literal::

    yt : [INFO     ] 2012-12-13 02:55:15,433 xlim = 0.000000 1.000000
    yt : [INFO     ] 2012-12-13 02:55:15,433 ylim = 0.000000 1.000000
    yt : [INFO     ] 2012-12-13 02:55:15,434 Making a fixed resolution buffer of (Density) 800 by 800
    yt : [INFO     ] 2012-12-13 02:55:15,442 xlim = 0.000000 1.000000
    yt : [INFO     ] 2012-12-13 02:55:15,443 ylim = 0.000000 1.000000
    yt : [INFO     ] 2012-12-13 02:55:15,445 Making a fixed resolution buffer of (Density) 800 by 800
    yt : [INFO     ] 2012-12-13 02:55:15,455 Making a fixed resolution buffer of (Density) 800 by 800
    yt : [INFO     ] 2012-12-13 02:55:16,493 Getting field particle_position_x from 1
    yt : [INFO     ] 2012-12-13 02:55:16,517 Getting field particle_position_y from 1


.. attachment-image:: ParticleGenerator_files/ParticleGenerator_ipynb_fig_00.png

In[5]:

.. sourcecode:: python

    pdims = np.array([10,10,10])
    ple = np.array([0.6,0.6,0.6])
    pre = np.array([0.9,0.9,0.9])
    particles2 = LatticeParticleGenerator(ug, pdims, ple, pre, field_list)
    particles2.assign_indices(function=add_indices, npart=np.product(pdims),
                              start_num=num_particles1)
    particles2.apply_to_stream()

.. parsed-literal::

    yt : [INFO     ] 2012-12-13 02:55:17,222 Adding particle_gas_density to list of fields


In[6]:

.. sourcecode:: python

    slc = SlicePlot(ug, 2, ["Density"], center=ug.domain_center)
    slc.set_cmap("Density","spring")
    slc.annotate_particles(0.2, p_size=10.0)
    slc.show()

.. parsed-literal::

    yt : [INFO     ] 2012-12-13 02:55:17,244 xlim = 0.000000 1.000000
    yt : [INFO     ] 2012-12-13 02:55:17,245 ylim = 0.000000 1.000000
    yt : [INFO     ] 2012-12-13 02:55:17,245 Making a fixed resolution buffer of (Density) 800 by 800
    yt : [INFO     ] 2012-12-13 02:55:17,254 xlim = 0.000000 1.000000
    yt : [INFO     ] 2012-12-13 02:55:17,254 ylim = 0.000000 1.000000
    yt : [INFO     ] 2012-12-13 02:55:17,257 Making a fixed resolution buffer of (Density) 800 by 800
    yt : [INFO     ] 2012-12-13 02:55:17,267 Making a fixed resolution buffer of (Density) 800 by 800
    yt : [INFO     ] 2012-12-13 02:55:18,032 Getting field particle_position_x from 1
    yt : [INFO     ] 2012-12-13 02:55:18,057 Getting field particle_position_y from 1


.. attachment-image:: ParticleGenerator_files/ParticleGenerator_ipynb_fig_01.png

In[7]:

.. sourcecode:: python

    indices = np.sort(np.int32(ug.h.all_data()["particle_index"]))
    print "All indices unique = ", np.all(np.unique(indices) == indices)

.. parsed-literal::

    yt : [INFO     ] 2012-12-13 02:55:18,817 Getting field particle_index from 1


.. parsed-literal::

    All indices unique =  True


In[8]:

.. sourcecode:: python

    fo = [ic.BetaModelSphere(1.0,0.1,0.5,[0.5,0.5,0.5],{"Density":(10.0)})]
    rc = [fm.flagging_method_registry["overdensity"](4.0)]
    pf = refine_amr(ug, rc, fo, 3)

.. parsed-literal::

    yt : [INFO     ] 2012-12-13 02:55:18,824 Refining another level.  Current max level: 0
    yt : [INFO     ] 2012-12-13 02:55:20,011 Parameters: current_time              = 0.0
    yt : [INFO     ] 2012-12-13 02:55:20,012 Parameters: domain_dimensions         = [128 128 128]
    yt : [INFO     ] 2012-12-13 02:55:20,012 Parameters: domain_left_edge          = [ 0.  0.  0.]
    yt : [INFO     ] 2012-12-13 02:55:20,013 Parameters: domain_right_edge         = [ 1.  1.  1.]
    yt : [INFO     ] 2012-12-13 02:55:20,014 Parameters: cosmological_simulation   = 0.0
    yt : [INFO     ] 2012-12-13 02:55:20,014 Parameters: current_time              = 0.0
    yt : [INFO     ] 2012-12-13 02:55:20,015 Parameters: domain_dimensions         = [128 128 128]
    yt : [INFO     ] 2012-12-13 02:55:20,015 Parameters: domain_left_edge          = [ 0.  0.  0.]
    yt : [INFO     ] 2012-12-13 02:55:20,016 Parameters: domain_right_edge         = [ 1.  1.  1.]
    yt : [INFO     ] 2012-12-13 02:55:20,016 Parameters: cosmological_simulation   = 0.0
    yt : [INFO     ] 2012-12-13 02:55:20,018 Adding Density to list of fields
    yt : [INFO     ] 2012-12-13 02:55:20,019 Refining another level.  Current max level: 1
    yt : [INFO     ] 2012-12-13 02:55:20,583 Parameters: current_time              = 0.0
    yt : [INFO     ] 2012-12-13 02:55:20,584 Parameters: domain_dimensions         = [128 128 128]
    yt : [INFO     ] 2012-12-13 02:55:20,584 Parameters: domain_left_edge          = [ 0.  0.  0.]
    yt : [INFO     ] 2012-12-13 02:55:20,585 Parameters: domain_right_edge         = [ 1.  1.  1.]
    yt : [INFO     ] 2012-12-13 02:55:20,586 Parameters: cosmological_simulation   = 0.0
    yt : [INFO     ] 2012-12-13 02:55:20,586 Parameters: current_time              = 0.0
    yt : [INFO     ] 2012-12-13 02:55:20,587 Parameters: domain_dimensions         = [128 128 128]
    yt : [INFO     ] 2012-12-13 02:55:20,587 Parameters: domain_left_edge          = [ 0.  0.  0.]
    yt : [INFO     ] 2012-12-13 02:55:20,588 Parameters: domain_right_edge         = [ 1.  1.  1.]
    yt : [INFO     ] 2012-12-13 02:55:20,588 Parameters: cosmological_simulation   = 0.0
    yt : [INFO     ] 2012-12-13 02:55:20,590 Adding Density to list of fields
    yt : [INFO     ] 2012-12-13 02:55:20,591 Refining another level.  Current max level: 2
    yt : [INFO     ] 2012-12-13 02:55:21,147 Parameters: current_time              = 0.0
    yt : [INFO     ] 2012-12-13 02:55:21,148 Parameters: domain_dimensions         = [128 128 128]
    yt : [INFO     ] 2012-12-13 02:55:21,148 Parameters: domain_left_edge          = [ 0.  0.  0.]
    yt : [INFO     ] 2012-12-13 02:55:21,149 Parameters: domain_right_edge         = [ 1.  1.  1.]
    yt : [INFO     ] 2012-12-13 02:55:21,150 Parameters: cosmological_simulation   = 0.0
    yt : [INFO     ] 2012-12-13 02:55:21,150 Parameters: current_time              = 0.0
    yt : [INFO     ] 2012-12-13 02:55:21,150 Parameters: domain_dimensions         = [128 128 128]
    yt : [INFO     ] 2012-12-13 02:55:21,151 Parameters: domain_left_edge          = [ 0.  0.  0.]
    yt : [INFO     ] 2012-12-13 02:55:21,151 Parameters: domain_right_edge         = [ 1.  1.  1.]
    yt : [INFO     ] 2012-12-13 02:55:21,152 Parameters: cosmological_simulation   = 0.0
    yt : [INFO     ] 2012-12-13 02:55:21,165 Adding Density to list of fields
    yt : [INFO     ] 2012-12-13 02:55:21,169 Adding particle_position_z to list of fields
    yt : [INFO     ] 2012-12-13 02:55:21,170 Adding particle_position_x to list of fields
    yt : [INFO     ] 2012-12-13 02:55:21,170 Adding particle_position_y to list of fields
    yt : [INFO     ] 2012-12-13 02:55:21,171 Adding particle_index to list of fields
    yt : [INFO     ] 2012-12-13 02:55:21,171 Adding particle_gas_density to list of fields


In[9]:

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

    yt : [INFO     ] 2012-12-13 02:55:21,239 Getting field x from 3
    yt : [INFO     ] 2012-12-13 02:55:21,689 Getting field Density from 3
    yt : [INFO     ] 2012-12-13 02:55:21,817 Getting field dx from 3
    yt : [INFO     ] 2012-12-13 02:55:21,954 Getting field dy from 3
    yt : [INFO     ] 2012-12-13 02:55:22,110 Getting field dz from 3
    yt : [INFO     ] 2012-12-13 02:55:22,296 Getting field dx from 3
    yt : [INFO     ] 2012-12-13 02:55:22,472 Getting field y from 3
    yt : [INFO     ] 2012-12-13 02:55:22,594 Getting field dy from 3
    yt : [INFO     ] 2012-12-13 02:55:22,777 Getting field z from 3
    yt : [INFO     ] 2012-12-13 02:55:22,904 Getting field dz from 3


In[10]:

.. sourcecode:: python

    slc = SlicePlot(pf, 2, ["Density","ParticleGasDensity"], center=pf.domain_center)
    slc.set_log("Density", True)
    slc.set_log("ParticleGasDensity", True)
    slc.set_cmap("all", "spring")
    slc.annotate_grids()
    slc.annotate_particles(0.01,p_size=3)
    slc.show()

.. parsed-literal::

    yt : [INFO     ] 2012-12-13 02:55:24,319 xlim = 0.000000 1.000000
    yt : [INFO     ] 2012-12-13 02:55:24,319 ylim = 0.000000 1.000000
    yt : [INFO     ] 2012-12-13 02:55:24,320 Making a fixed resolution buffer of (Density) 800 by 800
    yt : [INFO     ] 2012-12-13 02:55:24,328 Making a fixed resolution buffer of (ParticleGasDensity) 800 by 800
    yt : [INFO     ] 2012-12-13 02:55:24,339 xlim = 0.000000 1.000000
    yt : [INFO     ] 2012-12-13 02:55:24,340 ylim = 0.000000 1.000000
    yt : [INFO     ] 2012-12-13 02:55:24,342 Making a fixed resolution buffer of (ParticleGasDensity) 800 by 800
    yt : [INFO     ] 2012-12-13 02:55:24,351 Making a fixed resolution buffer of (Density) 800 by 800
    yt : [INFO     ] 2012-12-13 02:55:24,362 Making a fixed resolution buffer of (ParticleGasDensity) 800 by 800
    yt : [INFO     ] 2012-12-13 02:55:24,371 Making a fixed resolution buffer of (Density) 800 by 800
    yt : [INFO     ] 2012-12-13 02:55:27,080 Getting field particle_position_x from 3
    yt : [INFO     ] 2012-12-13 02:55:27,206 Getting field particle_position_y from 3
    yt : [INFO     ] 2012-12-13 02:55:27,572 Getting field particle_position_x from 3
    yt : [INFO     ] 2012-12-13 02:55:27,696 Getting field particle_position_y from 3


.. attachment-image:: ParticleGenerator_files/ParticleGenerator_ipynb_fig_02.png

.. attachment-image:: ParticleGenerator_files/ParticleGenerator_ipynb_fig_03.png

