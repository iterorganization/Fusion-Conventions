# [DRAFT] Geometry Descriptions for Fusion Conventions

This document describes how to attach geometric data to a labeled N-dimensional
array. For convience, this variable will be referred to as _data_variable_.

The _data_variable_ must have an attribute `geometry`. The string-value of this
attribute must be equal to the name of a 0-dimensional variable in the data
structure, which will be refered to as the _geometry_container_. Note that
multiple data variables may refer to the same _geometry_container_.

The _geometry_container_ must have at least the following two attributes

- `node_coordinates`,
- `geometry_type`.

The string-value of the attribute `node_coordinates` contains the names of the
1D variables in the data structure that hold the actual geometric data, all
separated by a single space. Each of
these variables must hold an attribute `standard_name`, indicating which
spatial coordinate this variable represents. The value of this attribute
must differ for each of these variables.

The attribute `geometry_type` indicates how to interpret the geometric data.
Based on the value of this attribute the _geometry_container_ must have other
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

The dimension of the variables mentioned in the attribute `node_coordinates` of
the _geometry_container_ must also be a dimension of _data_variable_.

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
            r:standard_name = "_radial_distance";

        double phi(b_field_pol_probe);
            phi:standard_name = "_azimuth";
        
        double z(b_field_pol_probe);
            z:standard_name = "_vertical_distance";

### unit_vector

**Use case:**

This geometry type describes unit normal vectors in 3D space. It
can be used for point-measurements of projections of vector quantities, such as
magnetic fields.

**Extra requirements:**

In this case, the geometry_container must also have an attribute
`node_orientations`.

The point in space from which this unit vector starts, is described by the 3
variables in `node_coordinates`.

The direction of the unit vector is described by the two 1D variables whose
names must be mentioned in `node_orientations`, seperated by a single space.
These variables represent the _normal_poloidal_angle and _normal_toroidal_angle,
and must have an attribute `standard_name` with value "_normal_poloidal_angle"
and "_normal_toroidal_angle", respectively.

The dimension of the variables mentioned in the attributes
`node_coordinates` and `node_orientations` of the _geometry_container_ must also
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
            r:standard_name = "_radial_distance";

        double phi(b_field_pol_probe);
            phi:standard_name = "_azimuth";
        
        double z(b_field_pol_probe);
            z:standard_name = "_vertical_distance";

        double angle_normal_poloidal(b_field_pol_probe);
            angle_normal_poloidal:standard_name = "_normal_poloidal_angle";

        double angle_normal_toroidal(b_field_pol_probe);
            angle_normal_toroidal:standard_name = "_normal_toroidal_angle";

### line

**Use case:**

This geometric type describes connected line segments in 3D cartesian space. Each line segment is described by two points, the start and end point.

**Extra requirements:**

In this case, the _geometry_container_ must also have an attribute `node_count`.

The 1D variables described in the attribute `node_coordinates` of the geometry
container must have the same dimension, which will be refered to as their _node_
dimension. These 1D variables describe the space coordinates of each 'node'.

The string-value of the attribute `node_count` must be the name of an
integer-valued variable in the data structure, where its dimension must
also be a dimension of the corresponding variable _data_variable_.

Furthermore, this variable must return the number of nodes required to describe
the collection of connected line segments associated with a particular value in
_data_variable_. This number corresponds with the number of consecutive entries
in the 1D variables described in the attribute `node_coordinates`. It follows
that each of these numbers should be greater than 1.

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
            r:standard_name = "_radial_distance";

        double phi(node);
            phi:standard_name = "_azimuth";
        
        double z(node);
            z:standard_name = "_vertical_distance";
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
            r:standard_name = "_radial_distance";
            r:description = "Major radius";
            r:units = "m";

        double phi(node);
            phi:standard_name = "_azimuth";
            phi:description = "Toroidal angle (oriented counter-clockwise when viewing from above)";
            phi:units = "rad";
        
        double z(node);
            z:standard_name = "_vertical_distance";
            z:description = "Height";
            z:units = "m";
            
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

This geometry type describes a full circle, symmetric with respect to the
coordinate _azimuth. In other words, each point on the circle has the same value
for the coordinates _radial_distance and _vertical_distance. Therefore, it is
sufficient to describe this circle by only specifying this value of
_radial_distance and _vertical_distance.

**Extra requirements:**

The _geometry_container_ does not need any additional attributes.

The dimension of the variables mentioned in the attribute `node_coordinates` of
the _geometry_container_ must also be a dimension of _data_variable_.

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
            r:standard_name = "_radial_distance";
        
        double z(flux_loop);
            z:standard_name = "_vertical_distance";
    data:
        flux = 10.4, 10.6, 9.9,
            10.2, 10.4, 9.7;
        r = 3.4, 1.0, 5.8,
            3.4, 1.0, 5.8;
        z = 0.4, 7.7, 8.1,
            0.4, 7.7, 8.1;

### poloidal_line

**Use case:**

This geometry type describes an axisymmetric surface. Since each cross-section
in the plane "__radial_distance_ and __vertical_distance_" is the same for this
geometry, it is sufficient to describe it by a collection of connected
line-segments in this plane.

**Extra requirements:**

The required attributes of this type are exactly the same as with the geometric
type 'line'. The only difference is that the attribute `node_coordinates` must
not contain a variable whose attribute `standard_name` has value '_azimuth'.

**Example**

    dimensions:
        device = 3;
        time = 2;
        node = 15;


    variables:
        double field_value(time, device);
            diverter:geometry = "some_geometry_container";
        
        int some_geometry_container;
            some_geometry_container:geometry_type = "poloidal_line";
            some_geometry_container:node_coordinates = "r z" ;
            some_geometry_container:node_count = "some_node_count";

        int some_node_count(device)

        double r(node);
            r:standard_name = "_radial_distance";
        
        double z(node);
            z:standard_name = "_vertical_distance";

### poloidal_polygon

**Use case:**

This geometry type describes an axisymmetric volume. Since each cross-section in
the plane "__radial_distance_ and __vertical_distance_" is the same for this
geometry, it is sufficient to describe it by a polygon in this plane.

**Extra requirements:**

The required attributes of this type are exactly the same as with the geometric
type 'polygon'. The only difference is that the attribute `node_coordinates`
must not contain a variable whose attribute `standard_name` has value
'_azimuth'.

## Geometries containing Multiple parts

**Use case:**

If the geometry consists of several disconnected parts of the same
`geometry_type` other than [`point`](#point), then the _geometry_container_ must
contain the attribute `part_node_count`. If the geometry consists of several
disconnected [`points`](#point), then the _geometry_container_ should not
contain the attribute `part_node_count`, since each 'part' would contain only a
single node.

**Requirements:**

The attribute `part_node_count` contains the name of the integer-valued variable
that represents the number of nodes per part. The dimension of this variable
should be different from the dimension of the variables mentioned in both
`node_coordinates` and, if present, `node_count`.

**Example**

    dimensions:
        device = 3;
        node = 17;
        part = 5;

    variables:
        double field(device);
            field:geometry = "geometry_container";
        
        int geometry_container;
            geometry_container:geometry_type = "poloidal_point";
            geometry_container:node_count = "node_count" ;
            geometry_container:node_coordinates = "r z" ;
            geometry_container:part_node_count = "part_node_count" ;

        int node_count(device);

        int part_node_count(part); // Number of nodes per part.
        // Which parts belong to which device can be infered from node_count and 
        // part_node_count together.

        double r(node);
            r:units = "m";
            r:standard_name = "_radial_distance";
        
        double z(node);
            z:units = "m";
            z:standard_name = "_vertical_distance";

## Holes in the geometry poloidal_polygon

**Use case:**

In case the geometry of type [`poloidal_polygon`](#poloidal_polygon) consist of holes,
then the _geometry_container_ must contain the attributes `part_node_count` and
`interior`.

**Extra requirements:**

The attribute `part_node_count` contains the name of the integer-valued variable
that represents the number of nodes per part, and the attribute `interior`
contains the name of the integer-valued variable that indicates which part is
considered as the interior of the geometry (value 0) and which part is considered
exterior (value 1). These variables must have the same dimension.

Each part of the geometry denoting the exterior of the geometry must be
completely contained by another part representing the interior.

**Example**

    dimensions:
        device = 3;
        node = 17;
        part = 5;

    variables:
        double field(device);
            field:geometry = "geometry_container";
        
        int geometry_container;
            geometry_container:geometry_type = "poloidal_polygon";
            geometry_container:node_count = "node_count" ;
            geometry_container:node_coordinates = "r z" ;
            geometry_container:part_node_count = "part_node_count" ;
            geometry_container:interior = "interior" ;

        int node_count(device);

        int part_node_count(part); // Number of nodes per part.

        int interior(part); // Indicates whether surface enclosed by part is 
        // considered included (0) or excluded (1)

        double r(node);
            r:units = "m";
            r:standard_name = "_radial_distance";
        
        double z(node);
            z:units = "m";
            z:standard_name = "_vertical_distance";


    data:
        field = 9.8, 6.7, 3.6;
        node_count = 7, 4, 6;
        part_node_count = 3, 4, 4, 3, 3;
        interior = 0, 0, 0, 0, 1; // Triangle & rectangle, rectangle, and 
        // triangle with triangular hole around centre
        r = 5.1, 4.1, 4.6, 4.1, 4.6, 4.6, 4.1, 
            6.9, 8.3, 8.3, 6.9,
            2.3, 2.3, 4.7, 
            2.6, 2.6, 3.0;
        z = 3.8, 2.8, 2.8, 2.8, 2.8, 2.2, 2.2,
            1.2, 1.2, 0.7, 0.7,
            8.2, 7.0, 7.6,
            7.9, 7.3, 7.5;

## Adding labels to the geometry

**Use case:**

If one wants to add a label to a geometry, which could be used when plotting the
geometries, then this is possible by including the attribute `label` in the
_geometry_container_.

**Extra requirements:**

If the _geometry_container_ has the attribute `label`, then the string-value of
this attribute must be the name of a string-valued variable. The dimension of
  this variable must also be a dimension of _data_variable_ and, if the
  attribute `node_count` is present, must be the same as the dimension of the
 variable mentioned in the attribute `node_count`.

**Example**

    dimensions:
        flux_loop = 3;
        time = 2;

    variables:
        string device_id(flux_loop);
            device_id:description = "Device identifier of flux loop";

        double flux(time, flux_loop);
            flux:geometry = "some_geometry_container";
        
        int some_geometry_container;
            some_geometry_container:geometry_type = "poloidal_point";
            some_geometry_container:node_coordinates = "r z" ;
            some_geometry_container:label = "device_id";

        double r(flux_loop);
            r:standard_name = "_radial_distance";
        
        double z(flux_loop);
            z:standard_name = "_vertical_distance";
    data:
        device_id = "55.AD.00-MSA-1001", "55.AD.00-MSA-1002", "55.AD.00-MSA-1003";
        flux = 10.4, 10.6, 9.9,
            10.2, 10.4, 9.7;
        r =  3.4, 1.0, 5.8;
        z =  0.4, 7.7, 8.1;

## More specific geometry information

**Use case:**

If one wants to add more specific geometry information to a geometry of type
[`poloidal_line`](#poloidal_line) or [`poloidal_polygon`](#poloidal_polygon),
then the attribute `geometric_shape` needs to be attached to the
_geometry_container_. This attribute allows applications to obtain more accurate
geometry information, especially when the actual geometry contains curvature as
in the case of circles and annuli.

**Extra requirements:**

If the _geometry_container_ has the attribute `geometric_shape`, then the
string-value of this attribute must be the name of a 2D float-valued variable of
shape $N \times k$, where $N$ is the number of nodes. The first entry of each
length-$k$ array represents an integer identifier determining the meaning of the
other entries. This identifier will be refered to as the _shape_identifier_. The
dimension of the first axis of this variable must also be a dimension of
_data_variable_ and, if the attribute `node_count` is present, must be the same
as the dimension of the variable mentioned in the attribute `node_count`.

The variable mentioned in the attribute `geometric_shape` may contain 'NaN'
values, such that not every value of _shape_identifier_ should require the use
of the remaining $k-1$ entries and not every geometry needs to be associated
with a specific geometry shape.

Consider a length-$k$ array of the variable mentioned in the attribute
`geometric_shape`: _[_shape_identifier_, $x_1$,..., $x_{k-1}$ ]_. The table below
shows what the values of $x_i$ represent based on the value of
_shape_identifier_

| Shape              | _shape_identifier_ | $x_1$                             | $x_2$                               | $x_3$        | $x_4$        |
|--------------------|--------------------|-----------------------------------|-------------------------------------|--------------|--------------|
| Poloidal circle    | 1                  | _radial_distance<br>of the centre | _vertical_distance<br>of the centre | Radius       | -            |
| Poloidal annulus   | 2                  | _radial_distance<br>of the centre | _vertical_distance<br>of the centre | Inner radius | Outer radius |
| Poloidal rectangle | 3                  | _radial_distance<br>of the centre | _vertical_distance<br>of the centre | Width         | Height       |

**Example**

    dimensions:
        time = 2;
        coil_element = 3;
        coil_node = 27;
        coil_part = 4;
        coil_shape_size = 5;

    variables:
        double coil.resistance(time, coil_element);
            coil.resistance:standard_name = "";
            coil.resistance:units = "Ohm";
            coil.resistance:geometry = "coil_geometry_container";
        
        int coil_geometry_container;
            coil_geometry_container:geometry_type = "poloidal_polygon";
            coil_geometry_container:node_coordinates = "coil_element_r coil_element_z";
            coil_geometry_container:node_count = "coil_element_node_count";
            coil_geometry_container:part_node_count = "coil_element_part_node_count";
            coil_geometry_container:interior_name = "coil_element_interior";
            coil_geometry_container:geometric_shape = "coil_element_shapes";

        int coil_element_node_count(coil_element);

        int coil_element_part_node_count(coil_part);

        int coil_element_interior(coil_part);

        double coil_element_r(coil_node);
            coil_element_r:standard_name = "_radial_distance";
        
        double coil_element_z(coil_node);
            coil_element_z:standard_name = "_vertical_distance";

        double coil_element_shapes(coil_element, coil_shape_size);

    data:
        coil.resistance = 0.0057, 0.00791, 0.0061,
            0.088, 0.034, 0.077;
        coil_element_node_count = 20, 4, 3; // An annulus (each circle described
        // by 10 points), a rectangle and a triangle
        coil_element_part_node_count = 10, 10, 4, 3;
        coil_element_interior = 0, 1, 0, 0;
        coil_element_r = 1.76 , 1.634, 1.304, 0.896, 0.566, 0.44 , 0.566, 0.896, 1.304,
            1.634,  1.22 , 1.197, 1.137, 1.063, 1.003, 0.98 , 1.003, 1.063, 1.137,
            1.197, 2.1, 2.1, 2.6, 2.6, 0.33, 1.1, 0.33;
        coil_element_z = 0.3  ,  0.688,  0.928,  0.928,  0.688,  0.3  , -0.088, -0.328,
            -0.328, -0.088, 0.3  , 0.371, 0.414, 0.414, 0.371, 0.3  , 0.229, 0.186, 0.186,
            0.229, 1.5, 1.8, 1.8, 1.5, 2.2, 2.5, 2.8;
        coil_element_shapes = 2, 1.1, 0.3, 0.66, 0.12,
            3, 2.35, 1.65, 0.5, 0.3,
            0, 0, 0, 0, 0// no shape identifier for rectangle
        
