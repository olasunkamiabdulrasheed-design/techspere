from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Resource


def resource_list(request):
    category = request.GET.get("category", "")
    resources = Resource.objects.all()
    if category:
        resources = resources.filter(category=category)
    return render(request, "resources/resource_list.html", {
        "resources": resources,
        "categories": Resource.CATEGORY_CHOICES,
        "selected_category": category,
    })


def resource_detail(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    return render(request, "resources/resource_detail.html", {"resource": resource})


@login_required
def resource_create(request):
    if request.method == "POST":
        title = (request.POST.get("title") or "").strip()[:255]
        description = (request.POST.get("description") or "").strip()[:2000]
        category = request.POST.get("category")
        external_link = (request.POST.get("external_link") or "").strip()[:500]
        file = request.FILES.get("file")

        valid_categories = [c[0] for c in Resource.CATEGORY_CHOICES]
        if category not in valid_categories:
            category = "other"

        if title and (file or external_link):
            Resource.objects.create(
                uploader=request.user,
                title=title,
                description=description,
                category=category,
                file=file,
                external_link=external_link,
            )
            return redirect("resource_list")

    return render(request, "resources/resource_create.html", {
        "categories": Resource.CATEGORY_CHOICES,
    })


def resource_download(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    resource.download_count += 1
    resource.save(update_fields=["download_count"])
    if resource.file:
        file_url = resource.file.url
        if "/upload/" in file_url:
            file_url = file_url.replace("/upload/", "/upload/fl_attachment/")
        return redirect(file_url)
    return redirect(resource.external_link)
