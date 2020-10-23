#!/usr/bin/python3

import sys

assert len(sys.argv) == 3  # *.py, file_name, ratio

trainset_base = sys.argv[1]
ratio = float(sys.argv[2])
assert 0 < ratio < 1

for ext in ('src', 'ctx', 'trg'):
    trainset = f"{trainset_base}.{ext}"
    partial_trainset = f"{trainset_base}_{ratio}.{ext}"

    with open(trainset) as f_r, open(partial_trainset, 'w') as f_w:
        lines = f_r.readlines()

        partial_len = int(len(lines) * ratio)
        partial_lines = lines[:partial_len]

        f_w.write(''.join(partial_lines))
