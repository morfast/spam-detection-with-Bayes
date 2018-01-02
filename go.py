#!/usr/bin/python

import sys
import collections

all_word_count = {}
normal_word_count = {}
spam_word_count = {}
n_spam = 0
n_normal = 0
n_total = 0

def add_to_dict(d, word):
    if word in d.keys():
        d[word] += 1
    else:
        d[word] = 1

def count_words():
    global all_word_count 
    global normal_word_count 
    global spam_word_count 
    global n_spam
    global n_normal
    global n_total
    for line in open(sys.argv[1]):
        spline = line.strip().split()
        if spline[0] == "ham":
            is_spam = False
        else:
            is_spam = True
    
        for word in set(spline[1:]):
            add_to_dict(all_word_count, word)
            n_total += 1
            if is_spam:
                add_to_dict(spam_word_count, word)
                n_spam += 1
            else:
                add_to_dict(normal_word_count, word)
                n_normal += 1
    
def predict(mail):
    global all_word_count 
    global normal_word_count 
    global spam_word_count 
    global n_spam
    global n_normal
    global n_total
    global spam_keywords

    all_words = {}
    for word in mail:
        add_to_dict(all_words, word)
    emerge_words = all_words.keys()

    pro = (float(n_spam)/n_total)
    for spam_word in spam_keywords:
        if spam_word in emerge_words:
            pro *= spam_word_count[spam_word]/float(n_spam) 
        else:
            pass
            #pro *= 1.0/n_spam 

    denominator = 1.0
    for spam_word in spam_keywords:
        if spam_word in emerge_words:
            denominator *= (all_word_count[spam_word]/float(n_total))
        else:
            pass
            #denominator *= 1.0/n_total

    return pro / (pro + denominator)



# prediction
def prediction_test():
    for line in open(sys.argv[2]):
        spline = line.strip().split()
        if spline[0] == "ham":
            is_spam = False
        else:
            is_spam = True
        print "%s %4.2f" % (is_spam, predict(spline[1:]))
    
def train():
    global all_word_count 
    global normal_word_count 
    global spam_word_count 
    global n_spam
    global n_normal
    global n_total
    global spam_keywords
    count_words()
    i = 0
    spam_keywords = []
    for key, value in sorted(spam_word_count.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        #print "%s: %s" % (key, value)
        spam_keywords.append(key)
        i += 1
        if i > 50: break

train()
prediction_test()

