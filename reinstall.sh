#reinstall the CNN package
#by running ./reinstall.sh in command-line
mkdir build
cd build
cmake .. -DCMAKE_INSTALL_PREFIX:PATH=/homes/kovacs/toolbox
make install
