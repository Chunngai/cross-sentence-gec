import os
import json
import re
from typing import List
from glob import glob

from gec import filepath

basename = os.path.basename
splitext = os.path.splitext


def remove_spaces(text: str) -> str:
    """Remove spaces in the text.

    Args:
        text: The text from which spaces will be removed. E.g. "This is a sentence."

    Returns: A string with all spaces removed. E.g. "Thisisasentence."
    """

    return "".join(text.split())


def sentence_in_raw_document(sentence: str, raw_document: str) -> bool:
    """Check if the sentence is in the document.

    Args:
        sentence: A sentence that may be in the raw document.
        raw_document: A raw document that may contain the sentence.

    Returns: True if the sentence is in the raw document, else False.

    `sentence` is from a .m2 file and tokenized, while `raw_document` is from a .json or .sgml file
    whose sentences are not tokenized. Spaces in both the sentence and the document are removed
    to avoid differences resulted from tokenization.
    """

    return remove_spaces(sentence) in remove_spaces(raw_document)


def get_tokenized_sentences_from_m2_files(m2_file_paths: List[str]) -> List[str]:
    """Get all source sentences in .m2 files (those beginning with "S "), which have been tokenized.

    Args:
        m2_file_paths: Paths of .m2 files containing tokenized sentences.

    Returns: A list containing all source sentences.
    """

    sentence_start_index = 2
    tokenized_sentences: List[str] = []
    for m2_file_path in m2_file_paths:
        with open(m2_file_path) as m2_file:
            for line in m2_file.readlines():
                if line.startswith("S "):  # "S " marks the start of a sentence.
                    tokenized_sentence = line[sentence_start_index:].strip()  # Removes the trailing linefeed.
                    tokenized_sentences.append(tokenized_sentence)

    return tokenized_sentences


def get_documents_from_json(document_file_paths: List[str], m2_file_paths: List[str]) -> List[List[str]]:
    """Get documents from .json files.

    Args:
        document_file_paths: Paths of .json files containing documents.
        m2_file_paths: Paths of .m2 files containing tokenized sentences.

    Returns: A list containing all documents, whose sentences are tokenized.

    The .json files contain sentences in document-level, but the sentences are not tokenized.
    Thus the corresponding .m2 files are used to get the tokenized version of the sentences
    and to construct documents with tokenized sentences.
    """

    def _normalize(text: str) -> str:
        """Normalize the input by replacing the keys in a norm dict by the corresponding values.

        Args:
            text: The text to be normalized.

        Returns: A normalized string.
        """
        norm_dict = {"’": "'",
                     "´": "'",
                     "‘": "'",
                     "′": "'",
                     "`": "'",
                     '“': '"',
                     '”': '"',
                     '˝': '"',
                     '¨': '"',
                     '„': '"',
                     '『': '"',
                     '』': '"',
                     '–': '-',
                     '—': '-',
                     '―': '-',
                     '¬': '-',
                     '、': ',',
                     '，': ',',
                     '：': ':',
                     '；': ';',
                     '？': '?',
                     '！': '!',
                     'ِ': ' ',
                     '\u200b': ' '}
        norm_dict = {ord(k): v for k, v in norm_dict.items()}
        return text.translate(norm_dict)

    # Extracts tokenized sentences.
    tokenized_sentences = get_tokenized_sentences_from_m2_files(m2_file_paths=m2_file_paths)

    # Extracts documents.
    documents: List[List[str]] = []
    current_tokenized_sentence_index = 0
    current_tokenized_sentence = tokenized_sentences[current_tokenized_sentence_index]
    for document_file_path in document_file_paths:
        with open(document_file_path) as document_file:
            # Each line in the document file is a json object.
            raw_json_objects: List[str] = document_file.readlines()

            for raw_json_object in raw_json_objects:
                json_object = json.loads(raw_json_object)

                # Gets a raw document (simple text) and normalizes it.
                raw_document: str = json_object["text"]
                normalized_raw_document: str = _normalize(raw_document)

                # Constructs a document.
                document: List[str] = []
                partial_normalized_raw_document_spaces_removed = remove_spaces(normalized_raw_document)
                while sentence_in_raw_document(sentence=current_tokenized_sentence,
                                               raw_document=partial_normalized_raw_document_spaces_removed):
                    document.append(current_tokenized_sentence)

                    # Prevents sentences in the next document
                    # from being recognized as sentences in the current document.
                    # E.g. a sentence exists in 2 consecutive documents.
                    partial_normalized_raw_document_spaces_removed = \
                        partial_normalized_raw_document_spaces_removed.replace(
                            remove_spaces(current_tokenized_sentence), "", 1
                        )

                    # Ready to evaluate the next tokenized sentence.
                    current_tokenized_sentence_index += 1
                    try:
                        current_tokenized_sentence = tokenized_sentences[current_tokenized_sentence_index]
                    except IndexError:  # When the error occurs, the last sentence has been evaluated.
                        break

                documents.append(document)

    return documents


def get_documents_from_sgml(document_file_paths: List[str], m2_file_paths: List[str],
                            dataset_name: str) -> List[List[str]]:
    """Get documents from .sgml files.

    Args:
        document_file_paths: Paths of .sgml files containing documents.
        m2_file_paths: Paths of .m2 files containing tokenized sentences.
        dataset_name: The name of the dataset. (conll2013 / conll2014 / nucle)

    Returns: A list containing all documents, whose sentences are tokenized.

    The .sgml files contain sentences in document-level. Sentences in the .sgml files are not tokenized,
    thus the corresponding .m2 files are used to get the tokenized version of the sentences
    and to construct documents with tokenized sentences.
    """

    # Extracts tokenized sentences.
    tokenized_sentences = get_tokenized_sentences_from_m2_files(m2_file_paths=m2_file_paths)

    # Extracts documents.
    documents: List[List[str]] = []
    current_tokenized_sentence_index = 0
    current_tokenized_sentence = tokenized_sentences[current_tokenized_sentence_index]
    for document_file_path in document_file_paths:
        with open(document_file_path) as document_file:
            raw_sgml: str = document_file.read()

            # Fixes a parsing error in nucle.
            if dataset_name == "nucle":
                raw_sgml = raw_sgml.replace(
                    "<nuclearstreet.com/files/folders/1654/download.aspx>",
                    "nuclearstreet.com/filesfolders/1654/download.aspx>"
                )

            doc_pattern = re.compile(r"<DOC.+?/DOC>", flags=re.DOTALL)
            docs = doc_pattern.findall(raw_sgml)
            for doc in docs:
                # nid_pattern = re.compile(r'<DOC nid="(\d+)">')
                # nid = nid_pattern.search(doc).group(1)

                partial_raw_document: str = ""

                title_pattern = re.compile(r"<TITLE>(.+?)</TITLE>", flags=re.DOTALL)
                try:
                    title = title_pattern.search(doc).group(1).strip()
                except AttributeError:
                    pass
                else:
                    partial_raw_document += title

                p_pattern = re.compile(r"<P>(.+?)</?P>", flags=re.DOTALL)
                paras: List[str] = [para.strip() for para in p_pattern.findall(doc)]
                partial_raw_document += " ".join(paras)

                # Fixes parsing errors in nucle caused by "<...>".
                if dataset_name == "nucle":
                    fake_tag_pattern = re.compile(r"<[^{|^\s].+?>")
                    partial_raw_document = fake_tag_pattern.sub("", partial_raw_document)

                partial_raw_document_spaces_removed = remove_spaces(partial_raw_document)

                # Constructs a document.
                document: List[str] = []
                while sentence_in_raw_document(sentence=current_tokenized_sentence,
                                               raw_document=partial_raw_document_spaces_removed):
                    document.append(current_tokenized_sentence)

                    # Prevents sentences in the next document
                    # from being recognized as sentences in the current document.
                    # E.g. a sentence exists in 2 consecutive documents.
                    partial_raw_document_spaces_removed = partial_raw_document_spaces_removed.replace(
                        remove_spaces(current_tokenized_sentence), "", 1)

                    # Ready to evaluate the next tokenized sentence.
                    current_tokenized_sentence_index += 1
                    try:
                        current_tokenized_sentence = tokenized_sentences[current_tokenized_sentence_index]
                    except IndexError:  # When the error occurs, the last sentence has been evaluated.
                        break

                documents.append(document)

    return documents


def get_documents_from_lang8_entries_train(document_file_paths: List[str]) -> List[List[str]]:
    """Get documents from the training set of lang8-english "entries.train".

    Args:
        document_file_paths: Contains a single path which is the path of "entries.train".

    Returns: A list containing all documents, whose sentences are tokenized.

    Sentences in "entries.train" are well tokenized, thus .m2 files are not needed to get tokenized sentences.
    """

    # Extracts documents.
    documents: List[List[str]] = []
    for document_file_path in document_file_paths:
        with open(document_file_path) as document_file:
            lines: List[str] = document_file.readlines()

            # Constructs a document.
            document: List[str] = []
            for line in lines:
                try:
                    document_sentence = line.split("\t")[4].strip()
                    document.append(document_sentence)
                except IndexError:  # An '\n' separating 2 documents.
                    documents.append(document)
                    document = []

    return documents


def get_documents(document_file_paths: List[str], m2_file_paths: List[str], raw_ori_file_path: str) -> List[List[str]]:
    """Get documents according to the dataset.

    Args:
        document_file_paths: Paths of files containing documents. (.json / .sgml / "entries.train")
        m2_file_paths: Paths of .m2 files containing tokenized sentences.
        raw_ori_file_path: The path of raw/{DATASET_NAME}.ori.

    Returns: A list of documents with all sentences tokenized.

    Documents of fce, wi.train, wi.dev are saved in .json format;
    documents of conll2013, conll2014 and nucle are saved in .sgml format;
    documents of lang8 are saved in "entries.train".
    """

    # Gets the name of the dataset.
    dataset_name = splitext(basename(raw_ori_file_path))[0]

    if dataset_name in ["fce", "wi.train", "wi.dev"]:  # json.
        return get_documents_from_json(document_file_paths, m2_file_paths)
    elif dataset_name in ["conll2013", "conll2014", "nucle"]:  # sgml.
        return get_documents_from_sgml(document_file_paths, m2_file_paths, dataset_name)
    else:  # lang8.
        return get_documents_from_lang8_entries_train(document_file_paths)


def get_context(document_level_index: int, document: List[str],
                previous_sentences_number: int, following_sentences_number: int,
                previous_context_tag: str, following_context_tag: str) -> str:
    """Get the context of the sentence.

    Args:
        document_level_index: The index of the sentence in document-level.
        document: The document containing the sentence.
        previous_sentences_number: The number of previous context sentences.
        following_sentences_number: The number of following context sentences.
        following_context_tag: The tag for indicating a previous context sentence.
        previous_context_tag: The tag for indicating a following context sentence.

    Returns: The concatenation of context sentences, separated by tags
    (`previous_context_tag` for previous context sentences and `following_context_tag` for following context sentences.

    E.g.
    If `document` is [
        "Guten Tag !",
        "Guten Tag !",
        "Wie geht 's ?",
        "Gut . Und dir ?",
        "Gut .",
        "Einen schoenen Tag noch !",
        "Gleichfalls !"
    ],
    `document_level_index` is 2, `previous_sentences_number` and `following_sentences_number` are both 3,
    the sentence querying for context is document[2], i.e. "Wie geht 's ?".
    Its previous context should be the first and the second sentences
    (2 previous sentences here, not 3, since there are only 2 sentences before the querying sentence,
    and the document boundary cannot be crossed),
    and its following context should be the forth, fifth and sixth sentences.
    And context to be returned is:
    "<prev> Guten Tag ! <prev> Guten Tag ! <fol> Gut . Und dir ? <fol> Gut . <fol> Einen schoenen Tag noch !".
    """

    def _is_valid_document_level_index(document_level_index: int, document: List[str]) -> bool:
        """Check if the document-level index is valid.

        Args:
            document_level_index: The document-level index of a sentence.
            document: The document containing a sentence corresponding to the document-level index.

        Returns: True if the index is valid, else False.

        Negative indices, which may be generated when making previous context,
        are not allowed, as corresponding sentences are following context
        for the sentence being evaluated.
        """
        return 0 <= document_level_index < len(document)

    # Gets previous context.
    previous_context_sentences = ""
    for previous_context_sentence_index in range(document_level_index - previous_sentences_number,
                                                 document_level_index):
        if _is_valid_document_level_index(document_level_index=previous_context_sentence_index, document=document):
            previous_context_sentence = document[previous_context_sentence_index]
            previous_context_sentences = f"{previous_context_sentences} " \
                                         f"{previous_context_tag} {previous_context_sentence}"

    # Gets following context.
    following_context_sentences = ""
    for following_context_sentence_index in range(document_level_index + 1,
                                                  document_level_index + following_sentences_number + 1):
        if _is_valid_document_level_index(document_level_index=following_context_sentence_index, document=document):
            following_context_sentence = document[following_context_sentence_index]
            following_context_sentences = f"{following_context_sentences} " \
                                          f"{following_context_tag} {following_context_sentence}"

    context = previous_context_sentences + following_context_sentences

    return context


def make_context(raw_ori_file_path: str, document_file_paths: List[str], m2_file_paths: List[str],
                 previous_sentences_number: int = 1, following_sentences_number: int = 0,
                 previous_context_tag: str = "<prev>", following_context_tag: str = "<fol>"):
    """Create a context file for a dataset.

    Args:
        raw_ori_file_path: The path of raw/{DATASET_NAME}.ori.
        document_file_paths: Paths of files containing documents. (.json / .sgml / "entries.train")
        m2_file_paths: Paths of .m2 files containing tokenized sentences.
        previous_sentences_number: The number of previous context sentences, 1 by default.
        following_sentences_number: The number of following context sentences, 0 by default.
        previous_context_tag: The tag indicating a previous context sentence, <prev> by default.
        following_context_tag: The tag indicating a following context sentence, <fol> by default.
    """

    # Gets all sentences from `raw_ori_file_path`.
    with open(raw_ori_file_path) as raw_ori_file:
        raw_ori_sentences = raw_ori_file.readlines()

    # Gets all documents.
    documents: List[List[str]] = get_documents(document_file_paths=document_file_paths, m2_file_paths=m2_file_paths,
                                               raw_ori_file_path=raw_ori_file_path)

    # Saves documents.
    if save_documents:
        document_path = f"{splitext(raw_ori_file_path)[0]}.doc_"
        with open(f"{document_path}", 'w') as f:
            for i in range(len(documents)):
                f.write(f"{i}\t")
                f.write(str(documents[i]))
                f.write("\n\n")

    # Gets the path of the context file.
    raw_ori_file_path_without_extension = splitext(raw_ori_file_path)[0]
    raw_ctx_file_path = f"{raw_ori_file_path_without_extension}.ctx"

    # Gets context for each sentence in .ori.
    current_document_index = 0
    current_document: List[str] = documents[current_document_index]
    current_document_masked: List[str] = current_document[:]
    previous_raw_ori_sentence = None
    previous_raw_ori_sentence_document_level_index = None
    with open(raw_ctx_file_path, "w") as raw_ctx_file:
        for raw_ori_sentence in raw_ori_sentences:
            raw_ori_sentence = raw_ori_sentence.strip()

            # There are some sentences that are the same in lang8.ori,
            # which share document level index & context.
            # There is also a sentence pair in wi.train.ori and a pair in wi.dev.ori
            # which are the same and adjacent.
            # They also share document level index & context.
            if raw_ori_sentence != previous_raw_ori_sentence:
                # In most cases the loop will be executed only once.
                # But for nucle the loop may be executed twice
                # when no sentence is wrong in a document in nucle
                # since correct sentences in the m2 file of nucle
                # are ignored when creating nucle.ori.
                while raw_ori_sentence not in current_document_masked:
                    current_document_index += 1
                    current_document = documents[current_document_index]
                    current_document_masked: List[str] = current_document[:]

                # Gets the document-level index of the sentence.
                try:
                    document_level_index = current_document_masked.index(raw_ori_sentence)
                except ValueError:
                    # print(raw_ori_sentence)
                    # print(remove_spaces(raw_ori_sentence))
                    # print(current_document_masked_spaces_removed)
                    raise
            else:
                document_level_index = previous_raw_ori_sentence_document_level_index

            previous_raw_ori_sentence = raw_ori_sentence
            previous_raw_ori_sentence_document_level_index = document_level_index

            # Prevents sentences in the next document from being recognized as sentences in the current document.
            # E.g. a sentence exists in 2 consecutive documents.
            current_document_masked[document_level_index] = ""

            # Gets the context of the current sentence.
            context = get_context(document_level_index=document_level_index, document=current_document,
                                  previous_sentences_number=previous_sentences_number,
                                  following_sentences_number=following_sentences_number,
                                  previous_context_tag=previous_context_tag,
                                  following_context_tag=following_context_tag)

            # Writes the context to file.
            raw_ctx_file.write(context)
            raw_ctx_file.write("\n")


if __name__ == '__main__':

    fp = filepath.FilePath()

    # fce.
    fce_raw_ori_path = fp.FCE_ORI
    fce_doc_paths = sorted(glob("/home/neko/GEC/helo_word-master_restricted/data/bea19/fce/json/fce.*.json"))
    fce_m2_paths = sorted(glob(f'{fp.fce_m2}/*m2'))

    # wi train.
    wi_train_raw_ori_path = fp.WI_TRAIN_ORI
    wi_train_doc_paths = [
        "/home/neko/GEC/helo_word-master_restricted/data/bea19/wi+locness/json/A.train.json",
        "/home/neko/GEC/helo_word-master_restricted/data/bea19/wi+locness/json/A.train.json",
        "/home/neko/GEC/helo_word-master_restricted/data/bea19/wi+locness/json/B.train.json",
        "/home/neko/GEC/helo_word-master_restricted/data/bea19/wi+locness/json/C.train.json",
        "/home/neko/GEC/helo_word-master_restricted/data/bea19/wi+locness/json/B.train.json",
        "/home/neko/GEC/helo_word-master_restricted/data/bea19/wi+locness/json/C.train.json",
    ]
    wi_train_m2_paths = sorted(glob(f'{fp.wi_m2}/*train*m2'))

    # wi dev.
    wi_dev_raw_ori_path = fp.WI_DEV_ORI
    wi_dev_doc_paths = sorted(glob("/home/neko/GEC/helo_word-master_restricted/data/bea19/wi+locness/json/*.dev.json"))
    wi_dev_m2_paths = sorted(glob(f'{fp.wi_m2}/ABCN.dev.gold.bea19.m2'))

    # conll2013.
    conll2013_raw_ori_path = fp.CONLL2013_ORI
    conll2013_doc_paths = sorted(
        glob("/home/neko/GEC/helo_word-master_restricted/data/conll2013/release2.3.1/revised/data/official.sgml"))
    conll2013_m2_paths = sorted(glob(f'{fp.conll2013_m2}/official-preprocessed.m2'))

    # conll2014.
    conll2014_raw_ori_path = fp.CONLL2014_ORI
    conll2014_doc_paths = sorted(glob(
        "/home/neko/GEC/helo_word-master_restricted/data/conll2014/conll14st-test-data/noalt/official-2014.0.sgml"))
    conll2014_m2_paths = sorted(glob(f'{fp.conll2014_m2}/official-2014.combined.m2'))

    # nucle.
    nucle_raw_ori_path = fp.NUCLE_ORI
    nucle_doc_paths = sorted(glob("/home/neko/GEC/helo_word-master_restricted/data/bea19/nucle3.3/data/nucle3.2.sgml"))
    nucle_m2_paths = sorted(glob(f'{fp.nucle_m2}/*m2'))

    # lang8.
    lang8_raw_ori_path = fp.LANG8_ORI
    # TODO: entries.train is in lang8_en, and it should be included in the datasets.
    lang8_doc_paths = sorted(glob("/home/neko/GEC/helo_word-master_restricted/data/bea19/lang8.bea19/entries.train"))
    lang8_m2_paths = None

    # ------

    save_documents = True

    # Single dataset.
    # ori_path = lang8_raw_ori_path
    # doc_paths = lang8_doc_paths
    # m2_paths = lang8_m2_paths

    n_prev = 3
    n_fol = 3

    #     make_context(ori_path, doc_paths, m2_paths, n_prev, n_fol)

    # Batch testing.
    correct_ver = {
        "fce": 3,
        "wi.train": 4,
        "wi.dev": 4,
        "conll2013": 3,
        "conll2014": 3,
        "nucle": 2,
        "lang8": 3
    }

    for dataset in [
        "fce", "wi_train", "wi_dev",
        "conll2013", "conll2014", "nucle",
        "lang8"
    ]:
        make_context(eval(f"{dataset}_raw_ori_path"),
                     eval(f"{dataset}_doc_paths"),
                     eval(f"{dataset}_m2_paths"),
                     n_prev, n_fol)

        # dataset = ".".join(dataset.split("_"))
        # with open(f"/home/neko/GEC/helo_word-master_restricted/data/parallel/raw/{dataset}.ctx") as f_ctx, \
        #         open(f'/home/neko/GEC/helo_word-master_restricted/data/parallel/raw/{dataset}.'
        #              f'ctx_v{correct_ver[dataset]}_correct') as f_ctx_correct:
        #     print(f"{dataset}: {f_ctx.read() == f_ctx_correct.read()}")
