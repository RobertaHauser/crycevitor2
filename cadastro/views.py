from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods


from .forms import UnidadeForm
from .models import Unidade

# Create your views here.

def unidade_list(request):
    template_name = 'cadastro/unidade_list.html'
    form = UnidadeForm(request.POST or None)

    unidades = Unidade.objects.all()

    context = {'object_list': unidades, 'form': form}
    return render(request, template_name, context)


@require_http_methods(['POST'])
def unidade_create(request):
    form = UnidadeForm(request.POST or None)

    if form.is_valid():
        form.instance.created_by=request.user
        unidade = form.save()

    context = {'object': unidade}
    return render(request, 'cadastro/unidade_hx.html', context)