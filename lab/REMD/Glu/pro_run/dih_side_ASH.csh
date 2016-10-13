#!/bin/csh
ptraj confamb.prmtop << EOF
trajin remd.300K.mdcrd 1 10000 1
dihedral d1 :2@OD1 :2@CG :2@OD2 :2@HD2 out dih_side.txt
