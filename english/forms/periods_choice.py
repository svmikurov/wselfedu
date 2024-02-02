from django import forms


def get_periods(edge_period: str = 'end_period') -> dict:
    periods = {
        1: 'Сегодня',
        2: 'Три дня назад',
        3: 'Неделя назад',
        4: 'Четыре недели назад',
    }
    if edge_period == 'start_period':
        periods.update({
            9: 'Начало не выбрано'
        })
    return periods


class PeriodsChooseForm(forms.Form):
    start_period = forms.ChoiceField(
        choices=get_periods('start_period'),
        default=get_periods('start_period').get(9),
    )
    end_period = forms.ChoiceField(
        choices=get_periods(),
        default=get_periods().get(1),
    )

    def check_periods(self):
        if self.start_period > self.end_period:
            return
