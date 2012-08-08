from django.db import models

# Create your models here.

class Embassy(models.Model):
    name = models.CharField(max_length = 200)
    facebook_id = models.IntegerField(blank = True, null = True)
    twitter_id = models.IntegerField(blank = True, null = True)
    twitter_username = models.CharField(max_length = 200, blank = True)
    last_tweet_id = models.IntegerField(blank = True, null = True)
    youtube_id = models.IntegerField(blank = True, null = True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Embassies"
    