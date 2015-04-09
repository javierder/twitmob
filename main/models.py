from django.db import models
from django.contrib.auth.models import User

class Campaign(models.Model):
	title = models.CharField(max_length=300)
	description = models.TextField()
	owner = models.ForeignKey(User)
	created = models.DateTimeField(auto_now_add=True)
	start_time = models.DateTimeField()
	allow_personal_tweets = models.BooleanField(default=True)
	hashtag = models.CharField(max_length=50)

	def max_length(self):
		return 140 - len(self.hashtag) -1 

	def total_count(self):
		return self.usercampaign_set.all().count()

	def total_messages(self):
		return self.campaignmessage_set.all().count()

	def slug(self):
		return self.title.replace(" ","-")

class UserCampaign(models.Model):
	user = models.ForeignKey(User)
	campaign = models.ForeignKey(Campaign)
	joined = models.DateTimeField(auto_now_add=True)

class CampaignMessage(models.Model):
	creator = models.ForeignKey(User)
	campaign = models.ForeignKey(Campaign)
	created = models.DateTimeField(auto_now_add=True)
	last_updated = models.DateTimeField(auto_now=True)
	text = models.TextField()

	def users_count(self):
		return self.usermessage_set.values("user__id").distinct().count()

class UserMessage(models.Model):
	user = models.ForeignKey(User)
	sent = models.DateTimeField(default=None, blank=True, null=True)
	message = models.ForeignKey(CampaignMessage)
