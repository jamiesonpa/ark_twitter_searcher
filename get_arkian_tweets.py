import streamlit as st
import tweepy
import datetime
from datetime import datetime
from datetime import timedelta

api_key = st.secrets["api_key"]
api_secret = st.secrets["api_secret"]
bearer_token = st.secrets["bearer_token"]
access_token = st.secrets["access_token"]
access_secret = st.secrets["access_secret"]


auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)


def search_twitter(arkian,searchcriteria,api,rts, start, end):
    arkian = arkian.replace("@","")

    tweets = tweepy.Cursor(api.user_timeline, screen_name=arkian, tweet_mode="extended", include_rts=rts).items()
    # tweets = api.user_timeline(screen_name=arkian, 
    #                         # 200 is the maximum allowed count
    #                         count=200,
    #                         include_rts = rts,
    #                         # Necessary to keep full_text 
    #                         # otherwise only the first 140 words are extracted
    #                         tweet_mode = 'extended'
    #                         )
    tweets_to_print = []
    total_tweets = []
    for info in tweets:
        total_tweets.append(info)
        if info.full_text.find(searchcriteria) != -1:
            created_date = str(info.created_at).split(" ")[0]
            tweet_date = datetime.strptime(created_date,"%Y-%m-%d")
            if start.date() <= tweet_date <= end.date():
                tweets_to_print.append(info)
            else:
                pass

            # print("ID: {}".format(info.id))
            # print(info.created_at)
            # print(info.full_text)
            # print("\n")
    if len(tweets_to_print) == 0:
        st.write("Retrieved " + str(len(total_tweets)) + " total tweets, and searched them for keyword '" + searchcriteria + "'.")
        st.write("No tweets with '" + str(searchcriteria) + "' were found in the last 200 tweets of @" + arkian)
    else:
        st.write("Retrieved " + str(len(total_tweets)) + " total tweets, and searched them for keyword '" + searchcriteria + "'.")
        for tweet in tweets_to_print:
            st.write("["+str(tweet.created_at) + "] @" + arkian + ": " + str(tweet.full_text))


st.title("ARK Twitter Searcher v0.1")
arkian = st.sidebar.text_input("twitter handle of ARK employee")
searchcriteria = st.sidebar.text_input("text to search")
retweets = st.sidebar.checkbox("Include retweets?")

one_year_ago = datetime.now() - timedelta(days=365)
start_date = st.sidebar.date_input("From", value = one_year_ago)
end_date = st.sidebar.date_input("To")
search = st.sidebar.button("Search")


if search:
    st.write("Searching "+str(arkian)+"...")
    search_twitter(arkian, searchcriteria, api, retweets, start_date, end_date)

