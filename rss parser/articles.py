import feedparser
import datetime 
from time import mktime
import csv
from dateutil import parser, tz


# Site contains links to multiple RSS feeds
#https://github.com/registerguard/django-newswall/wiki/Some-words-about-feedparser,-timezones-and-parsing-RSS-feeds


# Forked from Adam Carter

def parse_feeds(url1, url2):
    feed1 = feedparser.parse(url1)
    feed2 = feedparser.parse(url2)
    an_hour_ago = datetime.datetime.now() - datetime.timedelta(hours=1)
    recent_posts1 = [entry for entry in feed1.entries if datetime.datetime.fromtimestamp(mktime(entry.updated_parsed)) > an_hour_ago]
    recent_posts1 += [entry for entry in feed2.entries if datetime.datetime.fromtimestamp(mktime(entry.updated_parsed)) > an_hour_ago]
    
    """
    #More experimental
    published = feed1.entries[0].published
    dt = parser.parse(published)

    print("below is the published data\n")
    print(published)
    print("below is parsed daytime\n")
    print(dt) # that is timezone aware
    print("below is time zone\n")
    print(dt.utcoffset()) # time zone of time
    print("below is UTC \n")
    print(dt.astimezone(tz.tzutc())) # that is timezone aware as UTC

    for post in recent_posts1:
        local_now = utc_now.astimezone(post.updated)
        
        print(post.updated, ", converted to ",local_now )
    """
    recent_posts1.sort( key=lambda x: x.published_parsed)

    for post in recent_posts1:
        pub = post.published
        dayTime = parser.parse(pub)
        print("(", dayTime.astimezone(tz.tzutc()), ") ", post.title, sep="")
    
    print('uhh hello')
    with open('feed.csv', mode='w') as feed_file:
        feed_writer = csv.writer(feed_file, delimiter=',', quotechar='"',quoting=csv.QUOTE_MINIMAL)
        for post in recent_posts1:
            pub = post.published
            dayTime = parser.parse(pub)
            
            #entry = dayTime.astimezone(tz.tzutc()), post.title
            #entry = date_time.strftime("%m/%d/%Y, %H:%M:%S")
            feed_writer.writerow([dayTime.astimezone(tz.tzutc()), post.title])

    #show only items from last hour
    print("**********done*************")

#  This is how we run a test case within a python file
if __name__ == '__main__':
    parse_feeds('https://www.npr.org/rss/rss.php','https://www.fandango.com/rss/newmovies.rss')
    print('\n Next feed is')
    parse_feeds('http://billmaher.hbo.libsynpro.com/rss', 'https://www.craigslist.org/about/best/all/index.rss')

# We have two links
# NPR movies
# https://www.npr.org/rss/rss.php?id=1045
# RSS Link
# https://www.npr.org/rss/

# Fandango New Movies
# https://www.fandango.com/rss/newmovies.rss