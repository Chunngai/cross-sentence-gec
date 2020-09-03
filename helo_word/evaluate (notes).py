import argparse
import logging
import os
from tqdm import tqdm

from gec import util
from gec.filepath import Path
from gec.generate import generate
from gec.postprocess import postprocess
from gec.track import choice_track


logging.basicConfig(level=logging.INFO)


def main(args):
    track = choice_track(args.track)

    assert args.subset in track.subsets
    assert bool(args.ckpt_dir) ^ bool(args.ckpt_fpath)
    if args.find_best:
        assert bool(args.ckpt_dir)

    databin_path = track.get_databin_path('pretrain')
    # (NOTE) gold_m2: trg.
    # (NOTE) ori_path: src.
    gold_m2, ori_path, ori_bpe_path, gen_subset, scorer_type = track.get_subset_datapath(args.subset)

    # ckpt_dir
    if args.ckpt_dir is not None:
        # (NOTE) checkpoint_best.pt and checkpoint_last.pt are not included.
        ckpt_files = util.get_sorted_ckpts(args.ckpt_dir)
        # (NOTE) Path of the eval rsts to be stored.
        output_dir = track.get_output_dir(args.ckpt_dir)
    # ckpt_fpath
    else:
        # (NOTE) checkpoint_best.pt and checkpoint_last.pt are not included.
        ckpt_files = [args.ckpt_fpath]
        # (NOTE) Path of the eval rsts to be stored.
        output_dir = track.get_output_dir(args.ckpt_fpath)

    if not args.find_best:
        # (NOTE) Evals all checkpoints for `ckpt_dir` (checkpoint1.pt, checkpoint2.pt, ... ),
        # (NOTE) or the checkpoint file for `ckpt_fpath`.
        for ckpt in tqdm(ckpt_files):
            run_ckpt(databin_path, ckpt, output_dir, scorer_type,
                     gold_m2, ori_path, ori_bpe_path, gen_subset,
                     args.remove_unk_edits, args.remove_error_type_lst,
                     args.apply_rerank, args.preserve_spell, args.max_edits)

    logging.info(f"[Evaluate] highest score on {ori_path}")
    # (NOTE) Finds the best fscore and checkpoint from all the *.report.
    find_best(output_dir, ori_path, scorer_type)


def find_best(output_dir, ori_path, scorer_type):
    if output_dir is None:
        return None, None
    highest_fscore, highest_ckpt = util.find_highest_score(output_dir, ori_path, scorer_type)
    logging.info(f"[Evaluate] highest fscore: {highest_fscore}, ckpt: {highest_ckpt}")
    if highest_fscore == 0 and highest_ckpt == '.pt':
        logging.error(f"[Evaluate] cannot find the highest ckpt")
        exit()
    return highest_fscore, highest_ckpt


def evaluate(scorer_type, ori_file, cor_file, gold_m2_file, report_path):
    if scorer_type == "errant":
        logging.info("[Evaluate] errant")
        scorer = Path.errant

        logging.info("[Evaluate] 1. parallel to m2")
        m2_file = f"{cor_file}.m2"
        prompt = f"python {Path.parallel_to_m2} -orig {ori_file} -cor {cor_file} -out {m2_file}"
        os.system(prompt)

        logging.info("[Evaluate] 2. compare m2")
        prompt = f"python {scorer} -hyp {m2_file} -ref {gold_m2_file} -cat 3 -v | tee {report_path}"
        os.system(prompt)

    elif scorer_type == "m2scorer":
        logging.info("[Evaluate] m2scorer")
        scorer = Path.m2scorer
        prompt = f"python2.7 {scorer} {cor_file} {gold_m2_file} > {report_path}"
        os.system(prompt)


def run_ckpt(databin_path, ckpt, output_dir, scorer_type,
             gold_m2_file, ori_path, ori_bpe_path, gen_subset,
             remove_unk_edits, remove_error_type_lst,
             apply_rerank, preserve_spell, max_edits):

    # (NOTE) Makes the dir for storing outputs of the eval.
    logging.info(f"[Run-ckpt] working on {ckpt}")
    os.makedirs(output_dir, exist_ok=True)

    # (NOTE) Checkpoint name. i.e. checkpoint1.pt.
    ckpt_lst = ckpt.split(":")
    ckpt_basename = ''
    for c in ckpt_lst:
        b = util.get_basename(c, include_path=False, include_extension=False)
        ckpt_basename += b
    # (NOTE) Name of the data. i.e. wi.dev.
    data_basename = util.get_basename(ori_path, include_path=False, include_extension=False)
    # (NOTE) i.e. checkpoint1.wi.dev.
    system_out_basename = os.path.join(output_dir, f"{ckpt_basename}.{data_basename}")

    # (NOTE) Uses fairseq to generate outputs, and stores the rsts in *.out.
    system_out = f"{system_out_basename}.out"
    if not os.path.isfile(system_out):
        logging.info(f"[Run-ckpt] 1. generate into {system_out}")
        # (NOTE) Out: *.out
        # (NOTE) `databin_path`: provides "S" and "T" in *.out.
        # (NOTE) `system_out`: provides "H" in *.out.
        generate(databin_path, ckpt, system_out, ori_path=ori_bpe_path, gen_subset=gen_subset)

    # (NOTE) Extracts the outputs (i.e. hypothesis) to *.cor.
    cor_path = util.get_cor_path(system_out, remove_unk_edits, remove_error_type_lst,
                                 apply_rerank, preserve_spell, max_edits)
    if not os.path.isfile(cor_path):
        logging.info(f"[Run-ckpt] 2. postprocess into {cor_path}")
        # (NOTE) Out: *.cor
        # (NOTE) Generates *.out.pred and *.out._m2
        postprocess(ori_path, system_out, cor_path, remove_unk_edits, remove_error_type_lst,
                    apply_rerank, preserve_spell, max_edits)

    # (NOTE) Evals / Scores using the scorer.
    report_path = f"{util.get_basename(cor_path, include_extension=False)}.report"
    if not os.path.isfile(report_path):
        logging.info(f"[Run-ckpt] 3. evaluation into {report_path}")
        # (NOTE) Out: *.report
        # (NOTE) Generates *cor.m2
        if scorer_type is not None and gold_m2_file is not None:
            evaluate(scorer_type, ori_path, cor_path, gold_m2_file, report_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--track", type=int, required=True)
    parser.add_argument("--subset", type=str, required=True)

    parser.add_argument("--ckpt-dir", type=str, default=None)
    parser.add_argument("--ckpt-fpath", type=str, default=None)

    parser.add_argument("--remove-unk-edits", action="store_true")
    parser.add_argument("--remove-error-type-lst", type=str, nargs="+", default=[], help="error types to be removed (e.g.. R:OTHER)")
    parser.add_argument("--apply-rerank", action="store_true", help="do the lm score rerank")
    parser.add_argument("--preserve-spell", action="store_true", help="preserve spelling correction during the lm rerank")
    parser.add_argument("--max-edits", type=int, default=None, help="max edit distance during the lm rerank")  # (MODIFIED) max_edits -> max-edits

    parser.add_argument("--find-best", action="store_true")

    args = parser.parse_args()

    main(args)
