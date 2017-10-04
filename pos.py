from nltk import word_tokenize, pos_tag, FreqDist, tag

sentence = "At eight o'clock on Thursday morning Arthur didn't feel very good."

####Sentence Tokenizer####
tokens = word_tokenize(sentence)
print (tokens)

####pos tagging####
tagged = pos_tag(tokens)
print (tagged)

#dalam format word/tag
print ([tag.tuple2str(t) for t in tagged])

#frekuensi pos pada text
tag_fd = FreqDist(tag for (word, tag) in tagged)
print (tag_fd.most_common())

#plot frequency distribution
#tag_fd.plot(cumulative=False) 

