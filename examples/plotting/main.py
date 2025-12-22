from plotter import Plotter

# ITER

## Magnetics
iter_magnetics = Plotter("../../data/ITER/iter-md-magnetics_geom_container.nc")
iter_magnetics.add("b_field_pol_probe.field.data")
iter_magnetics.add("b_field_phi_probe.field.data")
iter_magnetics.add("flux_loop.flux")
iter_magnetics.show()

## PF Active
iter_pf_active = Plotter("../../data/ITER/iter-pf-active-111001_geom_container.nc")
iter_pf_active.add("coil.resistance", num_phi=30, max_phi=360)
iter_pf_active.show()

#  WEST
plotter_west = Plotter("../../data/WEST/west-57929_geom_container.nc")
plotter_west.add("b_field_pol_probe.field.data")
plotter_west.add("b_field_tor_probe.field.data")
plotter_west.add("flux_loop.flux", num_phi=20, max_phi=270)
plotter_west.show()
