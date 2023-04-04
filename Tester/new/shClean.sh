# Delete the existing gnco files, then force remake the FTP project
#! /bin/bash

# Delete old input and output
rm -r ./input/*
# rm -r ./output/*
rm -r ~/ftpshare/*

# Clean make
cd ../../Source/Release/
make clean

# Clean ftpshare
cd ~/ftpshare


