## Reference
[Form fields](https://docs.djangoproject.com/en/4.2/ref/forms/fields/#module-django.forms.fields)  
[Привязка загруженных файлов к форме](https://docs.djangoproject.com/en/4.2/ref/forms/api/#binding-uploaded-files-to-a-form)    
[radio](https://django.readthedocs.io/en/stable/intro/tutorial04.html)  
[Создание формы в html из model.py или form.py](Создание формы в html из model.py или form.py)

[Использование form в html из model.py или из form.py](#Использование form в html из model.py или из form.py)


### [Создание формы](https://docs.djangoproject.com/en/4.2/topics/forms/#building-a-form)  
 `form.html`

```
<form action="/your-name/" method="post">
    <label for="your_name">Your name: </label>
    <input type="text" name="your_name" value="{{ current_name }}">
    <input type="submit" value="OK">
</form>
```
```
for="your_name"  
name="your_name"
```
Отобразит:
```
текстовое поле / <input type="text" ...>  
название поля / <label ...>Your name: </label>  
предварительное заполнение / <input ... value="{{ current_name }}">  
кнопку с надписью / <input type="submit" value="OK">  
вернет данные по адресу / <form action="/url/" ...>
```

[ссылка на Django документацию](https://docs.djangoproject.com/en/4.2/topics/forms/#the-template)
```
<form action="/url/" method="post">
    {% csrf_token %}
    {{ form }}
    <input type="submit" value="Submit">
</form>

```
#### Создание формы с использованием модели
`form.py`
```
from django import forms

from models import MyModel

class MyForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = ('name',)
```
#### Создание формы без модели
`form.py`
```
from django import forms

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
```
```
необязательно к заполнению / required=False  
<textarea> /widget=forms.Textarea    
```
`views.py`
```
@login_required
def discussions_create(request):
    """Create discussion"""
    # Если запрос Post, тогда обрабатываем форму.
    # https://docs.djangoproject.com/en/5.0/ref/request-response/#django.http.HttpRequest.method
    # https://docs.djangoproject.com/en/5.0/ref/request-response/#django.http.HttpRequest.POST
    if request.method == 'POST':
        # Создадим экземпляр формы
        # и заполним его данными запроса (укажем параметры)
        # Получим данные POST для заполнения формы.
        request_form_data = request.POST
        # https://docs.djangoproject.com/en/5.0/ref/request-response/#django.http.HttpRequest.POST
        request_files = request.FILES
        # Создадим форму для редактирования.
        form = DiscussionCreateForm(request_form_data, request_files)

        if form.is_valid:
            new_discussion = form.save(commit=False)
            # https://docs.djangoproject.com/en/5.0/ref/request-response/#django.http.HttpRequest.user
            new_discussion.author = request.user
            new_discussion.save()
            return redirect(new_discussion.get_absolute_url())

    else:
        # Если поступит GET запрос или другой, вернуть пустую форму
        form = DiscussionCreateForm()

    return render(request, 'discussions/create_form.html', {'form': form})
```
Редирект по get_absolute_url  
модели Discussion формы DiscussionCreateForm
```
return redirect(new_discussion.get_absolute_url())
```
#### Добавить пользователя в форму
```
class CreatePost(LoginRequiredMixin, CreateView):
    form_class = CreatePostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.success_url = reverse_lazy(
            'posts:user',
            kwargs={'username': self.request.user.username}
        )
        return super().form_valid(form)
```

### Использование form в html из model.py или из form.py
`view.py`
```
class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
```
или
```
class CreatePost(LoginRequiredMixin, CreateView):
    form_class = CreatePostForm
```