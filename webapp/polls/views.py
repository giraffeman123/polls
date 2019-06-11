from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.views import login, AuthenticationForm
from django.utils import timezone

from .forms import QuestionForm
from .models import Question, Choice

# loading index.html with generic view
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions(not including those set to 
        be published in the future)."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by(
            "-pub_date"
        )


# loading detail.html with generic view
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


# loading detail.html with generic view
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


class QuestionCreateView(generic.CreateView):
    form_class = QuestionForm
    template_name = "polls/create_question.html"
    success_url = "/polls"

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


def log_in(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return HttpResponseRedirect(reverse("polls:index"))

    return render(request, "polls/login.html", {"form": form})


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
