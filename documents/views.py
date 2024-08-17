from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
import requests
from urllib.parse import urlparse
from django.core.cache import cache
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Document, EducationalLink
from core.models import Vote
from .forms import DocumentForm, EducationalLinkForm
from django.db.models import Prefetch
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.core.validators import URLValidator
from django.http import JsonResponse
from pathlib import Path
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
dotenv_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path)


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

    content_type = ContentType.objects.get_for_model(Document)

    if request.user.is_authenticated:
        documents = documents.prefetch_related(
            Prefetch(
                "votes",
                queryset=Vote.objects.filter(user=request.user),
                to_attr="user_votes",
            )
        )
        for document in documents:
            document.user_vote = (
                document.user_votes[0].vote if document.user_votes else 0
            )
    else:
        for document in documents:
            document.user_vote = 0

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
        "content_type": content_type,
        "page_title": "Educational Documents",
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

    content_type = ContentType.objects.get_for_model(EducationalLink)

    if request.user.is_authenticated:
        links = links.prefetch_related(
            Prefetch(
                "votes",
                queryset=Vote.objects.filter(user=request.user),
                to_attr="user_votes",
            )
        )
        for link in links:
            link.user_vote = link.user_votes[0].vote if link.user_votes else 0
    else:
        for link in links:
            link.user_vote = 0

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
        "content_type": content_type,
        "page_title": "Educational Links",
    }
    return render(request, "documents/link_list.html", context)


def is_url_safe(url):
    # Parse the URL to get the domain
    domain = urlparse(url).netloc

    # Check whitelist first (faster and doesn't use API quota)
    whitelist = [
        "coursera.org",
        "edx.org",
        "udacity.com",
        "khanacademy.org",
        "mit.edu",
        "stanford.edu",
        "harvard.edu",
        "youtube.com",
    ]
    if any(domain.endswith(white_domain) for white_domain in whitelist):
        return True

    # If not in whitelist, check cache
    cache_key = f"url_safety_{domain}"
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return cached_result

    # If not in cache, use Google Safe Browsing API
    api_key = os.getenv("API_KEY")
    api_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}"
    my_domain = os.getenv("MY_DOMAIN")

    payload = {
        "client": {"clientId": my_domain, "clientVersion": "1.0.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}],
        },
    }

    response = requests.post(api_url, json=payload)
    result = response.json()

    is_safe = "matches" not in result

    # Cache the result for future checks (cache for 1 day)
    cache.set(cache_key, is_safe, 60 * 60 * 24)

    return is_safe


@login_required
def add_link(request):
    if request.method == "POST":
        form = EducationalLinkForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]

            try:
                URLValidator()(url)
            except ValidationError:
                form.add_error("url", "Invalid URL format")
                return render(request, "documents/add_link.html", {"form": form})

            if not is_url_safe(url):
                form.add_error(
                    "url",
                    "This URL may not be safe. If you believe this is a mistake, please contact the administrator.",
                )
                return render(request, "documents/add_link.html", {"form": form})

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
