#!/bin/bash

set -e
set -x

# [NEW] Uses the src of tuna to speed up the doenload.
INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple/
# [NEW] Adds timeout.
TIMEOUT=180

# apt-get packages (required for hunspell & pattern)
sudo apt-get update  # [MODIFIED] sudo is needed.
sudo apt-get install libhunspell-dev libmysqlclient-dev -y  # [MODIFIED] sudo is needed.

# pip packages
pip install --upgrade pip
pip install --upgrade -r requirements.txt --timeout $TIMEOUT -i $INDEX_URL  # [MODIFIED] Adds -i and --timeout.

# python -m spacy download en
# [Note] The above command may not be able to work.
# [MODIFIED] Alternative of `python -m spacy download en`
EN_CORE_WEB_SM='https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.3.1/en_core_web_sm-2.3.1.tar.gz'  # For spacy >= 2.3.0, <2.4.0
pip install $EN_CORE_WEB_SM --timeout $TIMEOUT
python -m spacy link en_core_web_sm en  # Creates a shourcut link.

# custom fairseq (fork of 0.6.1 with gec modifications)
pip install --editable fairseq

# errant
# [Note] Does not specify the ver. of errant.
git clone https://github.com/chrisjbryant/errant

# pattern3 (see https://www.clips.uantwerpen.be/pages/pattern for any installation issues)
pip install pattern3 --timeout $TIMEOUT -i $INDEX_URL  # Adds -i and --timeout.

# python -c "import site; print(site.getsitepackages())"
# ['PATH_TO_SITE_PACKAGES']
# cp tree.py PATH_TO_SITE_PACKAGES/pattern3/text/
# [MODIFIED] Does the cp in python, instead of using the command above.
python -c "import site, os; \
	path_to_site_packages = site.getsitepackages(); \
	[os.system(f'cp tree.py {path}/pattern3/text/') if os.path.exists(path) else None for path in path_to_site_packages]"

###### NEW ######
pip install torch -i $INDEX_URL --timeout $TIMEOUT  # Needed by spell in preprocess.py

mkdir repo_info
mv README.md repo_info
mv LICENSE repo_info
