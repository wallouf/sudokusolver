#!/bin/bash

#
# Run it on an AWS EC2 LINUX with CLI installed
cd ~
sudo yum update -y
sudo yum install git-core -y
sudo yum install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user #allows ec2-user to call docker

#LOG OUT / LOG IN REQUIRED
git clone https://github.com/amtam0/lambda-tesseract-api.git
cd lambda-tesseract-api/
bash build_tesseract4.sh #takes a few minutes
bash build_py37_pkgs.sh

#Set up AWS lambda layer after with runtime python3.6, 

#url: https://s3.amazonaws.com/layers.wallouf/opencv-python.zip
#url: https://s3.amazonaws.com/layers.wallouf/pillow.zip
#url: https://s3.amazonaws.com/layers.wallouf/pytesseract.zip
#url: https://s3.amazonaws.com/layers.wallouf/tesseract-layer.zip

#In the lambda: Create an Environment Variable. Key : PYTHONPATH and Value : /opt/