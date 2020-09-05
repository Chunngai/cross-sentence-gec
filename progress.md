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
5. The paper uses a hierarchical way to summarize context info because RNN cannot due with long-term dependencies well?

### Questions
- [ ] P1 R | Considering target side history: suffers from err prop. Why?

### Code
Provided.

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
(1) errant for bea2019 -> spacy 1.9.0 -> python3.6 & pip3.6  
(2) Python 2.7  
(3) pytorch 1.4.0  
9. Warnings & Errors:  

(1) train.py  # Solution: pytorch <= 1.4.0
  > /home/neko/GEC/helo_word-master/fairseq/fairseq/optim/adam.py:121: UserWarning: This overload of add_ is deprecated:  
	add_(Number alpha, Tensor other)  
Consider using one of the following signatures instead:  
	add_(Tensor other, \*, Number alpha) (Triggered internally at  /pytorch/torch/csrc/utils/python_arg_parser.cpp:766.)  

(2) evaluate.py  # Solution: pytorch <= 1.4.0
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

(3) evaluate.py  # Solution: spacy==1.9.0
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
In: 1 Introduction
>• we introduce a context-aware neural model, which is effective and has a sufficiently simple and interpretable interface between the context and the rest of the translation model;  
>• we analyze the flow of information from the context and identify pronoun translation as the key phenomenon captured by the model;  
>• by comparing to automatically predicted or human-annotated coreference relations, we observe that the model implicitly captures anaphora.  

### Methods
**Context Source**  
The proposed model makes use of one previous sentence as context info.

**Model the Context**  
It models the context using a Transformer encoder with 6 layers, whose structure is identical to the original Transformer. Parameters of the first 5 layers of the context encoder are shared with the source sentence encoder.

**Integration**  
The source sentence encoder consists of 6 layers, with the first 5 identical to the original Transformer. The output of the 5th source encoder layer is fed into a multi-head attention, which is the same as the previous 5 layers.

The last layer of the source encoder is where the context is integrated into. In addition to the multi-head attention mentioned above, one more multi-head attention sub-layer is set in the last layer of the source encoder to receive the output from the last layer of the context encoder as K and V, similar to the enc-dec attention in the Transformer decoder. Q of the multi-head attention is from the output of the 5-th layer in the source encoder.

Outputs of two multi-head attentions are implemented add & norm respectively, and summed using a gate. The gated sum is then fed into the feed forward neural network of the last layer of the source encoder. The gated sum $c_i$ is computed as follows
$$
c_i = g_i \odot c^{s-attn}_i + (1 - g_i) \odot c^{c-attn}_i  \\
g_i = \sigma (W_g [c^{s-attn}_i, c^{c-attn}_i] + b_g)
$$
where $c^{s-attn}_i$ is the output of the source sentence multi-head attention and $c^{c-attn}_i$ the output of the context sentence multi-head attention, after add & norm, respectively.

### Training
**Shared encoder parameters**  
In: 3 Context-aware model architecture
> In contrast to related work (Jean et al., 2017; Wang et al., 2017), we found in preliminary experiments that using separate encoders does not yield an accurate model. Instead we share the parameters of the first N − 1 layers with the source encoder.

**Distinguish between the context and the source sentence**  
In: 3 Context-aware model architecture
> Since major proportion of the context encoder’s parameters are shared with the source encoder, we add a special token (let us denote it \<bos\>) to the beginning of context sentences, but not source sentences, to let the shared layers know whether it is encoding a source or a context sentence.

Note that \<eos\> presents in both the context sentence and the source sentence, while <bos> is only in the context sentence.

### Comparison With Other Methods
1. In: 1 Introduction
> When compared to simply concatenating input sentences, as proposed by Tiedemann and Scherrer (2017), our architecture appears both more accurate (+0.6 BLEU) and also guarantees that the contextual information cannot bypass the attention layer and hence remain undetected in our analysis.

2. In: 3 Context-aware model architecture
> In contrast to related work (Jean et al., 2017; Wang et al., 2017), we found in preliminary experiments that using separate encoders does not yield an accurate model. Instead we share the parameters of the first N − 1 layers with the source encoder.

Some other papers use additional encoder to model context, whose parameters are shared. Is it possible that using separate encoders yield inaccurate results is because of the structure of the proposed model?

3. In 5.1: Overall performance
> Tiedemann and Scherrer (2017) only used a special symbol to mark where the context sentence ends and the source sentence begins. This technique performed badly with the non recurrent Transformer architecture in preliminary experiments, resulting in a substantial degradation of performance (over 1 BLEU).

### Notes
1. The model preforms well for pronouns in the machine translation task in the paper. In the machine translation task here the tense of sources and targets are not difficult to maintain consistent. But that may not the case for gec tasks. Thus the model may make use of context info to make corrections in gec training, not only be limited to pronouns.
2. The proposed model integrates the context on the encoder side.
3. In 5.1: Overall performance
> We also notice that, unlike the previous sentence, the next sentence does not appear beneficial. This is a first indicator that discourse phenomena are the main reason for the observed improvement, rather than topic effects.

4. The paper uses random context for experiments to show that the model is not merely better regularized by the context.
5. Plotting the attention weight matrix can be a way to see if the context info helps.
6. Encoding the context using a different encoder is still worth a try, despite the preliminary result of the paper.

### Future work
1. In: 7 Conclusions
> Improving the attention component is likely to boost translation performance.

### Questions
- [ ] What if exchange the position of $g_i$ and $(1 - g_i)$ in the gating mechanism?
- [ ] The is a <bos> needed for context sentence?
- [ ] P2 L | R effective ...
- [ ] P3 R | In: 3 Context-aware model architecture
> Since major proportion of the context encoder’s parameters are shared with the source encoder, we add a special token (let us denote it \<bos\>) to the beginning of context sentences, but not source sentences, to let the shared layers know whether it is encoding a source or a context sentence.

Why does the paper distinguish between the context and the source sentence?

- [ ] P4 R | binary flag.


### Source Code
Not provided.

---

# Aug 20
## · Papers · | Additional Encoder & Transformer | Improving the Transformer Translation Model with Document-Level Context, Zhang et al., 2018
### Contributions
In: 1 Introduction
> 1. Increased capability to capture context: the use of multi-head attention, which significantly reduces the path length between long-range dependencies, helps to improve the capability to capture document-level context;
> 2. Small computational overhead: as all newly introduced modules are based on highly parallelizable multi-head attention, there is no significant slowdown in both training and decoding;
> 3. Better use of limited labeled data: our approach is capable of maintaining the superiority over the sentence-level counterpart even when only small-scale document-level parallel corpora are available.

### Methods
**Context Source**  
The paper experiments with the length of previous sentences (1, 2, 3) and finds that the model preforms best when the length is 2. Thus they uses the previous 2 sentences as context. The 2 sentences are concatenated directly.

**Model the Context**  
The proposed method uses an additional Transformer encoder to model the context. The structure of the encoder layer is identical to the original Transformer. After experiments they find that a single encoder sub-layer is enough. Thus the sub-layer number of the additional encoder for modeling context is set to 1.

**Integration**  
The output of the last layer in the context encoder is used as context info. It's integrated into both the encoder and the decoder.

The Transformer encoder for source sentences in the paper has one more multi-head attention sub-layer than the original Transformer encoder, which is for integrating the context info. The sub-layer is above the self-attention sub-layer and below the feed forward neural network sub-layer. Similar to the enc-dec attention in the Transformer decoder, Q of the context attention sub-layer is from the output of the self-attention below it, and K and V is the context info, i.e. the output of the last layer in the context encoder.

Similar to the encoder mentioned above, the decoder also has one more sub-layer, which is also a multi-head attention sub-layer. It is above the self-attention sub-layer and below the enc-dec attention sub-layer. The source of Q, K, V is identical to those in the encoder, i.e., Q from the output of the self-attention sub-layer below, and K, V from the output of the context encoder.

For filtering context info, the paper replaces the residual connections after the context attention in the encoder and the decoder with a gating mechanism, respectively.
The original residual connection is
$$
Residual(H) = H + SubLayer(H)
$$
where H is the input of the sub-layer. Here it is the output (Q) of the self-attention sub-layer below. $SubLayer(·)$ here is actually the context attention.  
The gating which replaces the residual connection in the context-attention sub-layer is as follows
$$
Gating(H) = \lambda H + (1 - \lambda) SubLayer(H)  \\
\lambda = \sigma (W_i H + W_s SubLayer(H))
$$

### Training
**Solving the problem of lack of enough document-level parallel data**  
In: 2.4 Training
> Unfortunately, large-scale document-level parallel corpora are usually unavailable, even for resource-rich languages such as English and Chinese. Under small-data training conditions, document level NMT is prone to underperform sentence-level NMT because of poor estimates of low-frequency events. To address this problem, we adopt the idea of freezing some parameters while tuning the re- maining part of the model (Jean et al., 2015; Zoph et al., 2016).

> In the first step, sentence-level parameters $\theta_s$ are estimated on the combined sentence-level parallel corpus $D_s ∪ D_d$. Note that the newly introduced modules (high-lighted in red in Figure 1(b)) are inactivated in this step. $P(y|x; θ_s)$ is identical to the original Transformer model, which is a special case of our model.
$$
\hat{\theta_s} = \mathop{argmax}\limits_{\theta_s} \sum_{<x, y> \in D_s \cup D_d} log P(y | x; \theta_s)
$$

Note that the $x$ and $y$ here are sentences.

> In the second step, document-level parameters $θ_d$ are estimated on the document-level parallel corpus $D_d$ only:
$$
\hat{\theta_d} = \mathop{argmax}\limits_{\theta_d} \sum_{<x, y> \in D_d} log P(Y | X; \hat{\theta_s}, \theta_d)
$$

Note that the $X$ and $Y$ here are documents.

**When no preceding sentence**  
In: 2.4 Training
> If there is no preceding sentence, we simply use a single begin-of-sentence token.

### Comparison With Other Methods
1. In: 4 Related Work
> Voita et al. (2018) also extended Transformer to model document-level context, but our work is different in modeling and training strategies. The experimental part is also different. While Voita et al. (2018) focus on anaphora resolution, our model is able to improve the overall translation quality by integrating document-level context.

### Notes
1. In: 1 Introduction
> To the best of our knowledge, only one existing work has endeavored to model document-level context for the Transformer model

The paper is after Voita et al., 2018 and it seems that Voita et al., 2018 is the first work to model context with Transformer.

2. In: 2.2 Document-level Context Representation
> As document-level context often includes several sentences, it is important to capture long-range dependencies and identify relevant information.

Thus multi-head attention.

3. The output in the proposed model has a \<bos\> at the beginning. (The original Transformer also does?)

4. In 2.4: Training
> Under small-data training conditions, document level NMT is prone to underperform sentence-level NMT because of poor estimates of low-frequency events. To address this problem, we adopt the idea of freezing some parameters while tuning the remaining part of the model (Jean et al., 2015; Zoph et al., 2016).

> Our approach is also similar to pre-training which has been widely used in NMT (Shen et al. ,2016; Tu et al., 2018). The major difference is that our approach keeps θ̂ s fixed when estimating $θ_d$ to prevent the model from overfitting on the relatively smaller document-level parallel corpora.

Applicable for gec?

5. In 3.2: Effect of Context Length
> This confirms the finding of Tu et al. (2018) that long-distance context only has limited influence.

6. In 3.7: Effect of Two-Step Training
> We find that document-level NMT achieves much worse results than sentence-level NMT (i.e., 36.52 vs. 39.53) when only small-scale document-level parallel corpora are available. Our two-step training method is capable of addressing this problem by exploiting sentence-level corpora.

Corpora of gec is small. Will the performance of the gec model be worse using document-level data than using sentence-level data in the same size?

### Ideas
1. Generate document-level data for pretraining.

### Questions
- [ ] P1 R | In: 1 Introduction
> Since large-scale document-level parallel corpora are usually hard to acquire, we propose to train sentence-level model parameters on sentence-level parallel corpora first and then estimate document-level model parameters on document-level parallel corpora while keeping the learned original sentence-
level Transformer model parameters fixed.

Why don't they treat the sentence-level corpora as document-level corpora with no preceding context and train the whole model in one shot?

- [ ] P2 L | The translation error propagation problem.
- [ ] P5 L | In 2.4: Training
> Under small-data training conditions, document-level NMT is prone to underperform sentence-level NMT because of poor estimates of low-frequency events.

- [ ] P6 L | Length penalty.

### Source Code
Provided.

## · Papers · | Hierarchical Attention & RNN | Document-Level Neural Machine Translation with Hierarchical Attention Networks, Miculicich et al., 2018
### Contributions
In: 1 Introduction
> (i) We propose a HAN framework for translation to capture context and inter-sentence connections in a structured and dynamic manner.  
> (ii) We integrate the HAN in a very competitive NMT architecture (Vaswani et al., 2017) and show significant improvement over two strong baselines on multiple data sets.   
> (iii) We perform an ablation study of the contribution of each HAN configuration, showing that contextual information obtained from source and target sides are complementary.

### Methods
**Context Source**  
The paper experiments with the context sentence length and finds the model performs best with 3 previous sentences. Thus the paper uses 3 previous sentences as context.

**Model the Context**  
The context is modeled in a hierarchical way.  
First each context sentence $j$ is summarized into a vector $s^j$ in a word-level abstraction.
$$
q_w = f_w(h_t)  \\
s^j = \mathop{MultiHead}\limits_{i}(q_w, h^j_i)
$$
where $h_t$ is the last hidden state of the word to be encoded or decoded at time step t, $f_w(·)$ is a linear transformation function to generate the query $q_w$. $h^j_i$ is the last hidden state of the i-th word in the j-th context sentence.
Then each $s^j$ is summarized into the contextual information $d_t$ required at time t in a sentence-level abstraction.
$$
q_s = f_s(h_t)  \\
d_t = FFN(\mathop{MultiHead}\limits_{j}(q_s, s^j))
$$
where $f_s(·)$ is a linear transformation function to get the query $q_s$.

In: 2.1 Hierarchical Attention Network
> The context can be used during encoding or decoding a word,  
and it can be taken from previously encoded source sentences, previously decoded target sentences, or from previous alignment vectors (i.e. context vectors (Bahdanau et al., 2015)).  
The different configurations will define the input query and values of the attention function.  

> In this work we experiment with five of them: one at encoding time, three at decoding time, and one combining both.

(1)
> At encoding time the query is a function of the hidden state $h_{x_t}$ of the current word to be encoded $x_t$, and the values are the encoded states of previous sentences $h^j_{x_i}$ (HAN encoder).

> At decoding time, the query is a function of the hidden state $h_{y_t}$ of the current word to be decoded $y_t$ , and the values can be

(2)
> (a) the encoded states of previous sentences $h^j_{x_i}$ (HAN decoder source),

(3)
> (b) the decoded states of previous sentences $h^j_{y_i}$ (HAN decoder), and

(4)
> (c\) the alignment vectors $c^j_i$ (HAN decoder alignment).

(5)
> Finally, we combine complementary target-source sides of the context by joining HAN encoder and HAN decoder.

**Integration**  
The context info is integrated with a gating mechanism.
$$
\lambda_t = \sigma(W_h h_t + W_d d_t)  \\
\tilde{h_t} = \lambda h_t + (1 - \lambda_t)d_t
$$
where $\tilde{h_t}$ is the last hidden state at time step t., as replacement of $h_t$ during the final classification layer.

### Training
In: 3.2 Model Configuration and Training
> Inspired by Tu et al. (2018) we trained the models in two stages. First we optimize the parameters for the NMT without the HAN, then we proceed to optimize the parameters of the whole network.

### Comparison With Other Methods
1. The model proposed in the paper is similar to the one in Wang et al., 2017. The difference is that Wang et al. model the context with RNNs without attention, while the proposed method here uses the multi-head attention to model context dynamically.

2. In 1: Introduction
> Most of these methods use an additional encoder (Jean et al., 2017; Wang et al., 2017) to extract contextual information from previous source-side sentences. However, this requires additional parameters and it does not exploit the representations already learned by the NMT encoder.

3. In 1: Introduction
> The cache-based memory keeps past context as a set of words, where each cell corresponds to one unique word keeping the hidden representations learned by the NMT while translating it. However, in this method, the word representations are stored irrespective of the sentences where they occur, and those vector representations are disconnected from the original NMT network.

### Notes
1. The model here considers context from both the source side and the target side, which are said complementary.

2. In: 3.2 Model Configuration and Training
> An important portion of the improvement comes from the HAN encoder, which can be attributed to the fact that the source-side always contains correct information, while the target-side may contain erroneous predictions at testing time.

Using the last hidden state of the context from both the source side and the target side brings better performance for their complementary information, despite the error propagation.

3. The attention of each head in the multi-head attention can be used for analysis, as in the appendix.

### Questions
- [ ] P1 L | In 1: Introduction
> Most of these methods use an additional encoder (Jean et al., 2017; Wang et al., 2017) to extract contextual information from previous source-side sentences. However, this requires additional parameters and it does not exploit the representations already learned by the NMT encoder.

But the model here also requires additional parameters?

- [ ] P2 L | Error propagation?

- [ ] P3 R | In: 3.2 Model Configuration and Training
> Inspired by Tu et al. (2018) we trained the models in two stages. First we optimize the parameters for the NMT without the HAN, then we proceed to optimize the parameters of the whole network.

What's the purpose?

### Source Code
Provided.

---

# Aug 24

## · Papers · | Additional Encoder & Transformer | Selective Attention for Context-aware Neural Machine Translation, Maruf et al., 2019
### Contributions
In: 1 Introduction
> (i) we propose a novel and efficient top-down approach to hierarchical attention for context-aware NMT,  
> (ii) we compare variants of selective attention with both context-agnostic and context-aware baselines, and  
> (iii) we run experiments in both online (only past context) and offline (both past and future context) settings on three English-German datasets.  

### Methods
**Context Source**  
The proposed model makes use of the whole document to be context.

**Model the Context**  
The proposed method uses a context layer to model the context, which can be seen as an additional encoder. The context layer is similar to the encoder layer of the Transformer, consisting of 2 sub-layers. The first sub-layer is a multi-head context attention, which contains a hierarchical context attention module or a flat attention module. The second sub-layer is a normal feed forward neural network. Each sub-layer is followed by a layer-norm, but without residual connections, for the reason quoted below.

In: Footnote of 3.1 Document-level Context Layer
> We do not have residual connections after sub-layers in our Document-level Context Layer as we found them to have a deteriorating effect on the translation scores (also reported by Zhang et al. (2018)).

The paper uses 2 ways to implement the context attention, with a hierarchical context attention module or with a flat attention module.

**(1) Hierarchical context attention**  
The hierarchical context attention module is extended from the Transformer attention.  

The first step is a sentence-level key matching. Basically the step here evaluates the relative importance of each sentence in the document.
$$
\alpha_s = sparsemax(Q_s K^T_s / \sqrt{d_k})
$$
where $\alpha_s$ is a sequence containing weights of all sentences in the document. $d_k$ is the dimension of the keys.  
$sparsemax(·)$ is applied instead of $softmax(·)$ to make the selective attention that focus the attention on the relevant sentences, while ignoring the remaining.  
$Q_s$ and $K_s$ here are sentence-level, and have different sources depending on the manner of integration (integrating into the encoder OR the decoder).  
An additive mask is used before $sparsemax(·)$ to mask the current sentence or the current and future sentences, for offline (considering both the previous and the latter) setting and online setting (considering only the previous), respectively.

Except the sentence-level matching there is also a word-level matching. It determines the relative importance of each word in a sentence $j$.
$$
\alpha^j_w = sparsemax(Q_w {K^j_w}^T / \sqrt{d_k})
$$
where $\alpha^j_w$ is a sequence consisting weights of all words in the sentence.
$softmax(·)$ is used for comparison in the experiments of the paper.

The third step is re-scaling attention weights. The step here considers both the importance of sentences and words.
$$
\alpha^j_{hier} = \alpha_s(j) \alpha^j_w
$$
where $\alpha_s(j)$ is the relative importance of the j-th sentence.
$\alpha^j_{hier}$ is then concatenated
$$
\alpha_{hier} = Concat(\alpha^j_{hier})
$$
$\alpha_{hier}$ here can be interpreted as that the importance of a word in sentence $j$ and the importance of sentence $j$ in the whole document altogether contribute to the final importance of that word in the document. The length of $\alpha_{hier}$ is identical to the number of words in the document.  
$Q_w and K_w$ here are word-level, and have different sources depending on the manner of integration (integrating into the encoder OR the decoder).

Finally the value reading assigns the weights to each word.
$$
\alpha_{hier} V_w
$$

Multi-head is also used.
$$
\mbox{H-MULTIHEAD}(Q_s, K_s, Q_w, K_w, V_w) = Concat(head_1, ..., head_H) W_O  \\
head_h = \mbox{H-MULTIHEAD}(Q_s W^{Q_s}_h, Q_w W^{Q_w}_h, K_s W^{K_s}_h, K_w W^{K_w}_h, V_w W^{V_w}_h)
$$

**(2) Flat attention**  
It's basically the same as the scaled dot-product attention in the Transformer.
$$
Attention(Q, K, V) = softmax(Q K^T / \sqrt{d_k}) V
$$
$Q$ and $K$ here can either be sentence-level or word-level.

**Integration**  
The paper uses 2 integration methods: monolingual and bilingual, to integrate the context into the NMT model.  
For the monolingual one, the output of the context layer is integrated with the output of the last layer in the encoder. For the bilingual one, the output of the context layer is integrated with the output of the last layer in the decoder. Both use a gating mechanism to filter context info.

$$
\gamma_i = \sigma (W_r r_i + W_d d_i)  \\
\tilde{r_i} = \gamma_i \odot r_i + (1 - \gamma_i) \odot d_i
$$
where $r_i$ is the output of the last layer in the encoder (monolingual) or decoder (bilingual). $d_i$ is the output of the context layer. $\tilde{r_i}$ is the integrated output of the encoder or decoder.

The source of $Q$, $K$ and $V$ depend on the integration method.  
For the monolingual one, $Q$ is a linear transformation of the output of the last layer in the encoder. For the bilingual one, $Q$ is a linear transformation of the output of the enc-dec attention in the last layer of the decoder.  
$K$ and $V$ are from a pre-trained sentence-level NMT model. For the monolingual one, $Q_w$ and $V_w$ are representations of all source words in the document which are from the last layer of the encoder. $Q_s$ and $V_s$ are representations of all sentences in the document, each of which are formed by averaging the word representations in that sentence. For the bilingual one, keys and values are from outputs of the enc-dec attention sub-layer and the self-attention sub-layer in the last layer of the decoder, respectively.

### Training
In: 2.2 Document-level Machine Translation
> The first step involves pre-training a standard sentence-level NMT model, and the second step involves optimising the parameters of the whole model, i.e., both the document-level and the sentence-level parameters.

### Decoding
In: 2.2 Document-level Machine Translation
> a two-pass Iterative Decoding strategy (Maruf and Haffari, 2018): first, the translation of each sentence is initialised using the sentence-based NMT model; then, each translation is updated using the context-aware NMT model fixing the other sentences’ translations.

In: 4.1 Setup
> For inference, we use Iterative Decoding only when using the bilingual context. All experiments are run on a single Nvidia P100 GPU with 16GBs of memory.

### Comparison With Other Methods
1. The paper considers the whole document as context, which is different from other papers considering only a few previous sentences as context.

2. In: 1 Introduction
> Only one existing work has endeavoured to consider the full document context (Maruf and Haffari, 2018), thus proposing a more generalised approach to document-level NMT. However, the model is re- strictive as the document-level attention computed is sentence-based and static (computed only once for the sentence being translated).

3. In: 1 Introduction
> A more recent work (Miculicich et al., 2018) proposes to use a hierarchical attention network (HAN) (Yang et al., 2016) to model the contextual information in a structured manner using word-level and sentencelevel abstractions; yet, it uses a limited number of past source and target sentences as context and is not scalable to entire document.

4. In: 1 Introduction
> In this work, we propose a selective attention approach to first selectively focus on relevant sentences in the global document-context and then attend to key words in those sentences, while ignoring the rest.

It assumes that not each sentence in the document is equally important. A word is more related to the current querying word if it's more important in that context sentence, and that context sentence is more important in the whole document.

5. In: Footnote of 3.3 Integrated Model
> We do not integrate context into both encoder and decoder as it would have redundant information from the source (the context incorporated in the decoder is bilingual), in addition to increasing the complexity of the model.

Zhang et al., 2018, however, consider that the context info in both sides is complementary.

6. The sparse attention focuses on words that are really matter, while ignoring the rest, which is unlike the softmax.

### Notes
1. The paper makes use of the WHOLE document as context, not merely a few previous sentences.

2. The word-level flat attention here is similar to the Transformer attention for modeling context info  in other papers, which takes the concatenation of a few sentences as input, except for that words in each sentence are considered here.

3. The context layer proposed in the paper can be seen as an additional encoder with a single layer. However, the additional encoder here is capable of taking all sentences in the document into account.   
Modeling the context info in a hierarchical way (sentence-level & word-level) and the sparsemax as the replacement of softmax may be the keys that enable the model to do that. The keys and values for the context-attention provided by a pre-trained sentence-level NMT model may also be a reason.

4. In: 4.2 Main Results
> This, in our opinion, does not mean that we should never look into the future, but just that NMT models in general are highly subjective to data, and whether context-aware models benefit from future context is also dependent on that.

### Questions
1. P2 R | In: 2.2 Document-level Machine Translation
> The first step involves pre-training a standard sentence-level NMT model, and the second step involves optimising the parameters of the whole model, i.e., both the document-level and the sentence-level parameters.

What's the purpose?

2. P2 R | What's the purpose of two-pass iterative decoding?

3. P3 L | In: Footnote of 3.1 Document-level Context Layer
> We do not have residual connections after sub-layers in our Document-level Context Layer as we found them to have a deteriorating effect on the translation scores (also reported by Zhang et al. (2018)).

It seems that the condition here is not the same as that in Zhang et al. The input and output of the context-attention sub-layer here are both context.

### Source Code
Provided.

### TODO
- [ ] Read: Maruf et al., 2018
- [ ] Learn: Sparse Transformer

---

# Aug 25
## · Papers · | Additional Encoder & Transformer | Hierarchical Modeling of Global Context for Document-Level Neural Machine Translation, Tan et al., 2019
### Contributions
In: 1 Introduction
> we propose to improve document-level translation with the aid of global context, which is hierarchically extracted from the entire document with a sentence encoder modeling intra-sentence dependencies and a document encoder modeling document-level inter-sentence context.
> we propose a novel method to feed back the extracted global document context to each word in a top to-down manner to clarify the translation of words in specific surrounding contexts.
> We conduct experiments on both the traditional RNNSearch model and the state-of-the-art Transformer model.

### Methods
**Context Source**  
The paper considers the whole document as context.

**Model the Context**  
In the sentence-level, each sentence $S_i$ is encoded using a sentence encoder (Transformer encoder for Transformer) into a sentence representation $H_i$.
$$
H_i = SentEnc(S_i)
$$
In the document-level, each sentence representation $H_i$ is first fed into a multi-head self-attention. Then the output of the self-attention is summed up on the axis of the sentence length. The summed vector is then encoded by a document encoder (Transformer encoder for Transformer, which shares the same parameters with the sentence encoder as Voita et al., 2018) into $H_i$.
$$
h_{S_i} = \mbox{MultiHead-Self}(H_i, H_i, H_i)  \\
\tilde{h_{S_i}} = \sum_{h \in h_{S_i}} h  \\
H_S = DocEnc(\tilde{h_S})
$$

The global context is then back propagated to equip each word with global document context. This is done by one more multi-head attention.
$$
\alpha_{i, j} = \mbox{MultiHead-Ctx}(h_{i, j}, h_{i, j}, H_{S_i})  \\
d_{ctx_{i, j}} = \alpha_{i, j} H_{S_i}
$$
where $h_{i, j}$ is the representation of the j-th word in the i-th sentence. $d_{ctx_{i, j}}$ is the corresponding context info distributed in the word.  
Basically the step here means how much context info contained in $H_{S_i}$ should be assigned to the word $h_{i, j}$. It may be similar to the gating in other papers.

**Integration**  
In the encoding phase, the context info is integrated via a residual connections.
$$
h_{ctx_{i, j}} = h_{i ,j} + \mbox{ResidualDrop}(d_{ctx_{i, j}}, P)
$$
where $h_{ctx_{i, j}}$ is the integrated representation of the word. $\mbox{ResidualDrop}(·)$ is the residual connection function and $P$ is the rate of residual dropout.  
The step here may be in the last layer of the sentence encoder?

In the decoding phase, the context info is integrated via an additional multi-head attention.
$$
C = [d_{ctx_1}; d_{ctx_2}; ...; d_{ctx_N}]  \\
G^{(n)} = \mbox{MultiHead-Attn}(T^{(n)}, C^{(n)}, C^{(n)})
$$
where $T^{(n)}$ is the output of the self-attention sub-layer in the decoder.  
**Note that the $d_{ctx_i}$ of $C$ is $h_{ctx_1}$ in the paper. But it should be $d_{ctx_1}$ according to the description in "2.2 Integrating the HM-GDC model into NMT" of the paper:**
> we introduce an additional sub-layer into the decoder that performs multi-head attention over the output of the document encoder, which we refer to as DocEnc-Decoder attention (shown in Figure 3). Different from (Vaswani et al., 2017), the keys and values of our DocEnc-Decoder attention come from the output of the document encoder.

$G^{(n)}$ is then added with $E^{(n)}$ which is the output of the enc-dec attention sub-layer to form the final output of the decoder layer.
$$
H^{(n)} = E^{(n)} + G^{(n)}
$$

### Training
**Shared parameters**  
For the transformer model, The parameters of the multi-head self-attention in the sentence-level encoder and the document-level encoder are shared, following Voita et al., 2018.

**Two-step training**  
A two step training strategy is used.  
First the sentence-level parameters are trained with the union of sentence-level and document-level data.
$$
\hat{\theta_s} = \mathop{arg max}\limits_{\theta_s} \sum_{<x, y> \in D_s} log P(y | x; \theta_s)
$$
Then the document-level parameters are trained and the sentence-level parameters are fine-tuned with the document-level data.
$$
\hat{\theta_d} = \mathop{arg max}\limits_{\theta_d} \sum_{<x, y> \in D_d} log P(y | x; \theta_d, \hat{\theta_s})
$$

### Comparison With Other Methods
1. Many NMT models considering context suffer from incomplete document context.

### Notes
1. In: Abstract
> With this hierarchical architecture, we feedback the extracted global document context to each word in a top-down fashion to distinguish different translations of a word according to its specific surrounding context.

2. In: 1 Introduction
> However, when there exists a huge gap between the pre-context and the context after the current sentence $s i$ , the guidance from pre-context is not sufficient for the NMT model to fully disambiguate the sentence $s i$. On the one hand, the translation of the current sentence $s i$ may be inaccurate due to the one-sidedness of partial context. On the other hand, translating the succeeding sentences in the document may much suffer from the semantic bias due to the transmissibility of the improper pre-context.

3. In: 1 Introduction
> To avoid the issue of translation bias propagation caused by improper pre-context, we propose to extract global context from all sentences of a document once for all.

4. The two-step training is similar to the pretrain-train(-finetune) training method in gec.

5. In: 3.2 Experimental Results
> using a large-scale corpus with out-of-domain parallel pairs $D_s$ to pre-train the Transformer model results in worse performance due to domain inadaptability (the first and the fourth row in the second group). By contrast, our proposed model can effectively eliminate this domain inadaptability (the third and sixth row in the second group).

### Questions
- [ ] P3 L | The multi-head self-attention for $H_i$ should be the feature extraction in the sentence-level instead of the document-level? Why does the paper say that it determines the relative importance of different $H_i$?

- [ ] P1 R | In: 1 Introduction
> On the other hand, translating the succeeding sentences in the document may much suffer from the semantic bias due to the transmissibility of the improper pre-context.

What does it mean?

- [ ] P2 L | In: Introduction
> thus effectively avoiding the transmissibility of improper pre-context.

Why?

### Source Code
Not provided.

---

# Aug 26 - Sep 2

## Document-level context -> GEC
1. - [x] Find all available document-level gec datasets.  

(1) bea2019-fce: train

  fce.{train | dev | test}.json

  helo_word-master_restricted/data/bea19/fce/m2/fce.dev.gold.bea19.m2
  helo_word-master_restricted/data/bea19/fce/m2/fce.test.gold.bea19.m2
  helo_word-master_restricted/data/bea19/fce/m2/fce.train.gold.bea19.m2

(2) bea2019-wi+locness: train & finetune & dev & test

  {A.{train | dev} | B.{train | dev} | C.{train | dev} | N.dev}.json  

  train:
  helo_word-master_restricted/data/bea19/wi+locness/m2/A.train.gold.bea19.m2
  helo_word-master_restricted/data/bea19/wi+locness/m2/ABC.train.gold.bea19.m2
  helo_word-master_restricted/data/bea19/wi+locness/m2/B.train.gold.bea19.m2
  helo_word-master_restricted/data/bea19/wi+locness/m2/C.train.gold.bea19.m2

  dev:
  helo_word-master_restricted/data/bea19/wi+locness/m2/ABCN.dev.gold.bea19.m2

(3) nucle: train & finetune

  nucle3.2.sgml  

  helo_word-master_restricted/data/bea19/nucle3.3/bea2019/nucle.train.gold.bea19.m2

(4) conll2013: dev

  {original | revised}/data/official.sgml  

  helo_word-master_restricted/data/conll2013/release2.3.1/revised/data/official-preprocessed.m2

(5) conll2014: test

  noalt/official-2014.{0 | 1}.sgml  
  alt/alternative-team{a | b | c}.sgml

  helo_word-master_restricted/data/conll2014/conll14st-test-data/noalt/official-2014.combined.m2

(6) lang8-multi: train

  crosentgec/data/tmp/lang-8-20111007-L1-v2.xml

```
[
    '/home/neko/GEC/helo_word-master_restricted/data/bea19/fce/m2/fce.dev.gold.bea19.m2',
    '/home/neko/GEC/helo_word-master_restricted/data/bea19/fce/m2/fce.test.gold.bea19.m2',
    '/home/neko/GEC/helo_word-master_restricted/data/bea19/fce/m2/fce.train.gold.bea19.m2'
]

[
    '/home/neko/GEC/helo_word-master_restricted/data/bea19/lang8.bea19/lang8.train.auto.bea19.m2'
]

[
    '/home/neko/GEC/helo_word-master_restricted/data/bea19/nucle3.3/bea2019/nucle.train.gold.bea19.m2'
]

[
    '/home/neko/GEC/helo_word-master_restricted/data/bea19/wi+locness/m2/A.train.gold.bea19.m2',
    '/home/neko/GEC/helo_word-master_restricted/data/bea19/wi+locness/m2/ABC.train.gold.bea19.m2',
    '/home/neko/GEC/helo_word-master_restricted/data/bea19/wi+locness/m2/B.train.gold.bea19.m2',
    '/home/neko/GEC/helo_word-master_restricted/data/bea19/wi+locness/m2/C.train.gold.bea19.m2'
]

[
    '/home/neko/GEC/helo_word-master_restricted/data/bea19/wi+locness/m2/ABCN.dev.gold.bea19.m2'
]

[
    '/home/neko/GEC/helo_word-master_restricted/data/conll2013/release2.3.1/revised/data/official-preprocessed.m2'
]

[
    '/home/neko/GEC/helo_word-master_restricted/data/conll2014/conll14st-test-data/noalt/official-2014.combined.m2'
]
```

2. Retrieve src, trg, ctx from document-level gec datasets.
```
IN: ori_filename, doc_filename, n_prev, n_fol
OUT: ctx_filename

def get_documents(indices):
    sentences = oris[indices]

    doc_indices = []
    for i in len(docs):
        doc = docs[i]
        if doc.contains(sentences):  # Uses `ori_sentence` to get the document.
            doc_indices.append(i)

    return doc_indices

def get_document(ori_sentence_index):
    for j in 1...10:
        doc_indices = get_documents(i, i+j)
        if len(doc_indices) == 1:
            doc_index = doc_indices[0]
            return docs[doc_index]

        doc_indices = get_documents(i-j+1, i+1)
        if len(doc_indices) == 1:
            doc_index = doc_indices[0]
            return docs[doc_index]




oris = open(ori_filename, "r").readlines()  # An array consisting all sentences.
docs = open(doc_filename, "r").readlines()  # A formatted raw file containing documents.
f_ctx = open(ctx_filename, "w")

# Gets all documents.
documents = get_documents(doc)  # Depends on the format of `doc_filename` (json / sgml / xml).

# Extracts contexts.
for i in 0..<oris.len:
    ori_sentence = oris[i]

    # Gets the document consisting `ori_sentence`
    doc = get_document(i)

    # Gets the position of `ori_sentence`.
    index = doc.index_of(ori_sentence)

    # Gets the context.
    context = doc[index - n_prev : index + n_fol + 1]
    context -= ori_sentence

    # Writes to file.
    f_ctx.write(context)
```
ori: [FILE_NAME].ori
doc: [FILE_NAME].[{json | sgml | xml}]

---

Sep 2 - Sep 4
Extend fairseq to support context.

---

Sep 5

Extend fairseq.

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

## Related
- [x] Convolutional Sequence to Sequence Learning {  
&emsp;&emsp;task: mt,  
&emsp;&emsp;model: conv,  
&emsp;&emsp;author: Gehring et al.,  
&emsp;&emsp;year: 2017,  
&emsp;&emsp;labels: {  
&emsp;&emsp;&emsp;&emsp;fairseq  
&emsp;&emsp;}  
}

## Context
### Early Papers
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

### RNN based
- [x] Document-Level Neural Machine Translation with Hierarchical Attention Networks {  
&emsp;&emsp;task: mt,  
&emsp;&emsp;model: rnn,  
&emsp;&emsp;author: Miculicich et al.,  
&emsp;&emsp;year: 2018,  
&emsp;&emsp;labels: {  
&emsp;&emsp;&emsp;&emsp;document-level,  
&emsp;&emsp;&emsp;&emsp;hierarchical attention
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

- [x] Improving the Transformer Translation Model with Document-Level Context {  
&emsp;&emsp;task: mt,  
&emsp;&emsp;model: transformer,  
&emsp;&emsp;author: Zhang et al.,  
&emsp;&emsp;year: 2018,  
&emsp;&emsp;conference: ACL,  
&emsp;&emsp;labels: {  
&emsp;&emsp;&emsp;&emsp;additional encoder  
&emsp;&emsp;}  
}

- [x] Selective Attention for Context-aware Neural Machine Translation {  
&emsp;&emsp;task: mt,  
&emsp;&emsp;model: transformer,  
&emsp;&emsp;author: Maruf et al.,  
&emsp;&emsp;year: 2019,  
&emsp;&emsp;conference: NAACL,  
&emsp;&emsp;labels: {  
&emsp;&emsp;&emsp;&emsp;additional encoder
&emsp;&emsp;}  
}

- [x] Hierarchical Modeling of Global Context for Document-Level Neural Machine Translation {  
&emsp;&emsp;task: mt,  
&emsp;&emsp;model: transformer,  
&emsp;&emsp;author: Tan et al.,  
&emsp;&emsp;year: 2019,  
&emsp;&emsp;conference: IJCNLP,  
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
&emsp;&emsp;&emsp;&emsp;document-level
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
