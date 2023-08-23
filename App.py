import streamlit as st
from PIL import Image
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from newspaper import Article
import io
import nltk
nltk.download('punkt')

st.set_page_config(page_title='SummarizeMe: Your News Insights Bot 📰🤖', page_icon='./Meta/newspic.ico')


def fetch_news_search_topic(topic):
    site = 'https://news.google.com/rss/search?q={}'.format(topic)
    op = urlopen(site)
    rd = op.read()  
    op.close()  
    sp_page = soup(rd, 'xml')  
    news_list = sp_page.find_all('item')  
    return news_list


def fetch_top_news():
    site = 'https://news.google.com/news/rss'
    op = urlopen(site)   
    rd = op.read()   
    op.close()   
    sp_page = soup(rd, 'xml')  
    news_list = sp_page.find_all('item')  
    return news_list


def fetch_category_news(topic):
    site = 'https://news.google.com/news/rss/headlines/section/topic/{}'.format(topic)
    op = urlopen(site)   
    rd = op.read()   
    op.close()   
    sp_page = soup(rd, 'xml')   
    news_list = sp_page.find_all('item')   
    return news_list


def fetch_news_poster(poster_link):
    try:
        u = urlopen(poster_link)
        raw_data = u.read()
        image = Image.open(io.BytesIO(raw_data))
        st.image(image, use_column_width=True)
    except:
        image = Image.open('./Meta/no_image.jpg')
        st.image(image, use_column_width=True)


def display_news(list_of_news, news_quantity):
    c = 0
    for news in list_of_news:
        c += 1
       
        st.write('**({}) {}**'.format(c, news.title.text))
        news_data = Article(news.link.text)
        try:
            news_data.download()
            news_data.parse()
            news_data.nlp()
        except Exception as e:
            st.error(e)
        fetch_news_poster(news_data.top_image)
        with st.expander(news.title.text):
            st.markdown(
                '''<p style='text-align: justify;'>{}"</p>'''.format(news_data.summary),
                unsafe_allow_html=True)
            st.markdown("[Read more at {}...]({})".format(news.source.text, news.link.text))
        st.success("Published Date: " + news.pubDate.text)
        if c >= news_quantity:
            break


def run():
    st.title("HuntsBrief: News, Simplified")
    image = Image.open('./Meta/newspic.png')

    col1, col2, col3 = st.columns([3, 5, 3])

    with col1:
        st.write("")

    with col2:
        st.image(image, use_column_width=False)

    with col3:
        st.write("")
    category = ['Choose Wisely', 'News on Fire🔥', 'My Beloved Topics❤️', 'Hunt for Gossip🕵️']
    cat_op = st.selectbox('Select your Category', category)
    if cat_op == category[0]:
        st.warning('Oopsie-doodle! Looks like you forgot to pick a category, my friend!')
    elif cat_op == category[1]:
        st.subheader("🗞️Presenting the Latest Trending News Just for You!🗞️")
        no_of_news = st.slider('Number of News:', min_value=3, max_value=10, step=1)
        news_list = fetch_top_news()
        display_news(news_list, no_of_news)
    elif cat_op == category[2]:
        av_topics = ['Choose Topic', 'WORLD', 'NATION', 'BUSINESS', 'TECHNOLOGY', 'ENTERTAINMENT', 'SPORTS', 'SCIENCE',
                     'HEALTH']
        st.subheader("Choose your Beloved Topic")
        chosen_topic = st.selectbox("Choose your Beloved Topic", av_topics)
        if chosen_topic == av_topics[0]:
            st.warning("Time to Make a Selection, My Friend!: do it faslty, or I'll choose for you!")
        else:
            no_of_news = st.slider('Number of News:', min_value=3, max_value=10, step=1)
            news_list = fetch_category_news(chosen_topic)
            if news_list:
                st.subheader("✅ Here are the some {} News for you".format(chosen_topic))
                display_news(news_list, no_of_news)
            else:
                st.error("Give me a topic to explore🔍 {}".format(chosen_topic))

    elif cat_op == category[3]:
        user_topic = st.text_input("Let's Dive into a Topic🔍")
        no_of_news = st.slider('Number of News:', min_value=3, max_value=10, step=1)

        if st.button("Search") and user_topic != '':
            user_topic_pr = user_topic.replace(' ', '')
            news_list = fetch_news_search_topic(topic=user_topic_pr)
            if news_list:
                st.subheader("✅ Here are the some {} News for you".format(user_topic.capitalize()))
                display_news(news_list, no_of_news)
            else:
                st.error("No News found for {}".format(user_topic))
        else:
            st.warning("Give me a topic to explore🔍")


run()
