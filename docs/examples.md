# Examples

Below shows some example file structures using the Fusion Conventions. The
descriptions use the [NetCDF Common Data Language
(CDL)](https://docs.unidata.ucar.edu/nug/2.0-draft/cdl.html) to describe
dimensions, variables and metadata.

## Poloidal field coils

The following dataset describes currents and voltages of the active poloidal
field coils in the 2D variables `pf_coil_current` and `pf_coil_voltage`.

This dataset contains two dimensions: `time` (which can be any size) and
`poloidal_field_coil` (which has 16 elements). The `time` dimension represents a
continuous axis, with coordinate values given by the `time` variable. The
`poloidal_field_coil` dimension represents a discrete axis, with labels provided
by the coordinate variable with the same name.


```c++ title="Example dataset for active poloidal field coil data"
netcdf pf_active {
    
dimensions:
    poloidal_field_coil = 16 ;
    time = unlimited ;

variables:
    double time(time) ;
        time:standard_name = "time" ;
        time:units = "s" ;
        time:interface_name = "pf_active/time" ;

    string poloidal_field_coil(poloidal_field_coil) ;
        poloidal_field_coil:standard_name = "poloidal_field_coil" ;
        poloidal_field_coil:interface_name = "pf_active/coil/name" ;
        // Machine description (in IDS format) for these coils:
        poloidal_field_coil:machine_description =
            "imas://uda.iter.org/uda?path=/work/imas/shared/imasdb/ITER_MD/3/111001/4&backend=hdf5" ;

    double pf_coil_current(poloidal_field_coil, time) ;
        pf_coil_current:standard_name = "coil_current" ;
        pf_coil_current:units = "A" ;
        pf_coil_current:interface_name = "pf_active/coil/current/data" ;

    double pf_coil_voltage(poloidal_field_coil, time) ;
        pf_coil_voltage:standard_name = "coil_voltage" ;
        pf_coil_voltage:units = "V" ;
        pf_coil_voltage:interface_name = "pf_active/coil/voltage/data" ;

// Global attributes:
:conventions = "Fusion-0.1" ;

}
```

## 1D plasma profiles

The following dataset describes 1D plasma profiles over time. For brevity, we
only have three profiles: the total plasma pressure (`pressure`), the electron
temperature (`electron_temperature`) and the electron density
(`electron_density`). All variables are 2-dimensional, depending on `time` and
position in the 1D grid. The coordinates (`psi` and `rho_tor_norm`) are
time-dependent, and therefore listed as [Auxiliary
Coordinates](index.md#coordinate-types).

```c++ title="Example dataset for combining 1D profiles from core_profiles and equilibrium"
netcdf profiles_1d {

dimensions:
    grid_psi = 64
    time = unlimited

variables:
    double time(time) ;
        time:standard_name = "time" ;
        time:units = "s" ;
        time:interface_name = "equilibrium/time core_profiles/time" ;

    double psi(time, grid_psi):
        grid_psi:standard_name = "poloidal_flux" ;
        grid_psi:units = "Wb" ;
        grid_psi:interface_name = 
            "equilibrium/time_slice/profiles_1d/psi core_profiles/profiles_1d/grid/psi" ;

    double rho_tor_norm(time, grid_psi):
        rho_tor_norm:standard_name = "normalized_toroidal_flux_coordinate" ;
        rho_tor_norm:units = "1" ;
        rho_tor_norm:interface_name =
            "equilibrium/time_slice/profiles_1d/rho_tor_norm core_profiles/profiles_1d/grid/rho_tor_norm" ;

    double pressure(time, grid_psi):
        pressure:standard_name = "plasma_pressure" ;
        pressure:units = "Pa" ;
        pressure:interface_name = "equilibrium/time_slice/profiles_1d/pressure" ;
        pressure:coordinates = "psi rho_tor_norm" ;

    double electron_temperature(time, grid_psi):
        electron_temperature:standard_name = "electron_temperature" ;
        electron_temperature:units = "eV" ;
        electron_temperature:interface_name = "core_profiles/profiles_1d/electrons/temperature" ;
        electron_temperature:coordinates = "psi rho_tor_norm" ;

    double electron_density(time, grid_psi):
        electron_density:standard_name = "electron_density" ;
        electron_density:units = "m^-3" ;
        electron_density:interface_name = "core_profiles/profiles_1d/electrons/density" ;
        electron_density:coordinates = "psi rho_tor_norm" ;

// Global attributes:
:conventions = "Fusion-0.1" ;

}
```

If the normalized toroidal flux coordinates `rho_tor_norm` are not dependent on
the time, this dataset can be represented as in below code block. Now
`rho_tor_norm` is a 1D coordinate and also the name of the dimension. `psi`
remains an [Auxiliary Coordinate](index.md#coordinate-types).

```c++ title="Example dataset for 1D profiles, with time-independent rho_tor_norm"
netcdf profiles_1d {

dimensions:
    rho_tor_norm = 64
    time = unlimited

variables:
    double time(time) ;
        time:standard_name = "time" ;
        time:units = "s" ;
        time:interface_name = "equilibrium/time core_profiles/time" ;

    double psi(time, rho_tor_norm):
        psi:standard_name = "poloidal_flux" ;
        psi:units = "Wb" ;
        psi:interface_name = 
            "equilibrium/time_slice/profiles_1d/psi core_profiles/profiles_1d/grid/psi" ;

    double rho_tor_norm(rho_tor_norm):
        rho_tor_norm:standard_name = "normalized_toroidal_flux_coordinate" ;
        rho_tor_norm:units = "1" ;
        rho_tor_norm:interface_name =
            "equilibrium/time_slice/profiles_1d/rho_tor_norm core_profiles/profiles_1d/grid/rho_tor_norm" ;

    double pressure(time, rho_tor_norm):
        pressure:standard_name = "plasma_pressure" ;
        pressure:units = "Pa" ;
        pressure:interface_name = "equilibrium/time_slice/profiles_1d/pressure" ;
        pressure:coordinates = "psi" ;

    double electron_temperature(time, rho_tor_norm):
        electron_temperature:standard_name = "electron_temperature" ;
        electron_temperature:units = "eV" ;
        electron_temperature:interface_name = "core_profiles/profiles_1d/electrons/temperature" ;
        electron_temperature:coordinates = "psi" ;

    double electron_density(time, rho_tor_norm):
        electron_density:standard_name = "electron_density" ;
        electron_density:units = "m^-3" ;
        electron_density:interface_name = "core_profiles/profiles_1d/electrons/density" ;
        electron_density:coordinates = "psi" ;

// Global attributes:
:conventions = "Fusion-0.1" ;

}
```

## 2D equilibrium profiles

The following dataset describes 2D equilibrium profiles on a rectangular grid.

```c++ title="Example dataset for 2D profiles on a rectangular grid"
netcdf profiles_1d {

dimensions:
    r = 64
    z = 128
    time = unlimited

variables:
    double time(time) ;
        time:standard_name = "time" ;
        time:units = "s" ;
        time:interface_name = "equilibrium/time" ;

    double r(r) ;
        r:standard_name = "radial_distance" ;
        r:units = "m" ;
        r:interface_name = "equilibrium/time_slice/profiles_2d/grid/dim1" ;

    double z(z) ;
        z:standard_name = "height" ;
        z:units = "m" ;
        z:interface_name = "equilibrium/time_slice/profiles_2d/grid/dim2" ;

    double psi(time, r, z):
        psi:standard_name = "poloidal_flux" ;
        psi:units = "Wb" ;
        psi:interface_name = "equilibrium/time_slice/profiles_2d/psi" ;

    double b_field_r(time, r, z):
        b_field_r:standard_name = "radial_magnetic_field" ;
        b_field_r:units = "T" ;
        b_field_r:interface_name =
            "equilibrium/time_slice/profiles_2d/b_field_r" ;

    double b_field_phi(time, r, z):
        b_field_phi:standard_name = "toroidal_magnetic_field" ;
        b_field_phi:units = "T" ;
        b_field_phi:interface_name =
            "equilibrium/time_slice/profiles_2d/b_field_phi" ;

    double b_field_z(time, r, z):
        b_field_z:standard_name = "vertical_magnetic_field" ;
        b_field_z:units = "T" ;
        b_field_z:interface_name =
            "equilibrium/time_slice/profiles_2d/b_field_z" ;

// Global attributes:
:conventions = "Fusion-0.1" ;

}
```

We can describe the 2D equilibrium profiles on a flux grid as well. Below
example shows a description using Boozer coordinates. Since the values of `psi`
are time-dependent, it is an Auxiliary Coordinate.

```c++ title="Example dataset for 2D profiles on a flux grid (Boozer coordinates)"
netcdf profiles_1d {

dimensions:
    psi_grid = 64
    theta = 64
    time = unlimited

variables:
    double time(time) ;
        time:standard_name = "time" ;
        time:units = "s" ;
        time:interface_name = "equilibrium/time" ;

    double psi(time, psi_grid) ;
        psi:standard_name = "poloidal_flux" ;
        psi:units = "m" ;
        psi:interface_name = "equilibrium/time_slice/profiles_2d/grid/dim1" ;

    double theta(theta) ;
        theta:standard_name = "boozer_theta" ;
        theta:units = "1" ;
        theta:interface_name = "equilibrium/time_slice/profiles_2d/grid/dim2" ;

    double b_field_r(time, psi_grid, theta):
        b_field_r:standard_name = "radial_magnetic_field" ;
        b_field_r:units = "T" ;
        b_field_r:interface_name =
            "equilibrium/time_slice/profiles_2d/b_field_r" ;
        b_field_r:coordinates = "psi" ;

    double b_field_phi(time, psi_grid, theta):
        b_field_phi:standard_name = "toroidal_magnetic_field" ;
        b_field_phi:units = "T" ;
        b_field_phi:interface_name =
            "equilibrium/time_slice/profiles_2d/b_field_phi" ;
        b_field_phi:coordinates = "psi" ;

    double b_field_z(time, psi_grid, theta):
        b_field_z:standard_name = "vertical_magnetic_field" ;
        b_field_z:units = "T" ;
        b_field_z:interface_name =
            "equilibrium/time_slice/profiles_2d/b_field_z" ;
        b_field_z:coordinates = "psi" ;

// Global attributes:
:conventions = "Fusion-0.1" ;

}
```
