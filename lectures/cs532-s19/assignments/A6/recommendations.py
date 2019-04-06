import collections
from math import sqrt

def loadMovieLens(path='./data'):
  # Get movie titles
    movies = {}
    for line in open(path + '/u.item'):
        (id, title) = line.split('|')[0:2]
        movies[id] = title
  # Load data
    prefs = {}
    for line in open(path + '/u.data'):
        (user, movieid, rating, ts) = line.split('\t')
        prefs.setdefault(user, {})
        prefs[user][movies[movieid]] = float(rating)
    #a modification of the sourcecode so we get a sorted dictionary for easy lookup
    prefs = collections.OrderedDict(sorted(prefs.items(), key=lambda x: int(x[0])))
    return prefs


def sim_distance(prefs, p1, p2):
    '''
    Returns a distance-based similarity score for person1 and person2.
    '''

    # Get the list of shared_items
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1
    # If they have no ratings in common, return 0
    if len(si) == 0:
        return 0
    # Add up the squares of all the differences
    sum_of_squares = sum([pow(prefs[p1][item] - prefs[p2][item], 2) for item in
                         prefs[p1] if item in prefs[p2]])
    return 1 / (1 + sqrt(sum_of_squares))

def sim_pearson(prefs, p1, p2):
    '''
    Returns the Pearson correlation coefficient for p1 and p2.
    '''

    # Get the list of mutually rated items
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1
    # If they are no ratings in common, return 0
    if len(si) == 0:
        return 0
    # Sum calculations
    n = len(si)
    # Sums of all the preferences
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])
    # Sums of the squares
    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])
    # Sum of the products
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])
    # Calculate r (Pearson score)
    num = pSum - sum1 * sum2 / n
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0:
        return 0
    r = num / den
    return r

def getRecommendations(prefs, person, similarity=sim_pearson):
    '''
    Gets recommendations for a person by using a weighted average
    of every other user's rankings
    '''

    totals = {}
    simSums = {}
    for other in prefs:
    # Don't compare me to myself
        if other == person:
            continue
        sim = similarity(prefs, person, other)
        # Ignore scores of zero or lower
        if sim <= 0:
            continue
        for item in prefs[other]:
            # Only score movies I haven't seen yet
            if item not in prefs[person] or prefs[person][item] == 0:
                # Similarity * Score
                totals.setdefault(item, 0)
                # The final score is calculated by multiplying each item by the
                #   similarity and adding these products together
                totals[item] += prefs[other][item] * sim
                # Sum of similarities
                simSums.setdefault(item, 0)
                simSums[item] += sim
    # Create the normalized list
    rankings = [(total / simSums[item], item) for (item, total) in
                totals.items()]
    # Return the sorted list
    rankings.sort()
    rankings.reverse()
    return rankings


def bot_and_top_matches(
    prefs,
    person,
    n=5,
    similarity=sim_pearson,
):
    '''
    Returns the best matches for person from the prefs dictionary.
    Number of results and similarity function are optional params.
    '''

    scores = [(similarity(prefs, person, other), other) for other in prefs
              if other != person]
    scores.sort()
    bottom_match = scores[0:n]
    scores.reverse()
    return scores[0:n], bottom_match


def transformPrefs(prefs):
    '''
    Transform the recommendations into a mapping where persons are described
    with interest scores for a given title e.g. {title: person} instead of
    {person: title}.
    '''

    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})
            # Flip item and person
            result[item][person] = prefs[person][item]
    return result

def calculateSimilarItems(prefs, n=10):
    '''
    Create a dictionary of items showing which other items they are
    most similar to.
    '''

    result = {}
    bad_result = {}
    # Invert the preference matrix to be item-centric
    itemPrefs = transformPrefs(prefs)
    c = 0
    for item in itemPrefs:
        # Status updates for large datasets
        c += 1
        if c % 100 == 0:
            print ('%d / %d' % (c, len(itemPrefs)))
        # Find the most similar items to this one
        (scores, bad_score) = bot_and_top_matches(itemPrefs, item, n=n, similarity=sim_distance)
        result[item] = scores
        bad_result[item] = bad_score
    return result, bad_result


pref = loadMovieLens()

#code for determining the users most similar to me
'''
buddies = []
with open("./data/u.user",'r') as findMe:
    for person in findMe:
        (userid, age, gender, occupation, zip) = person.split("|")
        if (int(age) < 34 and int(age) > 30 and gender == 'M'):
            buddies.append(person)

for i in buddies:
    pass
    #print(i)



#119|32|M|programmer|67401
#134|31|M|programmer|80236
#219|32|M|programmer|43212
#279|33|M|programmer|85251
#350|32|M|student|97301
#560|32|M|student|10003
#658|33|M|programmer|92626
#743|31|M|programmer|92660
#765|31|M|student|33066
#779|31|M|student|K7L5J
#890|32|M|student|97301


buddy_id = ['119','134','219','279','350','560','658','743','765','779','890']
for buddy in buddy_id:
    doppleganger = pref[buddy]
    doppleganger = collections.OrderedDict(sorted(doppleganger.items(), key=lambda x: int(x[1])))
    movieList = []
    for i in doppleganger:
        movieList.append(i)

    finalList = []
    finalList.append("***Worst:***")
    for i in range(0,5):
        finalList.append(movieList[i])
    finalList.append("***Best:***")
    for i in range(len(movieList) - 5, len(movieList)):
        finalList.append(movieList[i])
    with open("./candidates.txt",'a') as outFile:
        outFile.write(buddy + '\n')
        for i in finalList:
            outFile.write(i + '\n')
        outFile.write("_______________________\n")

'''
#779 is most similar to me



#Find the users most correlated and least correlated with 779
correlations = []
top_5 = []
bot_5 = []
for i in pref:
    if i != '779':
        c = sim_pearson(pref,i,'779')
        correlations.append([i,c])

correlations = sorted(correlations.__iter__(), key=lambda x: float(x[1]))
for i in range(0,5):
    bot_5.append(correlations[i])
for i in range(len(correlations) -5, len(correlations)):
    top_5.append(correlations[i])

top_5 = sorted(top_5.__iter__(), reverse=True, key=lambda x: float(x[1]))
bot_5 = sorted(bot_5.__iter__(), key=lambda x: float(x[1]))

with open("TopBot5.txt",'w') as outFile:
    outFile.write("Top 5\n")
    for i in top_5:
        outFile.write("%s\t%f\n" % (i[0], i[1]))
    outFile.write("Bot 5\n")
    for i in bot_5:
        outFile.write("%s\t%f\n" % (i[0], i[1]))







#calculate the rankings of films our proxy hasn't seen
recommend = getRecommendations(pref, '779')

recommend = sorted(recommend.__iter__(), key=lambda x: float(x[0]))
top_5 = []
bot_5 = []
for i in range(0,5):
    bot_5.append(recommend[i][1])
for i in range(len(recommend) -5, len(recommend)):
    top_5.append(recommend[i][1])

with open("recommend.txt",'w') as outFile:
    outFile.write("\n5 to watch\n")
    for i in top_5:
        outFile.write("%s\n" % i)
    outFile.write("\n5 to avoid\n")
    for i in bot_5:
        outFile.write("%s\n" % i)

#movie correlation
#my top 5
# 87|Searching for Bobby Fischer (1993)|01-Jan-1993||http://us.imdb.com/M/title-exact?Searching%20for%20Bobby%20Fischer%20(1993)|0|0|0|0|0|0|0|0|1|0|0|0|0|0|0|0|0|0|0
# 180|Apocalypse Now (1979)|01-Jan-1979||http://us.imdb.com/M/title-exact?Apocalypse%20Now%20(1979)|0|0|0|0|0|0|0|0|1|0|0|0|0|0|0|0|0|1|0
#272|Good Will Hunting (1997)|01-Jan-1997||http://us.imdb.com/M/title-exact?imdb-title-119217|0|0|0|0|0|0|0|0|1|0|0|0|0|0|0|0|0|0|0
#282|Time to Kill, A (1996)|13-Jul-1996||http://us.imdb.com/M/title-exact?Time%20to%20Kill,%20A%20(1996)|0|0|0|0|0|0|0|0|1|0|0|0|0|0|0|0|0|0|0
#318|Schindler's List (1993)|01-Jan-1993||http://us.imdb.com/M/title-exact?Schindler's%20List%20(1993)|0|0|0|0|0|0|0|0|1|0|0|0|0|0|0|0|0|1|0


#my bottom 5
#235|Mars Attacks! (1996)|13-Dec-1996||http://us.imdb.com/M/title-exact?Mars%20Attacks!%20(1996)|0|1|0|0|0|1|0|0|0|0|0|0|0|0|0|1|0|1|0
#271|Starship Troopers (1997)|01-Jan-1997||http://us.imdb.com/M/title-exact?Starship+Troopers+(1997)|0|1|1|0|0|0|0|0|0|0|0|0|0|0|0|1|0|1|0
#294|Liar Liar (1997)|21-Mar-1997||http://us.imdb.com/Title?Liar+Liar+(1997)|0|0|0|0|0|1|0|0|0|0|0|0|0|0|0|0|0|0|0
#367|Clueless (1995)|01-Jan-1995||http://us.imdb.com/M/title-exact?Clueless%20(1995)|0|0|0|0|0|1|0|0|0|0|0|0|0|0|0|0|0|0|0
#441 Amityville Horror, The (1979)|01-Jan-1979||http://us.imdb.com/M/title-exact?Amityville%20Horror,%20The%20(1979)|0|0|0|0|0|0|0|0|0|0|0|1|0|0|0|0|0|0|0

my_favs = ['Searching for Bobby Fischer (1993)','Apocalypse Now (1979)','Good Will Hunting (1997)','Time to Kill, A (1996)','Schindler\'s List (1993)']
my_hates = ['Mars Attacks! (1996)', 'Starship Troopers (1997)', 'Liar Liar (1997)', 'Clueless (1995)','Amityville Horror, The (1979)']
(pos_correlation,negative_correlation) = calculateSimilarItems(pref,5)

for i in my_favs:
    positive_correlations = pos_correlation.get(i)
    bad_correlation = negative_correlation.get(i)
    print(bad_correlation)
    with open('movies_I_might_want_to_watch.txt','a') as outFile:
        outFile.write("Movies Similar to %s:\n" % i)
        for j in positive_correlations:
            outFile.write(str(j[1]) + "\n")
        outFile.write("\nMovies not similar to %s:\n" % i)
        for k in bad_correlation:
            outFile.write(str(k[1]) + "\n")
        outFile.write("\n_____________________________________\n")

for i in my_hates:
    positive_correlations = pos_correlation.get(i)
    bad_correlation = negative_correlation.get(i)
    print(bad_correlation)
    with open('movies_I_might_dont_want_to_watch.txt','a') as outFile:
        outFile.write("Movies Similar to %s:\n" % i)
        for j in positive_correlations:
            outFile.write(str(j[1]) + "\n")
        outFile.write("\nMovies not similar to %s:\n" % i)
        for k in bad_correlation:
            outFile.write(str(k[1]) + "\n")
        outFile.write("\n_____________________________________\n")



#todo GET the most and least correlated for each film above.
