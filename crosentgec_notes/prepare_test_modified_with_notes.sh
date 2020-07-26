#!/bin/bash

# This scripts prepares test data for cross-sentence GEC.

set -e
set -x

if [ ! -d data/tmp ]
then
	mkdir -p data/tmp
fi
tmp_dir=data/tmp

# CoNLL-2014
#############
# downloading test data files
wget http://www.comp.nus.edu.sg/~nlp/conll14st/conll14st-test-data.tar.gz -O $tmp_dir/conll14st.tar.gz

# uncompressing the files
tar -zxvf $tmp_dir/conll14st.tar.gz -C $tmp_dir/
test_dir=$tmp_dir/conll14st-test-data

mkdir -p data/test/conll14st-test
out_dir=data/test/conll14st-test
python2 $test_dir/scripts/preprocess.py -l $test_dir/noalt/official-2014.0.sgml \
	$tmp_dir/conll14st-test.0.conll $tmp_dir/conll14st-test.0.conll.ann $tmp_dir/conll14st-test.0.conll.m2
python3 scripts/nucle_preprocess.py $tmp_dir/conll14st-test.0.conll $tmp_dir/conll14st-test.0.conll.m2 $tmp_dir/conll14st-test.0.xml
python2 scripts/sentence_pairs_with_ctx.py --test --input $tmp_dir/conll14st-test.0.xml \
	--src-ctx $out_dir/conll14st-test.tok.ctx --src-src $out_dir/conll14st-test.tok.src --trg-trg $tmp_dir/conll14st-test.0.tok.trg

# Note that the .m2 file in conll14-test is inconsistent with the .conll file in it.
#
# .m2:
# S Through those sites we are able to talk to them , to know what their activities are and who their friends are , etc. From the surface point of view it is no doubt that these sites help us to have a better relationship with our relatives despite of the distance .
# A 1 2|||Pform|||these|||REQUIRED|||-NONE-|||0
# A 25 26|||ArtOrDet|||a|||REQUIRED|||-NONE-|||0
# A 26 27|||Wci|||superficial|||REQUIRED|||-NONE-|||0
# A 30 30|||Mec|||,|||REQUIRED|||-NONE-|||0
# A 48 49|||Trans||||||REQUIRED|||-NONE-|||0
#
# .conll:
#
# 42	1	1	0	Through
# 42	1	1	1	those
# 42	1	1	2	sites
# 42	1	1	3	we
# 42	1	1	4	are
# 42	1	1	5	able
# 42	1	1	6	to
# 42	1	1	7	talk
# 42	1	1	8	to
# 42	1	1	9	them
# 42	1	1	10	,
# 42	1	1	11	to
# 42	1	1	12	know
# 42	1	1	13	what
# 42	1	1	14	their
# 42	1	1	15	activities
# 42	1	1	16	are
# 42	1	1	17	and
# 42	1	1	18	who
# 42	1	1	19	their
# 42	1	1	20	friends
# 42	1	1	21	are
# 42	1	1	22	,
# 42	1	1	23	etc
# 42	1	1	24	.
#
# 42	1	2	0	From
# 42	1	2	1	the
# 42	1	2	2	surface
# 42	1	2	3	point
# 42	1	2	4	of
# 42	1	2	5	view
# 42	1	2	6	it
# 42	1	2	7	is
# 42	1	2	8	no
# 42	1	2	9	doubt
# 42	1	2	10	that
# 42	1	2	11	these
# 42	1	2	12	sites
# 42	1	2	13	help
# 42	1	2	14	us
# 42	1	2	15	to
# 42	1	2	16	have
# 42	1	2	17	a
# 42	1	2	18	better
# 42	1	2	19	relationship
# 42	1	2	20	with
# 42	1	2	21	our
# 42	1	2	22	relatives
# 42	1	2	23	despite
# 42	1	2	24	of
# 42	1	2	25	the
# 42	1	2	26	distance
# 42	1	2	27	.
cp $test_dir/noalt/official-2014.combined.m2 $out_dir/conll14st-test.m2


# CoNLL-2013
#############
wget https://www.comp.nus.edu.sg/~nlp/conll13st/release2.3.1.tar.gz -O $tmp_dir/conll13st.tar.gz

tar -zxvf $tmp_dir/conll13st.tar.gz -C $tmp_dir/
test_dir=$tmp_dir/release2.3.1/original/data

mkdir -p data/test/conll13st-test
out_dir=data/test/conll13st-test
python3 scripts/nucle_preprocess.py $test_dir/official-preprocessed.conll $test_dir/official-preprocessed.m2 $tmp_dir/conll13st-test.xml
python2 scripts/sentence_pairs_with_ctx.py --test --input $tmp_dir/conll13st-test.xml \
	--src-ctx $out_dir/conll13st-test.tok.ctx --src-src $out_dir/conll13st-test.tok.src --trg-trg $tmp_dir/conll13st-test.0.tok.trg
cp $test_dir/official-preprocessed.m2 $out_dir/conll13st-test.m2

#rm -rf $tmp_dir
