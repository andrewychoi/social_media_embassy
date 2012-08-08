from django.db import models
from embassy.models import Embassy

# Create your models here.

class FacebookRecord(models.Model):
    embassy = models.ForeignKey(Embassy)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField()
    talking_about = models.IntegerField()
    
    def __unicode__(self):
        return str(self.embassy) + " at " + str(self.timestamp)
    
    class Meta:
        verbose_name = "Facebook record"