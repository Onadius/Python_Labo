#Amber REMD input template  

set n_cpu = 22
set n_rep = 22

# n_cpu must be a multiple of n_rep

mpirun -machinefile hosts -launcher rsh -np $n_cpu  sander.MPI -ng $n_rep -groupfile groupfile.txt

