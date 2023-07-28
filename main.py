import requests
import telebot
import datetime
from bs4 import BeautifulSoup

placeHolderImage = "https://motiabebe.github.io/ShegerFM-Scrapping/images/ShegerFM_Logo.png"

def scrapNews(url):
    # Open the URL and read the content
    content = requests.get(url).content

    # Parse the HTML content using BeautifulSoup
    website_soup = BeautifulSoup(content, 'html.parser')

    # Get the news titles and links
    scraped_news = website_soup.find_all(attrs={"data-hook": "item-container"})

    titles = [t.find('a').text for t in scraped_news]
    links = [articleLink.find('a')['href'] for articleLink in scraped_news]

    images_soup = website_soup.find_all(attrs={"data-hook": "gallery-item-image-img"})

    # if the number of titles and images are equal
    if len(titles) == len(images_soup):
        images = [image['src'] for image in images_soup]
    else:
        images = [placeHolderImage for image in titles]

    subtitles_soup = website_soup.find_all(attrs={"data-hook": "post-description"})
    subtitles = [subtitle.find('div').text for subtitle in subtitles_soup]

    posted_time_soup = website_soup.find_all(attrs={"data-hook": "time-to-read"})
    posted_time = []

    for time in posted_time_soup:
        # if minutes convert to hours
        if 'minute' or 'minutes' in time.text:
            posted_time.append(int(time.text.split(' ')[0]) / 60)
        # if hours
        elif 'hour' or 'hours' in time.text:
            posted_time.append(int(time.text.split(' ')[0]))
        # the rest append as it is
        else:
            posted_time.append(time.text)

    return titles, subtitles, links, images, posted_time
           

# Create a Telegram bot
shegerBot = telebot.TeleBot(token='5855711747:AAG09yZQVoN1_0O73HGyW54UE9-ggprGco8')

# Function to post news to the bot
def post_news():
    # Get the news
    titles, subtitles, links, images, posted_time = scrapNews("https://www.shegerfm.com")

    # Get the current time and add 3 hours to it (Ethiopian time)
    currentTime = datetime.datetime.now() + datetime.timedelta(hours=3)

    timeMessage = "News for " + currentTime.strftime("%Y-%m-%d %H:%M") + "\n \n" + "Powered by Sheger FM"

    # Send current time to the bot
    shegerBot.send_photo(chat_id='@shegerNewsUpdates', photo=placeHolderImage, caption=timeMessage)

    # Loop through the news
    for i in range(len(titles)):
        # check if the news is posted is not older than 6 hours ago
        if posted_time[i] > 6:
            continue
        elif posted_time[i] is type(str):
            continue

        # if photo is available
        if images[i] != None:
            shegerBot.send_photo(chat_id='@shegerNewsUpdates', photo=images[i], caption=titles[i] + "\n \n " + subtitles[i] + "\n \n" + "Read more: " + links[i])
        else:
        # if no photo is available
            shegerBot.send_message(chat_id='@shegerNewsUpdates', photo=placeHolderImage, caption=titles[i] + "\n \n" + subtitles[i] + "\n \n" + "Read more: " + links[i])

    # get more news at current time + 6 hours
    shegerBot.send_message(chat_id='@shegerNewsUpdates', text="Get more news at " + (currentTime + datetime.timedelta(hours=6)).strftime("%Y-%m-%d %H:%M"))



# Post news to the bot
post_news()
