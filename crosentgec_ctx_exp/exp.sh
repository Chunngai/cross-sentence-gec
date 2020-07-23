#!/bin/bash

set -e
set -x

tmp_dir=data/tmp

sudo python2 scripts/sentence_pairs_with_ctx.py --train --tokenize --maxtokens 80 --mintokens 1 --input $tmp_dir/lang8-train.xml  \
        --src-ctx $tmp_dir/lang8.src-trg.ctx --src-src $tmp_dir/lang8.src-trg.src --trg-trg $tmp_dir/lang8.src-trg.trg

sudo python2 scripts/sentence_pairs_with_ctx_modified.py --train --tokenize --maxtokens 80 --mintokens 1 --input $tmp_dir/lang8-train.xml  \
        --src-ctx $tmp_dir/lang8.src-trg.ctx_ --src-src $tmp_dir/lang8.src-trg.src_ --trg-trg $tmp_dir/lang8.src-trg.trg_

echo ------
diff $tmp_dir/lang8.src-trg.ctx $tmp_dir/lang8.src-trg.ctx_

echo ------
diff $tmp_dir/lang8.src-trg.src $tmp_dir/lang8.src-trg.src_

echo ------
diff $tmp_dir/lang8.src-trg.trg $tmp_dir/lang8.src-trg.trg_