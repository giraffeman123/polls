from django.shortcuts import render

# Create your views here.
from django.contrib.auth.views import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.encoding import smart_str
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
    DetailView,
    FormView,
)
from django.utils import timezone

from .forms import QuestionForm, ChoiceForm
from .models import Question, Choice


class ValidateFormMixin:
    def form_invalid(self, form):
        if not form.is_valid():
            messages.error(self.request, "Invalid form.")
            return super(ValidateFormMixin, self).form_invalid(form)


# loading index.html with generic view
class IndexView(ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions(not including those set to 
        be published in the future)."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by(
            "-pub_date"
        )


class ChartView(ListView):
    template_name = "polls/charts.html"
    context_object_name = "questions_list"

    def get_queryset(self):
        """
        Return all questions published
        """
        return Question.objects.all()


# loading detail.html with generic view
class DetailView(DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


# loading detail.html with generic view
class ResultsView(DetailView):
    model = Question
    template_name = "polls/results.html"


class QuestionDelete(DeleteView):
    model = Question
    template_name = "polls/delete_question.html"

    def get_success_url(self):
        return reverse("polls:index")


class QuestionUpdate(ValidateFormMixin, SuccessMessageMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = "polls/update_question.html"

    def get_success_url(self):
        return reverse("polls:index")


class QuestionCreateView(ValidateFormMixin, SuccessMessageMixin, CreateView):
    form_class = QuestionForm
    template_name = "polls/create_question.html"
    success_message = "Your Choice was created successfully!"

    def get_success_url(self):
        return reverse("polls:cr_choice")


class ChoiceCreateView(ValidateFormMixin, SuccessMessageMixin, CreateView):
    form_class = ChoiceForm
    template_name = "polls/create_choice.html"
    success_message = "Your Choice was created successfully!"

    def get_success_url(self):
        return reverse("polls:index")


class LoginView(ValidateFormMixin, FormView):
    form_class = AuthenticationForm
    template_name = "polls/login.html"

    def get_success_url(self):
        return reverse("polls:index")

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)


def export_db_to_xslx(request):
    wb = Workbook()
    filename = "questions.xlsx"
    sheet_obj = wb.active
    sheet_obj.title = "Questions"

    count = 2
    sheet_obj["A1"] = "ID"
    sheet_obj["B1"] = "Question"
    sheet_obj["C1"] = "Choices"
    all_questions = Question.objects.all()
    for question in all_questions:
        sheet_obj["A" + str(count)] = question.id
        sheet_obj["B" + str(count)] = question.question_text
        for choice in question.choice_set.all():
            sheet_obj["C" + str(count)] = (
                "[" + choice.choice_text + "-" + str(choice.votes) + "]"
            )
        count += 1

    response = HttpResponse()
    response["Content-Type"] = "application/vnd.ms-excel"
    response["Content-Disposition"] = "attachment; filename=/%s" % smart_str(filename)
    wb.save(response)
    return response


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {"question": question, "error_message": "You didn't select a choice."},
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})


# loading index.html with loader method and no generic view
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    template = loader.get_template("polls/index.html")
    context = {"latest_question_list": latest_question_list}
    # output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(template.render(context, request))


# loading index.html with render method and no generic view
def index_render(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)


# detail method with shortcut get_object_or_404 and no generic view
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


# detail method without shortcut get_object_or_404 and no generic view
def detail_without_shortcut(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "polls/detail.html", {"question": question})
