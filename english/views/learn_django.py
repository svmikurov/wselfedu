from django.urls import reverse_lazy
from django.views.generic import FormView

from english.forms import CalendarForm


class CalendarView(FormView):
    template_name = 'english/calendar.html'
    form_class = CalendarForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        date = form.cleaned_data['date5']
        print(date)
        return super(CalendarView, self).form_valid(form)
