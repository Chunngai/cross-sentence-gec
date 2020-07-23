#!/bin/bash

set -e
set -x

###### prepare_data.sh

###### Lang8

sudo apt-get -y install python3-pip
pip3 install langid

###### NUCLE

# python2 installation for Ubuntu 20.04 or later.
sudo add-apt-repository universe
sudo apt update 
sudo apt -y install python2
# python2 installation for Ubuntu before 20.04.
sudo apt-get install python2.7

# setuptools
wget https://files.pythonhosted.org/packages/25/5d/cc55d39ac39383dd6e04ae80501b9af3cc455be64740ad68a4e12ec81b00/setuptools-0.6c11-py2.7.egg
sudo sh set*

# pyyaml
wget https://pyyaml.org/download/pyyaml/PyYAML-3.08.tar.gz
tar xzvf Py*
cd PyYAML-3.08/
sudo python2 setup.py install

# nltk
wget https://files.pythonhosted.org/packages/dd/71/c976e54dc7f7af84622955cf5c5b1863cab815979c930add7eb4095db8b7/nltk-2.0b7.tar.gz
tar xzvf nltk*
cd nltk-2.0b7/
sudo python2 setup.py install

echo "nltk_data/tokenizers/punkt/english.pickle" should be placed in one of the following folders:
echo	'/home/neko/nltk_data'
echo	'/usr/share/nltk_data'
echo	'/usr/local/share/nltk_data'
echo	'/usr/lib/nltk_data'
echo	'/usr/local/lib/nltk_data'

###### download.sh
sudo apt-get -y install curl
