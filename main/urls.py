from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [    
    path('', views.home.as_view(), name='home'),
    path("login/", views.login.as_view(), name="login"),
    path('logout/', views.logout_request.as_view(), name='logout_request'),
    path('contact_us/', login_required(views.contact_us.as_view()), name='contact_us'),
    path('forum/top_user/', views.top.as_view(), name='top'),
    path('forum/profile/<int:user_id>/', login_required(views.profile.as_view()), name='profile'),
    path('forum/', views.forum.as_view(), name="forum"),
    path('forun/sort/tags/', views.forum_tags.as_view(), name="forum_tags"),
    path('forum/tag/<int:tag_id>/', views.tag_questions.as_view(), name="tag_questions"),
    path('forum/question/<int:question_id>/', views.question.as_view(), name='question'),
    path('forum/question/upvote/<int:question_id>/', login_required(views.question_upvote.as_view()), name='question_upvote'),
    path('forum/answer/upvote/<int:answer_id>/', login_required(views.answer_upvote.as_view()), name='answer_upvote'),
    path('subscribe/', views.subscribe.as_view(), name='subscribe'),
    path('forum/question_post/', login_required(views.post.as_view()), name='post'),
    path('forum/answer_post/<int:question_id>/', login_required(views.post_answer.as_view()), name='post_answer'),
    path('forum/question_report/<int:question_id>/', login_required(views.question_report.as_view()), name='question_report'),
    path('forum/answer_report/<int:answer_id>/', login_required(views.answer_report.as_view()), name='answer_report'),
    path('forum/comments/<int:question_id>/', login_required(views.question_comments.as_view()), name='question_comments'),
    path('forum/answer_comments/<int:answer_id>/', login_required(views.answer_comments.as_view()), name='answer_comments'),
    path('forum/question/usercomment/<int:question_id>/', login_required(views.comment_q.as_view()), name='comment_q'),
    path('forum/answer/usercomment/<int:answer_id>/', login_required(views.comment_a.as_view()), name='comment_a'),
    
    path('forum/user/profile/<int:user_id>/', login_required(views.user_profile.as_view()), name='user_profile'),
    path('forum/user/question/<int:user_id>/', login_required(views.user_question.as_view()), name='user_question'),
    path('forum/user/notification/question/<int:user_id>/', login_required(views.user_q_notification.as_view()), name='user_q_notification'),
    path('forum/user/notification/answer/<int:user_id>/', login_required(views.user_a_notification.as_view()), name='user_a_notification'),
    
    path('forum/admin/', login_required(views.admin_dashboard.as_view()), name='admin_dashboard'),
    path('forum/admin/user/', login_required(views.admin_user.as_view()), name='admin_user'),
    path('forum/admin/question/', login_required(views.admin_question.as_view()), name='admin_question'),
    path('forum/admin/tags/', login_required(views.admin_tags.as_view()), name='admin_tags'),
    path('forum/admin/report/question/', login_required(views.admin_report_question.as_view()), name='admin_report_question'),
    path('forum/admin/report/question/action/<int:report_id>/', login_required(views.admin_report_question_action.as_view()), name='admin_report_question_action'),
    path('forum/admin/report/answer/', login_required(views.admin_report_answer.as_view()), name='admin_report_answer'),
    path('forum/admin/report/answer/action/<int:report_id>/', login_required(views.admin_report_answer_action.as_view()), name='admin_report_answer_action'),
    path('forum/admin/notification/question/', login_required(views.admin_notification_question.as_view()), name='admin_notification_question'),
    path('forum/admin/notification/answer/', login_required(views.admin_notification_answer.as_view()), name='admin_notification_answer'),
    path('forum/admin/email/', login_required(views.admin_email.as_view()), name='admin_email'),
    path('forum/admin/message/', login_required(views.admin_message.as_view()), name='admin_message'),
    path('forum/admin/message/read/<int:message_id>', login_required(views.admin_message_read.as_view()), name='admin_message_read'),
    
]
