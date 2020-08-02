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
- [ ] Read: Context Gates for Neural Machine Translation (ref by the above paper)  
- [ ] P2 L | Learn: rescoring.  
- [x] P2 R | Read: Convolutional sequence to sequence learning (Fairseq)  
  After exp: not read
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
- [ ] P4 L | Pretraining decoder: unmathced params?  
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
- [ ] Read: Toward Making the Most of Context in Neural Machine Translation  
- [x] Review: LSTM, GRU  
- [ ] Read: papers about Transformer + Context  
- [ ] How to train the avg and ens?  

# Aug 1
## · Papers | Fairseq ·
  ### Questions
  - [ ] (Fairseq) P2 L | Each convolution ... Why does the param W is 2d?  
  - [ ] (Fairseq) P2 L | where A, B ... What's A, B?  
  - [ ] (Fairseq) P4 L | ...compared to recurrent nets where ... In a timestep only one GLU in the decoder?

# Aug 2
## · Questions ·
- [ ] Err prop exists in crosentgec?
- [ ] Less err prop on trg side in gec since less err on trg side?

## · Papers | Additional Encoder | Exploiting Cross-Sentence Context for Neural Machine Translation, Wang et al., 2017 ·  
### Contributions  
(1) A hierarchical way to get context  
(2) 2 strategies: warm-start & auxiliary (with / -out gate)  

### Notes
(1) P3 L | Diff from the crosentgec, the gating here considers the last output of the decoder.  
(2) P3 R | Considers the previous 3 sentences rather than 1.  
(3) P5 L | Summarizes the context alone, more flexible.  
(4) P5 L | No attn when getting context info, thus less computational costs. -> is able to consider more previous sentences  

### Questions
- [ ] P1 R | Considering target side history: suffers from err prop. Why?
