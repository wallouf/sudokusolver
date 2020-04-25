#!/bin/bash

#
# Run it on an AWS EC2 LINUX with CLI installed
#

sudo yum install python36 -y

mkdir -p build/python/lib/python3.6/site-packages
pip-3.6 install opencv-python -t build/python/lib/python3.6/site-packages/

cd build/
zip -r package.zip .

aws s3 cp package.zip s3://opencv.layers.wallouf

#Set up AWS lambda layer after with runtime python3.6, url: https://s3.amazonaws.com/layers.wallouf/package.zip
