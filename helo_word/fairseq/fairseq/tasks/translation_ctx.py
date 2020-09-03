# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree. An additional grant of patent rights
# can be found in the PATENTS file in the same directory.

"""
Code for supporting context is marked with [CONTEXT].
"""

import itertools
import os

from fairseq import options, utils
from fairseq.data import (
    ConcatDataset,
    data_utils,
    Dictionary,
    IndexedCachedDataset,
    IndexedDataset,
    IndexedRawTextDataset,

    # [CONTEXT]
    # LanguagePairDataset,
    LanguageTripleDataset,
)

from . import FairseqTask, register_task


# [CONTEXT]
# @register_task('translation')
@register_task('translation_ctx')
# [CONTEXT]
# class TranslationTask(FairseqTask):
class TranslationContextTask(FairseqTask):
    """
    Translate from one (source) language to another (target) language.

    Args:
        src_dict (Dictionary): dictionary for the source language
        tgt_dict (Dictionary): dictionary for the target language

    .. note::

        The translation task is compatible with :mod:`fairseq-train`,
        :mod:`fairseq-generate` and :mod:`fairseq-interactive`.

    The translation task provides the following additional command-line
    arguments:

    .. argparse::
        :ref: fairseq.tasks.translation_parser
        :prog:
    """

    @staticmethod
    def add_args(parser):
        """Add task-specific arguments to the parser."""
        # fmt: off
        parser.add_argument('data', nargs='+', help='path(s) to data directorie(s)')
        parser.add_argument('-s', '--source-lang', default=None, metavar='SRC',
                            help='source language')
        parser.add_argument('-t', '--target-lang', default=None, metavar='TARGET',
                            help='target language')
        parser.add_argument('--lazy-load', action='store_true',
                            help='load the dataset lazily')
        parser.add_argument('--raw-text', action='store_true',
                            help='load raw text dataset')
        parser.add_argument('--left-pad-source', default='True', type=str, metavar='BOOL',
                            help='pad the source on the left')
        parser.add_argument('--left-pad-target', default='False', type=str, metavar='BOOL',
                            help='pad the target on the left')
        parser.add_argument('--left-pad-context', default='True', type=str, metavar='BOOL',
                            help='pad the context on the left')  # [CONTEXT]
        parser.add_argument('--max-source-positions', default=1024, type=int, metavar='N',
                            help='max number of tokens in the source sequence')
        parser.add_argument('--max-target-positions', default=1024, type=int, metavar='N',
                            help='max number of tokens in the target sequence')
        # TODO: [CONTEXT] Should set larger?
        parser.add_argument('--max-context-positions', default=1024, type=int, metavar='N',
                            help='max number of tokens in the context sequence')  # [CONTEXT]
        parser.add_argument('--upsample-primary', default=1, type=int,
                            help='amount to upsample primary dataset')
        # fmt: on

    @staticmethod
    # [CONTEXT]/
    # def load_pretrained_model(path, src_dict_path, tgt_dict_path, arg_overrides=None):
    def load_pretrained_model(path, src_dict_path, tgt_dict_path, ctx_dict_path, arg_overrides=None):
        model = utils.load_checkpoint_to_cpu(path)
        args = model['args']
        state_dict = model['model']
        args = utils.override_model_args(args, arg_overrides)
        src_dict = Dictionary.load(src_dict_path)
        tgt_dict = Dictionary.load(tgt_dict_path)
        ctx_dict = Dictionary.load(ctx_dict_path)  # [CONTEXT]/
        # [CONTEXT]/
        # assert src_dict.pad() == tgt_dict.pad()
        # assert src_dict.eos() == tgt_dict.eos()
        # assert src_dict.unk() == tgt_dict.unk()
        assert src_dict.pad() == tgt_dict.pad() == ctx_dict.pad()
        assert src_dict.eos() == tgt_dict.eos() == ctx_dict.eos()
        assert src_dict.unk() == tgt_dict.unk() == ctx_dict.unk()

        # [CONTEXT]/
        # task = TranslationTask(args, src_dict, tgt_dict)
        task = TranslationContextTask(args, src_dict, tgt_dict, ctx_dict)
        model = task.build_model(args)
        model.upgrade_state_dict(state_dict)
        model.load_state_dict(state_dict, strict=True)
        return model

    # [CONTEXT]
    # def __init__(self, args, src_dict, tgt_dict):
    def __init__(self, args, src_dict, tgt_dict, ctx_dict):
        super().__init__(args)
        self.src_dict = src_dict
        self.tgt_dict = tgt_dict
        self.ctx_dict = ctx_dict  # [CONTEXT]

    @classmethod
    def setup_task(cls, args, **kwargs):
        """Setup the task (e.g., load dictionaries).

        Args:
            args (argparse.Namespace): parsed command-line arguments
        """
        args.left_pad_source = options.eval_bool(args.left_pad_source)
        args.left_pad_target = options.eval_bool(args.left_pad_target)
        args.left_pad_context = options.eval_bool(args.left_pad_context)  # [CONTEXT]

        # find language pair automatically
        if args.source_lang is None or args.target_lang is None:
            args.source_lang, args.target_lang = data_utils.infer_language_pair(args.data[0])
        if args.source_lang is None or args.target_lang is None:
            raise Exception('Could not infer language pair, please provide it explicitly')

        # load dictionaries
        ctx_dict = cls.load_dictionary(os.path.join(args.data[0], 'dict.ctx.txt'))  # [CONTEXT]
        src_dict = cls.load_dictionary(os.path.join(args.data[0], 'dict.{}.txt'.format(args.source_lang)))
        tgt_dict = cls.load_dictionary(os.path.join(args.data[0], 'dict.{}.txt'.format(args.target_lang)))
        # [CONTEXT]/
        # assert src_dict.pad() == tgt_dict.pad()
        # assert src_dict.eos() == tgt_dict.eos()
        # assert src_dict.unk() == tgt_dict.unk()
        assert src_dict.pad() == tgt_dict.pad() == ctx_dict.pad()
        assert src_dict.eos() == tgt_dict.eos() == ctx_dict.eos()
        assert src_dict.unk() == tgt_dict.unk() == ctx_dict.unk()
        print('| [{}] dictionary: {} types'.format('ctx', len(ctx_dict)))  # [CONTEXT]
        print('| [{}] dictionary: {} types'.format(args.source_lang, len(src_dict)))
        print('| [{}] dictionary: {} types'.format(args.target_lang, len(tgt_dict)))

        # [CONTEXT]
        # return cls(args, src_dict, tgt_dict)
        return cls(args, src_dict, tgt_dict, ctx_dict)

    def load_dataset(self, split, combine=False, **kwargs):
        """Load a given dataset split.

        Args:
            split (str): name of the split (e.g., train, valid, test)
        """

        def split_exists(split, src, tgt, lang, data_path):
            filename = os.path.join(data_path, '{}.{}-{}.{}'.format(split, src, tgt, lang))
            if self.args.raw_text and IndexedRawTextDataset.exists(filename):
                return True
            elif not self.args.raw_text and IndexedDataset.exists(filename):
                return True
            return False

        def indexed_dataset(path, dictionary):
            if self.args.raw_text:
                return IndexedRawTextDataset(path, dictionary)
            elif IndexedDataset.exists(path):
                if self.args.lazy_load:
                    return IndexedDataset(path, fix_lua_indexing=True)
                else:
                    return IndexedCachedDataset(path, fix_lua_indexing=True)
            return None

        src_datasets = []
        tgt_datasets = []
        ctx_datasets = []  # [CONTEXT]

        data_paths = self.args.data

        for dk, data_path in enumerate(data_paths):
            for k in itertools.count():
                split_k = split + (str(k) if k > 0 else '')

                # infer langcode
                src, tgt = self.args.source_lang, self.args.target_lang
                if split_exists(split_k, src, tgt, src, data_path):
                    prefix = os.path.join(data_path, '{}.{}-{}.'.format(split_k, src, tgt))
                elif split_exists(split_k, tgt, src, src, data_path):
                    prefix = os.path.join(data_path, '{}.{}-{}.'.format(split_k, tgt, src))
                else:
                    if k > 0 or dk > 0:
                        break
                    else:
                        raise FileNotFoundError('Dataset not found: {} ({})'.format(split, data_path))

                src_datasets.append(indexed_dataset(prefix + src, self.src_dict))
                tgt_datasets.append(indexed_dataset(prefix + tgt, self.tgt_dict))
                ctx_datasets.append(indexed_dataset(prefix + 'ctx', self.ctx_dict))  # [CONTEXT]

                print('| {} {} {} examples'.format(data_path, split_k, len(src_datasets[-1])))

                if not combine:
                    break

        # [CONTEXT]/
        # assert len(src_datasets) == len(tgt_datasets)
        assert len(src_datasets) == len(tgt_datasets) == len(ctx_datasets)

        if len(src_datasets) == 1:
            # [CONTEXT]/
            # src_dataset, tgt_dataset = src_datasets[0], tgt_datasets[0]
            src_dataset, tgt_dataset, ctx_dataset = src_datasets[0], tgt_datasets[0], ctx_datasets[0]
        else:
            sample_ratios = [1] * len(src_datasets)
            sample_ratios[0] = self.args.upsample_primary
            src_dataset = ConcatDataset(src_datasets, sample_ratios)
            tgt_dataset = ConcatDataset(tgt_datasets, sample_ratios)
            ctx_dataset = ConcatDataset(ctx_datasets, sample_ratios)  # [CONTEXT]/

        # [CONTEXT]
        # self.datasets[split] = LanguagePairDataset(
        self.datasets[split] = LanguageTripleDataset(
            src_dataset, src_dataset.sizes, self.src_dict,
            tgt_dataset, tgt_dataset.sizes, self.tgt_dict,
            ctx_dataset, ctx_dataset.sizes, self.ctx_dict,  # [CONTEXT]
            left_pad_source=self.args.left_pad_source,
            left_pad_target=self.args.left_pad_target,
            left_pad_context=self.args.left_pad_context,  # [CONTEXT]
            max_source_positions=self.args.max_source_positions,
            max_target_positions=self.args.max_target_positions,
            max_context_positions=self.args.max_context_positions,  # [CONTEXT]
        )

    def build_dataset_for_inference(self, src_tokens, src_lengths):
        # [CONTEXT]/
        # return LanguagePairDataset(src_tokens, src_lengths, self.source_dictionary)
        return LanguageTripleDataset(src_tokens, src_lengths, self.source_dictionary)

    def max_positions(self):
        """Return the max sentence length allowed by the task."""
        # [CONTEXT]/
        # return (self.args.max_source_positions, self.args.max_target_positions)
        return (self.args.max_context_positions, self.args.max_source_positions, self.args.max_target_positions)

    # [CONTEXT]
    @property
    def context_dictionary(self):
        """Return the context :class:`~fairseq.data.Dictionary`."""
        return self.ctx_dict

    @property
    def source_dictionary(self):
        """Return the source :class:`~fairseq.data.Dictionary`."""
        return self.src_dict

    @property
    def target_dictionary(self):
        """Return the target :class:`~fairseq.data.Dictionary`."""
        return self.tgt_dict
