#!/bin/bash

set -e
set -x

# [NEW] Exits if the ver of python is not 3.6.*.
case `python -V` in
	"Python 3.6."[0-9][0-9]*)
		;;
	*)
		exit
esac

# [NEW] Uses the src of tuna to speed up the download.
INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple/
# INDEX_URL=https://mirrors.aliyun.com/pypi/simple/
# [NEW] Adds timeout.
TIMEOUT=180

# apt-get packages (required for hunspell & pattern)
# [MODIFIED] sudo is needed.
sudo apt-get update
sudo apt-get install libhunspell-dev libmysqlclient-dev -y

# pip packages
pip install --upgrade pip
pip install --upgrade -r requirements.txt --timeout $TIMEOUT -i $INDEX_URL  # [MODIFIED] Adds -i and --timeout.

# python -m spacy download en
# [Note] The above command may not be able to work.
# [MODIFIED] Alternative of `python -m spacy download en`.
EN_CORE_WEB_SM='https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-1.2.0/en_core_web_sm-1.2.0.tar.gz'  # For spacy 1.9.0.
pip install $EN_CORE_WEB_SM --timeout $TIMEOUT
python -m spacy link en_core_web_sm en  # Creates a shortcut link.

# custom fairseq (fork of 0.6.1 with gec modifications)
pip install --editable fairseq

# errant
#git clone https://github.com/chrisjbryant/errant
# [Note] Ver. of errant should be compatible.
# [MODIFIED] Specifies the bea2019st branch of errant.
if [ ! -d errant ]
then
	git clone https://github.com/chrisjbryant/errant -b bea2019st
fi

# pattern3 (see https://www.clips.uantwerpen.be/pages/pattern for any installation issues)
pip install pattern3 --timeout $TIMEOUT -i $INDEX_URL  # [MODIFIED] Adds -i and --timeout.

# python -c "import site; print(site.getsitepackages())"
# ['PATH_TO_SITE_PACKAGES']
# cp tree.py PATH_TO_SITE_PACKAGES/pattern3/text/
# [MODIFIED] Does the cp in python, instead of using the command above.
python -c "import site, os; \
	path_to_site_packages = site.getsitepackages(); \
	[os.system(f'cp tree.py {path}/pattern3/text/') if os.path.exists(path) else None for path in path_to_site_packages]"

###### NEW ######
pip install torch==1.4.0 -i $INDEX_URL --timeout $TIMEOUT

# Moves README.md and LICENSE to repo_info.
mkdir repo_info
mv README.md repo_info
mv LICENSE repo_info

# average_perceptron_tagger.picker is needed in the perturbation step. 
sudo mkdir -p /usr/local/lib/nltk_data/taggers/averaged_perceptron_tagger/
sudo mv averaged_perceptron_tagger.pickle  /usr/local/lib/nltk_data/taggers/averaged_perceptron_tagger/

