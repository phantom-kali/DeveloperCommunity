from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CodeSnippet
from .forms import CodeSnippetForm

def snippet_list(request):
    snippets = CodeSnippet.objects.all()
    return render(request, 'snippets/list.html', {'snippets': snippets})

@login_required
def add_snippet(request):
    if request.method == 'POST':
        form = CodeSnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.user = request.user
            snippet.save()
            return redirect('snippet_list')
    else:
        form = CodeSnippetForm()
    return render(request, 'snippets/add.html', {'form': form})

def snippet_detail(request, pk):
    snippet = CodeSnippet.objects.get(pk=pk)
    return render(request, 'snippets/detail.html', {'snippet': snippet})