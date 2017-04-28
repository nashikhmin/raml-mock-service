#!/usr/bin/env bash

file=$1
echo copy RAML file...
cp ${file} interface.raml

echo start Docker build...
sudo docker build . -t veor12/mock-service

#TODO: uncommit it after other will have been completed
#echo delete temporaly files...
#rm interface.raml