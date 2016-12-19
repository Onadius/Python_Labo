#!/bin/csh
ptraj prmtop.rep1 << EOF
trajin mdcrd.001 remdtraj remdtrajtemp 300.00
trajout remd.300K.mdcrd nobox
