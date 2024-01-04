[commit=False](#commit=False)

## Create with form

### Используем класс View
`view.py`  
```
class CreatePost(LoginRequiredMixin, CreateView):
    form_class = CreatePostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
```
Можем добавить `success_url` в `def form_valid(self, form):`
```
        ...
        self.success_url = reverse_lazy(
            'posts:user',
            kwargs={'username': self.request.user.username}
        )
        return super().form_valid(form)

```

### Используем функцию
`view.py`  
```
@login_required
def discussions_create(request):

    if request.method == 'POST':
        # Создадим экземпляр формы
        # Заполним его данными запроса (укажем параметры)
        
        # Получим данные POST для заполнения формы.
        request_form_data = request.POST
        request_files = request.FILES

        # Создадим форму для редактирования.
        form = DiscussionCreateForm(request_form_data, request_files)

        if form.is_valid:
            new_discussion = form.save(commit=False)
            new_discussion.author = request.user
            new_discussion.save()

            # Редирект по get_absolute_url модели Discussion формы DiscussionCreateForm
            return redirect(new_discussion.get_absolute_url())

    else:
        # Если поступит GET запрос или другой, вернуть пустую форму
        form = DiscussionCreateForm()

    return render(request, 'discussions/create_form.html', {'form': form})
```

#### commit=False
[docs.django](https://docs.djangoproject.com/en/5.0/topics/forms/modelforms/#the-save-method)
```
1. commit=True  
default  
2. commit=False  
if form.is_valid:
    new_discussion = form.save(commit=False)
    new_discussion.save()
```
```
Вернет объект, который еще не был сохранен в базе данных.  
В этом случае вам придется вызвать метод save() для полученного экземпляра модели.  
Это полезно, если вы хотите выполнить пользовательскую обработку объекта перед его сохранением
или если вы хотите использовать один из специализированных вариантов сохранения модели.
```