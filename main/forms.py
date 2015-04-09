from main import models
from django.forms import ModelForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, Div, HTML
from crispy_forms.bootstrap import FormActions, PrependedText, AppendedText


class CampaignForm(ModelForm):


	i_agree = forms.BooleanField(required=True,initial=True)

	def __init__(self, *args, **kwargs):
		super(CampaignForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-2'
		self.helper.field_class = 'col-lg-8'
		self.helper.help_text_inline = True

		self.fields['i_agree'].label = "Post a tweet in my timeline promoting this Crowd"
		self.fields['i_agree'].help_text = "Hey, if you don't promote your Crowd...nobody will come!"
		self.fields['allow_personal_tweets'].label = "Allow users to create custom tweets"
		self.fields['allow_personal_tweets'].help_text = "If you set this, users will be able to create their own tweets. If not they'll only be able to select one of yours."
		self.fields['start_time'].help_text = "All times are XXX; check <a href='#'>this!</a>"
		self.fields['hashtag'].help_text = "Dont' add the # sign, we already do that for you :)"
		# self.fields['title'].help_text = "Something to help identify your Crowd"
		# self.fields['description'].help_text = "Decribe your Crowd in the best possible way"



		self.helper.layout = Layout(
			Fieldset(
				'',
				'title',
				'allow_personal_tweets',
				AppendedText('start_time','<i class="glyphicon glyphicon-calendar"></i>'

					),
				
				'description',
				

				PrependedText('hashtag',"#",placeholder="SaySomething",title="asdasd"),
				Field('i_agree',label="hola"),
				),

				FormActions(
					Submit('save', 'Save your new Crowd!', css_class="pull-right btn-success"),

			)
		)

	class Meta:
		model = models.Campaign
		exclude = ['owner','created']

	def clean_hashtag(self):
		hashtag = self.cleaned_data['hashtag']
		
		if hashtag.find("#") > -1:
			raise forms.ValidationError(u"Don't use a # in your hashtag, we'll include it.")

		if hashtag.find(" ") > -1:
			raise forms.ValidationError(u"Don't use spaes in your hashtag.")


		return hashtag

	# def clean_start_time(self):


	# 	hashtag = self.cleaned_data['start_time']
	# 	return hashtag


# title = models.CharField(max_length=300)
# description = models.TextField()
# owner = models.ForeignKey(User)
# created = models.DateTimeField(auto_now_add=True)
# start_time = models.DateTimeField()
# allow_personal = models.BooleanField(default=True)
# hashtag = models.CharField(max_length=50)