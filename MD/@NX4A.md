#Datatypes


## @NX4A - Configuration fo Rigid bodies

A file format to specify the configration of rigid bodies, like TIP4P water molecules.

|Data|Type|Description |
|-----|-----|-----|
|@NX4A|5 fixed characters|A tag |
|N|integer|Number of rigid bodies |
|x y z a b c d|Seven real numbers separated by a space character.|Coordinate of the center of mass (in Angstrom) and the orientation in quaternion. |
|...|(repeat N times)| |






