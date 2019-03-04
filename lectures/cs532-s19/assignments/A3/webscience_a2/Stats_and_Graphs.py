from collections import Counter
import json
import math
from scipy import stats
import matplotlib.pyplot as plt

def featurescaling(x, x_min, x_max):
    return ((x - x_min)/ (x_max - x_min))

def getFirstKey(item):
    return item[0]

def getSecondKey(item):
    return item[1]

def getThirdKey(item):
    return item[2]


def getTaub_or_Pearson(tfidf_PR_Alexa_list, desiredIndextoSortBy, IndextoCompareAgainst, getPearsonCorrelation = False):
    pairs = []
    sort_list = []
    compar_list = []

    if desiredIndextoSortBy == 0:
        pairs = sorted(tfidf_PR_Alexa_list, key=getFirstKey)
    elif desiredIndextoSortBy == 1:
        pairs = sorted(tfidf_PR_Alexa_list, key=getSecondKey)
    elif desiredIndextoSortBy == 2:
        pairs = sorted(tfidf_PR_Alexa_list, key=getThirdKey)

    tfIDF_List = []
    pr_list = []
    alexa_list = []

    for entry in pairs:
        tfIDF_List.append(entry[0])
        pr_list.append(entry[1])
        alexa_list.append(entry[2])

    if desiredIndextoSortBy == 0:
        sort_list = tfIDF_List
    elif desiredIndextoSortBy == 1:
        sort_list = pr_list
    elif desiredIndextoSortBy == 2:
        sort_list = alexa_list

    if IndextoCompareAgainst == 0:
        compar_list = tfIDF_List
    elif IndextoCompareAgainst == 1:
        compar_list = pr_list
    elif IndextoCompareAgainst == 2:
        compar_list = alexa_list

    if getPearsonCorrelation == False:
        result = stats.kendalltau(sort_list, compar_list)
    else:
        result = stats.pearsonr(sort_list,compar_list)
    return result



wordcount = ""
goodURL = json.load(open("urlsClean.json"))
docs_in_corpus = 0
docs_where_term_appears = 0

for url in goodURL:
    docs_in_corpus += 1

for url in goodURL:
    try:
        x = goodURL[url]["keywords"]["Mueller"]
        docs_where_term_appears += 1
    except Exception as e:
        pass

for url in goodURL:
    try:
        x = goodURL[url]["keywords"]
        with open("./texthtml/" + goodURL[url]["html_text_filename"]) as file:
            finalCheck = file.read()
            wordcount = Counter(finalCheck.split())

            count = 0
            for key in wordcount:
                count += wordcount[key]

            #TF_IDF calculation https://en.wikipedia.org/wiki/Tf%E2%80%93idf
            tf = finalCheck.count("Mueller") / count #tf = term frequency
            goodURL[url]["keywords"]["Mueller"]["TF"] = tf
            idf = math.log(docs_in_corpus/(1 + docs_where_term_appears), 2) # 1+ on inverse doc frequency to prevent x/0 errors
            goodURL[url]["keywords"]["Mueller"]["IDF"] = idf
            goodURL[url]["keywords"]["Mueller"]["TF-IDF"] = tf * idf
            #normalize our manually input alexa and PR values if they exist
            #https://en.wikipedia.org/wiki/Normalization_(statistics) note, we are using the formula for Feature scaling
            try:
                goodURL[url]["keywords"]["Mueller"]["PR_normalized"] = featurescaling(goodURL[url]["keywords"]["Mueller"]["PR"],0,10) #normalizing data
                x = 1 / featurescaling(goodURL[url]["keywords"]["Mueller"]["Alexa-global"],1,10000000) #alex scores are in reverse we are adjusting for this.
                goodURL[url]["keywords"]["Mueller"]["Alexa-global_normalized"] = featurescaling(x, 1, 3000000) #numbers are abitrary to force our Alexa ranks to < 1
            except Exception as e:
                pass
    except KeyError as e:
        pass


#tau calculations
#generate a 2d list containing the normalized TFIDF, PR, and Alexa ranks for selected URLs
pairs = []
for url in goodURL:
    try:
        pairs.append([goodURL[url]["keywords"]["Mueller"]["TF-IDF"],goodURL[url]["keywords"]["Mueller"]["PR_normalized"], goodURL[url]["keywords"]["Mueller"]["Alexa-global_normalized"]])
    except Exception as e:
        pass

#calculate our tau-b and p scores
tfidf_PR_taub_and_pvalue = getTaub_or_Pearson(pairs, 0, 1)
tfidf_Alexa_taub_and_pvalue = getTaub_or_Pearson(pairs, 0, 2)
PR_Alexa_taub_and_pvalue = getTaub_or_Pearson(pairs, 1, 2)

print(tfidf_PR_taub_and_pvalue)
print(tfidf_Alexa_taub_and_pvalue)
print(PR_Alexa_taub_and_pvalue)

tfidf_PR_pearson_and_pvalue = getTaub_or_Pearson(pairs, 0, 1, True)
tfidf_Alexa_pearson_and_pvalue = getTaub_or_Pearson(pairs, 0, 2, True)
PR_Alexa_pearson_and_pvalue = getTaub_or_Pearson(pairs, 1, 2, True)

print(tfidf_PR_pearson_and_pvalue)
print(tfidf_Alexa_pearson_and_pvalue)
print(PR_Alexa_pearson_and_pvalue)


#produce our graphs

#kendall-taub
bars = plt.bar([0,1,2] ,[tfidf_PR_taub_and_pvalue[0],tfidf_Alexa_taub_and_pvalue[0],PR_Alexa_taub_and_pvalue[0]], width=0.8)


# https://stackoverflow.com/questions/40489821/how-to-write-text-above-the-bars-on-a-bar-plot-python
for rect in bars:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width()/2.0, height + 0.05, '%f' % height, ha='center', va="bottom")


labels = ['TF-IDF/PR','TF-IDF/Alexa','PR/Alexa']
plt.xticks([0, 1, 2], labels=labels)
plt.xlabel("Pairs")
plt.ylabel("Kendall Tau-b")
plt.ylim(-0.2,1)
plt.title("Correlation between ranking algorithms using Kendall tau-b")
plt.tight_layout()

plt.show()

#plot p values for kendall-tau
bars = plt.bar([0,1,2] ,[tfidf_PR_taub_and_pvalue[1],tfidf_Alexa_taub_and_pvalue[1],PR_Alexa_taub_and_pvalue[1]], width=0.8)
for rect in bars:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width()/2.0, height + 0.02, '%f' % height, ha='center', va="bottom")

labels = ['TF-IDF/PR','TF-IDF/Alexa','PR/Alexa']
plt.xticks([0, 1, 2], labels=labels)
plt.xlabel("Pairs")
plt.ylabel("p-value")
plt.ylim(0,1)
plt.title("P values for Kendall-tau pairs")
plt.tight_layout()
plt.show()

#pearson-correlation
bars = plt.bar([0,1,2] ,[tfidf_PR_pearson_and_pvalue[0],tfidf_Alexa_pearson_and_pvalue[0],PR_Alexa_pearson_and_pvalue[0]], width=0.8)


# https://stackoverflow.com/questions/40489821/how-to-write-text-above-the-bars-on-a-bar-plot-python
for rect in bars:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width()/2.0, height + 0.05, '%f' % height, ha='center', va="bottom")


labels = ['TF-IDF/PR','TF-IDF/Alexa','PR/Alexa']
plt.xticks([0, 1, 2], labels=labels)
plt.xlabel("Pairs")
plt.ylabel("Pearson Correlation")
plt.ylim(0,0.5)
plt.title("Correlation between ranking algorithms using Pearson Correlation")
plt.tight_layout()

plt.show()

#plot p values for Pearson Correlation
bars = plt.bar([0,1,2] ,[tfidf_PR_pearson_and_pvalue[1],tfidf_Alexa_pearson_and_pvalue[1],PR_Alexa_pearson_and_pvalue[1]], width=0.8)
for rect in bars:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width()/2.0, height + 0.02, '%f' % height, ha='center', va="bottom")

labels = ['TF-IDF/PR','TF-IDF/Alexa','PR/Alexa']
plt.xticks([0, 1, 2], labels=labels)
plt.xlabel("Pairs")
plt.ylabel("p-value")
plt.ylim(0,1)
plt.title("P values for Pearson pairs")
plt.tight_layout()
plt.show()




with open('urlsClean.json', 'w')as outFile:
    pretty_data = json.dumps(goodURL, indent=4)
    outFile.write(pretty_data)

