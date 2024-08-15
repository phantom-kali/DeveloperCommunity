from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import CodeSnippet, Comment
from .forms import CodeSnippetForm, CommentForm

def snippet_list(request):
    snippets = CodeSnippet.objects.all().order_by('-created_at')
    paginator = Paginator(snippets, 10)  # 10 snippets per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'snippets/snippet_list.html', {'page_obj': page_obj})

@login_required
def create_snippet(request):
    if request.method == 'POST':
        form = CodeSnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.user = request.user
            snippet.save()
            return redirect('snippet_detail', pk=snippet.pk)
    else:
        form = CodeSnippetForm()
    return render(request, 'snippets/create_snippet.html', {'form': form})

def snippet_detail(request, pk):
    snippet = get_object_or_404(CodeSnippet, pk=pk)
    comments = snippet.comments.all().order_by('-created_at')
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.snippet = snippet
            comment.save()
            return redirect('snippet_detail', pk=pk)
    else:
        comment_form = CommentForm()
    
    return render(request, 'snippets/snippet_detail.html', {
        'snippet': snippet,
        'comments': comments,
        'comment_form': comment_form
    })

@login_required
def edit_snippet(request, pk):
    snippet = get_object_or_404(CodeSnippet, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CodeSnippetForm(request.POST, instance=snippet)
        if form.is_valid():
            form.save()
            return redirect('snippet_detail', pk=pk)
    else:
        form = CodeSnippetForm(instance=snippet)
    return render(request, 'snippets/edit_snippet.html', {'form': form, 'snippet': snippet})

@login_required
def delete_snippet(request, pk):
    snippet = get_object_or_404(CodeSnippet, pk=pk, user=request.user)
    if request.method == 'POST':
        snippet.delete()
        return redirect('snippet_list')
    return render(request, 'snippets/delete_snippet.html', {'snippet': snippet})