from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.views import View
import datetime
from django.utils import timezone

from django.template import loader
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage

from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from django.utils.html import strip_tags

from .models import total_site_visit, today_site_visit, monthly_site_visit, question_count, answer_count, today_question_count, today_answer_count, email_subscribe
from .models import question_table,userdata,answer_table,q_upvote,a_upvote,q_report,a_report,question_comment,answer_comment
from .models import question_tag,tag,contact
from .forms import post_question_form, post_answer_form, comment_form, contact_form,q_report_action_form,a_report_action_form,email_form

class admin_message_read(View):
    def get(self, request, message_id):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if user.is_superuser == False:
            return HttpResponse('<h1>You are not authorised to this page.</h1>')
        else:
            username = User.objects.get(id=user_id).username
            image = userdata.objects.get(user_id=user_id).image
            contact_count = contact.objects.filter(seen=False).count()
            question = q_report.objects.filter(seen=False).count()
            answer = a_report.objects.filter(seen=False).count()
            a_notification = answer_table.objects.filter(admin_seen=False).count()
            q_notification = question_table.objects.filter(admin_seen=False).count()
            notification = a_notification + q_notification
            datas = {
                'username': username,
                'image': image,
                'c_count': contact_count,
                'a_notification': a_notification,
                'q_notification': q_notification,
                'notification' : notification
            }
            user_id = contact.objects.get(id=message_id).user_id
            username = User.objects.get(id=user_id).username
            time = contact.objects.get(id=message_id).time
            time = str(time).split(' ')
            time = time[0]
            subject = contact.objects.get(id=message_id).subject
            data = contact.objects.get(id=message_id)
            data.seen = True
            data.save()
            datas1 = {
                'username': username,
                'time': time,
                'subject': subject
            }
            return render(request, 'admin-message-read.html', {
                'datas': datas,
                'datas1': datas1
            })
    
    def post(self, request, message_id):
        return redirect('/forum/admin/message')

class admin_message(View):
    def get(self, request):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if user.is_superuser == False:
            return HttpResponse('<h1>You are not authorised to this page.</h1>')
        else:
            username = User.objects.get(id=user_id).username
            image = userdata.objects.get(user_id=user_id).image
            contact_count = contact.objects.filter(seen=False).count()
            question = q_report.objects.filter(seen=False).count()
            answer = a_report.objects.filter(seen=False).count()
            a_notification = answer_table.objects.filter(admin_seen=False).count()
            q_notification = question_table.objects.filter(admin_seen=False).count()
            notification = a_notification + q_notification
            datas = {
                'username': username,
                'image': image,
                'c_count': contact_count,
                'a_notification': a_notification,
                'q_notification': q_notification,
                'notification' : notification
            }
            messages = contact.objects.order_by('seen')
            datas1 = list()
            for message in messages:
                message_id = message.id
                user_id = message.user_id
                username = User.objects.get(id=user_id).username
                if message.seen == True:
                    datas1.append({
                        'seen': True,
                        'message_id': message_id,
                        'username': username
                    })
                else:
                    datas1.append({
                        'message_id': message_id,
                        'username': username
                    })
            return render(request, 'admin-message.html', {
                'datas': datas,
                'datas1': datas1
            })

class admin_email(View):
    def get(self, request):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if user.is_superuser == False:
            return HttpResponse('<h1>You are not authorised to this page.</h1>')
        else:
            username = User.objects.get(id=user_id).username
            image = userdata.objects.get(user_id=user_id).image
            contact_count = contact.objects.filter(seen=False).count()
            question = q_report.objects.filter(seen=False).count()
            answer = a_report.objects.filter(seen=False).count()
            a_notification = answer_table.objects.filter(admin_seen=False).count()
            q_notification = question_table.objects.filter(admin_seen=False).count()
            notification = a_notification + q_notification
            datas = {
                'username': username,
                'image': image,
                'c_count': contact_count,
                'a_notification': a_notification,
                'q_notification': q_notification,
                'notification' : notification
            }
            form = email_form()
            return render(request, 'admin-email.html', {
                'datas': datas,
                'form': form
            })
    def post(self, request):
        form = email_form(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            user = form['user']
            if int(user) == 0:
                users = User.objects.all()
                email = list()
                for item in users:
                    if len(item.email)>0:
                        email.append(item.email)
                    else:
                        pass
            else:
                email = User.objects.get(id=user).email
                email = [email,]
            subject = form['subject']
            message = form['message']
            email_from = settings.EMAIL_HOST_USER
            
            html_message = loader.render_to_string('email.html', {
                    'message':  message
                })
            send_mail( subject, message, email_from, email,fail_silently=True,html_message=html_message) 
        return HttpResponse('OK')

class admin_notification_answer(View):
    def get(self, request):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if user.is_superuser == False:
            return HttpResponse('<h1>You are not authorised to this page.</h1>')
        else:
            username = User.objects.get(id=user_id).username
            image = userdata.objects.get(user_id=user_id).image
            contact_count = contact.objects.filter(seen=False).count()
            question = q_report.objects.filter(seen=False).count()
            answer = a_report.objects.filter(seen=False).count()
            a_notification = answer_table.objects.filter(admin_seen=False).count()
            q_notification = question_table.objects.filter(admin_seen=False).count()
            notification = a_notification + q_notification
            datas = {
                'username': username,
                'image': image,
                'c_count': contact_count,
                'a_notification': a_notification,
                'q_notification': q_notification,
                'notification' : notification
            }
            answers = answer_table.objects.order_by('admin_seen')
            datas1 = list()
            for answer in answers:
                question_id = answer.question_id
                user_id = answer.user_id
                username = User.objects.get(id=user_id).username
                if answer.admin_seen == True:
                    datas1.append({
                        'seen': True,
                        'username': username,
                        'question_id': question_id
                    })
                else:
                    datas1.append({
                        'username': username,
                        'question_id': question_id
                    })
                answer.admin_seen = True
                answer.save()
            return render(request, 'admin-a-notification.html', {
                'datas': datas,
                'datas1': datas1
            })

class admin_notification_question(View):
    def get(self, request):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if user.is_superuser == False:
            return HttpResponse('<h1>You are not authorised to this page.</h1>')
        else:
            username = User.objects.get(id=user_id).username
            image = userdata.objects.get(user_id=user_id).image
            contact_count = contact.objects.filter(seen=False).count()
            question = q_report.objects.filter(seen=False).count()
            answer = a_report.objects.filter(seen=False).count()
            a_notification = answer_table.objects.filter(admin_seen=False).count()
            q_notification = question_table.objects.filter(admin_seen=False).count()
            notification = a_notification + q_notification
            datas = {
                'username': username,
                'image': image,
                'c_count': contact_count,
                'a_notification': a_notification,
                'q_notification': q_notification,
                'notification' : notification
            }
            questions = question_table.objects.order_by('admin_seen')
            datas1 = list()
            for question in questions:
                question_id = question.question_id
                user_id = question.user_id
                username = User.objects.get(id=user_id).username
                if question.admin_seen == True:
                    datas1.append({
                        'seen': True,
                        'username': username,
                        'question_id': question_id
                    })
                else:
                    datas1.append({
                        'username': username,
                        'question_id': question_id
                    })
                question.admin_seen = True
                question.save()
            return render(request, 'admin-q-notification.html', {
                'datas': datas,
                'datas1': datas1
            })

class admin_report_answer_action(View):
    def get(self, request, report_id):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if user.is_superuser == False:
            return HttpResponse('<h1>You are not authorised to this page.</h1>')
        else:
            username = User.objects.get(id=user_id).username
            image = userdata.objects.get(user_id=user_id).image
            contact_count = contact.objects.filter(seen=False).count()
            question = q_report.objects.filter(seen=False).count()
            answer = a_report.objects.filter(seen=False).count()
            a_notification = answer_table.objects.filter(admin_seen=False).count()
            q_notification = question_table.objects.filter(admin_seen=False).count()
            notification = a_notification + q_notification
            datas = {
                'username': username,
                'image': image,
                'c_count': contact_count,
                'a_notification': a_notification,
                'q_notification': q_notification,
                'notification' : notification
            }
            answer_id = a_report.objects.get(id=report_id).answer_id
            question_id = answer_table.objects.get(answer_id=answer_id).question_id
            question_title = question_table.objects.get(question_id=question_id).title
            question_desc = question_table.objects.get(question_id=question_id).description
            answer_desc = answer_table.objects.get(answer_id=answer_id).description
            datas1={
                'question_title': question_title,
                'question_desc': question_desc,
                'answer_desc': answer_desc
            }
            form = a_report_action_form()
            return render(request, 'admin-a-report-action.html', {
                'datas': datas,
                'datas1': datas1,
                'form': form
            })
    
    def post(self, request, report_id):
        answer_id = a_report.objects.get(id=report_id).answer_id
        form = a_report_action_form(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            if form['delete'] == True and form['action'] == False:
                data = a_report.objects.get(id=report_id).delete()
            elif form['delete'] == True and form['action'] == True:
                data = a_report.objects.get(id=report_id).delete()
                data = answer_table.objects.get(answer_id=answer_id).delete()
            elif form['delete'] == False and form['action'] == True:
                data = a_report.objects.get(id=report_id).delete()
                data = answer_table.objects.get(answer_id=answer_id).delete()
        return redirect('/forum/admin/report/answer')

class admin_report_answer(View):
    def get(self, request):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if user.is_superuser == False:
            return HttpResponse('<h1>You are not authorised to this page.</h1>')
        else:
            username = User.objects.get(id=user_id).username
            image = userdata.objects.get(user_id=user_id).image
            contact_count = contact.objects.filter(seen=False).count()
            question = q_report.objects.filter(seen=False).count()
            answer = a_report.objects.filter(seen=False).count()
            a_notification = answer_table.objects.filter(admin_seen=False).count()
            q_notification = question_table.objects.filter(admin_seen=False).count()
            notification = a_notification + q_notification
            datas = {
                'username': username,
                'image': image,
                'c_count': contact_count,
                'a_notification': a_notification,
                'q_notification': q_notification,
                'notification' : notification
            }
            answers = a_report.objects.order_by('seen')
            datas1 = list()
            for answer in answers:
                answer_id = answer.answer_id
                report_id = answer.id
                question_id = answer_table.objects.get(answer_id=answer_id).question_id
                question_title = question_table.objects.get(question_id=question_id).title
                seen = a_report.objects.get(id=report_id).seen
                if seen == True:
                    datas1.append({
                        'seen': seen,
                        'report_id': report_id,
                        'question_title': question_title
                    })
                else:
                    datas1.append({
                        'report_id': report_id,
                        'question_title': question_title
                    })
            return render(request, 'admin-a-report.html', {
                'datas': datas,
                'datas1': datas1
            })

class admin_report_question_action(View):
    def get(self, request, report_id):
        question_id = q_report.objects.get(id=report_id).question_id
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if user.is_superuser == False:
            return HttpResponse('<h1>You are not authorised to this page.</h1>')
        else:
            username = User.objects.get(id=user_id).username
            image = userdata.objects.get(user_id=user_id).image
            contact_count = contact.objects.filter(seen=False).count()
            question = q_report.objects.filter(seen=False).count()
            answer = a_report.objects.filter(seen=False).count()
            a_notification = answer_table.objects.filter(admin_seen=False).count()
            q_notification = question_table.objects.filter(admin_seen=False).count()
            notification = a_notification + q_notification
            datas = {
                'username': username,
                'image': image,
                'c_count': contact_count,
                'a_notification': a_notification,
                'q_notification': q_notification,
                'notification' : notification
            }
            question_title = question_table.objects.get(question_id=question_id).title
            question_desc = question_table.objects.get(question_id=question_id).description
            datas1={
                'question_title': question_title,
                'question_desc': question_desc
            }
            data = q_report.objects.get(id=report_id)
            data.seen = True
            data.save()
            form = q_report_action_form()
            return render(request, 'admin-q-report-action.html', {
                'datas': datas,
                'datas1': datas1,
                'form': form
            })
    
    def post(self, request, report_id):
        form = q_report_action_form(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            if form['delete'] == True and form['action'] == False:
                data = q_report.objects.get(id=report_id).delete()
            elif form['delete'] == True and form['action'] == True:
                question_id = q_report.objects.get(id=report_id).question_id
                data = q_report.objects.get(id=report_id).delete()
                data = question_table.objects.get(question_id=question_id).delete()
            elif form['delete'] == False and form['action'] == True:
                question_id = q_report.objects.get(id=report_id).question_id
                data = q_report.objects.get(id=report_id).delete()
                data = question_table.objects.get(question_id=question_id).delete()
        return redirect('/forum/admin/report/question')

class admin_report_question(View):
    def get(self, request):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if user.is_superuser == False:
            return HttpResponse('<h1>You are not authorised to this page.</h1>')
        else:
            username = User.objects.get(id=user_id).username
            image = userdata.objects.get(user_id=user_id).image
            contact_count = contact.objects.filter(seen=False).count()
            question = q_report.objects.filter(seen=False).count()
            answer = a_report.objects.filter(seen=False).count()
            a_notification = answer_table.objects.filter(admin_seen=False).count()
            q_notification = question_table.objects.filter(admin_seen=False).count()
            notification = a_notification + q_notification
            datas = {
                'username': username,
                'image': image,
                'c_count': contact_count,
                'a_notification': a_notification,
                'q_notification': q_notification,
                'notification' : notification
            }
            questions = q_report.objects.order_by('seen')
            datas1 = list()
            for question in questions:
                question_id = question.question_id
                report_id = question.id
                question_title = question_table.objects.get(question_id=question_id).title
                seen = q_report.objects.get(id=report_id).seen
                if seen == True:
                    datas1.append({
                        'seen': seen,
                        'report_id': report_id,
                        'question_title': question_title
                    })
                else:
                    datas1.append({
                        'report_id': report_id,
                        'question_title': question_title
                    })
            return render(request, 'admin-q-report.html', {
                'datas': datas,
                'datas1': datas1
            })

class admin_tags(View):
    def get(self, request):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if user.is_superuser == False:
            return HttpResponse('<h1>You are not authorised to this page.</h1>')
        else:
            username = User.objects.get(id=user_id).username
            image = userdata.objects.get(user_id=user_id).image
            contact_count = contact.objects.filter(seen=False).count()
            question = q_report.objects.filter(seen=False).count()
            answer = a_report.objects.filter(seen=False).count()
            a_notification = answer_table.objects.filter(admin_seen=False).count()
            q_notification = question_table.objects.filter(admin_seen=False).count()
            notification = a_notification + q_notification
            datas = {
                'username': username,
                'image': image,
                'c_count': contact_count,
                'a_notification': a_notification,
                'q_notification': q_notification,
                'notification' : notification
            }
            tags = tag.objects.all()
            datas1 = list()
            for item in tags:
                title = item.title
                question = question_tag.objects.filter(tag_id=item.id).count()
                datas1.append({
                    'tag_id': item.id,
                    'title': title,
                    'question': question
                })
            return render(request, 'admin-tags.html', {
                'datas': datas,
                'datas1': datas1
            })

class admin_question(View):
    def get(self, request):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if user.is_superuser == False:
            return HttpResponse('<h1>You are not authorised to this page.</h1>')
        else:
            username = User.objects.get(id=user_id).username
            image = userdata.objects.get(user_id=user_id).image
            contact_count = contact.objects.filter(seen=False).count()
            question = q_report.objects.filter(seen=False).count()
            answer = a_report.objects.filter(seen=False).count()
            a_notification = answer_table.objects.filter(admin_seen=False).count()
            q_notification = question_table.objects.filter(admin_seen=False).count()
            notification = a_notification + q_notification
            datas = {
                'username': username,
                'image': image,
                'c_count': contact_count,
                'a_notification': a_notification,
                'q_notification': q_notification,
                'notification' : notification
            }
            questions = question_table.objects.all()
            datas1 = list()
            for question in questions:
                question_id = question.question_id
                question_title = question.title
                answer = answer_table.objects.filter(question_id=question_id).count()
                datas1.append({
                    'question_id': question_id,
                    'question_title': question_title,
                    'answer': answer
                })
            return render(request, 'admin-question.html', {
                'datas': datas,
                'datas1': datas1
            })

class admin_user(View):
    def get(self, request):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if user.is_superuser == False:
            return HttpResponse('<h1>You are not authorised to this page.</h1>')
        else:
            username = User.objects.get(id=user_id).username
            image = userdata.objects.get(user_id=user_id).image
            contact_count = contact.objects.filter(seen=False).count()
            question = q_report.objects.filter(seen=False).count()
            answer = a_report.objects.filter(seen=False).count()
            a_notification = answer_table.objects.filter(admin_seen=False).count()
            q_notification = question_table.objects.filter(admin_seen=False).count()
            notification = a_notification + q_notification
            datas = {
                'username': username,
                'image': image,
                'c_count': contact_count,
                'a_notification': a_notification,
                'q_notification': q_notification,
                'notification' : notification
            }
            users = User.objects.all()
            datas1 = list()
            for user in users:
                user_id = user.id
                username = user.username
                user_image = userdata.objects.get(user_id=user_id).image
                user_points = userdata.objects.get(user_id=user_id).points
                datas1.append({
                    'user_id': user_id,
                    'username': username,
                    'user_image': user_image,
                    'user_points': user_points
                })
            return render(request, 'admin-user.html', {
                'datas': datas,
                'datas1': datas1
            })

class admin_dashboard(View):
    def get(self, request):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if user.is_superuser == False:
            return HttpResponse('<h1>You are not authorised to this page.</h1>')
        else:
            username = User.objects.get(id=user_id).username
            image = userdata.objects.get(user_id=user_id).image
            contact_count = contact.objects.filter(seen=False).count()
            question = q_report.objects.filter(seen=False).count()
            answer = a_report.objects.filter(seen=False).count()
            a_notification = answer_table.objects.filter(admin_seen=False).count()
            q_notification = question_table.objects.filter(admin_seen=False).count()
            notification = a_notification + q_notification
            datas = {
                'username': username,
                'image': image,
                'c_count': contact_count,
                'a_notification': a_notification,
                'q_notification': q_notification,
                'notification' : notification
            }
            report = question+answer
            return render(request, 'admin-dashboard.html', {
                'datas': datas,
                'report': report
            })

class contact_us(View):
    def get(self, request):
        form = contact_form()
        return render(request, 'contact-us.html', {
            'form': form
        })
    
    def post(self, request):
        form = contact_form(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            user_id = request.user.id
            subject = form['subject']
            data = contact()
            data.user_id = user_id
            data.subject = subject
            data.save()
            return render(request, 'posted.html')

class user_a_notification(View):
    def get(self, request, user_id):
        datas3 = list()
        datas4 = list()
        datas5 = list()
        questions = question_table.objects.filter(user_id=user_id)
        for question in questions:
            try:
                data = answer_table.objects.get(question_id=question.question_id, seen=False)
                username = User.objects.get(id=data.user_id).username
                datas3.append({
                    'username': username,
                    'question_id': data.question_id
                })
            except:
                pass
        for question in questions:
            comments = question_comment.objects.filter(question_id=question.question_id, seen=False)
            for comment in comments:
                username = User.objects.get(id=comment.user_id).username
                datas4.append({
                    'username': username,
                    'question_id': comment.question_id
                })
        answers = answer_table.objects.filter(user_id=user_id)
        for answer in answers:
            try:
                comments = answer_comment.objects.filter(answer_id=answer.answer_id)
                for comment in comments:
                    username = User.objects.get(id=comment.user_id).username
                    if comment.seen == True:
                        pass
                    else:
                        datas5.append({
                            'answer_id': comment.answer_id,
                            'username': username
                        })
            except:
                pass
        username1 = User.objects.get(id=user_id).username
        image = userdata.objects.get(user_id=user_id).image
        datas = list()
        answers = answer_table.objects.filter(user_id=user_id)
        for answer in answers:
            try:
                comments = answer_comment.objects.filter(answer_id=answer.answer_id)
                for comment in comments:
                    username = User.objects.get(id=comment.user_id).username
                    if username == request.user.username:
                        username = 'you'
                    if comment.seen == True:
                        datas.append({
                            'seen': comment.seen,
                            'answer_id': comment.answer_id,
                            'username': username
                        })
                    else:
                        datas.append({
                            'answer_id': comment.answer_id,
                            'username': username
                        })
                        comment.seen = True
                        comment.save()
            except:
                pass
        return render(request, 'user-a-notification.html', {
            'username': username1,
            'image': image,
            'n_total': len(datas3)+len(datas4)+len(datas5),
            'q_total': len(datas3),
            'a_total': len(datas5),
            'c_total': len(datas4),
            'datas': datas
        })

class user_q_notification(View):
    def get(self, request, user_id):
        datas3 = list()
        datas4 = list()
        datas5 = list()
        questions = question_table.objects.filter(user_id=user_id)
        for question in questions:
            try:
                data = answer_table.objects.get(question_id=question.question_id, seen=False)
                username = User.objects.get(id=data.user_id).username
                datas3.append({
                    'username': username,
                    'question_id': data.question_id
                })
            except:
                pass
        for question in questions:
            comments = question_comment.objects.filter(question_id=question.question_id, seen=False)
            for comment in comments:
                username = User.objects.get(id=comment.user_id).username
                datas4.append({
                    'username': username,
                    'question_id': comment.question_id
                })
        answers = answer_table.objects.filter(user_id=user_id)
        for answer in answers:
            try:
                comments = answer_comment.objects.filter(answer_id=answer.answer_id)
                for comment in comments:
                    username = User.objects.get(id=comment.user_id).username
                    if comment.seen == True:
                        pass
                    else:
                        datas5.append({
                            'answer_id': comment.answer_id,
                            'username': username
                        })
            except:
                pass
        username1 = User.objects.get(id=user_id).username
        image = userdata.objects.get(user_id=user_id).image
        datas1 = list()
        datas2 = list()
        questions = question_table.objects.filter(user_id=user_id)
        for question in questions:
            try:
                data = answer_table.objects.get(question_id=question.question_id, seen=False)
                username = User.objects.get(id=data.user_id).username
                if username == request.user.username :
                    username = 'you'
                else:
                    username = User.objects.get(id=data.user_id).username
                datas1.append({
                    'username': username,
                    'question_id': data.question_id
                })
                data.seen = True
                data.save()
            except:
                pass
        for question in questions:
            comments = question_comment.objects.filter(question_id=question.question_id, seen=False)
            for comment in comments:
                username = User.objects.get(id=comment.user_id).username
                if username == request.user.username :
                    username = 'you'
                else:
                    username = User.objects.get(id=comment.user_id).username
                datas2.append({
                    'username': username,
                    'question_id': comment.question_id
                })
                comment.seen = True
                comment.save()
        return render(request, 'user-q-notification.html', {
            'username': username1,
            'image': image,
            'n_total': len(datas3)+len(datas4)+len(datas5),
            'q_total': len(datas3),
            'a_total': len(datas5),
            'c_total': len(datas4),
            'datas1': datas1,
            'datas2': datas2
        })

class user_question(View):
    def get(self, request, user_id):
        datas3 = list()
        datas4 = list()
        datas5 = list()
        questions = question_table.objects.filter(user_id=user_id)
        for question in questions:
            try:
                data = answer_table.objects.get(question_id=question.question_id, seen=False)
                username = User.objects.get(id=data.user_id).username
                datas3.append({
                    'username': username,
                    'question_id': data.question_id
                })
            except:
                pass
        for question in questions:
            comments = question_comment.objects.filter(question_id=question.question_id, seen=False)
            for comment in comments:
                username = User.objects.get(id=comment.user_id).username
                datas4.append({
                    'username': username,
                    'question_id': comment.question_id
                })
        answers = answer_table.objects.filter(user_id=user_id)
        for answer in answers:
            try:
                comments = answer_comment.objects.filter(answer_id=answer.answer_id)
                for comment in comments:
                    username = User.objects.get(id=comment.user_id).username
                    if comment.seen == True:
                        pass
                    else:
                        datas5.append({
                            'answer_id': comment.answer_id,
                            'username': username
                        })
            except:
                pass
        username1 = User.objects.get(id=user_id).username
        image = userdata.objects.get(user_id=user_id).image
        questions = question_table.objects.filter(user_id=user_id)
        datas = list()
        for question in questions:
            answer = answer_table.objects.filter(question_id=question.question_id).count()
            datas.append({
                'question_id': question.question_id,
                'question': question.title,
                'answer': answer
            })
        return render(request, 'user-questions.html', {
            'username': username1, 
            'image': image,
            'n_total': len(datas3)+len(datas4)+len(datas5),
            'q_total': len(datas3),
            'a_total': len(datas5),
            'c_total': len(datas4),
            'datas': datas
            })

class user_profile(View):
    def get(self, request, user_id):
        datas3 = list()
        datas4 = list()
        datas5 = list()
        questions = question_table.objects.filter(user_id=user_id)
        for question in questions:
            try:
                data = answer_table.objects.get(question_id=question.question_id, seen=False)
                username = User.objects.get(id=data.user_id).username
                datas3.append({
                    'username': username,
                    'question_id': data.question_id
                })
            except:
                pass
        for question in questions:
            comments = question_comment.objects.filter(question_id=question.question_id, seen=False)
            for comment in comments:
                username = User.objects.get(id=comment.user_id).username
                datas4.append({
                    'username': username,
                    'question_id': comment.question_id
                })
        answers = answer_table.objects.filter(user_id=user_id)
        for answer in answers:
            try:
                comments = answer_comment.objects.filter(answer_id=answer.answer_id)
                for comment in comments:
                    username = User.objects.get(id=comment.user_id).username
                    if comment.seen == True:
                        pass
                    else:
                        datas5.append({
                            'answer_id': comment.answer_id,
                            'username': username
                        })
            except:
                pass
        username1 = User.objects.get(id=user_id).username
        email = User.objects.get(id=user_id).email
        points = userdata.objects.get(user_id=user_id).points
        image = userdata.objects.get(user_id=user_id).image
        question = question_table.objects.filter(user_id=user_id).count()
        answer = answer_table.objects.filter(user_id=user_id).count()
        user_joined = User.objects.get(id=user_id).date_joined
        user_joined = str(user_joined).split(' ')
        user_joined = user_joined[0]
        data = {
            'username': username1,
            'email': email,
            'points': points,
            'image': image,
            'question': question,
            'answer': answer,
            'joined': user_joined
        }
        return render(request, 'user-dashboard.html', {
            'n_total': len(datas3)+len(datas4)+len(datas5),
            'q_total': len(datas3),
            'a_total': len(datas5),
            'c_total': len(datas4),
            'data': data
            })

class top(View):
    def __init__(self):
        data_update()
        
    def get(self, request):
        users = userdata.objects.order_by('-points')
        datas = list()
        for user in users:
            user_image = userdata.objects.get(user_id=user.user_id).image
            username = User.objects.get(id=user.user_id).username
            user_points = userdata.objects.get(user_id=user.user_id).points
            datas.append({
                'user_image':user_image,
                'username': username,
                'user_points': user_points,
                'user_id': user.user_id
            })
        return render(request, 'top.html', {'datas': datas})

class profile(View):
    def __init__(self):
        data_update()
        
    def get(self, request, user_id):
        username = User.objects.get(id=user_id).username
        user_joined = User.objects.get(id=user_id).date_joined
        user_joined = str(user_joined).split(' ')
        user_joined = user_joined[0]
        user_points = userdata.objects.get(user_id=user_id).points
        user_question = question_table.objects.filter(user_id=user_id).count()
        user_answer = answer_table.objects.filter(user_id=user_id).count()
        userdatas = {
            'username': username,
            'user_joined': user_joined,
            'user_points': user_points,
            'user_question': user_question,
            'user_answer': user_answer
        }
        return render(request, 'profile.html', {'userdata': userdatas})

class comment_a(View):
    def __init__(self):
        data_update()
        
    def get(self, request, answer_id):
        form = comment_form()
        return render(request, 'user_comment.html', {'form': form})
    
    def post(self, request, answer_id):
        description = request.POST.get('comment')
        if description=='':
            pass
        else:
            user_id = request.user.id
            data = answer_comment()
            data.user_id = user_id
            data.answer_id = answer_id
            data.description = description
            data.save()
        return render(request, 'posted.html')

class comment_q(View):
    def __init__(self):
        data_update()
        
    def get(self, request, question_id):
        form = comment_form()
        return render(request, 'user_comment.html', {'form': form})
    
    def post(self, request, question_id):
        description = request.POST.get('comment')
        if description=='':
            pass
        else:
            user_id = request.user.id
            data = question_comment()
            data.user_id = user_id
            data.question_id = question_id
            data.description = description
            data.save()
        return render(request, 'posted.html')

class answer_comments(View):
    def __init__(self):
        data_update()
        
    def get(self, request, answer_id):
        comments = answer_comment.objects.filter(answer_id=answer_id)
        commentdata = list()
        for comment in comments:
            user_id = answer_comment.objects.get(comment_id=comment.comment_id).user_id
            user_image = userdata.objects.get(user_id=user_id).image
            username = User.objects.get(id=user_id).username
            desc = comment.description
            commentdata.append({
                'user_id': user_id,
                'user_image': user_image,
                'username': username,
                'description': desc
            })
        return render(request, 'comment.html', {'answer_id': answer_id, 'commentdatas': commentdata})

class question_comments(View):
    def __init__(self):
        data_update()
        
    def get(self, request, question_id):
        question_title = question_table.objects.get(question_id=question_id).title
        comments = question_comment.objects.filter(question_id=question_id)
        commentdata = list()
        for comment in comments:
            user_id = question_comment.objects.get(comment_id=comment.comment_id).user_id
            user_image = userdata.objects.get(user_id=user_id).image
            username = User.objects.get(id=user_id).username
            desc = comment.description
            commentdata.append({
                'user_id': user_id,
                'user_image': user_image,
                'username': username,
                'description': desc
            })
        return render(request, 'comment.html', {'question_id': question_id, 'question_title': question_title, 'commentdatas': commentdata})

class answer_report(View):
    def __init__(self):
        data_update()
        
    def get(self, request, answer_id):
        user_id =request.user.id
        try:
            data = a_report.objects.get(answer_id=answer_id, user_id=user_id)
        except:
            data = a_report()
            data.answer_id = answer_id
            data.user_id = user_id
            data.save()
        return render(request, 'posted.html')

class question_report(View):
    def __init__(self):
        data_update()
        
    def get(self, request, question_id):
        user_id =request.user.id
        try:
            data = q_report.objects.get(question_id=question_id, user_id=user_id)
        except:
            data = q_report()
            data.question_id = question_id
            data.user_id = user_id
            data.save()
        return render(request, 'posted.html')

class post_answer(View):
    def __init__(self):
        data_update()
        
    def get(self, request, question_id):
        form = post_answer_form()
        user_id = question_table.objects.get(question_id=question_id).user_id
        username = User.objects.get(id=user_id).username
        user_joined = User.objects.get(id=user_id).date_joined
        user_joined = str(user_joined).split(' ')
        user_joined = user_joined[0]
        user_image = userdata.objects.get(user_id=user_id).image
        user_points = userdata.objects.get(user_id=user_id).points
        question_title = question_table.objects.get(question_id=question_id).title
        question_time = question_table.objects.get(question_id=question_id).time
        question_time = timezone.now() - question_time
        question_time = str(question_time).split(',')
        q_day = 0
        if len(question_time) > 1:
            q_day = str(question_time[0]).split(' ')
            q_day = q_day[0]
            question_time = str(question_time[1]).split('.')
            question_time = question_time[0]
            question_time = str(question_time).split(':')
            day = q_day
            hour = int(question_time[0])
            minute = int(question_time[1])
            second = int(question_time[2])
        else:
            question_time = str(question_time[0]).split('.')
            question_time = question_time[0]
            question_time = str(question_time).split(':')
            day = q_day
            hour = int(question_time[0])
            minute = int(question_time[1])
            second = int(question_time[2])
        question_time_day = day
        question_time_hour  =hour
        question_time_minute = minute
        question_time_second = second
        question_upvote = question_table.objects.get(question_id=question_id).upvote
        question_desc = question_table.objects.get(question_id=question_id).description
        question_tags = question_tag.objects.filter(question_id=question_id)
        tags = list()
        for item in question_tags:
            item = tag.objects.get(id=item.tag_id).title
            tags.append(item)
        questiondata={
            'user_id': user_id,
            'username': username,
            'user_joined': user_joined,
            'user_image':user_image,
            'user_points':user_points,
            'question_id': question_id,
            'question_title':question_title,
            'question_time_day':int(question_time_day),
            'question_time_hour':int(question_time_hour),
            'question_time_minute':int(question_time_minute),
            'question_time_second':int(question_time_second),
            'question_upvote':question_upvote,
            'question_tags': tags,
            'question_desc': question_desc
        }
        return render(request, 'post-answer.html', {'form': form, 'questiondata': questiondata})
    
    def post(self, request, question_id):
        answer = request.POST.get('answer')
        user_id =request.user.id
        try:
            data1 = answer_table.objects.get(user_id=user_id, description=answer)
        except:
            data1 = answer_table()
            data1.user_id = user_id
            data1.question_id = question_id
            data1.description = answer
            data1.save()
            data2 = answer_count.objects.get(id=1)
            data2.number +=1
            data2.save()
            today = datetime.date.today()
            try:
                data3 = today_answer_count.objects.get(date_day=today.day, date_month=today.month, date_year=today.year)
                data3.number +=1
                data3.save()
            except:
                data3 = today_answer_count()
                data3.date_day = today.day
                data3.date_month = today.month
                data3.date_year = today.year
                data3.save()
            data4 = userdata.objects.get(user_id=user_id)
            data4.points +=20
            data4.save()
        return render(request, 'posted.html')

class answer_upvote(View):
    def __init__(self):
        data_update()
        
    def get(self, request, answer_id):
        user_id = request.user.id
        try:
            data = a_upvote.objects.get(user_id=user_id,answer_id=answer_id)
        except:
            upvote0 = answer_table.objects.get(answer_id=answer_id)
            upvote0.upvote +=1
            upvote0.save()
            upvote1 = a_upvote()
            upvote1.user_id = userdata.objects.get(user_id=user_id).user_id
            upvote1.answer_id = answer_table.objects.get(answer_id=answer_id).answer_id
            upvote1.save()
            data = userdata.objects.get(user_id=user_id)
            data.points +=5
            data.save()
            id = answer_table.objects.get(answer_id=answer_id).user_id
            data = userdata.objects.get(user_id=id)
            data.points +=10
            data.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

class question_upvote(View):
    def __init__(self):
        data_update()
        
    def get(self, request, question_id):
        user_id = request.user.id
        try:
            data = q_upvote.objects.get(user_id=user_id, question_id=question_id)
        except:
            upvote0 = question_table.objects.get(question_id=question_id)
            upvote0.upvote +=1
            upvote0.save()
            upvote1 = q_upvote()
            upvote1.user_id = userdata.objects.get(user_id=user_id).user_id
            upvote1.question_id = question_table.objects.get(question_id=question_id).question_id
            upvote1.save()
            data = userdata.objects.get(user_id=user_id)
            data.points +=5
            data.save()
            id = question_table.objects.get(question_id=question_id).user_id
            data = userdata.objects.get(user_id=id)
            data.points +=10
            data.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        
class question(View):
    def __init__(self):
        data_update()
        
    def get(self, request, question_id):
        q_view = question_table.objects.get(question_id=question_id)
        q_view.views +=1
        q_view.save()
        
        user_id = question_table.objects.get(question_id=question_id).user_id
        username = User.objects.get(id=user_id).username
        user_joined = User.objects.get(id=user_id).date_joined
        user_joined = str(user_joined).split(' ')
        user_joined = user_joined[0]
        user_image = userdata.objects.get(user_id=user_id).image
        user_points = userdata.objects.get(user_id=user_id).points
        question_title = question_table.objects.get(question_id=question_id).title
        question_time = question_table.objects.get(question_id=question_id).time
        question_time = timezone.now() - question_time
        question_time = str(question_time).split(',')
        q_day = 0
        if len(question_time) > 1:
            q_day = str(question_time[0]).split(' ')
            q_day = q_day[0]
            question_time = str(question_time[1]).split('.')
            question_time = question_time[0]
            question_time = str(question_time).split(':')
            day = q_day
            hour = int(question_time[0])
            minute = int(question_time[1])
            second = int(question_time[2])
        else:
            question_time = str(question_time[0]).split('.')
            question_time = question_time[0]
            question_time = str(question_time).split(':')
            day = q_day
            hour = int(question_time[0])
            minute = int(question_time[1])
            second = int(question_time[2])
        question_time_day = day
        question_time_hour  =hour
        question_time_minute = minute
        question_time_second = second
        question_upvote = question_table.objects.get(question_id=question_id).upvote
        question_desc = question_table.objects.get(question_id=question_id).description
        question_tags = question_tag.objects.filter(question_id=question_id)
        tags = list()
        for item in question_tags:
            item = tag.objects.get(id=item.tag_id).title
            tags.append(item)
        comment_count = question_comment.objects.filter(question_id=question_id).count()
        questiondata={
            'comment_count': comment_count,
            'user_id': user_id,
            'username': username,
            'user_joined': user_joined,
            'user_image':user_image,
            'user_points':user_points,
            'question_id': question_id,
            'question_title':question_title,
            'question_time_day':int(question_time_day),
            'question_time_hour':int(question_time_hour),
            'question_time_minute':int(question_time_minute),
            'question_time_second':int(question_time_second),
            'question_upvote':question_upvote,
            'question_tags': tags,
            'question_desc': question_desc
        }
        answers = answer_table.objects.filter(question_id=question_id).order_by('-upvote', '-time')
        answerdatas = list()
        for answer in answers:
            answer_id = answer.answer_id
            user_id = answer.user_id
            username = User.objects.get(id=user_id).username
            user_joined = User.objects.get(id=user_id).date_joined
            user_joined = str(user_joined).split(' ')
            user_joined = user_joined[0]
            user_image = userdata.objects.get(user_id=user_id).image
            user_points = userdata.objects.get(user_id=user_id).points
            answer_time = answer_table.objects.get(answer_id=answer_id).time
            answer_time = timezone.now() - answer_time
            answer_time = str(answer_time).split(',')
            q_day = 0
            if len(answer_time) > 1:
                q_day = str(answer_time[0]).split(' ')
                q_day = q_day[0]
                answer_time = str(answer_time[1]).split('.')
                answer_time = answer_time[0]
                answer_time = str(answer_time).split(':')
                day = q_day
                hour = int(answer_time[0])
                minute = int(answer_time[1])
                second = int(answer_time[2])
            else:
                answer_time = str(answer_time[0]).split('.')
                answer_time = answer_time[0]
                answer_time = str(answer_time).split(':')
                day = q_day
                hour = int(answer_time[0])
                minute = int(answer_time[1])
                second = int(answer_time[2])
            answer_time_day = day
            answer_time_hour  =hour
            answer_time_minute = minute
            answer_time_second = second
            answer_desc = answer_table.objects.get(answer_id=answer_id).description
            answer_upvote = answer_table.objects.get(answer_id=answer_id).upvote
            comment_count = answer_comment.objects.filter(answer_id=answer_id).count()
            answerdatas.append({
                'comment_count': comment_count,
                'user_id': user_id,
                'user_image': user_image,
                'username': username,
                'answer_id': answer_id,
                'answer_time_day': answer_time_day,
                'answer_time_hour': answer_time_hour,
                'answer_time_minute': answer_time_minute,
                'answer_time_second': answer_time_second,
                'user_joined': user_joined,
                'user_points': user_points,
                'answer_desc': answer_desc,
                'answer_upvote': answer_upvote
            })
        return render(request, 'question.html', {'questiondata': questiondata, 'answerdatas': answerdatas})

class tag_questions(View):
    def __init__(self):
        data_update()
        
    def get(self, request, tag_id):
        datas = list()
        q_id = question_tag.objects.filter(tag_id=tag_id)
        for id in q_id:
            question = question_table.objects.get(question_id=id.question_id)
            question_id = question.question_id
            user_id = question.user_id
            username = User.objects.get(id=user_id).username
            user_joined = User.objects.get(id=user_id).date_joined
            user_joined = str(user_joined).split(' ')
            user_joined = user_joined[0]
            user_image = userdata.objects.get(user_id=user_id).image
            user_points = userdata.objects.get(user_id=user_id).points
            question_title = question_table.objects.get(question_id=question_id).title
            question_time = question_table.objects.get(question_id=question_id).time
            question_time = timezone.now() - question_time
            question_time = str(question_time).split(',')
            q_day = 0
            if len(question_time) > 1:
                q_day = str(question_time[0]).split(' ')
                q_day = q_day[0]
                question_time = str(question_time[1]).split('.')
                question_time = question_time[0]
                question_time = str(question_time).split(':')
                day = q_day
                hour = int(question_time[0])
                minute = int(question_time[1])
                second = int(question_time[2])
            else:
                question_time = str(question_time[0]).split('.')
                question_time = question_time[0]
                question_time = str(question_time).split(':')
                day = q_day
                hour = int(question_time[0])
                minute = int(question_time[1])
                second = int(question_time[2])
            question_time_day = day
            question_time_hour  =hour
            question_time_minute = minute
            question_time_second = second
            question_view = question_table.objects.get(question_id=question_id).views
            question_upvote = question_table.objects.get(question_id=question_id).upvote
            question_answer = answer_table.objects.filter(question_id=question_id).count()
            question_tags = question_tag.objects.filter(question_id=question_id)
            tags = list()
            for item in question_tags:
                item = tag.objects.get(id=item.tag_id).title
                tags.append(item)
            datas.append({
                'user_id': user_id,
                'username': username,
                'user_joined': user_joined,
                'user_image':user_image,
                'user_points':user_points,
                'question_id': question_id,
                'question_title':question_title,
                'question_time_day':int(question_time_day),
                'question_time_hour':int(question_time_hour),
                'question_time_minute':int(question_time_minute),
                'question_time_second':int(question_time_second),
                'question_view':question_view,
                'question_upvote':question_upvote,
                'question_answer':question_answer,
                'question_tags': tags
            })            
        return render(request, 'forum-home.html',{'datas':datas, 'sort_title': 'tags'})

class forum_tags(View):
    def __init__(self):
        data_update()
    
    def get(self, request):
        tags = tag.objects.all()
        datas = list()
        for item in tags:
            tag_id = item.id
            q_count = question_tag.objects.filter(tag_id=tag_id).count()
            q_ids = question_tag.objects.filter(tag_id=tag_id)
            sum=0
            for q_id in q_ids:
                question_id = question_table.objects.get(question_id=q_id.question_id)
                sum += answer_table.objects.filter(question_id=question_id).count()
            datas.append({
                'tag_id': tag_id,
                'tag_title': item.title,
                'tag_question': q_count,
                'tag_answer': sum
            })        
        return render(request, 'forum-tags.html', {'datas': datas})

class forum(View):
    def __init__(self):
        data_update()
        
    def get(self, request):
        datas = list()
        questions = question_table.objects.order_by('-time')
        for question in questions:
            question_id = question.question_id
            user_id = question.user_id
            username = User.objects.get(id=user_id).username
            user_joined = User.objects.get(id=user_id).date_joined
            user_joined = str(user_joined).split(' ')
            user_joined = user_joined[0]
            user_image = userdata.objects.get(user_id=user_id).image
            user_points = userdata.objects.get(user_id=user_id).points
            question_title = question_table.objects.get(question_id=question_id).title
            question_time = question_table.objects.get(question_id=question_id).time
            question_time = timezone.now() - question_time
            question_time = str(question_time).split(',')
            q_day = 0
            if len(question_time) > 1:
                q_day = str(question_time[0]).split(' ')
                q_day = q_day[0]
                question_time = str(question_time[1]).split('.')
                question_time = question_time[0]
                question_time = str(question_time).split(':')
                day = q_day
                hour = int(question_time[0])
                minute = int(question_time[1])
                second = int(question_time[2])
            else:
                question_time = str(question_time[0]).split('.')
                question_time = question_time[0]
                question_time = str(question_time).split(':')
                day = q_day
                hour = int(question_time[0])
                minute = int(question_time[1])
                second = int(question_time[2])
            question_time_day = day
            question_time_hour  =hour
            question_time_minute = minute
            question_time_second = second
            question_view = question_table.objects.get(question_id=question_id).views
            question_upvote = question_table.objects.get(question_id=question_id).upvote
            question_answer = answer_table.objects.filter(question_id=question_id).count()
            question_tags = question_tag.objects.filter(question_id=question_id)
            tags = list()
            for item in question_tags:
                item = tag.objects.get(id=item.tag_id).title
                tags.append(item)
            datas.append({
                'user_id': user_id,
                'username': username,
                'user_joined': user_joined,
                'user_image':user_image,
                'user_points':user_points,
                'question_id': question_id,
                'question_title':question_title,
                'question_time_day':int(question_time_day),
                'question_time_hour':int(question_time_hour),
                'question_time_minute':int(question_time_minute),
                'question_time_second':int(question_time_second),
                'question_view':question_view,
                'question_upvote':question_upvote,
                'question_answer':question_answer,
                'question_tags': tags
            })
            
        return render(request, 'forum-home.html',{'datas':datas, 'sort_title': 'latest added'})

class post(View):
    def __init__(self):
        data_update()
        
    def get(self, request):
        form = post_question_form()
        return render(request, 'post-question.html', {'form': form})
    
    def post(self, request):
        title = request.POST.get('title')
        desc = request.POST.get('description')
        
        tag1 = request.POST.get('tag1')
        tag2 = request.POST.get('tag2')
        tag3 = request.POST.get('tag3')
        
        user = request.user.id        
        data = question_table()
        data.user = userdata.objects.get(id=user)
        data.title = title
        data.description = desc
        data.save()
        
        if tag1==tag2 and tag1==tag3:
            data1 = question_tag()
            data1.tag = tag.objects.get(id=int(tag1)+1)
            data1.question = question_table.objects.get(question_id=data.question_id)
            data1.save()
        elif tag1==tag2 and tag1!=tag3:
            data1 = question_tag()
            data1.tag = tag.objects.get(id=int(tag1)+1)
            data1.question = question_table.objects.get(question_id=data.question_id)
            data1.save()
            data1 = question_tag()
            data1.tag = tag.objects.get(id=int(tag3)+1)
            data1.question = question_table.objects.get(question_id=data.question_id)
            data1.save()
        elif tag1!=tag2 and tag1==tag3:
            data1 = question_tag()
            data1.tag = tag.objects.get(id=int(tag1)+1)
            data1.question = question_table.objects.get(question_id=data.question_id)
            data1.save()
            data1 = question_tag()
            data1.tag = tag.objects.get(id=int(tag2)+1)
            data1.question = question_table.objects.get(question_id=data.question_id)
            data1.save()
        else:
            data1 = question_tag()
            data1.tag = tag.objects.get(id=int(tag1)+1)
            data1.question = question_table.objects.get(question_id=data.question_id)
            data1.save()
            data1 = question_tag()
            data1.tag = tag.objects.get(id=int(tag2)+1)
            data1.question = question_table.objects.get(question_id=data.question_id)
            data1.save()
            data1 = question_tag()
            data1.tag = tag.objects.get(id=int(tag3)+1)
            data1.question = question_table.objects.get(question_id=data.question_id)
            data1.save()
        data2 = question_count.objects.get(id=1)
        data2.number +=1
        data2.save()
        today = datetime.date.today()
        try:
            data3 = today_question_count.objects.get(date_day=today.day, date_month=today.month, date_year=today.year)
            data3.number +=1
            data3.save()
        except:
            data3 = today_question_count()
            data3.date_day = today.day
            data3.date_month = today.month
            data3.date_year = today.year
            data3.save()
        data4 = userdata.objects.get(user_id=user)
        data4.points +=10
        data4.save()
        return render(request, 'posted.html')
    
class subscribe(View):
    def __init__(self):
        data_update()
        
    def post(self, request):
        email = request.POST.get('email')
        if email!='':
            try:
                data = email_subscribe.objects.get(email=email)
            except:
                data = email_subscribe()
                data.email = email
                data.save()
        return redirect('/')

class login(View):
    def __init__(self):
        data_update()
        
    def get(self, request):
        return render(request, 'login.html')

class logout_request(View):
    def __init__(self):
        data_update()
        
    def get(self, request):
        logout(request)
        return redirect('/')

class home(View):
    
    def __init__(self):
        data_update()
        
    def get(self, request):
        return render(request, 'index.html')
    
def data_update():
    try:
        data1 = total_site_visit.objects.get(id=1)
        data1.number +=1
        data1.save()
    except:
        data1 = total_site_visit()
        data1.number=1
        data1.save()
    today = datetime.date.today()
    try:
        data2 = today_site_visit.objects.get(date_day=today.day, date_month=today.month, date_year=today.year)
        data2.number +=1
        data2.save()
    except:
        data2 = today_site_visit()
        data2.date_day = today.day
        data2.date_month = today.month
        data2.date_year = today.year
        data2.save()
    try:
        data3 = monthly_site_visit.objects.get(date_month=today.month, date_year=today.year)
        data3.number +=1
        data3.save()
    except:
        data3 = monthly_site_visit()
        data3.date_month = today.month
        data3.date_year = today.year
        data3.save()
    try:
        data4 = question_count.objects.get(id=1)
    except:
        data4 = question_count()
        data4.number = 0
        data4.save()
    try:
        data5 = answer_count.objects.get(id=1)
    except:
        data5 = answer_count()
        data5.number = 0
        data5.save()
    try:
        data6 = today_question_count.objects.get(date_day=today.day, date_month=today.month, date_year=today.year)
    except:
        data6 = today_question_count()
        data6.date_day = today.day
        data6.date_month = today.month
        data6.date_year = today.year
        data6.save()
    try:
        data7 = today_answer_count.objects.get(date_day=today.day, date_month=today.month, date_year=today.year)
    except:
        data7 = today_answer_count()
        data7.date_day = today.day
        data7.date_month = today.month
        data7.date_year = today.year
        data7.save()
    try:
        data8 = tag.objects.get(id=1)
    except:
        data8 = tag()
        data8.title = "python"
        data8.save()
        data8 = tag()
        data8.title = "c++"
        data8.save()
        data8 = tag()
        data8.title = "c"
        data8.save()
        data8 = tag()
        data8.title = "java"
        data8.save()
        data8 = tag()
        data8.title = "django"
        data8.save()