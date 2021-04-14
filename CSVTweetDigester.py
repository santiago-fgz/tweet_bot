import csv
import pandas as pd
import numpy as np

class CSVTweetDigester:
    def __init__(self):
        self.tweets = []
    
    def push_csv(self,csv_title,min_replies=0,min_shares=0,min_likes=0,min_len_txt=5):
        pd_csv = pd.read_csv(csv_title)
        n = len(pd_csv)
        df_Tweets = pd.DataFrame(pd_csv)
        df_Tweets['reply count'] = df_Tweets['reply count'].replace(np.nan,0)
        df_Tweets['retweet count'] = df_Tweets['retweet count'].replace(np.nan,0)
        df_Tweets['like count'] = df_Tweets['like count'].replace(np.nan,0)
        df_Tweets['text'] = df_Tweets['text'].replace(np.nan,'caca')
        #print(df_Tweets)
        for i in range(n):
            replies = df_Tweets['reply count'][i] # número de resp
            if isinstance(replies,str):
                replies = self.to_number(replies)
            
            shares = df_Tweets['retweet count'][i] # número de rt
            if isinstance(shares,str):
                shares = self.to_number(shares)
            
            likes = df_Tweets['like count'][i]  # número de likes
            if isinstance(likes,str):
                likes = self.to_number(likes)

            if replies >= min_replies and shares >= min_shares and likes >= min_likes:
                txt = df_Tweets['text'][i]
                norm_txt = self.normalizeTxt(txt)
                words_txt = norm_txt.split()
                len_txt = len(words_txt)
                if len_txt >= min_len_txt:
                    self.tweets.append(norm_txt)
    
    def to_number(self,strN):
        mult = strN[-1]
        tms = 1
        #strN.replace("\r","")
        #strN.replace("\n","")
        if mult == 'K':
            strN = strN.replace('K',"")
            tms = 1000
        try:
            fst = float(strN)
        except ValueError:
            fst = -1
        N = fst*tms
        return N

    def normalizeTxt(self,comt):
        # eliminar símbolos raros
        if comt:
            comt = self.checkTags(comt,"http")
            comt = comt.replace("@ ","")
            comt = self.checkTags(comt,"@")
            comt = comt.replace("."," . ")
            comt = comt.replace(";"," . ")
            comt = comt.replace("\n"," . ")
            comt = comt.replace("\r"," . ")
            comt = comt.replace("’","'") # checar los apóstrofes
            comt = comt.replace("“",'')
            comt = comt.replace("”",'')
            comt = comt.replace(","," . ")
            comt = comt.replace(":"," : ")
            comt = comt.replace("-","")
            comt = comt.replace("_","")
            comt = comt.replace("~","")
            comt = comt.replace("*","")
            comt = comt.replace("•","")
            comt = comt.replace("+","")
            comt = comt.replace('"',"")
            #comt = comt.replace("'","")
            comt = comt.replace("!"," ! ")
            comt = comt.replace("?"," ? ")
            comt = comt.replace("¡","")
            comt = comt.replace("¿","")
            comt = comt.replace("("," . ")
            comt = comt.replace(")"," . ")
            comt = comt.replace("[","")
            comt = comt.replace("]","")
            comt = comt.replace("}","")
            comt = comt.replace("{","")
            comt = comt.replace("/","")
            comt = comt.replace("�","'")
            comt = comt.replace("©","")
            comt = comt.replace("ꨄ","")
            comt = comt.replace("➷","")
            comt = comt.replace("—","")
            comt = comt.lower()
            punct = ['.',':','?','!']
            comt = self.delete_double_punct(comt,punct) # HACER
        return comt

    def checkTags(self,comt,tag):
        tag = str(tag)
        ind_tag = comt.find(tag)
        res = 0
        while ind_tag >= 0:
            contin = True
            ind_curr = ind_tag + 1
            tag_complete = None
            while contin:
                ll = len(comt)
                if ind_curr == ll:
                    contin = False
                    tag_complete = comt[ind_tag:ll]
                else:
                    if comt[ind_curr] == " ":
                        contin = False
                        tag_complete = comt[ind_tag:ind_curr]
                if tag_complete:
                    comt = comt.replace(tag_complete,"")
                    tag_complete = None
                ind_curr += 1
            ind_tag = comt.find(tag)
        return comt

    def delete_double_punct(self,comt,punt): # INCOMPLETO
        return comt

    def write_txt(self,file_name):
        txt_file = open(file_name,"w",encoding='utf8')
        for twt in self.tweets:
            txt_file.write(twt + "\n")
