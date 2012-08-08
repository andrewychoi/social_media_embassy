from django.core.management import setup_environ
from social_media_embassy import settings

setup_environ(settings)

from embassy.models import Embassy

def insert_test_embassies():
    korean_embassy = Embassy(name = "US Embassy in Seoul",
                             facebook_id = 111794158722,
                             twitter_id = 61426538,
                             twitter_username = "usembassyseoul",
                             )
    korean_embassy.save()

if __name__=="__main__":
    insert_test_embassies()