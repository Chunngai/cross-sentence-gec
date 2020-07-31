# Jul 29

## Note
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
A main diff is that in 2.* ver, "a,b" is treated as a token, while in 3.* ver it is treated as ["a", " ", "b"]. The previous treatment may introduce more OOV?

2. The decoder is similar to that of bert?  
  A: Seems not.

## TODO
- [ ] try to train a model with ver 3.* tokenization.

---

# Jul 31

## Idea
1. Apply iterative decoding to improve performance, especially for long sentences.
2. P3 left | Attn: switch to multi-head attn?
3. P3 left | Other operation for context sentences except concat?
4. P4 left | Lang8: noisy. Use another dataset for training.
5. P4 right | What about using more previous sentences?
6. P4 right | What about using following sentences?
7. P7 left | Data synthetic both for training and evaluation.

## TODO
- [x] P2 left | Learn: auxiliary encoders.  
  - [ ] Read: Exploiting Cross-Sentence Context for Neural Machine Translation (ref by the above paper)
    - [ ] Read: Context Gates for Neural Machine Translation (ref by the above paper)
- [ ] P2 left | Learn: rescoring.
- [x] Learn: BERT
- [ ] P2 right | Read: Convolutional sequence to sequence learning
- [ ] P2 right | Read: Language modeling with gated convolutional networks
- [x] Learn: label smoothing
- [ ] Find other available datasets for training or evaluation.
- [ ] Read: Toward Making the Most of Context in Neural Machine Translation

## Question
- [x] P2 left | Incorporate probabilities computed by BERT as a feature.  
  BERT can be used as a feature extractor.
- [ ] P2 right | Do not explicitly consider previously corrected target sentences to avoid error propagation.
- [ ] P3 left | Why to compute the attn that way? proposed in other paper? Similar to the one proposed in Luong et al.?
- [ ] P3 left | The last decoder state.
- [ ] P3 right | Why does the gating can control crosent info?
- [ ] P3 right | Where does the gating mechanism come from? Is it similar to LSTM?
- [ ] P4 left | Pretraining decoder: unmathced params?
- [ ] P4 left | Dropping out entire word embeddings of source words: where is the code?
- [ ] P4 left | We also rescore the ...
- [ ] P4 left | What's the purpose of ensuring the dev set has a high number of err annotations?
- [ ] P4 right | What's the meaning of "perform significance tests using one-tailed sign test with bootstrap resampling on 100 samples."
- [ ] How to train the avg and ens?

## Note
1. P2 left | LM?
2. P6 right | Future work: large-scale cross-sentence GEC.
3. P8 left | Future work: evaluate more sophiscated models such as memory networks to capture entire document-level context
4. P8 left | Future work: incorporate external knowledge sources.
