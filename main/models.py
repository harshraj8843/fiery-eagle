from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import random
from ckeditor.fields import RichTextField

class backup(models.Model):
    date_day = models.IntegerField(default=0)
    date_month = models.IntegerField(default=0)
    date_year = models.IntegerField(default=0)
    sent = models.BooleanField(default=0)

class contact(models.Model):
    user = models.ForeignKey('userdata', on_delete=models.CASCADE)
    subject = models.CharField(max_length=1000)
    time = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

class a_report(models.Model):
    answer = models.ForeignKey('answer_table', on_delete=models.CASCADE)
    user = models.ForeignKey('userdata', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=0)

class q_report(models.Model):
    question = models.ForeignKey('question_table', on_delete=models.CASCADE)
    user = models.ForeignKey('userdata', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=0)

class a_upvote(models.Model):
    answer = models.ForeignKey('answer_table', on_delete=models.CASCADE)
    user = models.ForeignKey('userdata', on_delete=models.CASCADE)

class q_upvote(models.Model):
    question = models.ForeignKey('question_table', on_delete=models.CASCADE)
    user = models.ForeignKey('userdata', on_delete=models.CASCADE)

class question_tag(models.Model):
    question = models.ForeignKey('question_table', on_delete=models.CASCADE)
    tag = models.ForeignKey('tag', on_delete=models.CASCADE)

class tag(models.Model):
    title = models.CharField(max_length=50)

class answer_comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('userdata', on_delete=models.CASCADE)
    answer = models.ForeignKey('answer_table', on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    seen = models.BooleanField(default=0)

class question_comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('userdata', on_delete=models.CASCADE)
    question = models.ForeignKey('question_table', on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    seen = models.BooleanField(default=0)

class answer_table(models.Model):
    answer_id = models.AutoField(primary_key=True)
    question = models.ForeignKey('question_table', on_delete=models.CASCADE)
    user = models.ForeignKey('userdata', on_delete=models.CASCADE)
    description = RichTextField(blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
    upvote = models.IntegerField(default=0)
    seen = models.BooleanField(default=0)
    admin_seen = models.BooleanField(default=0)

class question_table(models.Model):
    question_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('userdata', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = RichTextField(blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
    upvote = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    admin_seen = models.BooleanField(default=0)

class userdata(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    question = models.IntegerField(default=0)
    answer = models.IntegerField(default=0)
    points = models.IntegerField(default=5)
    image = models.ImageField(upload_to="user", blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        userdata.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    x = random.randint(1,3)
    name = '../static/user/user'+str(x)+'.png'
    instance.userdata.image = name
    instance.userdata.save()

class email_subscribe(models.Model):
    email = models.EmailField(max_length=254)

class total_site_visit(models.Model):
    number = models.IntegerField(default=0)
    
class today_site_visit(models.Model):
    date_day = models.IntegerField(default=0)
    date_month = models.IntegerField(default=0)
    date_year = models.IntegerField(default=0)
    number = models.IntegerField(default=1)

class monthly_site_visit(models.Model):
    date_month = models.IntegerField()
    date_year = models.IntegerField()
    number = models.IntegerField(default=1)
    
class question_count(models.Model):
    number = models.IntegerField(default=0)

class answer_count(models.Model):
    number = models.IntegerField(default=0)

class today_question_count(models.Model):
    date_day = models.IntegerField(default=0)
    date_month = models.IntegerField(default=0)
    date_year = models.IntegerField(default=0)
    number = models.IntegerField(default=0)
    
class today_answer_count(models.Model):
    date_day = models.IntegerField(default=0)
    date_month = models.IntegerField(default=0)
    date_year = models.IntegerField(default=0)
    number = models.IntegerField(default=0)