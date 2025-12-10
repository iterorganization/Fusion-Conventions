from plotter import Plotter

# Plotting ITER
dataset = "../../data/iter-md-magnetics_geom_container.nc"
plotter_iter = Plotter(dataset)
plotter_iter.add("b_field_pol_probe.field.data")
plotter_iter.add("b_field_phi_probe.field.data")
plotter_iter.add("flux_loop.flux")
plotter_iter.show()

# Plotting WEST
dataset = "../../data/west-57929_geom_container.nc"
plotter_west = Plotter(dataset)
plotter_west.add("b_field_pol_probe.field.data")
plotter_west.add("b_field_tor_probe.field.data")
plotter_west.add("flux_loop.flux")
plotter_west.show()
