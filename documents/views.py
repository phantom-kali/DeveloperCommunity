from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Document, EducationalLink
from .forms import DocumentForm, EducationalLinkForm
from django.core.exceptions import ValidationError

@login_required
def document_list(request):
    documents = Document.objects.all().order_by("-created_at")

    category = request.GET.get("category")
    if category:
        documents = documents.filter(category__icontains=category)

    user = request.GET.get("user")
    if user:
        documents = documents.filter(user__username__icontains=user)

    query = request.GET.get("q")
    if query:
        documents = documents.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    paginator = Paginator(documents, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    categories = Document.objects.values_list("category", flat=True).distinct()

    context = {
        "page_obj": page_obj,
        "categories": categories,
        "current_category": category,
        "current_user": user,
        "query": query,
    }
    return render(request, "documents/document_list.html", context)


@login_required
def upload_document(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                document = form.save(commit=False)
                document.user = request.user
                document.save()
                return redirect("document_list")
            except ValidationError as e:
                form.add_error("file", e.message)
    else:
        form = DocumentForm()
    return render(request, "documents/upload_document.html", {"form": form})

@login_required
def document_detail(request, pk):
    document = get_object_or_404(Document, pk=pk)
    return render(request, "documents/document_detail.html", {"document": document})


@login_required
def delete_document(request, pk):
    document = get_object_or_404(Document, pk=pk, user=request.user)
    if request.method == "POST":
        document.delete()
        return redirect("document_list")
    return render(request, "documents/delete_document.html", {"document": document})

@login_required
def link_list(request):
    links = EducationalLink.objects.all().order_by("-created_at")

    category = request.GET.get("category")
    if category:
        links = links.filter(category__icontains=category)

    user = request.GET.get("user")
    if user:
        links = links.filter(user__username__icontains=user)

    query = request.GET.get("q")
    if query:
        links = links.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(url__icontains=query)
        )

    paginator = Paginator(links, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    categories = EducationalLink.objects.values_list("category", flat=True).distinct()

    context = {
        "page_obj": page_obj,
        "categories": categories,
        "current_category": category,
        "current_user": user,
        "query": query,
    }
    return render(request, "documents/link_list.html", context)


@login_required
def add_link(request):
    if request.method == "POST":
        form = EducationalLinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.user = request.user
            link.save()
            return redirect("link_list")
    else:
        form = EducationalLinkForm()
    return render(request, "documents/add_link.html", {"form": form})


@login_required
def delete_link(request, pk):
    link = get_object_or_404(EducationalLink, pk=pk, user=request.user)
    if request.method == "POST":
        link.delete()
        return redirect("link_list")
    return render(request, "documents/delete_link.html", {"link": link})
