# This script extracts sentence pairs from Lang-8, NUCLE and CoNLL-2014 data with XML format
# Python version: 2
# NLTK version: 2.0b7
# Usage example for Lang-8: python2 sentence_pairs_with_ctx.py --train --tokenize --maxtokens 80 --mintokens 1 --input lang8-train.xml  --src-ctx lang8.src-trg.ctx --src-src lang8.src-trg.src --trg-trg lang8.src-trg.trg
# Usage example for NUCLE: python2 sentence_pairs_with_ctx.py --train(--dev) --maxtokens 80 --mintokens 1 --input nucle-train(-dev).xml --src-ctx nucle(-dev).src-trg.ctx --src-src nucle(-dev).src-trg.src --trg-trg nucle(-dev).src-trg.trg
# Usage example for CoNLL-2014: python2 sentence_pairs_with_ctx.py --test --input conll14st-test.xml --src-ctx conll14st-test.tok.ctx --src-src conll14st-test.tok.src --trg-trg conll14st-test.tok.trg

import argparse
import xml.etree.cElementTree as ET
import nltk
parser = argparse.ArgumentParser()
parser.add_argument('--train', action='store_true', help='choose if we generate train data')
parser.add_argument('--dev', action='store_true', help='choose if we generate development data')
parser.add_argument('--test', action='store_true', help='choose if we generate test data')
parser.add_argument('--tokenize', action='store_true', help='choose if the dataset need to be tokenized.')
parser.add_argument('--maxtokens', type=int, help='set the maximum number of tokens in one sentence')
parser.add_argument('--mintokens', type=int, help='set the minimum number of tokens in one sentence')
parser.add_argument('--input', help='XML file need to be parsed')
parser.add_argument('--src-ctx', help='store context source sentences')
parser.add_argument('--src-src', help='store current source sentences')
parser.add_argument('--trg-trg', help='store current target sentences')
args = parser.parse_args()

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

def extract_from_xml(tokenize, input, src_ctx, src_src, trg_trg):
    count=0  # Counts the number of sentence pairs.
    essay_n = 0  # Counts the number of essays.
    source_n = 0  # Countes the number of src sentences.
    token_n = 0  # Counts the number of tokens.
    
    token_src_ctx = 0  # Counts the number of tokens in .ctx.
    token_src_src = 0  # Counts the number of tokens in .src.
    token_trg_trg = 0  # Counts the number of tokens in .trg.
    
    with open(src_ctx,'w') as ctx_file:
        with open(src_src,'w') as src_file:
            with open(trg_trg,'w') as tag_file:
                
                ###### Parsing.
                
                # Parses the xml tree.
                tree = ET.parse(input)
                # Gets the root.
                root = tree.getroot()
                
                for essay in root:
                    print
                    print "ESSAY", essay_n
                    
                    essay_n += 1
                    
                    ###### Init.
                    
                    # Inits ctxs.
                    ctx_1 = ''
                    ctx_2 = ''
                    # Inits src ctx, which is the previous two sentences of the cur src sentence. 
                    source_ctx = '\n'
                    # Inits current_ctx_token#.
                    cur_ctx_token = 0
                    
                    sentence_count = 0
                    for sentence in essay:
                        print
                        print "  SENTENCE", sentence_count
                        sentence_count += 1
                        
                        ###### Src.
                                                
                        # Finds a src sentence.
                        source = sentence.find('source')
                        
                        print "    SRC:", source.text
                        
                        # Inits an array for storing tokens of the src sentence.
                        cache_src = []
                                                
                        # If the src sentence is not judged to be written in English, continue.
                        if source.get('langid')!='en':
                            print "      (LANG_ERR)", "not judged to be en"
                            
                            continue
                        else:
                            if tokenize:
                                # Tokenizes the src sentence.
                                tokens_src = nltk.word_tokenize(source.text.strip())
                                                                
                                # Puts each token in the src token array.
                                for each in tokens_src:
                                    cache_src.append(each)
                                
                                # Gets the src sentence to be appended to .src.
                                source_src = " ".join(cache_src) + '\n'
                                
                                print "      (TOKENIZED)", source_src
                            else:
                                source_src = source.text.strip() + '\n'
                                cache_src = source.text.strip().split(' ')
                                
                                print "      (NOT TOKENIZED)", source_src
                        
                        # If token# > maxtoken#, continue.
                        if args.maxtokens and len(cache_src) > args.maxtokens:
                            print "      (MAX_TOKEN_ERR)", "token# (", len(cache_src), ") > (", args.maxtokens, ")"
                            
                            continue
                        # If token# < mintoken#, continue.
                        if args.mintokens and len(cache_src) < args.mintokens:
                            print "      (MIN_TOKEN_ERR)", "token# (", len(cache_src), ") < (", args.mintokens, ")"
                            
                            continue
                        
                        # Reaching here means the source sentence is 
                        # (1) an en sentence
                        # (2) mintoken# < token# < maxtoken#
                        source_n += 1
                        token_n += len(cache_src)
                        
                        ###### Trg.
                        
                        trg_count = 0
                        for target in sentence.findall('target'):
                            print "    TRG" + str(trg_count) + ":", target.text
                            
                            if target.get('langid')=='en':
                                # If the trg sentence is empty.
                                if not target.text:
                                    # In train mode, src-trg pair cannot be formed thus continue.
                                    if args.train:
                                        print "      (EMPTY_TRG_ERR)", "trg" + str(trg_count), "is empty"
                                        
                                        continue
                                    # In valid or test mode, treats the src as trg.
                                    else:
                                        target.text = source_src
                                
                                # Inits an array for storing tokens of the trg sentence.
                                cache_trg = []
                                
                                if tokenize:
                                    # Tokenizes the trg sentence.
                                    tokens_trg = nltk.word_tokenize(target.text.strip())
                                    
                                    # Puts each token in the trg token array.
                                    for each in tokens_trg:
                                        cache_trg.append(each)
                                    
                                    # Gets the trg sentence to be appended to .trg.
                                    target_trg = " ".join(cache_trg) + '\n'
                                    
                                    print "      (TOKENIZED)", target_trg
                                else:
                                    target_trg = target.text.strip() + '\n'
                                    cache_trg = target.text.strip().split(' ')
                                    
                                    print "      (NOT TOKENIZED)", target_trg
                                
                                # If token# > maxtoken#, continue.
                                if args.maxtokens and len(cache_trg) > args.maxtokens:
                                    print "      (MAX_TOKEN_ERR)", "token# (", len(cache_trg), ") > (", args.maxtokens, ")"
                                    
                                    continue
                                # If token# < mintoken#, continue
                                if args.mintokens and len(cache_trg) < args.mintokens:
                                    print "      (MIN_TOKEN_ERR)", "token# (", len(cache_trg), ") > (", args.mintokens, ")"
                                    
                                    continue
                                
                                # If not in test mode and src == trg, continue.
                                if source_src == target_trg and not args.test:
                                    print "      (SRC_TRG_IDENTICAL_ERR)", "src == trg"
                                    
                                    continue
                                    
                                ctx_file.write(source_ctx.encode('utf-8'))
                                token_src_ctx += cur_ctx_token
                                
                                print "    (CTX)", source_ctx
                                
                                src_file.write(source_src.encode('utf-8'))
                                token_src_src += len(cache_src)
                                
                                print "    (SRC)", source_src
                                
                                tag_file.write(target_trg.encode('utf-8'))
                                token_trg_trg += len(cache_trg)
                                
                                print "    (TRG)", target_trg
                                
                                # Reaching here means a src-trg pair is formed.
                                count+=1
                                
                            # If the trg sentence is not judged to be written in English, continue.
                            else:
                                print "      (LANG_ERR)", "not judged to be en"
                            
                                continue
                        
                        if not sentence.findall('target'):
                            print "    NO TRG"
                        
                        # Will be exe even if no trg provided.
                        ctx_1 = ctx_2
                        ctx_2 = source_src.strip()
                        # Concats the ctx with a space btw them.
                        source_ctx = (ctx_1 + ' ' + ctx_2).strip() + '\n'
                        cur_ctx_token = len(source_ctx.strip().split(' '))
    
    print '\n'
    
    print args.input, ':', essay_n, 'essays,', source_n, 'source sentences,', token_n, 'tokens.'  # essay#, src_sentence#, token#.
    print 'The number of source sentences / essays :', source_n / essay_n  # Avg src_sentence# of each essay.
    print 'The number of tokens / essays :', token_n / essay_n  # Avg token# of each essay.
    if tokenize:
        print count,'sentence pairs have been added with tokenization.'  # sentence_pair#.
    else:
        print count,'sentence pairs have been added without tokenization.'
    print src_ctx, token_src_ctx, 'tokens'  # ctx_token#.
    print src_src, token_src_src, 'tokens'  # src_token#.
    print trg_trg, token_trg_trg, 'tokens'  # trg_token#.


extract_from_xml(args.tokenize, args.input, args.src_ctx, args.src_src, args.trg_trg)




