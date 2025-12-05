# [DRAFT] Geometry Descriptions for Fusion Conventions

This document describes how to attach geometric data to a variable in a netCDF
file. For convience, this variable will be referred to as _data_variable_.

The _data_variable_ MUST have an attribute `geometry`. The string-value of this
attribute MUST be equal to the name of a 0 dimensional variable in the data
structure, which we will refer to as the _geometry_container_. Note that
multiple data variables may refer to the same _geometry_container_.

The _geometry_container_ MUST have at least the following two attributes

- `node_coordinates`,
- `geometry_type`.

The string-value of the attribute `node_coordinates` contains the names of the
variables in the data structure that hold the actual geometric data, all
separated by a single space. Each of
these variables must hold an attribute `standard_name`, indicating which
cylindrical coordinate this variable represents. The value of this attribute
MUST differ for each of these variables.

Space coordinates are described using the  cylindrical coordinate system, unless
explicitly specified otherwise.

The attribute `geometry_type` indicates how to interpret the geometric data.
Based on the value of this attribute the _geometry_container_ should have other
attributes as well. Valid values for this attribute are any of the following:

- [`point`](#point)
- [`unit_vector`](#unit_vector)
- [`line`](#line)
- [`polygon`](#polygon)
- [`poloidal_point`](#poloidal_point)
- [`poloidal_line`](#poloidal_line)
- [`poloidal_polygon`](#poloidal_polygon)

## Geometry types

### point

**Use case:**

This geometric type describes points in 3D space. It can be used for
point-measurements of scalar quantities, such as temperature.

**Extra requirements:**

The _geometry_container_ does not need any extra attributes for this geometry type.

Each of the dimensions of the variables mentioned in the attribute
`node_coordinates` of the _geometry_container_ MUST also be a dimension of
_data_variable_.

**Example**

    dimensions:
        b_field_pol_probe = 3;

    variables:
        double field(b_field_pol_probe);
            field:geometry = "some_geometry_container";
        
        int some_geometry_container;
            some_geometry_container:geometry_type = "point";
            some_geometry_container:node_coordinates = "r phi z" ;

        double r(b_field_pol_probe);
            r:standard_name = "_r_axis";

        double phi(b_field_pol_probe);
            phi:standard_name = "_phi_axis";
        
        double z(b_field_pol_probe);
            z:standard_name = "_z_axis";

### unit_vector

**Use case:**

This geometry type is describes unit normal vectors in 3D space. It
can be used for point-measurements of projections of vector quantities, such as
magnetic fields.

**Extra requirements:**

In this case, the geometry_container MUST also have an attribute
`node_orientations`.

The point in space from which this unit vector starts, is described by the 3
variables in `node_coordinates`.

The direction of the unit vector is described by the 2 variables in
`node_orientations`, where the first variable describes the angle between the
normal vector and the phi,z-plane in increasing phi direction, and the
second variable describes the angle between the normal vector and the horizontal
r,z-plane in increasing r direction.

Each of the dimensions of the variables mentioned in the attributes
`node_coordinates` and `node_orientations` of the _geometry_container_ MUST also
be a dimension of _data_variable_.

**Example**

    dimensions:
        b_field_pol_probe = 3;

    variables:
        double field(b_field_pol_probe);
            field:geometry = "some_geometry_container";
        
        int some_geometry_container;
            some_geometry_container:geometry_type = "unit_vector";
            some_geometry_container:node_coordinates = "r phi z" ;
            some_geometry_container:node_orientations = "angle_normal_poloidal angle_normal_toroidal" ;

        double r(b_field_pol_probe);
            r:standard_name = "_r_axis";

        double phi(b_field_pol_probe);
            phi:standard_name = "_phi_axis";
        
        double z(b_field_pol_probe);
            z:standard_name = "_z_axis";

        double angle_normal_poloidal(b_field_pol_probe);

        double angle_normal_toroidal(b_field_pol_probe);

### line

**Use case:**

This geometric type describes connected line segments in 3D space.

**Extra requirements:**

In this case, the _geometry_container_ MUST also have an attribute `node_count`.

The 1D variables described in the attribute `node_coordinates` of the geometry
container MUST have the same dimension, which will be refered to as their _node_
dimension. These 1D variables describe the space coordinates of each 'node'.

The string-value of the attribute `node_count` MUST be the name of an
integer-valued variable in the data structure, where each of its dimensions MUST
also be a dimension of the corresponding variable _data_variable_.

Furthermore, this variable MUST return the number of nodes required to describe
the collection of connected line segments associated with a particular value in
_data_variable_. This number corresponds with the number of consecutive entries
in the 1D variables described in the attribute `node_coordinates`. It follows
that each such numbers SHOULD be greater than 1.

Considering two consecutive nodes, the first node represents the beginning of a
line segment and the second node represents the end of this line segment.

Note: in this manner, only connected line segments can be described since the
last node of one line segment will be considered the start of the next line
segment. For the description of disconnected line segments, see section [Geometries containing Multiple parts](#geometries-containing-multiple-parts)

**Example**

    dimensions:
        device = 3;
        node = 15;
        time = 5;

    variables:
        double field(time, device);
            field:coordinates = "time r phi z";
            field:geometry = "other_geometry_container";
        
        int other_geometry_container ;
            other_geometry_container:geometry_type = "line";
            other_geometry_container:node_count = "some_node_count" ;
            other_geometry_container:node_coordinates = "r phi z" ;

        int some_node_count(device);

        double r(node);
            r:standard_name = "_r_axis";

        double phi(node);
            phi:standard_name = "_phi_axis";
        
        double z(node);
            z:standard_name = "_z_axis";
    data:
        node_count = 5, 4, 6;
        r = 3.57187, 3.57186, 3.57186, 3.57187, 3.57187, 3.57186, 3.57186,
            3.57186, 3.57186, 3.57186, 3.57187, 3.57186, 3.57186, 3.57187,
            3.57187;
        phi = 0.28012534, 0.28012534, 0.83199845, 0.83199845, 0.28012534,
            0.48153634, 0.48153634, 0.83199845, 0.83199845, 0.48153634,
            0.28012534, 0.28012534, 0.83199845, 0.83199845, 0.28012534 ;
        z = -2.54437, -1.64615, -1.64615, -2.54437, -2.54437, -1.64014,
            -0.52663, -0.52663, -1.64014, -1.64014, -0.51662,  0.47974,
            0.47974, -0.51662, -0.51662 ;

### polygon

**Use case:**

This geometric type describes polygons in 3D space.

**Extra requirements:**

The required attributes of this type are exactly the same as with the geometric
type 'line'. The only addition is that for each sequence of nodes, the last node
is assumed to form a connected line segment with the first node. It is allowed
to repeat the first node at the end of this sequence.

**Example**

    dimensions:
        flux_loop = 3;
        node = 15;
        time = 5;

    variables:
        double flux(time, flux_loop);
            flux:standard_name = "_flux_standard_name";
            flux:description = "Measured magnetic flux through loop with normal to enclosed surface determined by order of points";
            flux:units = "Wb";
            flux:coordinates = "time r phi z";
            flux:geometry = "geometry_container";
        
        int geometry_container ;
            geometry_container:geometry_type = "polygon";
            geometry_container:node_count = "node_count" ;
            geometry_container:node_coordinates = "r phi z" ;

        int node_count(flux_loop);

        double r(node);
            r:standard_name = "_major_radius";
            r:description = "Major radius";
            r:units = "m";
            r:standard_name = "_r_axis";

        double phi(node);
            phi:standard_name = "_toroidal_angle";
            phi:description = "Toroidal angle (oriented counter-clockwise when viewing from above)";
            phi:units = "rad";
            phi:standard_name = "_phi_axis";
        
        double z(node);
            z:standard_name = "_height";
            z:description = "Height";
            z:units = "m";
            z:standard_name = "_z_axis";
            
    data:
        time = 0.34, 0.67, 1.0, 1.34, 1.67;
        flux = 
            3.3, 4.1, 5.6, 
            6.8, 7.7, 8.3,
            1.9, 2.0, 3.0, 
            4.7, 5.3, 7.0,
            0.9, 1.6, 7.9 ;
        node_count = 5, 5, 5;
        r = 3.57187, 3.57186, 3.57186, 3.57187, 3.57187, 3.57186, 3.57186,
            3.57186, 3.57186, 3.57186, 3.57187, 3.57186, 3.57186, 3.57187,
            3.57187;
        phi = 0.28012534, 0.28012534, 0.83199845, 0.83199845, 0.28012534,
            0.48153634, 0.48153634, 0.83199845, 0.83199845, 0.48153634,
            0.28012534, 0.28012534, 0.83199845, 0.83199845, 0.28012534 ;
        z = -2.54437, -1.64615, -1.64615, -2.54437, -2.54437, -1.64014,
            -0.52663, -0.52663, -1.64014, -1.64014, -0.51662,  0.47974,
            0.47974, -0.51662, -0.51662 ;

### poloidal_point

**Use case:**

This geometry type is used to describe a full circle, symmetric with respect to
the phi-coordinate. In other words, each point on the circle has the same
r,z-value. Therefore, it is sufficient to describe this circle with a single
point in the r,z-plane.

**Extra requirements:**

The _geometry_container_ does not need any additional attributes.

Each of the dimensions of the variables mentioned in the attribute
`node_coordinates` of the _geometry_container_ MUST also be a dimension of
_data_variable_.

**Example**

    dimensions:
        flux_loop = 3;
        time = 2;

    variables:
        double flux(time, flux_loop);
            flux:geometry = "some_geometry_container";
        
        int some_geometry_container;
            some_geometry_container:geometry_type = "poloidal_point";
            some_geometry_container:node_coordinates = "r z" ;

        double r(flux_loop);
            r:standard_name = "_r_axis";
        
        double z(flux_loop);
            z:standard_name = "_z_axis";
    data:
        flux = 10.4, 10.6, 9.9,
            10.2, 10.4, 9.7;
        r = 3.4, 1.0, 5.8,
            3.4, 1.0, 5.8;
        z = 0.4, 7.7, 8.1,
            0.4, 7.7, 8.1;

### poloidal_line

TO-DO

### poloidal_polygon

TO-DO

## Geometries containing Multiple parts

If the geometry consists of several disconnected parts of the same
`geometry_type`, then the _geometry_container_ MUST contain the attribute
`part_node_count`.

 and  the data structure MUST have a dimension `part`.

The attribute `part_node_count` contains the name of the int-valued variable
that represents the number of nodes per part. The dimension of this variable
SHOULD be different from the dimension of the variables mentioned in
`node_coordinates`.

Note: which parts belong together can be infered from the corresponding
int-values in the variables of `node_count` and `part_node_count`.

**Example**

    dimensions:
        device = 3;
        node = 17;
        part = 5;

    variables:
        string name(device);
            name:description = "Device name of axisymmetric conductor loop";

        double area(part);
            area:units = "m^2";
            area:standard_name = "_cross_sectional_area_of_element";
        
        int geometry_container ;
            geometry_container:geometry_type = "poloidal_point";
            geometry_container:node_count = "node_count" ;
            geometry_container:node_coordinates = "r z" ;
            geometry_container:part_node_count = "part_node_count" ;

        int node_count(device);

        int part_node_count(part); // Number of nodes per part.

        double r(node);
            r:units = "m";
            r:standard_name = "_major_radius";
        
        double z(node);
            z:units = "m";
            z:standard_name = "_height";

## Holes in geometry polygon

TO-DO

**Example**

    dimensions:
        device = 3;
        node = 17;
        part = 5;

    variables:

        string name(device);
            name:description = "Device name of axisymmetric conductor loop";

        double area(part);
            area:units = "m^2";
            area:standard_name = "_cross_sectional_area_of_element";
        
        int geometry_container ;
            geometry_container:geometry_type = "polygon";
            geometry_container:node_count = "node_count" ;
            geometry_container:node_coordinates = "r phi z" ;
            geometry_container:part_node_count = "part_node_count" ;
            geometry_container:interior_ring = "interior_ring" ;

        int node_count(device);

        int part_node_count(part); // Number of nodes per part.
        // Which parts belong to which device can be infered from node_count and 
        // part_node_count together.

        int interior_ring(part); // Indicates whether surface enclosed by part is 
        // considered included (0) or excluded (1)

        double r(node);
            r:units = "m";
            r:standard_name = "_major_radius";
        
        double z(node);
            z:units = "m";
            z:standard_name = "_height";


    data:
        name = "55.A3.00-MLF-3001" , "55.A3.00-MLF-3002", "55.A3.00-MLF-3003";
        area = 9.8, 6.7, 8.3, 3.3, 7.0;
        node_count = 7, 4, 6;
        part_node_count = 3, 4, 4, 3, 3;
        interior_ring = 0, 0, 0, 0, 1; // Triangle & rectangle, rectangle, and 
        // triangle with triangular hole around centre
        r = 5.1, 4.1, 4.6, 4.1, 4.6, 4.6, 4.1, 
            6.9, 8.3, 8.3, 6.9,
            2.3, 2.3, 4.7, 
            2.6, 2.6, 3.0;
        z = 3.8, 2.8, 2.8, 2.8, 2.8, 2.2, 2.2,
            1.2, 1.2, 0.7, 0.7,
            8.2, 7.0, 7.6,
            7.9, 7.3, 7.5;
