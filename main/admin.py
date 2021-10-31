from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.total_site_visit)
admin.site.register(models.today_site_visit)
admin.site.register(models.monthly_site_visit)
admin.site.register(models.question_count)
admin.site.register(models.today_question_count)
admin.site.register(models.answer_count)
admin.site.register(models.today_answer_count)
admin.site.register(models.userdata)
admin.site.register(models.email_subscribe)
admin.site.register(models.tag)
admin.site.register(models.question_table)
admin.site.register(models.question_comment)
admin.site.register(models.question_tag)
admin.site.register(models.q_upvote)
admin.site.register(models.q_report)
admin.site.register(models.answer_table)
admin.site.register(models.answer_comment)
admin.site.register(models.a_upvote)
admin.site.register(models.a_report)