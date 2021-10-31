from django import forms
from ckeditor.fields import RichTextFormField
from .models import tag
from django.contrib.auth.models import User

class post_question_form(forms.Form):
    title = forms.CharField(label= 'Title ', max_length=50, required=True)
    description = RichTextFormField(label=' Description')
    try:
        tags = tag.objects.all()
    except:
        some_error = 'True, will find it later'
    CHOICES = list()
    x=0
    for i in tags:
        CHOICES.append((x,i.title))
        x+=1
    
    tag1 = forms.ChoiceField(choices=CHOICES)
    tag2 = forms.ChoiceField(choices=CHOICES)
    tag3 = forms.ChoiceField(choices=CHOICES)
    
class post_answer_form(forms.Form):
    answer = RichTextFormField(label='Answer ')
    
class comment_form(forms.Form):
    comment = RichTextFormField(label='Comment ')
    
class contact_form(forms.Form):
    subject = RichTextFormField(label='Subject ')

class q_report_action_form(forms.Form):
    delete = forms.BooleanField(label='Delete ', required=False)
    action = forms.BooleanField(label='Take Action ', required=False)
    
class a_report_action_form(forms.Form):
    delete = forms.BooleanField(label='Delete ', required=False)
    action = forms.BooleanField(label='Take Action ', required=False)

class email_form(forms.Form):
    try:
        datas = User.objects.all()
        emails = list()
        emails.append((0,'all'))
        for data in datas:
            emails.append((data.id,data.email))
    except:
        reason = 'some erro occured'
    user = forms.ChoiceField(choices=emails)
    subject = forms.CharField(label='Subject ', max_length=100, required=True)
    message = RichTextFormField(label='Message')
    