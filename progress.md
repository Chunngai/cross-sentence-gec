# Jul 29

## · Notes ·
1. Tokenization diff of diff ver.  

The script uses nltk-2.0b7 and python2 to tokenize data, producing some strange tokenizations.  

A sentence in the lang8 training set:  
> There is a big difference between the east and the west, when comes to education,i always admired how the westerner educate their posterity,their method is so gentle and kind,full of love and meaning,whereas the asian method is rather more of violence,for example the chinese people believe that a child should be educated with rods!  

Rst of nltk-2.0b7 + python2:
```
['There', 'is', 'a', 'big', 'difference', 'between', 'the', 'east', 'and', 'the', 'west', ',', 'when', 'comes', 'to', 'education,i', 'always', 'admired', 'how', 'the', 'westerner', 'educate', 'their', 'posterity,their', 'method', 'is', 'so', 'gentle', 'and', 'kind,full', 'of', 'love', 'and', 'meaning,whereas', 'the', 'asian', 'method', 'is', 'rather', 'more', 'of', 'violence,for', 'example', 'the', 'chinese', 'people', 'believe', 'that', 'a', 'child', 'should', 'be', 'educated', 'with', 'rods', '!']
```
Rst of nltk3.5 + python3:
```
['There', 'is', 'a', 'big', 'difference', 'between', 'the', 'east', 'and', 'the', 'west', ',', 'when', 'comes', 'to', 'education', ',', 'i', 'always', 'admired', 'how', 'the', 'westerner', 'educate', 'their', 'posterity', ',', 'their', 'method', 'is', 'so', 'gentle', 'and', 'kind', ',', 'full', 'of', 'love', 'and', 'meaning', ',', 'whereas', 'the', 'asian', 'method', 'is', 'rather', 'more', 'of', 'violence', ',', 'for', 'example', 'the', 'chinese', 'people', 'believe', 'that', 'a', 'child', 'should', 'be', 'educated', 'with', 'rods', '!']
```
A main diff is that in 2.* ver, "a,b" is treated as a token, while in 3.* ver it is treated as ["a", ",", "b"]. The previous treatment may introduce more OOV?

2. The decoder is similar to that of bert?  
  A: Seems not.

## · TODOs ·
- [ ] try to train a model with ver 3.* tokenization.

---

# Jul 31, Aug 1
## · Papers · | Crosentgec
### Ideas
1. P3 L | Attn: switch to multi-head attn?  
2. P3 L | Other operation for context sentences except concat?  
3. P3 R | Eq 10. What about LIN(concat(Y_l, C_l)) instead of addition of Lin?  
4. P4 L | Lang8: noisy. Use another dataset for training.  
5. P4 R | What about using more previous sentences?  
6. P4 R | What about using following sentences?  
7. P7 L | Data synthetic both for training and evaluation.  

### TODOs
- [x] P2 L | Learn: auxiliary encoders.  
- [x] Read: Exploiting Cross-Sentence Context for Neural Machine Translation (ref by the above paper)  
- [x] Read: Context Gates for Neural Machine Translation (ref by the above paper)  
  After exp: not read.
- [ ] P2 L | Learn: rescoring.  
- [x] P2 R | Read: Convolutional sequence to sequence learning (Fairseq)  
  After exp: not read.
- [x] P2 R | Learn: GLU  
- [x] Learn: BERT  
- [x] Learn: label smoothing  

### Questions
- [x] P2 L | Incorporate probabilities computed by BERT as a feature.  
  BERT can be used as a feature extractor.  
- [ ] P2 R | Do not explicitly consider previously corrected target sentences to avoid error propagation.  
- [x] P3 L | Why to compute the attn that way?  
  Attn with multi hops. Used by fairseq conv. Considers which words previously attended to and performs multi hops per time step.  
- [x] P3 L | Is the attn proposed in other paper?  
  In the fairseq paper.  
- [x] P3 L | Is the attn similar to the one proposed in Luong et al.?  
  Similar except for the way to calculate c_i. In the afirseq paper: c_i = \sum a_ij (z_j + e_j). Added e_j.  
- [ ] P3 L | The last decoder state.  
- [x] P3 R | Why does the gating can control crosent info?  
  Determines how much context info (C_l) should be retained when correcting the current sentence Y_l.  
- [x] P3 R | Where does the gating mechanism come from?  
  Similar to the one in Wang et al. 2017 (the paper read on Aug 2) except that the gating here does not consider the last output. Seems it's a common practice for gating.
- [x] P3 R | Is the gating mechanism similar to LSTM?  
- [ ] P4 L | Pretraining decoder: unmatched params?  
- [ ] P4 L | Dropping out entire word embeddings of source words: where is the code?  
- [ ] P4 L | We also rescore the ...  
- [ ] P4 L | What's the purpose of ensuring the dev set has a high number of err   annotations?  
- [ ] P4 R | What's the meaning of "perform significance tests using one-tailed sign test with bootstrap resampling on 100 samples."  

### Notes
1. P2 L | LM?  
2. P6 R | Future work: large-scale cross-sentence GEC.  
3. P8 L | Future work: evaluate more sophiscated models such as memory networks to capture entire document-level context  
4. P8 L | Future work: incorporate external knowledge sources.  
5. The papar used conv of fairseq.  

## · Ideas ·
1. Apply iterative decoding to improve performance, especially for long sentences.  
2. Decoder: multi-attn, two sets respectively. Use gating for one set.  
3. Filter lang8 before training, maybe shortest edit distance.  

## · TODOs ·
- [ ] Find other available datasets for training or evaluation.  
- [x] Read: Toward Making the Most of Context in Neural Machine Translation  
  After exp: not read.
- [x] Review: LSTM, GRU  
- [ ] How to train the avg and ens?  

---

# Aug 1
## · Papers · | Fairseq
  ### Questions
  - [ ] (Fairseq) P2 L | Each convolution ... Why does the param W is 2d?  
  - [ ] (Fairseq) P2 L | where A, B ... What's A, B?  
  - [ ] (Fairseq) P4 L | ...compared to recurrent nets where ... In a timestep only one GLU in the decoder?

---

# Aug 2

## · Papers · | Additional Encoder & Hierarchical RNN | Exploiting Cross-Sentence Context for Neural Machine Translation, Wang et al., 2017   
### Contributions  
1. A hierarchical way to get context  
2. 2 strategies: warm-start & auxiliary (with / -out gate)  

### Methods.
**Context Source**  
The proposed method considers 3 previous sentences in the same document as context.

**Model the Context**  
It models the context in a hierarchical way.   

First it encodes each sentence with a sentence-level RNN, and takes the last hidden state as the sentence-level representation $S_k$ of the whole sentence.
$$
S_k = h_{N, k} \\
h_{n, k} = f (h_{n-1}, k, x_{n, k})
$$
where $S_k$ is the k-th sentence (1 <= k <= 3), $h_{N, k}$ is the last hidden state of sentence $k$. $h_{n, k}$ is the n-th hidden state of a sentence, $f(·)$ is an activation func, and $x_{n, k}$ is the n-th input to the sentence.

Then $\{S_1, ..., S_k, ..., S_K\}$ is fed into a doc-level RNN, which is used to generate the doc-level representation $D$ of the context.
$$
D = h_K \\
h_k = f (h_{k - 1}, S_k)
$$
The doc-level representation $D$ is then integrated into the NMT model.

**Integration**  
The paper proposed 3 strategies to integrate the context $D$ into the NMT model.
1. Use $D$ to initialize the encoder, decoder or both.

2. Auxiliary context, without gating.
$$
s_i = f (s_{i - 1}, y_{i - 1}, c_i, D)
$$
where $s_i$, $y_{i - 1}$ and $c_i$ represents the decoder hidden state at the i-th timestep, the latest output, and the context from the NMT attention, respectively.

3. Gating Auxiliary Context.
$$
s_i = f (s_{i - 1}, y_{i - 1}, c_i, z_i \otimes D) \\
z_i = \sigma (U_z s_{i-1} + W_z y_{i-1} + C_z c_i)
$$

### Notes
1. P3 L | Diff from the crosentgec, the gating here considers the last output of the decoder.  
2. P3 R | Considers the previous 3 sentences rather than 1.  
3. P5 L | Summarizes the context alone, more flexible.  
4. P5 L | No attn when getting context info, thus less computational costs. -> is able to consider more previous sentences  
5. Code provided.

### Questions
- [ ] P1 R | Considering target side history: suffers from err prop. Why?

## · Questions ·
- [ ] Err prop exists in crosentgec?
- [ ] Less err prop on trg side in gec since less err on trg side?

---

# Aug 3
## · Papers · | Gates | Context Gates for Neural Machine Translation, Tu et al., 2017  
### Contributions
1. 3 kinds of context gates (src, trg, src & trg)

### Notes
1. Repeated output in gec: not enough info from trg?
2. The gates proposed by the paper is inspired by lstm and gru.
3. Code provided.

## · Papers · | Transformer & Context | Toward Making the Most of Context in Neural Machine Translation
### Contributions  
1. General purpose, can deal with 1 or more sentences.
2. Make full use of the whole doc, not merely the previous few.

### Notes
1. More context, more sensitive to noise: similar to overfitting?
2. Many models requiring additional global doc context cannot translate single sentences.
3. Something useful in related work.
4. No code, complicated.

### Questions
- [ ] Does the crosentgec model have the problem in Notes.2?

---

# Aug 4

## · Notes ·
1. Papers of GEC with context info after 2014: only the crosentgec is found, with keywords "context", "discourse", "cross-sentence", "document-level"

## · TODOs ·
- [x] Find some Transformer-based GEC papers, with code provided.  
  Fairseq implementation is better.  
  Lang8 and NUCLE as training set is better.  
  \-\-\-  
  Found three candidates:  
  1. Encoder-Decoder Models Can Benefit from Pre-trained Masked Language Models in Grammatical Error Correction  
  2. Improving Grammatical Error Correction via Pre-Training a Copy-Augmented Architecture with Unlabeled Data  
  3. A Neural Grammatical Error Correction System Built On Better Pre-training and Sequential Transfer Learning  

## · Papers · | GEC & Transformer & Fairseq | Encoder-Decoder Models Can Benefit from Pre-trained Masked Language Models in Grammatical Error Correction
### Contributions
1. Investigates how to effectively incorporate a pre-trained MLM into an encoder-decoder model for gec.  
  init / fuse / combime (mask / GED)

#### Notes
1. Seems not easy to further improve the performance of the model.  
2. Code provided, but seems it's not complete of something. Maybe it can be used for further improve the performance of a model.  
3. The crosentgec model also use a MLM.  

---

# Aug 5

## · Papers · | GEC & Transformer & Fairseq | Improving Grammatical Error Correction via Pre-Training a Copy-Augmented Architecture with Unlabeled Data
### Contributions
1. Copy-augmented arch for gec.  
2. Pretrain with DAE.
3. Adds token- / sentence level multi-task learning for the GEC task.

### Notes
1. Seems that the code is a mixture of multiple techniques, hard to tell the function of each part.

---

# Aug 5 - 6, 8 - 16

## · Papers · | GEC & Transformer & Fairseq | A Neural Grammatical Error Correction System Built On Better Pre-training and Sequential Transfer Learning

### Contributions
1. Realistic noising function.
2. Transfer learning.
3. Context-aware neural spellchecker.

### Notes
1. Uses fairseq-0.6.1.
2. Future work: multi-sentence context.
3. The code is detailed. The structure is clear and the modified parts in fairseq are explained in a file. Modified code is also marked with "[MODIFIED]".
4. The paper is also detailed.
5. Seems that the paper with its code is an ideal starting-point.
6. The mixture weight param of the copy aug arch is like the gating param, controlling how much info should be copied and how much be generated.
7. The type-based nosing approach is similar to the one proposed by us.
8. Requirements:
  1. errant for bea2019 -> spacy 1.9.0 -> python3.6
  2. Python 2.7
  3. pytorch 1.4.0
9. Warnings & Errors:
  1. train.py  # Solution: pytorch <= 1.4.0
  > /home/neko/GEC/helo_word-master/fairseq/fairseq/optim/adam.py:121: UserWarning: This overload of add_ is deprecated:  
	add_(Number alpha, Tensor other)  
Consider using one of the following signatures instead:  
	add_(Tensor other, \*, Number alpha) (Triggered internally at  /pytorch/torch/csrc/utils/python_arg_parser.cpp:766.)

  2. evaluate.py  # Solution: pytorch <= 1.4.0
  > Traceback (most recent call last):                                                                       
  File "/home/neko/.virtualenvs/gec_exp_1/bin/fairseq-generate", line 33, in <module>  
    sys.exit(load_entry_point('fairseq', 'console_scripts', 'fairseq-generate')())  
  File "/home/neko/GEC/helo_word-master/fairseq/fairseq_cli/generate.py", line 188, in cli_main  
    main(args)  
  File "/home/neko/GEC/helo_word-master/fairseq/fairseq_cli/generate.py", line 106, in main  
    hypos = task.inference_step(generator, models, sample, prefix_tokens)  
  File "/home/neko/GEC/helo_word-master/fairseq/fairseq/tasks/fairseq_task.py", line 242, in inference_step  
    return generator.generate(models, sample, prefix_tokens=prefix_tokens)  
  File "/home/neko/.virtualenvs/gec_exp_1/lib/python3.8/site-packages/torch/autograd/grad_mode.py", line 15, in decorate_context  
    return func(\*args, \**kwargs)  
  File "/home/neko/GEC/helo_word-master/fairseq/fairseq/sequence_generator.py", line 372, in generate  
    cand_scores, cand_indices, cand_beams = self.search.step(  
  File "/home/neko/GEC/helo_word-master/fairseq/fairseq/search.py", line 83, in step  
    torch.div(self.indices_buf, vocab_size, out=self.beams_buf)  
RuntimeError: Integer division of tensors using div or / is no longer supported, and in a future release div will perform true division as in Python 3. Use true_divide or floor_divide (// in Python) instead.
INFO:root:[Run-ckpt] 2. postprocess into /home/neko/GEC/helo_word-master/track1/outputs/pretrain-base-lr0.0005-dr0.3/checkpoint1.wi.dev.cor

  3. evaluate.py  # Solution: spacy==1.9.0
  > Traceback (most recent call last):  
  File "/home/neko/GEC/helo_word-master/errant/parallel_to_m2.py", line 79, in <module>  
    main(args)  
  File "/home/neko/GEC/helo_word-master/errant/parallel_to_m2.py", line 55, in main  
    cat = cat_rules.autoTypeEdit(auto_edit, proc_orig, proc_cor, gb_spell, tag_map, nlp, stemmer)  
  File "/home/neko/GEC/helo_word-master/errant/scripts/cat_rules.py", line 65, in autoTypeEdit  
    cat = getTwoSidedType(orig_toks, cor_toks, gb_spell, tag_map, nlp, stemmer)  
  File "/home/neko/GEC/helo_word-master/errant/scripts/cat_rules.py", line 187, in getTwoSidedType  
    if sameLemma(orig_toks[0], cor_toks[0], nlp) and \  
  File "/home/neko/GEC/helo_word-master/errant/scripts/cat_rules.py", line 333, in sameLemma  
    orig_lemmas.append(nlp.vocab.morphology.lemmatize(pos, orig_tok.lower, nlp.vocab.morphology.tag_map))  
  File "morphology.pyx", line 243, in spacy.morphology.Morphology.lemmatize  
  File "strings.pyx", line 152, in spacy.strings.StringStore.as_string  
  File "strings.pyx", line 120, in spacy.strings.StringStore.\_\_getitem__  
TypeError: unhashable type: 'dict'

10. They evals their outputs of wi+locness test set on codalab.

### TODOs
- [x] Learn: Copy-aug.

### Ideas
1. Noising func + back translation. Can also introduce typo or something.
2. The W&I+L dataset also contains doc-level errors and can be used to train a gec model considering contexts.

### Questions
- [x] P5 R | What's the minor tokenization issues?
  e.g. "a,b -> a, b"
- [ ] P5 R | Error type control.

---

# Aug 7

## · Ideas ·
1. Pre-trained embeddings.
2. Pre-trained LM models. (Is it ok to use a pre-trained decoder since the model is trained with pseudo data?)

---

# Aug 17

## ·TODOs·
- [x] Read: Does Neural Machine Translation Benefit from Larger Context?, Jean et al., 2017.

---

# Aug 18

## · Papers · | Additional Encoder, Attention & RNN | Does Neural Machine Translation Benefit from Larger Context?, Jean et al., 2017   
### Contributions  
1. Doc-level info for mt.

### Methods
**Context Source**  
The paper uses the source sentence immediately before the current source sentence as context.

**Model the Context**  
It models the context by an additional encoder and an additional attention model.   

The context is encoded by the additional encoder in the same manner as the NMT encoder, using bi-LSTM. Output of the additional encoder is $\{h^c_1, ..., h^c_{T_c}\}$, where $h^c_t = [\overrightarrow{h^c_t}; \overleftarrow{h^c_t}]$.

The additional attention model is as follows
$$
\alpha^c_{t, t^{\prime}} \propto exp(f^c_{att}(\hat{y}_{t^{\prime} - 1}, z_{t^{\prime} - 1}, h^c_t, s_{t^{\prime}}))
$$
where $t$ and $t^{\prime}$ are timesteps, $f^c_{att}$ is the additional attention model implemented as a feed forward network (the same as the NMT attention in the paper) taking the previous target symbol $\hat{y}_{t^{\prime} - 1}$, the previous decoder hidden state $z_{t^{\prime} - 1}$, the NMT encoder hidden state $h^c_t$ and the NMT attention vector $s_{t^{\prime}}$ as arguments. Compared to the NMT attention, the additional attention model here has a new argument $s_{t^{\prime}}$.

**Integration**  
The paper integrates the context into the NMT model in an auxiliary way.
$$
z_{t^{\prime}} = \phi(\hat{y}_{t^{\prime} - 1}, z_{t^{\prime} - 1}, s_{t^{\prime}}, c_{t^{\prime}})
$$
where $c_{t^{\prime}}$ is the additional doc-level attention context. Compared to the basic NMT decoder, the decoder with auxiliary info here has a new argument $c_{t^{\prime}}$.  

### Notes
1. Code not provided.

### Questions
- [ ] P2 L | How does the ff attn work?

---

# Aug 19
## · Papers · | Additional Encoder & Transformer | Context-Aware Neural Machine Translation Learns Anaphora Resolution, Voita et al., 2018
### Contributions
• we introduce a context-aware neural model, which is effective and has a sufficiently simple and interpretable interface between the context and the rest of the translation model;  
• we analyze the flow of information from the context and identify pronoun translation as the key phenomenon captured by the model;  
• by comparing to automatically predicted or human-annotated coreference relations, we observe that the model implicitly captures anaphora.  

### Methods
**Context Source**  
The proposed model makes use of one previous sentence as context info.

**Model the Context**  
It models the context using a Transformer encoder with 6 layers, whose structure is identical to the original Transformer. Parameters of the first 5 layers of the context encoder are shared with the source sentence encoder.

> Since major proportion of the context encoder’s parameters are shared with the source encoder, we add a special token (let us denote it \<bos\>) to the beginning of context sentences, but not source sentences, to let the shared layers know whether it is encoding a source or a context sentence.

Note that \<eos\> presents in both the context sentence and the source sentence, while <bos> is only in the context sentence.

**Integration**  
The source sentence encoder consists of 6 layers, with the first 5 identical to the original Transformer. The output of the 5th source encoder layer is fed into a multi-head attention, which is the same as the previous 5 layers.

The last layer of the source encoder is where the context is integrated into. In addition to the multi-head attention mentioned above, one more multi-head attention sub-layer is set in the last layer of the source encoder to receive the output from the last layer of the context encoder as K and V, similar to the enc-dec attention in the Transformer decoder. Q of the multi-head attention is from the output of the 5-th layer in the source encoder.

Outputs of two multi-head attentions are implemented add & norm respectively, and summed using a gate. The gated sum is then fed into the feed forward neural network of the last layer of the source encoder. The gated sum $c_i$ is computed as follows
$$
c_i = g_i \odot c^{s-attn}_i + (1 - g_i) \odot c^{c-attn}_i  \\
g_i = \sigma (W_g [c^{s-attn}_i, c^{c-attn}_i] + b_g)
$$
where $c^{s-attn}_i$ is the output of the source sentence multi-head attention and $c^{c-attn}_i$ the output of the context sentence multi-head attention, after add & norm, respectively.

### Comparison With Other Methods
1.
> When compared to simply concatenating input sentences, as proposed by Tiedemann and Scherrer (2017), our architecture appears both more accurate (+0.6 BLEU) and also guarantees that the contextual information cannot bypass the attention layer and hence remain undetected in our analysis.

2.
> As we will see in Section 4, previous techniques developed for recurrent encoder-decoders do not appear effective for the Transformer.

3.
> In contrast to related work (Jean et al., 2017; Wang et al., 2017), we found in preliminary experiments that using separate encoders does not yield an accurate model. Instead we share the parameters of the first N − 1 layers with the source encoder.

4.
> Tiedemann and Scherrer (2017) only used a special symbol to mark where the context sentence ends and the source sentence begins. This technique performed badly with the non recurrent Transformer architecture in preliminary experiments, resulting in a substantial degradation of performance (over 1 BLEU).

### Notes
1. The model preforms well for pronouns in the machine translation task in the paper. In the machine translation task here the tense of sources and targets are not difficult to maintain consistent. But that may not the case for gec tasks. Thus the model may make use of context info to make corrections in gec training, not only be limited to pronouns.
2. The proposed model integrates the context on the encoder side.
3.
> We also notice that, unlike the previous sentence, the next sentence does not appear beneficial. This is a first indicator that discourse phenomena are the main reason for the observed improvement, rather than topic effects.

4. The paper uses random context for experiments to show that the model is not merely better regularized by the context.
5. Plotting the attention weight matrix can be a way to see if the context info helps.
6. Encoding the context using a different encoder is still worth a try, despite the preliminary result of the paper.

### Future work
1.
> improving the attention component is likely to boost translation performance.

### Questions
- [ ] What if exchange the position of $g_i$ and $(1 - g_i)$ in the gating mechanism?
- [ ] The is a <bos> needed for context sentence?
- [ ] P2 L | R effective ...
- [ ] P4 R | binary flag.

---

# Papers

## Main
- [x] Cross-Sentence Grammatical Error Correction {  
&emsp;&emsp;task: gec,  
&emsp;&emsp;model: conv,  
&emsp;&emsp;author: Chollampatt et al.,  
&emsp;&emsp;year: 2019,  
&emsp;&emsp;conference: ACL,  
&emsp;&emsp;labels: {  
&emsp;&emsp;&emsp;&emsp;crosent  
&emsp;&emsp;}  
}  

- [x] A Neural Grammatical Error Correction System Built On Better Pre-training and Sequential Transfer Learning {  
&emsp;&emsp;task: gec,  
&emsp;&emsp;model: transformer,  
&emsp;&emsp;author: Choe et al.,  
&emsp;&emsp;year: 2019,  
&emsp;&emsp;conference: ACL,  
&emsp;&emsp;labels: {  
&emsp;&emsp;&emsp;&emsp;fairseq  
&emsp;&emsp;}  
}

## for Understanding Doc-Level Training
- [x] Convolutional Sequence to Sequence Learning {  
&emsp;&emsp;task: mt,  
&emsp;&emsp;model: conv,  
&emsp;&emsp;author: Gehring et al.,  
&emsp;&emsp;year: 2017,  
&emsp;&emsp;labels: {  
&emsp;&emsp;&emsp;&emsp;fairseq  
&emsp;&emsp;}  
}

- [x] Context Gates for Neural Machine Translation {  
&emsp;&emsp;task: mt,  
&emsp;&emsp;model: rnn,  
&emsp;&emsp;author: Tu et al.,  
&emsp;&emsp;year: 2017,  
&emsp;&emsp;labels: {  
&emsp;&emsp;&emsp;&emsp;document-level,  
&emsp;&emsp;&emsp;&emsp;gates  
&emsp;&emsp;}  
}

## Context
### Early Papers
- [x] Exploiting Cross-Sentence Context for Neural Machine Translation {  
&emsp;&emsp;task: mt,  
&emsp;&emsp;model: rnn,  
&emsp;&emsp;author: Wang et al.,  
&emsp;&emsp;year: 2017,  
&emsp;&emsp;conference: EMNLP,  
&emsp;&emsp;labels: {  
&emsp;&emsp;&emsp;&emsp;document-level,  
&emsp;&emsp;&emsp;&emsp;additional encoder,  
&emsp;&emsp;&emsp;&emsp;hierarchical rnn  
&emsp;&emsp;}  
}

- [x] Does Neural Machine Translation Benefit from Larger Context? {  
&emsp;&emsp;task: mt,  
&emsp;&emsp;model: rnn,  
&emsp;&emsp;author: Jean et al.,  
&emsp;&emsp;year: 2017,  
&emsp;&emsp;labels: {  
&emsp;&emsp;&emsp;&emsp;document-level,  
&emsp;&emsp;&emsp;&emsp;additional encoder & attention,  
&emsp;&emsp;}  
}

### Transformer-Based
- [x] Context-Aware Neural Machine Translation Learns Anaphora Resolution {  
&emsp;&emsp;task: mt,  
&emsp;&emsp;model: transformer,  
&emsp;&emsp;author: Voita et al.,  
&emsp;&emsp;year: 2018,  
&emsp;&emsp;conference: ACL,  
&emsp;&emsp;labels: {  
&emsp;&emsp;&emsp;&emsp;additional encoder  
&emsp;&emsp;}  
}

- [x] Toward Making the Most of Context in Neural Machine Translation {  
&emsp;&emsp;task: mt,  
&emsp;&emsp;model: transformer,  
&emsp;&emsp;author: Zheng et al.,  
&emsp;&emsp;year: 2020,  
&emsp;&emsp;conference: IJCAI,  
&emsp;&emsp;labels: {  
&emsp;&emsp;&emsp;&emsp;document-level,  
&emsp;&emsp;}  
}

## GEC
### Transformer-Based
- [x] Encoder-Decoder Models Can Benefit from Pre-trained Masked Language Models in Grammatical Error Correction {  
&emsp;&emsp;task: gec,  
&emsp;&emsp;model: transformer,  
&emsp;&emsp;author: Kaneko et al.,  
&emsp;&emsp;year: 2020,  
&emsp;&emsp;conference: ACL,  
&emsp;&emsp;labels: {  
&emsp;&emsp;&emsp;&emsp;fairseq  
&emsp;&emsp;}  
}

- [x] Improving Grammatical Error Correction via Pre-Training a Copy-Augmented Architecture with Unlabeled Data {  
&emsp;&emsp;task: gec,  
&emsp;&emsp;model: transformer,  
&emsp;&emsp;author: Zhao and Wang,  
&emsp;&emsp;year: 2019,  
&emsp;&emsp;conference: NAACL,  
&emsp;&emsp;labels: {  
&emsp;&emsp;&emsp;&emsp;fairseq  
&emsp;&emsp;}  
}
