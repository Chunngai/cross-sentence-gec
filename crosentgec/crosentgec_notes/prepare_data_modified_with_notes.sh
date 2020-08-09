#!/bin/bash

# This scripts prepares training and dev data for cross-sentence GEC.
# Author: shamil.cm@gmail.com, weiqi@u.nus.edu

set -e
set -x

if [ $# -ne 2 ]; then
	echo "Usage: `basename $0` <Lang8-file-path> <Nucle-file-path>"
fi

# paths to raw data files
LANG8V2=$1
NUCLE_TAR=$2

mkdir -p data/tmp
tmp_dir=data/tmp

# LANG-8 v2
#############
# Preparation of Lang-8 data
echo "[`date`] Preparing Lang-8 data... (NOTE:Can take several hours, due to LangID.py filtering...)" >&2

# Transforms Lang-8 English data from Json format into XML format.
# A unit in the json format is like:
# ------
# [
# 	"129116",
# 	"20577",
# 	"English",
# 	"Mandarin",
# 	[
# 		"Life is like summer flower",
# 		"In that morning,you came",
# 		"With dewdrop's aroma",
# 		"Diffused youth style",
# 		"You told me who's gazing you one phrase:Life is like summer flower",
# 		"Then you turned to go away",
# 		"Just like you came on that day",
# 		"Outside sky does diffuse the wind and cream of years",
# 		"My waiting is hovering around the end of the world",
# 		"Your smile is blooming softly in the wind",
# 		"Who once said such a phrase",
# 		"The flower that is blooming in summer",
# 		"It will be brilliant for ever",
# 		"Whose mood is tavelling",
# 		"Whose story is straying",
# 		"You say you want to start a new life",
# 		"New life is a wonderful fairy tale"
# 	],
# 	[
# 		[],
# 		[],
# 		["With [f-red]a[\/f-red] dewdrop's aroma"],
# 		["[f-red]A[\/f-red] [f-red]d[\/f-red]iffused youth style"],
# 		["You told me [sline]who's gazing you[\/sline] one phrase:Life is like [f-red]a[\/f-red] summer flower"],
# 		[],
# 		[],
# 		["Outside[f-red], the[\/f-red] sky [sline]does[\/sline] diffuse[f-red]s[\/f-red] the wind and [f-blue]cream (?)[\/f-blue] of years [f-blue]('rain' might be a better word =\/)[\/f-blue]"],
# 		[],
# 		[],
# 		[],
# 		[],
# 		["It will be brilliant forever"],
# 		[],
# 		[],
# 		[],
# 		[]
# 	]
# ]
# ------
# And its corresponding xml counterpart is like:
# ------
#<essay id="10" journal_id="129116" user_id="20577" learning_language="English" native_language="Mandarin">
#  <sentence id="0">
#    <source langid="en">Life is like summer flower</source>
#  </sentence>
#  <sentence id="1">
#    <source langid="en">In that morning,you came</source>
#  </sentence>
#  <sentence id="2">
#    <source langid="en">With dewdrop's aroma</source>
#    <target langid="en">With a dewdrop's aroma</target>
#  </sentence>
#  <sentence id="3">
#    <source langid="en">Diffused youth style</source>
#    <target langid="en">A diffused youth style</target>
#  </sentence>
#  <sentence id="4">
#    <source langid="en">You told me who's gazing you one phrase:Life is like summer flower</source>
#    <target langid="en">You told me one phrase:Life is like a summer flower</target>
#  </sentence>
#  <sentence id="5">
#    <source langid="en">Then you turned to go away</source>
#  </sentence>
#  <sentence id="6">
#    <source langid="en">Just like you came on that day</source>
#  </sentence>
#  <sentence id="7">
#    <source langid="en">Outside sky does diffuse the wind and cream of years</source>
#    <target langid="en">Outside, the sky diffuses the wind and cream (?) of years ('rain' might be a better word =/) </target>
#  </sentence>
#  <sentence id="8">
#    <source langid="en">My waiting is hovering around the end of the world</source>
#  </sentence>
#  <sentence id="9">
#    <source langid="en">Your smile is blooming softly in the wind</source>
#  </sentence>
#  <sentence id="10">
#    <source langid="en">Who once said such a phrase</source>
#  </sentence>
#  <sentence id="11">
#    <source langid="en">The flower that is blooming in summer</source>
#  </sentence>
#  <sentence id="12">
#    <source langid="en">It will be brilliant for ever</source>
#    <target langid="en">It will be brilliant forever</target>
#  </sentence>
#  <sentence id="13">
#    <source langid="en">Whose mood is tavelling</source>
#  </sentence>
#  <sentence id="14">
#    <source langid="en">Whose story is straying</source>
#  </sentence>
#  <sentence id="15">
#    <source langid="en">You say you want to start a new life</source>
#  </sentence>
#  <sentence id="16">
#    <source langid="en">New life is a wonderful fairy tale</source>
#  </sentence>
#</essay>
# ------
python3 scripts/lang8_preprocess.py --dataset $LANG8V2 --language English --id en --output $tmp_dir/lang-8-20111007-L1-v2.xml

# Partitions data in the generated xml into train set (xml) and dev set (xml), 
# with the size of dev data equals to 0 
# (hence no dev set generated, and the train set here is the same as the given data set). 
python3 scripts/partition_data_into_train_and_dev.py --dataset $tmp_dir/lang-8-20111007-L1-v2.xml --train $tmp_dir/lang8-train.xml --dev $tmp_dir/lang8-dev.xml --limit 0

# Extracts sentence pairs from the train set (xml),
# with the sentences tokenized (It's -> It 's, etc.),
#
# A sentence pair will be generated when the following conditions are met:
# (1) src is en.
# (2) min_token# < src_token# < max_token#.
#
# (3) at least one trg provided.
# (4) trg is en.
# (5) trg is not empty.
# (6) min_token# < trg_token# < max_token#.
#
# (7) src != trg.
#
# Take the 1st essay for an example:
#
# data in lang8-train.xml:
# ------
# <essay id="0" journal_id="728457" user_id="216037" learning_language="English" native_language="Japanese">
#   <sentence id="0">
#     <source langid="en">About winter</source>
#   </sentence>
#   <sentence id="1">
#     <source langid="en">This is my second post.</source>
#   </sentence>
#   <sentence id="2">
#     <source langid="en">I will appreciate it if you correct my sentences.</source>
#     <target langid="en">I would appreciate it if you could correct my sentences.</target>
#   </sentence>
#   <sentence id="3">
#     <source langid="en">It's been getting colder these days here in Japan.</source>
#     <target langid="en">It's been getting colder lately here in Japan. ("These days" is a phrase I often hear Japanese and Korean native speakers use in their English, although in native English speakers would probably say "lately" or "recently." It's sort of the equivalent of 最近.) </target>
#   </sentence>
#   <sentence id="4">
#     <source langid="en">The summer weather in Japan is not agreeable to me with its high humidity and temperature.</source>
#     <target langid="en">I find Japan's summer weather disagreeable because of its high humidity and temperature.</target>
#   </sentence>
#   <sentence id="5">
#     <source langid="en">So, as the winter is coming, I'm getting to feel better.</source>
#     <target langid="en">So, as the winter is coming, I'm starting to feel better.</target>
#   </sentence>
#   <sentence id="6">
#     <source langid="en">Coldness is my energy.</source>
#   </sentence>
#   <sentence id="7">
#     <source langid="en">lol</source>
#   </sentence>
#   <sentence id="8">
#     <source langid="en">And also, around the new year's holidays, we will have a lot of enjoyable events</source>
#   </sentence>
#   <sentence id="9">
#     <source langid="en">mostly with delicious foods, drinks, and good conversations.</source>
#   </sentence>
#   <sentence id="10">
#     <source langid="en">In addition, it is the time for skiing and snow boarding:) </source>
#   </sentence>
#   <sentence id="11">
#     <source langid="en">It is the very exciting season.</source>
#     <target langid="en">It is a very exciting season.</target>
#   </sentence>
#   <sentence id="12">
#     <source langid="en">But, before enjoying those kind of happy time, I have to do a kind of boring,</source>
#     <target langid="en">But, before enjoying those kind of happy times, I have to do a kind of boring,</target>
#   </sentence>
#   <sentence id="13">
#     <source langid="en">customary practice.</source>
#   </sentence>
#   <sentence id="14">
#     <source langid="en">Writing new year's greeting cards is somehow a pain in the neck.</source>
#   </sentence>
#   <sentence id="15">
#     <source langid="en">Actually, I don't have enough time to come up with an idea of the card's design.</source>
#   </sentence>
#   <sentence id="16">
#     <source langid="en">I wish i could come across an good one in my mind.</source>
#   </sentence>
#   <sentence id="17">
#     <source langid="en">Thank you for reading &amp; thanks for your time.</source>
#   </sentence>
# </essay>
# ------
# Extraction process:
# ------
# SENTENCE 0
#   SRC: About winter
#     (TOKENIZED) About winter
#
#   NO TRG
#
# SENTENCE 1
#   SRC: This is my second post.
#     (TOKENIZED) This is my second post .
#
#   NO TRG
#
# SENTENCE 2
#   SRC: I will appreciate it if you correct my sentences.
#     (TOKENIZED) I will appreciate it if you correct my sentences .
#
#   TRG0: I would appreciate it if you could correct my sentences.
#     (TOKENIZED) I would appreciate it if you could correct my sentences .
#
#   (CTX) About winter This is my second post .
#
#   (SRC) I will appreciate it if you correct my sentences .
#
#   (TRG) I would appreciate it if you could correct my sentences .
#
#
# SENTENCE 3
#   SRC: It's been getting colder these days here in Japan.
#     (TOKENIZED) It 's been getting colder these days here in Japan .
#
#   TRG0: It's been getting colder lately here in Japan. ("These days" is a phrase I often hear Japanese and Korean native speakers use in their English, although in native English speakers would probably say "lately" or "recently." It's sort of the equivalent of 最近.)
#     (TOKENIZED) It 's been getting colder lately here in Japan. ( " These days " is a phrase I often hear Japanese and Korean native speakers use in their English , although in native English speakers would probably say " lately " or " recently. " It 's sort of the equivalent of 最 近 . )
#
#   (CTX) This is my second post . I will appreciate it if you correct my sentences .
#
#   (SRC) It 's been getting colder these days here in Japan .
#
#   (TRG) It 's been getting colder lately here in Japan. ( " These days " is a phrase I often hear Japanese and Korean native speakers use in their English , although in native English speakers would probably say " lately " or " recently. " It 's sort of the equivalent of 最 近 . )
#
#
# SENTENCE 4
#   SRC: The summer weather in Japan is not agreeable to me with its high humidity and temperature.
#     (TOKENIZED) The summer weather in Japan is not agreeable to me with its high humidity and temperature .
#
#   TRG0: I find Japan's summer weather disagreeable because of its high humidity and temperature.
#     (TOKENIZED) I find Japan 's summer weather disagreeable because of its high humidity and temperature .
#
#   (CTX) I will appreciate it if you correct my sentences . It 's been getting colder these days here in Japan .
#
#   (SRC) The summer weather in Japan is not agreeable to me with its high humidity and temperature .
#
#   (TRG) I find Japan 's summer weather disagreeable because of its high humidity and temperature .
#
#
# SENTENCE 5
#   SRC: So, as the winter is coming, I'm getting to feel better.
#     (TOKENIZED) So , as the winter is coming , I 'm getting to feel better .
#
#   TRG0: So, as the winter is coming, I'm starting to feel better.
#     (TOKENIZED) So , as the winter is coming , I 'm starting to feel better .
#
#   (CTX) It 's been getting colder these days here in Japan . The summer weather in Japan is not agreeable to me with its high humidity and temperature .
#
#   (SRC) So , as the winter is coming , I 'm getting to feel better .
#
#   (TRG) So , as the winter is coming , I 'm starting to feel better .
#
#
# SENTENCE 6
#   SRC: Coldness is my energy.
#     (TOKENIZED) Coldness is my energy .
#
#   NO TRG
#
# SENTENCE 7
#   SRC: lol
#     (TOKENIZED) lol
#
#   NO TRG
#
# SENTENCE 8
#   SRC: And also, around the new year's holidays, we will have a lot of enjoyable events
#     (TOKENIZED) And also , around the new year 's holidays , we will have a lot of enjoyable events
#
#   NO TRG
#
# SENTENCE 9
#   SRC: mostly with delicious foods, drinks, and good conversations.
#     (TOKENIZED) mostly with delicious foods , drinks , and good conversations .
#
#   NO TRG
#
# SENTENCE 10
#   SRC: In addition, it is the time for skiing and snow boarding:)
#     (TOKENIZED) In addition , it is the time for skiing and snow boarding : )
#
#   NO TRG
#
# SENTENCE 11
#   SRC: It is the very exciting season.
#     (TOKENIZED) It is the very exciting season .
#
#   TRG0: It is a very exciting season.
#     (TOKENIZED) It is a very exciting season .
#
#   (CTX) mostly with delicious foods , drinks , and good conversations . In addition , it is the time for skiing and snow boarding : )
#
#   (SRC) It is the very exciting season .
#
#   (TRG) It is a very exciting season .
#
#
# SENTENCE 12
#   SRC: But, before enjoying those kind of happy time, I have to do a kind of boring,
#     (TOKENIZED) But , before enjoying those kind of happy time , I have to do a kind of boring,
#
#   TRG0: But, before enjoying those kind of happy times, I have to do a kind of boring,
#     (TOKENIZED) But , before enjoying those kind of happy times , I have to do a kind of boring,
#
#   (CTX) In addition , it is the time for skiing and snow boarding : ) It is the very exciting season .
#
#   (SRC) But , before enjoying those kind of happy time , I have to do a kind of boring,
#
#   (TRG) But , before enjoying those kind of happy times , I have to do a kind of boring,
#
#
# SENTENCE 13
#   SRC: customary practice.
#     (TOKENIZED) customary practice .
#
#   NO TRG
#
# SENTENCE 14
#   SRC: Writing new year's greeting cards is somehow a pain in the neck.
#     (TOKENIZED) Writing new year 's greeting cards is somehow a pain in the neck .
#
#   NO TRG
#
# SENTENCE 15
#   SRC: Actually, I don't have enough time to come up with an idea of the card's design.
#     (TOKENIZED) Actually , I do n't have enough time to come up with an idea of the card 's design .
#
#   NO TRG
#
# SENTENCE 16
#   SRC: I wish i could come across an good one in my mind.
#     (TOKENIZED) I wish i could come across an good one in my mind .
#
#   NO TRG
#
# SENTENCE 17
#   SRC: Thank you for reading & thanks for your time.
#     (TOKENIZED) Thank you for reading & thanks for your time .
#
#   NO TRG
# ------
python2 scripts/sentence_pairs_with_ctx.py --train --tokenize --maxtokens 80 --mintokens 1 --input $tmp_dir/lang8-train.xml  \
	--src-ctx $tmp_dir/lang8.src-trg.ctx --src-src $tmp_dir/lang8.src-trg.src --trg-trg $tmp_dir/lang8.src-trg.trg


# NUCLE
#############
# Preparation of NUCLE data
echo "[`date`] Preparing NUCLE data..." >&2
tar -zxvf $NUCLE_TAR -C $tmp_dir/
nucle_dir=$tmp_dir/release3.3

# Generates .conll, .conll.ann (not used later), .conll.m2 from the sgml file.
python2 $nucle_dir/scripts/preprocess.py -l $nucle_dir/data/nucle3.2.sgml \
	$tmp_dir/nucle3.2-preprocessed.conll $tmp_dir/nucle3.2-preprocessed.conll.ann $tmp_dir/nucle3.2-preprocessed.conll.m2

# Generates .xml from the .conll, .m2 file.
python3 scripts/nucle_preprocess.py $tmp_dir/nucle3.2-preprocessed.conll $tmp_dir/nucle3.2-preprocessed.conll.m2 $tmp_dir/nucle3.2.xml

# Partitions data in the generated xml into train set (xml) and dev set (xml),
# with the size (sentence#?) of dev data equals to 5000.
# A dev.m2 is generated with the data from .m2.
python3 scripts/partition_data_into_train_and_dev.py --dataset $tmp_dir/nucle3.2.xml \
	--train $tmp_dir/nucle-train.xml --dev $tmp_dir/nucle-dev.xml --limit 5000 --m2 $tmp_dir/nucle3.2-preprocessed.conll.m2 --dev-m2 $tmp_dir/nucle-dev.raw.m2

# Extracts sentence pairs from the train set (xml).
# Tokenization is not needed since data in the train set has been tokenized,
# which is because data in the generated .m2 file is tokenized.
#
# A sentence pair will be generated when the following conditions are met:
# (1) src is en.
# (2) min_token# < src_token# < max_token#.
#
# (3) at least one trg provided.
# (4) trg is en.
# (5) trg is not empty.
# (6) min_token# < trg_token# < max_token#.
#
# (7) src != trg.
python2 scripts/sentence_pairs_with_ctx.py --train --maxtokens 80 --mintokens 1 --input $tmp_dir/nucle-train.xml \
	--src-ctx $tmp_dir/nucle.src-trg.ctx --src-src $tmp_dir/nucle.src-trg.src --trg-trg $tmp_dir/nucle.src-trg.trg

# Extracts sentence pairs from the dev set (xml).
# Tokenization is not needed since data in the dev set has been tokenized,
# which is because data in the generated .dev.m2 file is tokenized.
#
# A sentence pair will be generated when the following conditions are met:
# (1) src is en.
# (2) min_token# < src_token# < max_token#.
#
# (3) at least one trg provided.
# (4) trg is en.
# (5) min_token# < trg_token# < max_token#.
#
# (6) src != trg.
python2 scripts/sentence_pairs_with_ctx.py --dev --maxtokens 80 --mintokens 1 --input $tmp_dir/nucle-dev.xml \
	--src-ctx $tmp_dir/nucle-dev.src-trg.ctx --src-src $tmp_dir/nucle-dev.src-trg.src --trg-trg $tmp_dir/nucle-dev.src-trg.trg

# Strips unchanged sentence pairs (that is, the original sentences are considered correct) from the m2 file.
python3 scripts/m2_preprocess.py --nucle-dev $tmp_dir/nucle-dev.src-trg.src --dev-m2 $tmp_dir/nucle-dev.raw.m2 --processed-m2 $tmp_dir/nucle-dev.preprocessed.m2


# preprocessed training and dev data
#############
mkdir -p data/processed
BPE_MODEL=models/bpe/mlconvgec_aaai18_bpe.model
out_dir=data/processed
for ext in ctx src trg; do
	# Cp lang8 data to data/processed/train.src-trg.{ctx|src|trg}.
	cat $tmp_dir/lang8.src-trg.$ext > $tmp_dir/train.src-trg.$ext
	# Append nucle train data to data/processed/train.src-trg.{ctx|src|trg}.
	cat $tmp_dir/nucle.src-trg.$ext >> $tmp_dir/train.src-trg.$ext

	# Cp nucle dev data to data/processed/valid.src-trg.{ctx|src|trg}.
	cp $tmp_dir/nucle-dev.src-trg.$ext $tmp_dir/valid.src-trg.$ext

	# Applies bpe.
	scripts/apply_bpe.py -c $BPE_MODEL < $tmp_dir/train.src-trg.$ext > $out_dir/train.src-trg.$ext
	scripts/apply_bpe.py -c $BPE_MODEL < $tmp_dir/valid.src-trg.$ext > $out_dir/valid.src-trg.$ext
done

cp $tmp_dir/nucle-dev.preprocessed.m2 data/nucle-dev.preprocessed.m2

#rm -rf $tmp_dir

# copy the dictionary
#BASEURL=https://tinyurl.com/yd6wvhgw/mlconvgec2018/models
BASEURL=http://sterling8.d2.comp.nus.edu.sg/downloads/GEC/mlconvgec2018/models
curl -L -o $out_dir/dict.ctx.txt $BASEURL/data_bin/dict.src.txt
curl -L -o $out_dir/dict.src.txt $BASEURL/data_bin/dict.src.txt
curl -L -o $out_dir/dict.trg.txt $BASEURL/data_bin/dict.trg.txt
