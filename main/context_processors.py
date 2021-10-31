from django.contrib.auth.models import User
from .models import total_site_visit, today_site_visit, monthly_site_visit, question_count, answer_count, today_question_count, today_answer_count
import datetime



def add_variable_to_context1(request):
    user = User.objects.all().count()
    question = question_count.objects.get(id=1).number
    answer = answer_count.objects.get(id=1).number
    visit = total_site_visit.objects.get(id=1).number
    today = datetime.date.today()
    t_question = today_question_count.objects.get(date_day=today.day, date_month=today.month, date_year=today.year).number
    t_answer = today_answer_count.objects.get(date_day=today.day, date_month=today.month, date_year=today.year).number
    t_visit = today_site_visit.objects.get(date_day=today.day, date_month=today.month, date_year=today.year).number
    m_visit = monthly_site_visit.objects.get(date_month=today.month, date_year=today.year).number
    
    data = {
        'logo': 'novicexp',
        'user': user,
        'question': question,
        'answer': answer,
        'visit': visit,
        't_question': t_question,
        't_answer': t_answer,
        't_visit': t_visit,
        'm_visit': m_visit
    }
    
    return {
        'data': data
    }