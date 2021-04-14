import random

class MarkovTweet:
    def __init__(self,order):
        self.order = order
        self.tweet_grams = []
        self.next_pword = []
        self.pstarts = []
    
    def learn_text(self,file_name):
        tweets = open(file_name,'r',encoding = 'utf8')
        for tweet in tweets:
            words = tweet.split()
            n = len(words) - self.order + 1
            for wd in range(n):
                gram = []
                for j in range(self.order):
                    gram.append(words[wd+j]) 
                if wd == 0:
                    self.pstarts.append(gram)
                indice = self.contained(gram)
                if indice == -1:
                    indice = len(self.tweet_grams)
                    self.tweet_grams.append(gram)
                    pword = []
                    self.next_pword.append(pword)
                if wd < n - 1:
                    self.next_pword[indice].append(words[wd+self.order])
    
    def contained(self,subArr):
        res = -1
        arr = self.tweet_grams
        od = self.order
        n = len(arr)
        if n>0:
            isCont = False
            contArr = 0
            while isCont == False and contArr < n:
                arri = arr[contArr]
                isSame = True
                contSubarr = 0
                while isSame == True and contSubarr < od:
                    if arri[contSubarr] != subArr[contSubarr]:
                        isSame = False
                    contSubarr = contSubarr + 1
                if isSame == 1:
                    isCont = True
                    res = contArr
                contArr = contArr + 1
        return res
    
    def tweet(self,num_max_words):
        sz = len(self.next_pword)
        new_tweet = random.choice(self.pstarts)
        for i in range(num_max_words - self.order):
            curr_gram = new_tweet[-self.order:]
            index = self.contained(curr_gram)
            if index >= 0 and index < sz and len(self.next_pword[index]) > 0:
                next_word = random.choice(self.next_pword[index])
                new_tweet.append(next_word)
            else:
                break
        n = len(new_tweet)
        my_tweet = ''
        for j in range(n):
            my_tweet = my_tweet + new_tweet[j] + ' '
        return my_tweet

