import argparse
import logging
import os

from gec.track import choice_track
from gec import util

logging.getLogger().setLevel(logging.INFO)


def main(args):
    track = choice_track(args.track)

    assert args.train_mode in track.train_modes
    if args.train_mode == 'pretrain':
        assert args.prev_model_output_dir is None

    # (NOTE) Data used for training.
    databin_path = track.get_databin_path(args.train_mode)
    # (NOTE) Config.
    model_config = track.get_model_config(args.model, args.lr, args.dropout, args.max_epoch, args.seed, args.reset)
    # (NOTE) NAME of the checkpoint dir.
    ckpt_dir = track.get_ckpt_dir(args.train_mode, args.model, args.lr, args.dropout, args.seed,
                                  args.prev_model_output_dir)
    # (NOTE) Path of the checkpoint to be restored.
    _, ori_path, _, _, scorer_type = track.get_subset_datapath('valid')
    fscore, restore_ckpt = find_restore(args.prev_model_output_dir, ori_path, scorer_type)

    train(databin_path, model_config, ckpt_dir, restore_ckpt, args.ngpu)


def train(databin_path, model_config, ckpt_dir, restore_ckpt, ngpu):

    # (NOTE) Makes the dir for storing checkpoints generated during training.
    os.makedirs(ckpt_dir, exist_ok=True)
    logging.info(f"[Train] working on {ckpt_dir}")

    # (NOTE) Uses distributed training or normal training depending on the number of available gpus,
    if ngpu > 1:
        prompt = f"python -m torch.distributed.launch --nproc_per_node {ngpu} $(which fairseq-train) {databin_path} " \
                 f"{model_config} --save-dir {ckpt_dir} "
    else:
        prompt = f"fairseq-train {databin_path} {model_config} --save-dir {ckpt_dir} "
    logging.info(f"[Train] {prompt}")

    # (NOTE) If a restore checkpoint is provided, appends it to the command (that is, `prompt`) to be executed.
    if restore_ckpt is not None:
        # (MODIFIED) #5
        # finetune_ckpt = os.path.basename(util.change_ckpt_dir(restore_ckpt, ckpt_dir))
        finetune_ckpt = util.change_ckpt_dir(restore_ckpt, ckpt_dir)

        # (NOTE) Makes it checkpoint1.pt.
        logging.info(f"[Train] copy the ckpt {restore_ckpt} into {finetune_ckpt}")
        os.system(f"cp {restore_ckpt} {finetune_ckpt}")

        prompt += f"--restore-file {finetune_ckpt} "

    # (NEW) Train log.
    prompt += f" | tee -a {os.path.join(ckpt_dir, 'train.log')}"

    # (NOTE) Runs the command.
    os.system(prompt)  # (NOTE) The checkpoint of each epoch is saved,
                       # along with checkpoint_best.pt and checkpoint_last.pt.


def find_restore(prev_model_output_dir, ori_path, scorer_type):
    if prev_model_output_dir is None:
        return None, None
    highest_fscore, highest_ckpt = util.find_highest_score(prev_model_output_dir, ori_path, scorer_type)
    logging.info(f"[Train] highest fscore: {highest_fscore}, ckpt: {highest_ckpt}")
    if highest_fscore == 0 and highest_ckpt == '.pt':
        logging.error(f"[Train] cannot find the highest ckpt")
        exit()
    return highest_fscore, highest_ckpt


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--track", type=int, required=True)
    parser.add_argument("--train-mode", type=str, required=True)
    parser.add_argument("--model", type=str, required=True)
    parser.add_argument("--ngpu", type=int, required=True)

    parser.add_argument("--lr", type=float, default=5e-4)
    parser.add_argument("--dropout", type=float, default=0.3)
    parser.add_argument("--max-epoch", type=int, default=5)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--reset", action='store_true')  # (NOTE) Resets the optimizer and lr scheduler.

    parser.add_argument("--prev-model-output-dir", type=str, default=None)

    args = parser.parse_args()

    main(args)
