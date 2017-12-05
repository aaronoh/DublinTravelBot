from nltk.corpus import twitter_samples
from nltk.tag import pos_tag_sents


tweets = twitter_samples.strings('positive_tweets.json')

tweets_tokens = twitter_samples.tokenized('positive_tweets.json')

#Will tag the tokenized tweets - tuple
tweets_tagged = pos_tag_sents(tweets_tokens)

# JJ = ADJ, NN = Singular Noun, NS = Plural Noun
JJ_count = 0
NN_count = 0


#loop through every tweet
for tweet in tweets_tagged:
    #loop through each token pair within each tweet
    for pair in tweet:
        #Count the number of ADJ, Singular and plura nouns
        tag = pair[1]
        if tag == 'JJ':
            JJ_count += 1
        elif tag == 'NN':
            NN_count += 1

print('Tweet ', tweets[0])
print('Tokenized Tweet ', tweets_tokens[0])
print('Tagged Tweet ',tweets_tagged[0])
print('Total number of adjectives = ', JJ_count)
print('Total number of singular nouns = ', NN_count)