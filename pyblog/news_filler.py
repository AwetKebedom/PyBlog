###################################################
######                                       ######
######         pyblog/news_filler.py         ###### 
######                                       ######
###################################################

import GoogleNews

def get_news(searched_word):
    news_wrapper = GoogleNews.GoogleNews()
    news_wrapper.search(searched_word)

    for page_ix in range(2,3):
        news_wrapper.getpage(page_ix)
        print("Fetched page", page_ix)

    search_result = news_wrapper.result()
    news_wrapper.clear()

    news = []
    print(search_result)
    for news_dict in search_result:
        title = news_dict['title']
        link  = news_dict['link']
        news.append((title, link))

    return news

get_news('israejk')
