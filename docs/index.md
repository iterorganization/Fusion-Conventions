# Fusion Conventions

## Abstract

This document describes the Fusion Conventions for storing nuclear fusion data
(modeling and/or experimental) as labeled N-dimensional arrays. The conventions
define metadata that provide a definitive description of what the data in each
variable represents, and of the spatial and temporal properties of the data.
This enables users of data from different sources to decide which quantities are
comparable, and facilitates building applications with powerful extraction,
regridding, and display capabilities.

The Fusion Conventions are inspired by the NetCDF Climate and Forecasting (CF)
Metadata Conventions. However, due to the different characteristics of CF and
Fusion data, these conventions are not a superset of the CF conventions.

These conventions don't specifically target the [netCDF data
format](https://www.unidata.ucar.edu/software/netcdf/). Other ND-array storage
formats that provide labelled dimensions and metadata attributes (such as
[zarr](https://zarr.dev/)) could be used as well.

## Introduction

TODO

## Datasets and Components

TODO

### Data Types

TODO

### Naming Conventions

It is recommended that variable, dimension, attribute and group names begin with
a letter and be composed of letters, digits, and underscores. By the word
_letters_ we mean the standard ASCII letters uppercase `A` to `Z` and lowercase
`a` to `z`. By the word digits we mean the standard ASCII digits `0` to `9`, and
similarly underscores means the standard ASCII underscore `_`.

Case is significant in names, but it is recommended that names should not be
distinguished purely by case. If case is disregarded, no two names should
be the same. It is also recommended that names should be obviously meaningful,
if possible, as this renders the file more effectively self-describing.

This convention does not standardize any variable or dimension names. Attribute
names and their contents, where standardized, are given in English in this
document and should appear in English in conforming datasets for the sake of
portability.

### Dimensions

TODO

### Variables

TODO

### Attributes

TODO

### Groups

TODO / decide if included in conventions

## Description of the Data

TODO

### Units

The `units` attribute is required for all variables that represent dimensional
quantities. The `units` attribute is permitted (with a value of `1`) but not
required for dimensionless quantities.

If a variable has the `standard_name` attribute, the value of `units` _must_
match the units defined by the [standard name](#standard-name). If a variable
does not have a standard name, it must be a string that can be recognized by the
[UDUNITS](https://www.unidata.ucar.edu/software/udunits/) package. It is highly
recommended that the `units` follow the same convention as the IMAS Standard
Names, that is:

- Units are expressed as [Coherent SI
  Units](https://en.wikipedia.org/wiki/International_System_of_Units#Coherent_and_non-coherent_SI_units),
  the atomic mass unit (`u`), elementary charge unit (`e`), electronvolt
  (`eV`) or combinations thereof.
- Derived units are separated by `.` and use `^` for exponents other than 1. For
  example `m.s^-1` (not `m/s`), `ohm.m`, `m^-3`, `m^2.sr`.

### Standard Name

TODO & link to <https://github.com/iterorganization/IMAS-Standard-Names>

### Ancillary Data

TODO (standard error, validity flags, ...)

### Flags

TODO

## Coordinate Types

TODO

## Coordinate Systems and Domain

TODO

## Labels and Alternative Coordinates

### Labels

Character strings can be used to provide a name or label for each element of an
axis. This is particularly useful for discrete axes. For instance, if a data
variable contains time series of current through a number of poloidal field
coils, it may be convenient to provide the names of the coils as labels.

### Alternative Coordinates

In some situations a dimension may have alternative sets of coordinates values.
Since there can only be one coordinate variable for the dimension (the variable
with the same name as the dimension), any alternative sets of values have to be
stored in auxiliary coordinate variables. For such alternative coordinate
variables, there are no mandatory attributes, but they may have any of the
attributes allowed for coordinate variables.
