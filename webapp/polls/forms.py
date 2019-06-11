from django.forms import ModelForm
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect

from .models import Question, Choice


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ["question_text", "pub_date"]
        
class ChoiceForm(ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text','votes']