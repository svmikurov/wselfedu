from django.urls import reverse_lazy
from django.views.generic import FormView

from english.forms import CalendarForm
from english.forms.word_lookup_params import WordLookupParamsForm


class CalendarView(FormView):
    template_name = 'english/calendar.html'
    form_class = CalendarForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        date = form.cleaned_data['date5']
        print(date)
        return super(CalendarView, self).form_valid(form)


class WordLookupParamsView(FormView):
    template_name = 'english/tasks/new_form.html'
    form_class = WordLookupParamsForm
    success_url = 'home'

    def form_valid(self, form):
        lookup_params = form.cleaned_data
        print(lookup_params)
        return super(WordLookupParamsView).form_valid(form)
