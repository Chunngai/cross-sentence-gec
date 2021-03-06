#!/bin/bash

set -x
set -e

if [ $# -lt 1 ]; then
    echo "`basename $0` <seedval> <optional-gpu-num>"
    exit 1
fi

## setting paths
################

SEED=$1
EXP_NAME=crosent
OUT_DIR=training/$EXP_NAME  # training/crosent
MODEL_DIR=$OUT_DIR/models/model$SEED/  # training/crosent/models/model$SEED

mkdir -p $MODEL_DIR

FAIRSEQPY=fairseq
APPLYBPE=scripts/apply_bpe.py  # Not used in the script.
BPE_MODEL=models/bpe/mlconvgec_aaai18_bpe.model  # Not used in the script.
DATA_DIR=data/processed
EMBED_PATH=models/embed/model.vec
DECODER_INIT_PATH=$PWD/models/decoder/lm.pt

## training
############

if [ $# -eq 1 ] ; then
    DEVICE=0
else
    DEVICE=$2
fi

TRAIN_LOG=$MODEL_DIR/train.log.txt
echo "MACHINE: `hostname` |  GPU: $DEVICE" | tee -a $TRAIN_LOG
echo "START TIME: `date`" | tee -a $TRAIN_LOG

# Extended fairseq:
# --arch fconv_dualenc_gec_gateaux
# --task translation_ctx
#
# Meaning of some opts:
# --update-freq: see https://fairseq.readthedocs.io/en/latest/getting_started.html?highlight=update-freq#large-mini-batch-training-with-delayed-updates
PYTHONPATH=$FAIRSEQPY:$PYTHONPATH CUDA_VISIBLE_DEVICES=$DEVICE python3 -u $FAIRSEQPY/train.py \
    --encoder-layers '[(1024,3)] * 7' --decoder-layers '[(1024,3)] * 7' \
    --encoder-embed-dim 500 --decoder-embed-dim 500  --decoder-out-embed-dim 500 \
    --encoder-embed-path $EMBED_PATH --decoder-embed-path $EMBED_PATH \
    --arch fconv_dualenc_gec_gatedaux --auxencoder-embed-dim 500 --auxencoder-embed-path $EMBED_PATH --auxencoder-layers '[(1024,3)] * 3' --task translation_ctx \
    --dropout 0.2 --clip-norm 0.1 --lr 0.25 --min-lr 1e-4 \
    --momentum 0.99 --max-epoch 100 --batch-size 48 --update-freq 2 \
    --no-progress-bar --seed $SEED --no-epoch-checkpoints \
    --criterion label_smoothed_cross_entropy --label-smoothing 0.1  \
    --source-token-dropout 0.2 \
    --restore-file $DECODER_INIT_PATH \
    --raw-text \
    --save-dir $MODEL_DIR $DATA_DIR | tee -a $TRAIN_LOG

echo "END TIME: `date`" | tee -a $TRAIN_LOG


