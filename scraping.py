import requests
from bs4 import BeautifulSoup
import pprint  # pretty print in terminal
import time

start_url = 'https://news.ycombinator.com/news'
mega_links = []
mega_subtext = []


def sort_stories_by_votes(hn_list):
    # common pattern to sort dictionaries, key lambda, reverse=T means sort high to low
    return sorted(hn_list, key=lambda k: k['votes'], reverse=True)


def create_custom_articles(links, subtext):
    hacker_news = []
    desired_min_points = 199
    for idx, item in enumerate(links):
        title = links[idx].getText()
        href = links[idx].get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > desired_min_points:
                hacker_news.append({'title': title, 'link': href, 'votes': points})
    return sort_stories_by_votes(hacker_news)


def grab_relevant_data(soup):
    article_links = soup.select('.titleline > a')
    subtext_lines = soup.select('.subtext')
    mega_links.extend(article_links)
    mega_subtext.extend(subtext_lines)
    return mega_subtext, mega_links


def request_information(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        next_page_a_tag = soup.select_one('.title > .morelink')

        # ensures request doesn't come in too quickly
        time.sleep(.15)

        # if a 'more' tag (pagination) exists, scrape again
        if next_page_a_tag is not None:
            new_href = next_page_a_tag.get('href')
            new_url = start_url + new_href

            print(f'scraping page {new_href}...')

            grab_relevant_data(soup)
            request_information(new_url)
        else:
            print('Organizing articles to your liking...')
            final_articles = create_custom_articles(mega_links, mega_subtext)
            return pprint.pprint(final_articles)
    except IndexError as e:
        print(f'{e}: index error')



request_information(start_url)
