import logging
import os
from glob import glob
import argparse
from gec import filepath, word_tokenize, bpe, perturb, m2, spell, \
    make_sp_context  # [CONTEXT]

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
            f"rm lang8.bea19.tar.gz",

            # [CONTEXT]
            f"unzip lang-8-en-1.0.zip -d {fp.bea19}/lang8.bea19",
            f"rm lang-8-en-1.0.zip"
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
    """
    print_log("STEP 5-7. wi dev 3k. For track 3 only.")
    maybe_do(fp.WI_DEV_3K_ORI, m2.m2_to_parallel,
             (sorted(glob(f'{fp.wi_m2}/ABCN.dev.gold.bea19.3k.m2')), fp.WI_DEV_3K_ORI, fp.WI_DEV_3K_COR, False, False))

    print_log("STEP 5-8. wi dev 1k. For track 3 only.")
    maybe_do(fp.WI_DEV_1K_ORI, m2.m2_to_parallel,
             (sorted(glob(f'{fp.wi_m2}/ABCN.dev.gold.bea19.1k.m2')), fp.WI_DEV_1K_ORI, fp.WI_DEV_1K_COR, False, False))
    """
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
    """
    print_log("STEP 6-6. wi test")
    maybe_do(fp.WI_TEST_SP_ORI, spell.check, (fp.WI_TEST_ORI, fp.WI_TEST_SP_ORI))

    print_log("STEP 6-7. wi dev 3k")
    maybe_do(fp.WI_DEV_3K_SP_ORI, spell.check, (fp.WI_DEV_3K_ORI, fp.WI_DEV_3K_SP_ORI))

    print_log("STEP 6-8. wi dev 1k")
    maybe_do(fp.WI_DEV_1K_SP_ORI, spell.check, (fp.WI_DEV_1K_ORI, fp.WI_DEV_1K_SP_ORI))
    """
    print_log("STEP 6-9. conll 2013")
    maybe_do(fp.CONLL2013_SP_ORI, spell.check, (fp.CONLL2013_ORI, fp.CONLL2013_SP_ORI))

    print_log("STEP 6-10. conll 2014")
    maybe_do(fp.CONLL2014_SP_ORI, spell.check, (fp.CONLL2014_ORI, fp.CONLL2014_SP_ORI))

    # [CONTEXT]
    print_log("STEP 6.5 make context")

    print_log("STEP 6.5-1. fce")
    maybe_do(fp.FCE_SP_CTX, make_sp_context.make_context, (fp.FCE_ORI, fp.FCE_SP_ORI,
                                                           fp.fce_docs, sorted(glob(f'{fp.fce_m2}/*m2')), 3, 3))

    print_log("STEP 6.5-2. lang8")
    maybe_do(fp.LANG8_SP_CTX, make_sp_context.make_context, (fp.LANG8_ORI, fp.LANG8_SP_ORI,
                                                             fp.lang8_docs, None, 3, 3))

    print_log("STEP 6.5-3. nucle")
    maybe_do(fp.NUCLE_SP_CTX, make_sp_context.make_context, (fp.NUCLE_ORI, fp.NUCLE_SP_ORI,
                                                             fp.nucle_docs, sorted(glob(f'{fp.nucle_m2}/*m2')), 3, 3))

    print_log("STEP 6.5-4. wi train")
    maybe_do(fp.WI_TRAIN_SP_CTX, make_sp_context.make_context, (fp.WI_TRAIN_ORI, fp.WI_TRAIN_SP_ORI,
                                                                fp.wi_train_docs, sorted(glob(f'{fp.wi_m2}/*train*m2')), 3, 3))

    print_log("STEP 6.5-5. wi dev")
    maybe_do(fp.WI_DEV_SP_CTX, make_sp_context.make_context, (fp.WI_DEV_ORI, fp.WI_DEV_SP_ORI,
                                                              fp.wi_dev_docs, sorted(glob(f'{fp.wi_m2}/ABCN.dev.gold.bea19.m2')), 3, 3))
    """
    print_log("STEP 6.5-6. wi test")
    maybe_do(fp.WI_TEST_SP_CTX, make_sp_context.make_context, (fp.WI_TEST_ORI, fp.WI_TEST_SP_ORI))

    print_log("STEP 6.5-7. wi dev 3k")
    maybe_do(fp.WI_DEV_3K_SP_CTX, make_sp_context.make_context, (fp.WI_DEV_3K_ORI, fp.WI_DEV_3K_SP_ORI))

    print_log("STEP 6.5-8. wi dev 1k")
    maybe_do(fp.WI_DEV_1K_SP_CTX, make_sp_context.make_context, (fp.WI_DEV_1K_ORI, fp.WI_DEV_1K_SP_ORI))
    """
    print_log("STEP 6.5-9. conll 2013")
    maybe_do(fp.CONLL2013_SP_CTX, make_sp_context.make_context, (fp.CONLL2013_ORI, fp.CONLL2013_SP_ORI,
                                                                 fp.conll2013_docs, sorted(glob(f'{fp.conll2013_m2}/official-preprocessed.m2')), 3, 3))

    print_log("STEP 6.5-10. conll 2014")
    maybe_do(fp.CONLL2014_SP_CTX, make_sp_context.make_context, (fp.CONLL2014_ORI, fp.CONLL2014_SP_ORI,
                                                                 fp.conll2014_docs, sorted(glob(f'{fp.conll2014_m2}/official-2014.combined.m2')), 3, 3))

    """ STEP III: BPE """
    print_log("STEP 7. bpe-tokenize")

    print_log("STEP 7-1. fce")
    maybe_do(fp.FCE_TOK_ORI, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.FCE_SP_ORI, fp.FCE_TOK_ORI))
    maybe_do(fp.FCE_TOK_COR, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.FCE_COR, fp.FCE_TOK_COR))
    maybe_do(fp.FCE_TOK_CTX, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.FCE_SP_CTX, fp.FCE_TOK_CTX))  # [CONTEXT]

    print_log("STEP 7-2. lang8")
    maybe_do(fp.LANG8_TOK_ORI, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.LANG8_SP_ORI, fp.LANG8_TOK_ORI))
    maybe_do(fp.LANG8_TOK_COR, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.LANG8_COR, fp.LANG8_TOK_COR))
    maybe_do(fp.LANG8_TOK_CTX, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.LANG8_SP_CTX, fp.LANG8_TOK_CTX))  # [CONTEXT]

    print_log("STEP 7-3. nucle")
    maybe_do(fp.NUCLE_TOK_ORI, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.NUCLE_SP_ORI, fp.NUCLE_TOK_ORI))
    maybe_do(fp.NUCLE_TOK_COR, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.NUCLE_COR, fp.NUCLE_TOK_COR))
    maybe_do(fp.NUCLE_TOK_CTX, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.NUCLE_SP_CTX, fp.NUCLE_TOK_CTX))  # [CONTEXT]

    print_log("STEP 7-4. wi train")
    maybe_do(fp.WI_TRAIN_TOK_ORI, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.WI_TRAIN_SP_ORI, fp.WI_TRAIN_TOK_ORI))
    maybe_do(fp.WI_TRAIN_TOK_COR, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.WI_TRAIN_COR, fp.WI_TRAIN_TOK_COR))
    maybe_do(fp.WI_TRAIN_TOK_CTX, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.WI_TRAIN_SP_CTX, fp.WI_TRAIN_TOK_CTX))  # [CONTEXT]

    print_log("STEP 7-5. wi dev")
    maybe_do(fp.WI_DEV_TOK_ORI, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.WI_DEV_SP_ORI, fp.WI_DEV_TOK_ORI))
    maybe_do(fp.WI_DEV_TOK_COR, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.WI_DEV_COR, fp.WI_DEV_TOK_COR))
    maybe_do(fp.WI_DEV_TOK_CTX, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.WI_DEV_SP_CTX, fp.WI_DEV_TOK_CTX))  # [CONTEXT]

    """
    print_log("STEP 7-6. wi test")
    maybe_do(fp.WI_TEST_TOK_ORI, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.WI_TEST_SP_ORI, fp.WI_TEST_TOK_ORI))
    # maybe_do(fp.WI_TEST_TOK_COR, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.WI_TEST_COR, fp.WI_TEST_TOK_COR))

    print_log("STEP 7-7. wi dev 3k")
    maybe_do(fp.WI_DEV_3K_TOK_ORI, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.WI_DEV_3K_SP_ORI, fp.WI_DEV_3K_TOK_ORI))
    maybe_do(fp.WI_DEV_3K_TOK_COR, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.WI_DEV_3K_COR, fp.WI_DEV_3K_TOK_COR))
    maybe_do(fp.WI_DEV_3K_TOK_CTX, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.WI_DEV_3K_SP_CTX, fp.WI_DEV_3K_TOK_CTX))

    print_log("STEP 7-8. wi dev 1k")
    maybe_do(fp.WI_DEV_1K_TOK_ORI, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.WI_DEV_1K_SP_ORI, fp.WI_DEV_1K_TOK_ORI))
    maybe_do(fp.WI_DEV_1K_TOK_COR, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.WI_DEV_1K_COR, fp.WI_DEV_1K_TOK_COR))
    maybe_do(fp.WI_DEV_1K_TOK_CTX, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.WI_DEV_1K_SP_CTX, fp.WI_DEV_1K_TOK_CTX))
    """

    print_log("STEP 7-9. conll2013")
    maybe_do(fp.CONLL2013_TOK_ORI, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.CONLL2013_SP_ORI, fp.CONLL2013_TOK_ORI))
    maybe_do(fp.CONLL2013_TOK_COR, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.CONLL2013_COR, fp.CONLL2013_TOK_COR))
    maybe_do(fp.CONLL2013_TOK_CTX, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.CONLL2013_SP_CTX, fp.CONLL2013_TOK_CTX))  # [CONTEXT]

    print_log("STEP 7-10. conll2014")
    maybe_do(fp.CONLL2014_TOK_ORI, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.CONLL2014_SP_ORI, fp.CONLL2014_TOK_ORI))
    maybe_do(fp.CONLL2014_TOK_COR, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.CONLL2014_COR, fp.CONLL2014_TOK_COR))
    maybe_do(fp.CONLL2014_TOK_CTX, bpe.bpe_tokenize, (fp.BPE_MODEL, fp.CONLL2014_SP_CTX, fp.CONLL2014_TOK_CTX))  # [CONTEXT]


