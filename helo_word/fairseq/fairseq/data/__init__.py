###############################################################################
# CUSTOM MODULE DEFINITION FOR GEC
###############################################################################

# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree. An additional grant of patent rights
# can be found in the PATENTS file in the same directory.

"""
Code for supporting context is marked with [CONTEXT].
"""

from .dictionary import Dictionary, TruncatedDictionary
from .fairseq_dataset import FairseqDataset
from .backtranslation_dataset import BacktranslationDataset
from .concat_dataset import ConcatDataset
from .indexed_dataset import IndexedCachedDataset, IndexedDataset, IndexedRawTextDataset
from .language_pair_dataset import LanguagePairDataset
from .language_triple_dataset import LanguageTripleDataset  # [CONTEXT]
from .monolingual_dataset import MonolingualDataset
from .round_robin_zip_datasets import RoundRobinZipDatasets
from .token_block_dataset import TokenBlockDataset
from .transform_eos_dataset import TransformEosDataset

"""Custom datasets for GEC"""
from .token_labeled_language_pair_dataset import (
    TokenLabeledIndexedRawTextDataset, TokenLabeledLanguagePairDataset
)

from .iterators import (
    CountingIterator,
    EpochBatchIterator,
    GroupedIterator,
    ShardedIterator,
)

__all__ = [
    'BacktranslationDataset',
    'ConcatDataset',
    'CountingIterator',
    'Dictionary',
    'EpochBatchIterator',
    'FairseqDataset',
    'GroupedIterator',
    'IndexedCachedDataset',
    'IndexedDataset',
    'IndexedRawTextDataset',
    'LanguagePairDataset',
    'LanguageTripleDataset',  # [CONTEXT]
    'MonolingualDataset',
    'RoundRobinZipDatasets',
    'ShardedIterator',
    'TokenBlockDataset',
    'TransformEosDataset',
    'TokenLabeledIndexedRawTextDataset',
    'TokenLabeledLanguagePairDataset'
]
