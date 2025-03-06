# Fusion Conventions

## Abstract

This document describes the Fusion Conventions for storing nuclear fusion data
(modeling and/or experimental) as labeled N-dimensional arrays. The conventions
define metadata that provide a definitive description of waht the data in each
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

TODO


