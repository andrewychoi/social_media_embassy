import urllib2
import simplejson
import time
from django.core.management import setup_environ
from social_media_embassy import settings

setup_environ(settings)

from embassy.models import Embassy
from embassy_facebook.models import FacebookRecord

def pull_from_facebook(embassy):
    fb_base_url = "https://graph.facebook.com/%s"
    fb_url = fb_base_url % embassy.facebook_id
    json_dict = simplejson.load(urllib2.urlopen(fb_url))
    print "Stats for FB page %s at %s" % (embassy.name, time.strftime("%a, %d %b %Y %H:%M:%S"))
    likes = json_dict['likes']
    talking_about = json_dict['talking_about_count']
    print "likes: %d" % json_dict['likes']
    print "talking_about: %d" % json_dict['talking_about_count']
    facebook_record = FacebookRecord(embassy = embassy, 
                                     likes = likes,
                                     talking_about = talking_about)
    facebook_record.save()

if __name__=="__main__":
    
    for embassy in Embassy.objects.all():
        pull_from_facebook(embassy)
