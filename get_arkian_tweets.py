import streamlit as st
import tweepy

api_key = "dHeErSR4abzN0dkE0A5t5RAZc"
api_secret = "ojdTqtit8lu7fr6aJRJk3esDjqPztlay0UFJOF3Giuy8euG2Wa"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAD6fVAEAAAAAwECVso6ShKF9u2%2Bi33ZGSH3NvCA%3DtqnCV1LuxS1K68NO21RKoXrPMR5KGwPI7gaisNxiGx6uzObjdS"
access_token = "1425496134299095042-Y890IXI5Ydhisb1POWHNaS5jLf5leH"
access_secret = "aVIteFYdwhTkqESbJmW6JV5pDclSgAvQg32OBzuFD43z3"

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def search_twitter(arkian,searchcriteria,api,rts):
    arkian = arkian.replace("@","")
    user = api.get_user(arkian)
    tweets = api.user_timeline(screen_name=user, 
                            # 200 is the maximum allowed count
                            count=200,
                            include_rts = retweets,
                            # Necessary to keep full_text 
                            # otherwise only the first 140 words are extracted
                            tweet_mode = 'extended'
                            )
    tweets_to_print = []
    for info in tweets:
        if info.full_text.find(searchcriteria) != -1:
            tweets_to_print.append(info)
            # print("ID: {}".format(info.id))
            # print(info.created_at)
            # print(info.full_text)
            # print("\n")
    if len(tweets_to_print) == 0:
        st.print("No tweets with '" + str(searchcriteria) + "' were found in the last 200 tweets of @" + arkian)
    else:
        for tweet in tweets_to_print:
            st.write("["+str(tweet.created_at) + "] @" + arkian + ": " + str(tweet.full_text))


st.title("ARK Twitter Searcher v0.1")
arkian = st.sidebar.text_input("twitter handle of ARK employee")
searchcriteria = st.sidebar.text_input("text to search")
retweets = st.sidebar.checkbox("Include retweets?")
search = st.sidebar.button("Search")

if search:
    search_twitter(arkian, searchcriteria, api, retweets)

