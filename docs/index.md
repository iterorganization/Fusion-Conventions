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

TODO

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

TODO

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
