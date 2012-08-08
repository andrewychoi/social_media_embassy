import time
import urllib2
import simplejson
from django.core.management import setup_environ
from social_media_embassy import settings

setup_environ(settings)

from embassy.models import Embassy
from embassy_twitter.models import TwitterRecord

def pull_from_twitter(embassy):
    if not embassy.twitter_id:
        embassy.twitter_id = get_twitter_id(embassy.twitter_username)
        embassy.save()

    if not embassy.last_tweet_id:
        start_url = "https://api.twitter.com/1/statuses/user_timeline.json?count=150&user_id=%d" % embassy.twitter_id
        next_page_url = start_url + "&max_id=%d"
        
        curr_page = simplejson.load(urllib2.urlopen(start_url))
        
        last_tweet_id = curr_page[0]['id']
        embassy.last_tweet_id = last_tweet_id
        embassy.save()
        
        num_tweets = 0
        
        while curr_page:
            print num_tweets
            tweet_id_list = []
            for tweet in curr_page:
                tweet_id_list.append(tweet['id'])
            num_tweets += len(tweet_id_list)
            next_max_id = min(tweet_id_list)
            curr_page = simplejson.load(urllib2.urlopen(next_page_url % next_max_id))
            
    else:
        old_last_tweet_id = embassy.last_tweet_id
        
        base_first_page_url = "https://api.twitter.com/1/statuses/user_timeline.json?count=150&user_id=%d&since_id=%d"
        first_page_url = base_first_page_url % (embassy.twitter_id, old_last_tweet_id)
        
        next_page_url = first_page_url + "&max_id=%d"

        curr_page = simplejson.load(urllib2.urlopen(first_page_url))
                
        num_new_tweets = 0
        
        if curr_page:
            
            last_tweet_id = curr_page[0]['id']
            embassy.last_tweet_id = last_tweet_id
            embassy.save()
            
            while curr_page:
                for tweet in curr_page:
                    tweet_id_list.append(tweet['id'])
                num_new_tweets += len(tweet_id_list)
                next_max_id = min(tweet_id_list)
                curr_page = simplejson.load(urllib2.urlopen(next_page_url % next_max_id))
            
        if TwitterRecord.objects.count() > 0:
            last_record = TwitterRecord.objects.latest(field_name = 'timestamp')
            num_old_tweets = last_record.tweets
        else:
            num_old_tweets = 0
        
        num_tweets = num_old_tweets + num_new_tweets
        
        print "Stats for Twitter page of %s at %s" % (embassy.name, time.strftime("%a, %d %b %Y %H:%M:%S"))
        print "number of tweets: %d" % num_tweets
    
    num_mentions = 0
    twitter_record = TwitterRecord(embassy = embassy,
                                   tweets = num_tweets,
                                   mentions = num_mentions
                                   )
    twitter_record.save()
    
def get_twitter_id(username):
    base_url = "https://api.twitter.com/users/show/%s.json"
    lookup_url = base_url % username
    lookup_json = simplejson.load(urllib2.urlopen(lookup_url))
    twitter_id = lookup_json['id']
    return twitter_id
    
if __name__=="__main__":
    for embassy in Embassy.objects.all():
        pull_from_twitter(embassy)