import streamlit as st
import tweepy

api_key = st.secrets["api_key"]
api_secret = st.secrets["api_secret"]
bearer_token = st.secrets["bearer_token"]
access_token = st.secrets["access_token"]
access_secret = st.secrets["access_secret"]


auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)


def search_twitter(arkian,searchcriteria,api,rts):
    arkian = arkian.replace("@","")

    tweets = api.user_timeline(screen_name=arkian, 
                            # 200 is the maximum allowed count
                            count=200,
                            include_rts = rts,
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
        st.write("No tweets with '" + str(searchcriteria) + "' were found in the last 200 tweets of @" + arkian)
    else:
        for tweet in tweets_to_print:
            st.write("["+str(tweet.created_at) + "] @" + arkian + ": " + str(tweet.full_text))


st.title("ARK Twitter Searcher v0.1")
arkian = st.sidebar.text_input("twitter handle of ARK employee")
searchcriteria = st.sidebar.text_input("text to search")
retweets = st.sidebar.checkbox("Include retweets?")
search = st.sidebar.button("Search")

if search:
    st.write(str(arkian))
    search_twitter(arkian, searchcriteria, api, retweets)

