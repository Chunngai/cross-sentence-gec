#!/bin/bash

set -e
set -x

###### prepare_data.sh

###### Lang8

sudo apt-get update
sudo apt-get -y install python3-pip
pip3 install langid

###### NUCLE

# python2
case `lsb_release -rs` in
        20.[0-9][0-9])
                sudo add-apt-repository universe
                sudo apt update
                sudo apt -y install python2
                ;;
        *)
                sudo apt-get install python2.7
                ;;
esac

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

# nltk data
sudo apt-get -y install git
git clone https://github.com/nltk/nltk_data
sudo mv nltk_data /usr/local/lib/

###### download.sh
sudo apt-get -y install curl
