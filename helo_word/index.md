### ！ **主要针对Ubuntu18.04和Ubuntu20.04**

# 开始之前
## 1 基本配置
&emsp;&emsp;将ubuntu的默认shell从dash更改为bash。终端输入：
```bash
# 备份原本的shell。
sudo cp /bin/sh /bin/sh.old
# 使sh指向bash。
sudo ln -fs /bin/bash /bin/sh
```

&emsp;&emsp;安装git和vim。终端输入：
```bash
sudo apt update
sudo apt -y install git
sudo apt -y install vim
```

## 2 Python
### 2.1 安装Python3.6 **（针对非18.04的Ubuntu，如20.04。Ubuntu18.04跳过该步骤。其他系统如果python3默认是3.6也跳过该步骤）**  
终端输入：
```bash
# 安装依赖。
# 这两个依赖平常使用可能不用安装。但如果这里不安装，运行论文的源码会出错。
sudo apt install -y libbz2-dev
sudo apt install -y libsqlite3-dev

# 进入Downloads目录。
cd ~/Downloads

# 下载python3.6安装包。
wget https://www.python.org/ftp/python/3.6.11/Python-3.6.11.tgz
# 解压。
tar xzvf Python-3.6.11.tgz

# 进入安装包目录。
cd Python-3.6.11

# 安装。
./configure
sudo make
sudo make altinstall  # 与其他python版本共存
```

### 2.2 安装Python2.7 **（针对非18.04的Ubuntu，如20.04。Ubuntu18.04跳过该步骤。其他系统如果python2默认是2.7也跳过该步骤）**  
终端输入：
```bash
# 添加atom仓库。
echo "" | wget -qO - https://packagecloud.io/AtomEditor/atom/gpgkey | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] https://packagecloud.io/AtomEditor/atom/any/ any main" > /etc/apt/sources.list.d/atom.list'
sudo apt-get update

# 安装atom。
sudo apt-get -y install atom
```
&emsp;&emsp;以上命令实际上是通过安装atom间接安装python2.7。atom是github的一个文本编辑软件，其依赖包含python2.7。这种安装方式不容易出错。当然也可以通过其他方式安装python2.7，但会比较复杂，**特别是对于Ubuntu20.04**。

---

&emsp;&emsp;**非Ubuntu18.04**的系统按照上述操作安装python3和python2之后，在终端输入python3后显示的应该是系统原！本！的！python3版本；在终端输入python2后显示的应该是python2.7。

---

### 2.3 虚拟环境
&emsp;&emsp;虚拟环境提供一个与系统隔离的**python环境**。为了避免错误，**论文代码在虚拟环境运行**。

&emsp;&emsp;首先安装虚拟环境的依赖。终端输入：
```bash
sudo apt -y install python3-venv
```

&emsp;&emsp;使用虚拟环境。终端输入：
```bash
# 在当前目录创建一个名为gec的虚拟环境（其实就是一个目录）。
python3.6 -m venv gec  # 一定要是python3.6！！！虚拟环境名（此处为gec）可以不同。

# 激活虚拟环境。
source gec/bin/activate  # 该命令只有在虚拟环境文件夹（此处为gec）所在目录运行才成功。
# 如果在其他位置激活虚拟环境，则应运行: source [虚拟环境文件夹位置]/bin/activate
```

&emsp;&emsp;此时，终端提示符的开头会显示虚拟环境的名字。如果虚拟环境名为gec，应该显示:（终端输入）
```bash
(gec) [user]@[machine_name]:[path]$
```
&emsp;&emsp;其中，`[user]`为用户名，`[machine_name]`为机器名，`[path]`为当前路径，它们的具体值取决于用户的设置。

&emsp;&emsp;**注意：激活虚拟环境后，可以切换到任意目录，就像没使用虚拟环境那样。基本上，虚拟环境只用于存储python的安装包。**

**&emsp;&emsp;虚拟环境激活后，在虚拟环境内应满足要求：  
&emsp;&emsp;1. 在终端输入`python`后，显示python3.6；  
&emsp;&emsp;2. 在终端输入`python2.7`后，显示python2.7。**

&emsp;&emsp;**如果以上两个要求不满足，运行论文的代码会出现问题！！！**

&emsp;&emsp;**后面的操作全部在虚拟环境进行！！！** 也就是说，终端的提示符应该是：
```bash
([虚拟环境名]) [user]@[machine_name]:[path]$
```
&emsp;&emsp;而不是
```bash
[user]@[machine_name]:[path]$
```

# 克隆仓库
&emsp;&emsp;终端输入：
```bash
# 克隆仓库到当前目录。
git clone https://github.com/kakaobrain/helo_word
```

# 准备数据
&emsp;&emsp;解压helo_word_data.zip。  

&emsp;&emsp;解压方式一：右键-解压。  
&emsp;&emsp;解压方式二：终端输入
```bash
unzip helo_word_data.zip
```

&emsp;&emsp;将解压后的文件夹内部的所有文件（包括10个压缩包和1个.pickle文件）放到helo_word文件夹的 **根目录**。

# 在helo_word文件夹打开终端，并进入虚拟环境
&emsp;&emsp;在**helo_word文件夹**打开终端。（在文件夹内右键点击终端就可以打开以该文件夹为当前位置的终端）  

&emsp;&emsp;进入虚拟环境。终端输入：
```bash
source [虚拟环境文件夹位置]/bin/activate
```
&emsp;&emsp;**！！注意：这之后的所有操作都在虚拟环境中进行**

# 安装依赖（对应[论文github](https://github.com/kakaobrain/helo_word)的Installation）
&emsp;&emsp;**！！注意：原本的命令可能无法正常工作。**建议输入如下命令，**代替** Installation中的命令。  

&emsp;&emsp;在**已经进入虚拟环境的终端**输入以下命令：
```bash
# [NEW] Uses the src of tuna to speed up the download.
INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple/
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

# average_perceptron_tagger.picker is needed in the perturbation step.
sudo mkdir -p /usr/local/lib/nltk_data/taggers/averaged_perceptron_tagger/
sudo mv averaged_perceptron_tagger.pickle  /usr/local/lib/nltk_data/taggers/averaged_perceptron_tagger/
```
&emsp;&emsp;修改的地方已在注释给出。其中，`[NEW]`表示新增，`[MODIFIED]`表示修改。`###### NEW ######`后面的内容源代码没有，却是之后的部分代码成功执行必须的。

## 版本控制（这部分不想看可以跳过）
&emsp;&emsp;以上代码的修改部分主要是为了保证软件或库的版本和论文一致。主要是以下几个地方：

### 1 Spacy: 1.9.0
&emsp;&emsp;论文使用的errant版本要求spacy为1.9.0。对应部分：
```bash
EN_CORE_WEB_SM='https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-1.2.0/en_core_web_sm-1.2.0.tar.gz'  # For spacy 1.9.0.
pip install $EN_CORE_WEB_SM --timeout $TIMEOUT
python -m spacy link en_core_web_sm en  # Creates a shortcut link.
```

&emsp;&emsp;额外指出，spacy1.9.0要求python3 <= 3.6。也就是依赖链为：该论文使用的errant -> spacy1.9.0 -> python3.6。

### 2 errant: bea2910st
&emsp;&emsp;论文的代码使用的是（相对现在而言）之前版本的errant。如果按照仓库文档提供的代码直接克隆errant，后续代码的执行会出错。修改的对应部分：
```bash
git clone https://github.com/chrisjbryant/errant -b bea2019st
```
&emsp;&emsp;这里使用了`-b`参数指定分支。

### 3 pytorch: 1.4.0
&emsp;&emsp;Pytorch的版本肯定为1.4.0或者之前，否则运行后续代码会有错误和警告。对应的修改部分：
```bash
pip install torch==1.4.0 -i $INDEX_URL --timeout $TIMEOUT
```
&emsp;&emsp;此处指定了pytorch的版本。

# 数据下载和预处理（对应[论文github](https://github.com/kakaobrain/helo_word)的Download & Preprocess Data）
&emsp;&emsp;对应的脚本为`preprocess.py`。该脚本包含下载数据的代码。由于部分数据较大、需要申请或需要fq才能获得，因此提前下载好数据（之前的“准备数据”部分已经将所需的全部数据放到helo_word的根目录）。现在要做的就是：将`preprocess.py`的代码**全部删除**，**替换** 成以下代码：
```python
import logging
import os
from glob import glob
import argparse
from gec import filepath, word_tokenize, bpe, perturb, m2, spell

logging.basicConfig(level=logging.INFO)


def maybe_do(fp, func, inputs):
    if os.path.exists(fp):
        logging.info(f"skip this step as {fp} already exists")
    else:
        func(*inputs)


def maybe_download(dir, cmd):
    if os.listdir(dir) != []:
        logging.info(f"skip this step as {dir} is NOT empty")
    else:
        # (MODIFIED)
        for sub_cmd in cmd:
            print(f"+ {sub_cmd}")  # (NEW)
            os.system(sub_cmd)


# (NEW)
def maybe_download_(pkg_name, command):
    """
    Does not download when the pkg is in the dir.
    """
    return f"if [ ! -f {pkg_name} ]; then {command}; fi"


# (NEW)
def print_log(log_info):
    """
    Prints the log following a '\n'.
    """
    print()
    logging.info(log_info)


if __name__ == "__main__":

    """ PARSE OPTS """

    parser = argparse.ArgumentParser()

    # 1. word-tokenize
    parser.add_argument("--max_tokens", type=int, default=150,
                        help="Maximum number of tokens in a sample")

    # 2. train bpe model
    parser.add_argument("--vocab_size", type=int, default=32000,
                        help="vocabulary size")

    # 3. perturbation -> bpe-tokenize
    parser.add_argument("--min_cnt", type=int, default=4)
    parser.add_argument("--word_change_prob", type=float, default=.9)
    parser.add_argument("--type_change_prob", type=float, default=.1)
    parser.add_argument("--n_epochs", type=int, nargs="+", default=[1, 12, 5],
                        help="list of n_epochs of gutenberg, tatoeba, and wiki103")

    args = parser.parse_args()

    """ MAKE DIRS """

    # (NOTE) fp contains all paths of dirs and paths.
    fp = filepath.FilePath()
    # (NOTE) Makes dirs for `dirname(file) for file in fp`.
    # (NOTE) ("files" refer to those whose var names are lowercase.)
    # (QUESTION) In the init method of `FilePath` `make_dirs` has already been invoked.
    # (QUESTION) Why is it invoked again?
    fp.make_dirs()

    """ DOWNLOAD DATA """
    print_log("###### STEP 0. Download data")

    print_log("###### STEP 0-1. Download Gutenberg Text")
    maybe_download(
        fp.gutenberg,

        [
            f"{maybe_download_('Gutenberg.zip', 'gdown https://drive.google.com/uc?id=0B2Mzhc7popBga2RkcWZNcjlRTGM')}",
            f"unzip Gutenberg.zip -d {fp.gutenberg}",
            f"rm Gutenberg.zip"
        ]
    )

    print_log("###### STEP 0-2. Download Tatoeba")
    maybe_download(
        fp.tatoeba,

        [
            f"{maybe_download_('sentences.tar.bz2', 'wget http://downloads.tatoeba.org/exports/sentences.tar.bz2')}",
            f"tar -C {fp.tatoeba} -xvjf sentences.tar.bz2",
            f"rm sentences.tar.bz2"
        ]
    )

    print_log("###### STEP 0-3. Download Wiki-103")
    maybe_download(
        fp.wiki103,

        [
            f"{maybe_download_('wikitext-103-v1.zip', 'wget https://s3.amazonaws.com/research.metamind.io/wikitext/wikitext-103-v1.zip')}",
            f"unzip wikitext-103-v1.zip -d {fp.wiki103}",
            f"mv {fp.wiki103}/wikitext-103/wiki.train.tokens {fp.wiki103}/wiki.train.tokens",
            f"rm wikitext-103-v1.zip"
        ]
    )

    # TODO: make these directories at filepath.py
    # make directories
    for dir_name in [f"{fp.bea19}", f"{fp.wi}", f"{fp.fce}", f"{fp.conll2013}", f"{fp.conll2014}"]:
        try:
            os.mkdir(dir_name)
        except:
            pass

    print_log("###### STEP 0-4. Download FCE")
    maybe_download(
        f"{fp.bea19}/fce",

        [
            f"{maybe_download_('fce_v2.1.bea19.tar.gz', 'wget https://www.cl.cam.ac.uk/research/nl/bea2019st/data/fce_v2.1.bea19.tar.gz')}",
            f"tar -C {fp.bea19} -xvzf fce_v2.1.bea19.tar.gz",
            f"rm fce_v2.1.bea19.tar.gz"
        ]
    )

    print_log("###### STEP 0-5. Download WI+LOCNESS")
    maybe_download(
        f"{fp.bea19}/wi+locness",

        [
            f"{maybe_download_('wi+locness_v2.1.bea19.tar.gz', 'wget https://www.cl.cam.ac.uk/research/nl/bea2019st/data/wi+locness_v2.1.bea19.tar.gz')}",
            f"tar -C {fp.bea19} -xvzf wi+locness_v2.1.bea19.tar.gz",
            f"cp {fp.wi}/test/ABCN.test.bea19.orig {fp.WI_TEST_ORI}",
            f"rm wi+locness_v2.1.bea19.tar.gz"
        ]
    )

    print_log("###### STEP 0-6.1. Download LANG8")
    try:
        os.mkdir(f"{fp.bea19}/lang8.bea19")  # (NOTE) `f"{fp.bea19}/lang8.bea19"` should be an attr of `fp`.
    except:
        pass
    maybe_download(
        f"{fp.bea19}/lang8.bea19",

        [
            f"tar -C {fp.bea19}/lang8.bea19 -xvzf lang8.bea19.tar.gz",
            f"rm lang8.bea19.tar.gz"
        ]
    )

    print_log("###### STEP 0-6.2. Download NUCLE")
    try:
        os.mkdir(f"{fp.bea19}/nucle3.3")  # (NOTE) `f"{fp.bea19}/nucle3.3"` should be an attr of `fp`.
    except:
        pass
    maybe_download(
        f"{fp.bea19}/nucle3.3",

        [
            f"tar -C {fp.bea19} -xvjf release3.3.tar.bz2",
            # (NOTE) The following 2 statements are for fixing the name of `fp.nucle3.3`.
            # (NOTE) It should be "release3.3.tar.bz2" actually.
            f"rm -rf {fp.bea19}/nucle3.3",
            f"mv {os.path.join(fp.bea19, 'release3.3')} {os.path.join(fp.bea19, 'nucle3.3')}",
            f"rm release3.3.tar.bz2"
        ]
    )

    print_log("######STEP 0-7. Download Conll 2013, 2014")
    maybe_download(
        fp.conll2013,

        [
            f"{maybe_download_('release2.3.1.tar.gz', 'wget https://www.comp.nus.edu.sg/~nlp/conll13st/release2.3.1.tar.gz')}",
            f"tar -C {fp.conll2013} -xvzf release2.3.1.tar.gz",
            f"rm release2.3.1.tar.gz"
        ]
    )

    maybe_download(
        fp.conll2014,

        [
            f"{maybe_download_('conll14st-test-data.tar.gz', 'wget https://www.comp.nus.edu.sg/~nlp/conll14st/conll14st-test-data.tar.gz')}",
            f"tar -C {fp.conll2014} -xvzf conll14st-test-data.tar.gz",
            f"rm conll14st-test-data.tar.gz"
        ]
    )

    print_log("###### STEP 0-8. Download language model")

    os.makedirs(os.path.dirname(filepath.Path.lm_path), exist_ok=True)
    os.makedirs(os.path.dirname(filepath.Path.lm_dict), exist_ok=True)
    maybe_download(
        filepath.Path.lm_databin,

        [
            f"{maybe_download_('wiki103_fconv_lm.tar.bz2', 'wget https://dl.fbaipublicfiles.com/fairseq/models/wiki103_fconv_lm.tar.bz2')}",
            f"tar -xvf wiki103_fconv_lm.tar.bz2",
            f"mv wiki103.pt {filepath.Path.lm_path}",
            f"mv dict.txt {filepath.Path.lm_dict}",
            f"rm wiki103_fconv_lm.tar.bz2",
            f"rm README.md"
        ]
    )

    # logging.info("STEP 0-8. Download M2 Scorer")
    # maybe_download(fp.m2scorer, "wget https://www.comp.nus.edu.sg/~nlp/sw/m2scorer.tar.gz")
    # maybe_download(fp.errant, "git clone https://github.com/chrisjbryant/errant.git")

    """ TOKENIZE DATA FOR PRETRAINING """
    print_log("STEP 1. Word-tokenize the original files and merge them")

    print_log("STEP 1-1. gutenberg")
    fpaths = sorted(glob(f'{fp.gutenberg}/Gutenberg/txt/*.txt'))
    maybe_do(fp.GUTENBERG_TXT, word_tokenize.gutenberg,
             (fpaths, fp.GUTENBERG_TXT, args.max_tokens))

    print_log("STEP 1-2. tatoeba")
    fpath = f'{fp.tatoeba}/sentences.csv'
    maybe_do(fp.TATOEBA_TXT, word_tokenize.tatoeba,
             (fpath, fp.TATOEBA_TXT, args.max_tokens))

    print_log("STEP 1-3. wiki103")
    fpath = f'{fp.wiki103}/wiki.train.tokens'
    maybe_do(fp.WIKI103_TXT, word_tokenize.wiki103,
             (fpath, fp.WIKI103_TXT, args.max_tokens))

    """ TRAIN BPE MODEL """
    print_log("STEP 2. Train bpe model")

    maybe_do(fp.BPE_MODEL, bpe.train,
             (fp.GUTENBERG_TXT, fp.BPE_MODEL.replace(".model", ""), args.vocab_size, 1.0, 'bpe'))

    """ wi.dev -> wi.dev.3k, wi.dev.1k """
    print_log("STEP 3. Split wi.dev into wi.dev.3k and wi.dev.1k")

    fpaths = sorted(glob(f'{fp.wi_m2}/*.dev.gold.bea19.m2'))
    wi_dev_3k_m2 = f'{fp.wi_m2}/ABCN.dev.gold.bea19.3k.m2'
    wi_dev_1k_m2 = f'{fp.wi_m2}/ABCN.dev.gold.bea19.1k.m2'
    maybe_do(wi_dev_3k_m2, m2.split_m2,
             (fpaths, wi_dev_3k_m2, wi_dev_1k_m2, 0.75))

    """ PERTURB DATA FOR PRETRAINING """
    """ AND MAKE PARALLEL FILES """
    print_log("STEP 4. Perturb and make parallel files")

    for track_no in ("1", "3", "0"):
        print_log(f"Track {track_no}")
        print_log("STEP 4-1. writing perturbation scenario")

        # (NOTE) Chooses files for collecting edits according to track.
        if track_no=="1":
            dir = f"{fp.wi_m2}/*train*.m2"
        elif track_no=="3":
            dir = f"{fp.wi_m2}/*dev.*3k*.m2"
        else:
            dir = f"{fp.nucle_m2}/*nucle*.m2"
        word2ptbs = perturb.make_word2ptbs(sorted(glob(dir)), args.min_cnt)

        # (NOTE) Perturbation + parallelization.

        print_log("STEP 4-2. gutenberg")
        maybe_do(eval(f"fp.GUTENBERG_ORI{track_no}"), perturb.do,
                 (word2ptbs, fp.BPE_MODEL, fp.GUTENBERG_TXT,
                  eval(f"fp.GUTENBERG_ORI{track_no}"), eval(f"fp.GUTENBERG_COR{track_no}"), args.n_epochs[0],
                  args.word_change_prob, args.type_change_prob))

        print_log("STEP 4-3. tatoeba")
        maybe_do(eval(f"fp.TATOEBA_ORI{track_no}"), perturb.do,
                 (word2ptbs, fp.BPE_MODEL, fp.TATOEBA_TXT,
                  eval(f"fp.TATOEBA_ORI{track_no}"), eval(f"fp.TATOEBA_COR{track_no}"), args.n_epochs[1],
                  args.word_change_prob, args.type_change_prob))

        print_log("STEP 4-4. wiki103")
        maybe_do(eval(f"fp.WIKI103_ORI{track_no}"), perturb.do,
                 (word2ptbs, fp.BPE_MODEL, fp.WIKI103_TXT,
                  eval(f"fp.WIKI103_ORI{track_no}"), eval(f"fp.WIKI103_COR{track_no}"), args.n_epochs[2],
                  args.word_change_prob, args.type_change_prob))

    """ PARALLELIZE DATA FOR TRAIN & DEV & TEST """
    print_log("STEP 5. m2 to parallel")

    print_log("STEP 5-1. fce")
    maybe_do(fp.FCE_ORI, m2.m2_to_parallel,
             (sorted(glob(f'{fp.fce_m2}/*m2')), fp.FCE_ORI, fp.FCE_COR, False, True))

    print_log("STEP 5-2. lang8")
    maybe_do(fp.LANG8_ORI, m2.m2_to_parallel,
             (sorted(glob(f'{fp.lang8_m2}/*m2')), fp.LANG8_ORI, fp.LANG8_COR, True, True))

    print_log("STEP 5-3. nucle")
    maybe_do(fp.NUCLE_ORI, m2.m2_to_parallel,
             (sorted(glob(f'{fp.nucle_m2}/*m2')), fp.NUCLE_ORI, fp.NUCLE_COR, False, True))

    print_log("STEP 5-4. wi train")
    maybe_do(fp.WI_TRAIN_ORI, m2.m2_to_parallel,
             (sorted(glob(f'{fp.wi_m2}/*train*m2')), fp.WI_TRAIN_ORI, fp.WI_TRAIN_COR, False, True))

    print_log("STEP 5-5. wi dev")
    maybe_do(fp.WI_DEV_ORI, m2.m2_to_parallel,
             (sorted(glob(f'{fp.wi_m2}/ABCN.dev.gold.bea19.m2')), fp.WI_DEV_ORI, fp.WI_DEV_COR, False, False))

    # logging.info("STEP 5-6. wi test")
    # if os.path.exists(WI_TEST_ORI): logging.info(f"skip this step as {WI_TEST_ORI} already exists.")
    # else: m2.m2_to_parallel(glob(f'{wi_m2}/*test*m2'), WI_TEST_ORI, WI_TEST_COR, False, True)

    print_log("STEP 5-7. wi dev 3k. For track 3 only.")
    maybe_do(fp.WI_DEV_3K_ORI, m2.m2_to_parallel,
             (sorted(glob(f'{fp.wi_m2}/ABCN.dev.gold.bea19.3k.m2')), fp.WI_DEV_3K_ORI, fp.WI_DEV_3K_COR, False, False))

    print_log("STEP 5-8. wi dev 1k. For track 3 only.")
    maybe_do(fp.WI_DEV_1K_ORI, m2.m2_to_parallel,
             (sorted(glob(f'{fp.wi_m2}/ABCN.dev.gold.bea19.1k.m2')), fp.WI_DEV_1K_ORI, fp.WI_DEV_1K_COR, False, False))

    print_log("STEP 5-9. conll2013. For track 0 only.")
    maybe_do(fp.CONLL2013_ORI, m2.m2_to_parallel,
             (sorted(glob(f'{fp.conll2013_m2}/official-preprocessed.m2')), fp.CONLL2013_ORI, fp.CONLL2013_COR, False, False))

    print_log("STEP 5-10. conll2014. For track 0 only.")
    maybe_do(fp.CONLL2014_ORI, m2.m2_to_parallel,
             (sorted(glob(f'{fp.conll2014_m2}/official-2014.combined.m2')), fp.CONLL2014_ORI, fp.CONLL2014_COR, False, False))

    """ STEP I: FIX TOKENIZATION ERRORS """
    """ STEP II: SPELLCHECK """
    print_log("STEP 6. spell-check")

    print_log("STEP 6-1. fce")
    maybe_do(fp.FCE_SP_ORI, spell.check, (fp.FCE_ORI, fp.FCE_SP_ORI))

    print_log("STEP 6-2. lang8")
    maybe_do(fp.LANG8_SP_ORI, spell.check, (fp.LANG8_ORI, fp.LANG8_SP_ORI))

    print_log("STEP 6-3. nucle")
    maybe_do(fp.NUCLE_SP_ORI, spell.check, (fp.NUCLE_ORI, fp.NUCLE_SP_ORI))

    print_log("STEP 6-4. wi train")
    maybe_do(fp.WI_TRAIN_SP_ORI, spell.check, (fp.WI_TRAIN_ORI, fp.WI_TRAIN_SP_ORI))

    print_log("STEP 6-5. wi dev")
    maybe_do(fp.WI_DEV_SP_ORI, spell.check, (fp.WI_DEV_ORI, fp.WI_DEV_SP_ORI))

    print_log("STEP 6-6. wi test")
    maybe_do(fp.WI_TEST_SP_ORI, spell.check, (fp.WI_TEST_ORI, fp.WI_TEST_SP_ORI))

    print_log("STEP 6-7. wi dev 3k")
    maybe_do(fp.WI_DEV_3K_SP_ORI, spell.check, (fp.WI_DEV_3K_ORI, fp.WI_DEV_3K_SP_ORI))

    print_log("STEP 6-8. wi dev 1k")
    maybe_do(fp.WI_DEV_1K_SP_ORI, spell.check, (fp.WI_DEV_1K_ORI, fp.WI_DEV_1K_SP_ORI))

    print_log("STEP 6-9. conll 2013")
    maybe_do(fp.CONLL2013_SP_ORI, spell.check, (fp.CONLL2013_ORI, fp.CONLL2013_SP_ORI))

    print_log("STEP 6-10. conll 2014")
    maybe_do(fp.CONLL2014_SP_ORI, spell.check, (fp.CONLL2014_ORI, fp.CONLL2014_SP_ORI))

    """ STEP III: BPE """
    print_log("STEP 7. bpe-tokenize")

    print_log("STEP 7-1. fce")
    maybe_do(fp.FCE_TOK_ORI, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.FCE_SP_ORI, fp.FCE_TOK_ORI))
    maybe_do(fp.FCE_TOK_COR, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.FCE_COR, fp.FCE_TOK_COR))

    print_log("STEP 7-2. lang8")
    maybe_do(fp.LANG8_TOK_ORI, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.LANG8_SP_ORI, fp.LANG8_TOK_ORI))
    maybe_do(fp.LANG8_TOK_COR, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.LANG8_COR, fp.LANG8_TOK_COR))

    print_log("STEP 7-3. nucle")
    maybe_do(fp.NUCLE_TOK_ORI, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.NUCLE_SP_ORI, fp.NUCLE_TOK_ORI))
    maybe_do(fp.NUCLE_TOK_COR, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.NUCLE_COR, fp.NUCLE_TOK_COR))

    print_log("STEP 7-4. wi train")
    maybe_do(fp.WI_TRAIN_TOK_ORI, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.WI_TRAIN_SP_ORI, fp.WI_TRAIN_TOK_ORI))
    maybe_do(fp.WI_TRAIN_TOK_COR, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.WI_TRAIN_COR, fp.WI_TRAIN_TOK_COR))

    print_log("STEP 7-5. wi dev")
    maybe_do(fp.WI_DEV_TOK_ORI, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.WI_DEV_SP_ORI, fp.WI_DEV_TOK_ORI))
    maybe_do(fp.WI_DEV_TOK_COR, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.WI_DEV_COR, fp.WI_DEV_TOK_COR))

    print_log("STEP 7-6. wi test")
    maybe_do(fp.WI_TEST_TOK_ORI, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.WI_TEST_SP_ORI, fp.WI_TEST_TOK_ORI))
    # maybe_do(fp.WI_TEST_TOK_COR, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.WI_TEST_COR, fp.WI_TEST_TOK_COR))

    print_log("STEP 7-7. wi dev 3k")
    maybe_do(fp.WI_DEV_3K_TOK_ORI, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.WI_DEV_3K_SP_ORI, fp.WI_DEV_3K_TOK_ORI))
    maybe_do(fp.WI_DEV_3K_TOK_COR, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.WI_DEV_3K_COR, fp.WI_DEV_3K_TOK_COR))

    print_log("STEP 7-8. wi dev 1k")
    maybe_do(fp.WI_DEV_1K_TOK_ORI, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.WI_DEV_1K_SP_ORI, fp.WI_DEV_1K_TOK_ORI))
    maybe_do(fp.WI_DEV_1K_TOK_COR, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.WI_DEV_1K_COR, fp.WI_DEV_1K_TOK_COR))

    print_log("STEP 7-9. conll2013")
    maybe_do(fp.CONLL2013_TOK_ORI, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.CONLL2013_SP_ORI, fp.CONLL2013_TOK_ORI))
    maybe_do(fp.CONLL2013_TOK_COR, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.CONLL2013_COR, fp.CONLL2013_TOK_COR))

    print_log("STEP 7-10. conll2014")
    maybe_do(fp.CONLL2014_TOK_ORI, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.CONLL2014_SP_ORI, fp.CONLL2014_TOK_ORI))
    maybe_do(fp.CONLL2014_TOK_COR, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.CONLL2014_COR, fp.CONLL2014_TOK_COR))
```

&emsp;&emsp;替换后运行该脚本：
```bash
python preprocess.py
```

# 训练 & 验证 & 测试模型（以[论文github](https://github.com/kakaobrain/helo_word)的Restricted Track为例）
&emsp;&emsp;训练模型之前，需要修改源代码的一些地方。  

&emsp;&emsp;(一)：将`train.py`的第41行：
```python
finetune_ckpt = os.path.basename(util.change_ckpt_dir(restore_ckpt, ckpt_dir))
```
改为
```python
finetune_ckpt = util.change_ckpt_dir(restore_ckpt, ckpt_dir)
```
原因见[issues#5](https://github.com/kakaobrain/helo_word/issues/5)。

&emsp;&emsp;（二）将`evaluate.py`的第129行：
```python
parser.add_argument("--max_edits", type=int, default=None, help="max edit distance during the lm rerank")
```
改为
```python
parser.add_argument("--max-edits", type=int, default=None, help="max edit distance during the lm rerank")
```
一个typo。

&emsp;&emsp;修改这两个地方之后按照文档的步骤训练模型就行了。
