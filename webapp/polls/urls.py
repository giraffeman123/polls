from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("create/question/", views.QuestionCreateView.as_view(), name="cr_question"),
    path("create/<int:pk>/choice/", views.ChoiceCreateView.as_view(), name="cr_choice"),
    path(
        "update/<int:pk>/question", views.QuestionUpdate.as_view(), name="updt_question"
    ),
    path(
        "delete/<int:pk>/question", views.QuestionDelete.as_view(), name="del_question"
    ),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("downloads/questions/xslx", views.export_db_to_xslx, name="export_db_to_xslx"),
    path("charts/", views.ChartView.as_view(), name="charts"),
    # path('render/', views.index_render, name='index_render'),
    # path('specifics/<int:question_id>/', views.detail, name='detail'),
    # path('<int:question_id>/results/', views.results, name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]
