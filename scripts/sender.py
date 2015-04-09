#!/usr/bin/env python
import sys
import os
import datetime
import time



parent_folder = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../")
sys.path.append(parent_folder)
from twython import Twython

from django.core.management import setup_environ
from twitmob import settings
setup_environ(settings)

from main.models import Campaign, UserCampaign, UserMessage

from twython_django_oauth.models import TwitterProfile
# get all campaigns that start between now and 15 minut

start_time = datetime.datetime.now() - datetime.timedelta(minutes=60)
end_time = datetime.datetime.now()


messages = UserMessage.objects.filter(message__campaign__start_time__gte=start_time).filter(message__campaign__start_time__lte=end_time)
print messages
messages = messages.filter(sent=None).order_by("pk")
print messages

for message in messages:
	before_10 = datetime.datetime.now() - datetime.timedelta(minutes=10)
	if not UserMessage.objects.filter(user=message.user,sent__gte=before_10).exists():
		#only send if we haven't sent a message for this user in the past 10 minutes.
		# we can tweak this later
		twitprof = TwitterProfile.objects.filter(user=message.user)
		if twitprof.exists():
			twitprof = twitprof[0]
			twitter = Twython(settings.TWITTER_KEY, settings.TWITTER_SECRET,
				                  twitprof.oauth_token, twitprof.oauth_secret)
			full_tweet = "%s #%s" % (message.message.text, message.message.campaign.hashtag) 
			print "Sending..."
			try:
				twitter.updateStatus(status=full_tweet)
				message.sent = datetime.datetime.now()
				message.save()
			except:
				print sys.exc_info()
		
					
