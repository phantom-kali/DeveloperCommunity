from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import ErrorMessage, Solution
from .forms import ErrorMessageForm, SolutionForm

def error_list(request):
    errors = ErrorMessage.objects.all().order_by('-created_at')
    paginator = Paginator(errors, 10)  # Show 10 errors per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'errors/error_list.html', {'page_obj': page_obj})

@login_required
def create_error(request):
    if request.method == 'POST':
        form = ErrorMessageForm(request.POST)
        if form.is_valid():
            error = form.save(commit=False)
            error.user = request.user
            error.save()
            return redirect('error_detail', pk=error.pk)
    else:
        form = ErrorMessageForm()
    return render(request, 'errors/create_error.html', {'form': form})

def error_detail(request, pk):
    error = get_object_or_404(ErrorMessage, pk=pk)
    solutions = error.solutions.all().order_by('-created_at')
    
    if request.method == 'POST':
        solution_form = SolutionForm(request.POST)
        if solution_form.is_valid():
            solution = solution_form.save(commit=False)
            solution.user = request.user
            solution.error_message = error
            solution.save()
            return redirect('error_detail', pk=pk)
    else:
        solution_form = SolutionForm()
    
    return render(request, 'errors/error_detail.html', {
        'error': error,
        'solutions': solutions,
        'solution_form': solution_form
    })

@login_required
def edit_error(request, pk):
    error = get_object_or_404(ErrorMessage, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ErrorMessageForm(request.POST, instance=error)
        if form.is_valid():
            form.save()
            return redirect('error_detail', pk=pk)
    else:
        form = ErrorMessageForm(instance=error)
    return render(request, 'errors/edit_error.html', {'form': form, 'error': error})

@login_required
def delete_error(request, pk):
    error = get_object_or_404(ErrorMessage, pk=pk, user=request.user)
    if request.method == 'POST':
        error.delete()
        return redirect('error_list')
    return render(request, 'errors/delete_error.html', {'error': error})

@login_required
def accept_solution(request, error_pk, solution_pk):
    error = get_object_or_404(ErrorMessage, pk=error_pk, user=request.user)
    solution = get_object_or_404(Solution, pk=solution_pk, error_message=error)
    
    # Reset all solutions to not accepted
    error.solutions.update(is_accepted=False)
    
    # Set the selected solution as accepted
    solution.is_accepted = True
    solution.save()
    
    return redirect('error_detail', pk=error_pk)