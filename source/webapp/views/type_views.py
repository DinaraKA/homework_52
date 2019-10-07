from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from django.db.models import ProtectedError
from webapp.models import Type
from webapp.forms import TypeForm
from .base_views import CreateView

class TypeIndexView(ListView):
    context_object_name = 'types'
    model = Type
    template_name = 'type/type_index.html'


class TypeCreateView(CreateView):
    model = Type
    template_name = 'type/type_create.html'
    form_class = TypeForm

    def get_redirect_url(self):
        return reverse('type_index')


class TypeUpdateView(View):
    def get(self, request, pk):
        type = get_object_or_404(Type, pk=pk)
        form = TypeForm(data={
            'type_name': type.type_name
        })
        return render(request, 'type/type_update.html', context={'form': form, 'type':type})

    def post(self, request, pk):
        type = get_object_or_404(Type, pk=pk)
        form = TypeForm(data=request.POST)
        if form.is_valid():
            type.type_name=form.cleaned_data['type_name']
            type.save()
            return redirect('type_index')
        else:
            return render(request, 'type/type_update.html', context={'form': form, 'type':type})


class TypeDeleteView(View):
    def get(self, request, pk):
        type = get_object_or_404(Type, pk=pk)
        return render(request, 'type/type_delete.html', context={'type':type})

    def post(self, request, pk):
        type = get_object_or_404(Type, pk=pk)
        try:
            type.delete()
            return redirect('type_index')
        except ProtectedError:
            return render(request, 'error.html')


