import requests
import telebot
from telebot import types
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

# Command Handlers
@shegerBot.message_handler(commands=['start'])
def send_welcome(message):

    sub_menu = types.InlineKeyboardMarkup()

    news_btn = types.InlineKeyboardButton(text="ወሬ 📰", callback_data="news")
    today_btn = types.InlineKeyboardButton(text="የዛሬ ወሬ 🕕", callback_data="today")
    local_btn = types.InlineKeyboardButton(text="የአገር ውስጥ ወሬ 🗺️", callback_data="local")
    world_btn = types.InlineKeyboardButton(text="የውጭ ወሬ 🌐", callback_data="world")
    business_btn = types.InlineKeyboardButton(text="ቢዝነስ ወሬ 💲", callback_data="business")
    ecomony_btn = types.InlineKeyboardButton(text="ምጣኔ ሐብት 🎢", callback_data="ecomony")

    sub_menu.add(news_btn, today_btn, local_btn, world_btn, business_btn, ecomony_btn)

    welcome_message = "Welcome to Sheger News Updates \n" + "\n \n" + "Use the buttons below to browse the news." + "\n \n" + "Powered by Sheger FM"

    shegerBot.send_message(chat_id='@shegerNewsUpdates', text=welcome_message, reply_markup=sub_menu)

# Callback Handlers
@shegerBot.callback_query_handler(func=lambda call: call.data == "news")
def news(call):
    # Call the post_news function with the url of the news
    # post_news("https://www.shegerfm.com/ወሬ")
    post_news("https://motiabebe.github.io/ShegerFM-Scrapping/scraped-html/ወሬ.html")

@shegerBot.callback_query_handler(func=lambda call: call.data == "today")
def today(call):
    # Call the post_news function with the url of the news from today
    # post_news("https://www.shegerfm.com/ወሬ/categories/የዛሬወሬ")
    post_news("https://motiabebe.github.io/ShegerFM-Scrapping/scraped-html/የዛሬወሬ.html")
    
@shegerBot.callback_query_handler(func=lambda call: call.data == "local")
def local(call):
    # Call the post_news function with the url of the local news
    # post_news("https://www.shegerfm.com/ወሬ/categories/local-news")
    post_news("https://motiabebe.github.io/ShegerFM-Scrapping/scraped-html/local-news.html")

@shegerBot.callback_query_handler(func=lambda call: call.data == "world")
def world(call):
    # Call the post_news function with the url of the world news
    # post_news("https://www.shegerfm.com/ወሬ/categories/international-news")
    post_news("https://motiabebe.github.io/ShegerFM-Scrapping/scraped-html/international-news.html")

@shegerBot.callback_query_handler(func=lambda call: call.data == "business")
def business(call):
    # Call the post_news function with the url of the business news
    # post_news("https://www.shegerfm.com/ወሬ/categories/business-news")
    post_news("https://motiabebe.github.io/ShegerFM-Scrapping/scraped-html/business-news.html")

@shegerBot.callback_query_handler(func=lambda call: call.data == "ecomony")
def ecomony(call):
    # post_news("https://www.shegerfm.com/ወሬ/categories/economy")
    post_news("https://motiabebe.github.io/ShegerFM-Scrapping/scraped-html/economy.html")


# Command Handlers
@shegerBot.message_handler(commands=['help'])
def send_help(message):
    # A help message with the list of commands and a news button
    menu = types.InlineKeyboardMarkup()
    get_news = types.InlineKeyboardButton(text="News", callback_data="news")
    menu.add(get_news)
    help_message = "Use the following commands to navigate the bot \n \n" + "/start - start the bot \n" + "/help - get help \n" + "/news - get news menu \n \n" + "Click the button below to get news \n" + "Powered by Sheger FM"
    shegerBot.reply_to(message, help_message, reply_markup=menu)

@shegerBot.message_handler(commands=['news'])
def send_news(message):
    # A news menu with buttons
    menu = types.InlineKeyboardMarkup()
    get_news = types.InlineKeyboardButton(text="News", callback_data="news")
    menu.add(get_news)
    news_message = "Click the button below to get news \n" + "Powered by Sheger FM"
    shegerBot.reply_to(message, news_message, reply_markup=menu)


# Function to post news to the bot
def post_news(url):
    # Get the news
    titles, subtitles, links, images, posted_time = scrapNews(url)

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
    # shegerBot.send_message(chat_id='@shegerNewsUpdates', text="Get more news at " + (currentTime + datetime.timedelta(hours=6)).strftime("%Y-%m-%d %H:%M"))

# Run the bot
print("Bot is running...")
shegerBot.polling()




