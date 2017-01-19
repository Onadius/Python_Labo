#!/bin/csh
ptraj confamb.prmtop << EOF
trajin remd.300K.mdcrd 1 10000 1
dihedral d1 :2@OE1 :2@CD :2@OE2 :2@HE2 out dih_side.txt
