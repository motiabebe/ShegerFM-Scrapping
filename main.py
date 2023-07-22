import requests
import telebot
import datetime
from bs4 import BeautifulSoup

# URL to scrape
url = 'https://www.shegerfm.com/'

# Open the URL and read the content
content = requests.get(url).content

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(content, 'html.parser')

# Get the div with class 'blog-post-post-list-link-hashtag-hover-color'
newsfeed_soup = soup.find_all('div', class_='blog-post-post-list-link-hashtag-hover-color')

# Extract the title and link for each div
# titles = [t.find('a').text for t in title_divs]
titles = []
for title in newsfeed_soup:
    titles.append(title.find('a').text)

links = [articleLink.find('a')['href'] for articleLink in newsfeed_soup]

images_soup = soup.find_all(attrs={"data-hook": "gallery-item-image-img"})
images = []
for image in images_soup:
    images.append(image['src'])

posted_time_soup = soup.find_all(attrs={"data-hook": "time-ago"})
posted_time = []

for time in posted_time_soup:
    # if minutes convert to hours
    if 'minute' in time.text:
        posted_time.append(int(time.text.split(' ')[0]) / 60)
    # if hours
    elif 'hour' in time.text:
        posted_time.append(int(time.text.split(' ')[0]))
    elif 'day' in time.text:
        posted_time.append(int(time.text.split(' ')[0]) * 24)


subtitles_soup = soup.find_all('div', class_='CHRJex JMCi2v pu51Xe lyd6fK xs2MeC')
subtitles = [subtitle.find('div').text for subtitle in subtitles_soup]
             

# Create a Telegram bot
shegerBot = telebot.TeleBot(token='5855711747:AAG09yZQVoN1_0O73HGyW54UE9-ggprGco8')

# Function to post news to the bot
def post_news():
    # Get the current time
    currentTime = datetime.datetime.now()
    # Send current time to the bot
    shegerBot.send_photo(chat_id='@shegerNewsUpdates', photo="https://motiabebe.github.io/ShegerFM-Scrapping/images/ShegerFM%20Full.png", caption="News for " + currentTime.strftime("%Y-%m-%d %H:%M") + "\n \n" + "Powered by Sheger FM")

    # Loop through the news
    for i in range(len(titles)):
        # check if the news is posted is not older than 6 hours ago
        if posted_time[i] > 6:
            continue
        elif posted_time[i] is type(str):
            continue

        # if photo is available
        if images[i] != None:
            # use a placeholder image
            shegerBot.send_photo(chat_id='@shegerNewsUpdates', photo=images[i], caption=titles[i] + "\n \n " + subtitles[i] + "\n \n" + "Read more: " + links[i])
        else:
            # send using a placeholder image
            shegerBot.send_message(chat_id='@shegerNewsUpdates', photo="https://motiabebe.github.io/ShegerFM-Scrapping/images/ShegerFM%20Full.png", caption=titles[i] + "\n \n" + subtitles[i] + "\n \n" + "Read more: " + links[i])

    # get more news at 7, 12, 18
    if currentTime.hour == 7 or currentTime.hour == 12 or currentTime.hour == 18:
        shegerBot.send_message(chat_id='@shegerNewsUpdates', text="Get more news at: " + str(currentTime.hour) + ":00")


# Post news to the bot
post_news()

