# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseForbidden

from django.contrib.auth import logout


import json
import datetime

from main.models import *
from django.db.models import Count
from twython_django_oauth.models import TwitterProfile

from twython import Twython
from twitmob import settings


from main import forms


def force_logout(request):

	logout(request)
	return redirect("/")

@login_required
def my_crowds(request):

	now = datetime.datetime.now() - datetime.timedelta(minutes=60)
	context = RequestContext(request)

	my_joined_campaigns = Campaign.objects.filter(usercampaign__user=request.user)

	my_joined_campaigns = my_joined_campaigns.exclude(start_time__lte=now).order_by("-start_time")

	my_campaigns = Campaign.objects.filter(owner=request.user)
	my_campaigns = my_campaigns.exclude(start_time__lte=now).order_by("-start_time")
	

	context["my_joined_campaigns"] = my_joined_campaigns
	context["my_campaigns"] = my_campaigns

	return render_to_response("my_crowds.html", context_instance=context)

@login_required
def force_login(request):
	return redirect("/")

def home(request):
	context = RequestContext(request)

	now = datetime.datetime.now() - datetime.timedelta(minutes=60)

	popular = Campaign.objects.filter().annotate(num_joiners=Count('usercampaign')).order_by("-num_joiners","-start_time")
	

	popular = popular.exclude(start_time__lte=now)
	if popular.count() > 9:
		popular = popular[0:9]

	context["popular"] = popular
	context["pill"] = "home"

	return render_to_response("home.html", context_instance=context)

def redirect_crowd(request, id):
	crowd = get_object_or_404(Campaign,pk=id)
	return redirect("join_campaign",crowd.pk,crowd.hashtag)


@login_required
def leave_campaign(request):

	camp = get_object_or_404(Campaign,pk=request.GET["id"])

	all_messages = UserMessage.objects.filter(user=request.user,message__campaign=camp)
	for m in all_messages:
		m.delete()

	[x.delete() for x in UserCampaign.objects.filter(user=request.user,campaign=camp)]
	try:
		pass
	except:
		pass

	return redirect("join_campaign",request.GET["id"])



@login_required
def new_campaign(request):
	context = RequestContext(request)

	if request.POST:

		post_data = {}
		
		# for k in request.POST.keys():
			# post_data[k] = request.POST[k]
		# print post_data
		# post_data["start_time"] = "%s %s" % (post_data["date"] , post_data["time"])
		form = forms.CampaignForm(request.POST)
		if form.is_valid():
			campaign = form.save(commit=False)
			campaign.owner = request.user
			campaign.save()

			twitprof = TwitterProfile.objects.filter(user=request.user)
			if twitprof.exists():
				twitprof = twitprof[0]
			twitter = Twython(settings.TWITTER_KEY, settings.TWITTER_SECRET,
				                  twitprof.oauth_token, twitprof.oauth_secret)
			full_tweet = "I've just created a new twitter crowd for #%s, join me at http://microwder.com/c/%d" % (campaign.hashtag, campaign.pk) 
			try:
				twitter.updateStatus(status=full_tweet)
			except:
				import sys
				print sys.exc_info()

			return redirect("edit_campaign",id=campaign.pk)

	else:
		form = forms.CampaignForm()

	context["form"] = form

	context["pill"] = "new_crowd"
	return render_to_response("new_campaign.html", context_instance=context)

@login_required
def edit_campaign(request,id):
	context = RequestContext(request)


	campaign = get_object_or_404(Campaign,id=id)
	if campaign.owner != request.user:
		return HttpResponseForbidden("You can't edit this Crowd.")
	context["campaign"] = campaign

	if not UserMessage.objects.filter(message__campaign=campaign,user=request.user).exists():
		context["notjoined"] = True


	return render_to_response("edit_campaign.html", context_instance=context)

@csrf_exempt
@login_required
def join_campaign(request,id, slug=None):

	context = RequestContext(request)

	campaign = get_object_or_404(Campaign,id=id)
	

	if request.GET.get("m",None) != None:

		if not UserCampaign.objects.filter(user=request.user,campaign=campaign).exists():
			uc = UserCampaign(user=request.user,campaign=campaign)
			uc.save()

		all_messages = UserMessage.objects.filter(user=request.user,message__campaign=campaign)
		for m in all_messages:
			m.delete()

		new_m = UserMessage()
		new_m.new_m = request.user
		new_m.message = CampaignMessage.objects.get(pk=request.GET["m"])
		new_m.user = request.user
		new_m.save()

	context["campaign"] = campaign

	has_joined = UserMessage.objects.filter(user=request.user,message__campaign=campaign)
	if has_joined.exists():
		context["joined_message"] = has_joined[0]
		context["has_joined"] = True

	else:
		context["has_joined"] = False


	return render_to_response("join_campaign.html", context_instance=context)


def campaigns(request):
	context = RequestContext(request)

	start = int(request.GET.get("start",0))
	sort = request.GET.get("sort","start")


	now = datetime.datetime.now() - datetime.timedelta(minutes=60)

	NUM_PAGE = 20

	campaigns = Campaign.objects.all().filter(start_time__gte=now).order_by(sort)
	campaigns = campaigns.annotate(num_joiners=Count('usercampaign'))

	if sort == "start":
		campaigns = campaigns.order_by("-start_time").order_by("-created")
	elif sort == "users":
		campaigns = campaigns.order_by("-num_joiners").order_by("-start_time")
	elif sort == "created":
		campaigns = campaigns.order_by("-created").order_by("-start_time")
	
		
	#.order_by("-num_joiners","-start_time")
	#campaigns = campaigns.exclude(start_time__lte=now)

	if campaigns.count() > start + NUM_PAGE:
		campaigns = campaigns[start:start+NUM_PAGE]
		context["next"] = start + NUM_PAGE
		if start - NUM_PAGE > -1:
			context["prev"] = start - NUM_PAGE
		else:
			context["prev"] = None
	else:
		campaigns = campaigns[start:]
		context["next"] = None
		if start - NUM_PAGE > -1:
			context["prev"] = start - NUM_PAGE
		else:
			context["prev"] = None
	
	context["campaigns"] = campaigns
	context["pill"] = "active_crowds"
	context["NUM_PAGE"] = NUM_PAGE
	context["sort"] = sort
	return render_to_response("campaigns.html", context_instance=context)


def delete_message(request):

	try:
		msg = CampaignMessage.objects.get(pk=request.GET["id"])

		if msg.creator == request.user or request.user == msg.campaign.owner:
			msg.delete()

		return HttpResponse("OK")
	except:
		return HttpResponse("Can't delete")

@csrf_exempt
def new_message(request):

	data = {}
	try:
		campaign = Campaign.objects.get(id=request.POST["campaign"])
	except:
		
		data["status"] = "error"
		data["error"] = "Campaign doesn't exist"
		return HttpResponse(json.dumps(data), mimetype="application/json")


	if campaign.allow_personal_tweets or request.user == campaign.owner: 
		message = CampaignMessage()

		message.creator = request.user
		message.campaign = campaign
		message.text = request.POST["message"]
		message.save()


		data["status"] = "OK"
		data["message"] = {"message":message.text,"hashtag":campaign.hashtag,"id":message.pk}
		data["message"]["creator"] = "You"
		data["message"]["created"] = message.created.strftime("%b. %d %Y, %I:%S %p")
		




		return HttpResponse(json.dumps(data), mimetype="application/json")
	else:
		return HttpResponse(json.dumps({'ERROR':'ERROR'}), mimetype="application/json")


