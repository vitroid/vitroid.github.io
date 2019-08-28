#software

#analysis

December 2017: This document is now obsolete.  See [github:GenIce](github:GenIce) page.


## Three steps to get an proton-disordered ice configuration


### 0. Prepare the position of oxygen atoms.

Initial data file named "oxygen.ar3a" is prepared. The file must contain the simulation cell size in @BOX3 format and the coordinates of oxygen atoms in @AR3A format.

```
@BOX3
22.5631452967369 23.4483086636094 22.107277423236    
@AR3A      
360      
12.4097297589778 13.0268384320562 5.06625139746566    
12.4097297589778 13.0268384320562 12.4353438718777    
12.4097297589778 13.0268384320562 19.8044363462897    
14.6660439801963 14.3295215041241 5.9873878282442    
14.6660439801963 14.3295215041241 13.3564803026562    
14.6660439801963 14.3295215041241 20.7255727770682    
...
```
See also: Prepare a Crystal from a Unit Cell


### 1. Compose an undirected graph.

Make an undirected graph as the template of hydrogen bond network according to the intermolecular distance between oxygen atoms. In the following example, 3 angstrom is specified as the threshold. Result is obtained in @NGPH format, in which ice rule is not satisfied.

```
makebonds 3 < oxygen.ar3a > undirected.ngph
```

### 2. Let the graph obey ice rule.

IceRandomize3 utility changes the direction of hydrogen bonds to let all the nodes obey the ice rule (2 in and 2 out at a node). Both input and output files are in @NGPH format.

```
IceRandomize3 < undirected.ngph > ice.ngph
```

### 2.5 Depolarize.

zerodipole.py changes the direction of hydrogen bonds in ice to depolarize (let the sum dipole be zero) by reverting the bonds on the homordomic paths. Input and output files are in @NGPH and @AR3A/@NX4A format.

```
cat ice.ngph ice.ar3a | python zerodipole.py > depolarized.ngph+ar3a
```

### 3. Generate the orientations of water molecules

Give the positions of oxygen atoms and the network topology to waterconfig2.pbc tool to get the water configurations.

```
cat oxygen.ar3a ice.ngph | waterconfig2.pbc > ice.nx4a
```
Resultant water configuration file is in @NX4A format.


## Known Problems

The initial oxygen atom positions must not include defects. All the atomic coordination number must be 4. There is another program (IceConfig) to make water configuration with defects which is not included in the following package.


## Program

[](storage:Generate a Proton-disordered Ice/icesynthesize.tar.gz)


## Example

```
% make
% make test
