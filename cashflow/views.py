from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from .models import CashFlow, Type, Status, Category, SubCategory

def cashflow_list(request):
    qs = CashFlow.objects.select_related("type", "status", "category", "subcategory").order_by("-date", "-id")

    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")
    type_id = request.GET.get("type")
    status_id = request.GET.get("status")
    category_id = request.GET.get("category")
    subcategory_id = request.GET.get("subcategory")

    if date_from:
        qs = qs.filter(date__gte=date_from)
    if date_to:
        qs = qs.filter(date__lte=date_to)
    if type_id:
        qs = qs.filter(type_id=type_id)
    if status_id:
        qs = qs.filter(status_id=status_id)
    if category_id:
        qs = qs.filter(category_id=category_id)
    if subcategory_id:
        qs = qs.filter(subcategory_id=subcategory_id)

    context = {
        "items": qs,
        "types": Type.objects.all(),
        "statuses": Status.objects.all(),
        "categories": Category.objects.all(),
        "subcategories": SubCategory.objects.all(),
        "saved_filters": {
            "date_from": date_from or "",
            "date_to": date_to or "",
            "type": type_id or "",
            "status": status_id or "",
            "category": category_id or "",
            "subcategory": subcategory_id or "",
        }
    }
    return render(request, "cashflow/list.html", context)


def cashflow_create(request):
    if request.method == "POST":
        data = request.POST
        item = CashFlow(
            date=data.get("date") or None,
            type_id=data.get("type") or None,
            status_id=data.get("status") or None,
            category_id=data.get("category") or None,
            subcategory_id=data.get("subcategory") or None,
            amount=data.get("amount") or None,
            comment=data.get("comment") or "",
        )
        try:
            item.save()
            return redirect("cashflow_list")
        except ValidationError as e:
            error = str(e)
    else:
        error = None
        item = None
    context = {
        "item": item,
        "types": Type.objects.all(),
        "statuses": Status.objects.all(),
        "categories": Category.objects.all(),
        "subcategories": SubCategory.objects.all(),
        "error": error,
        "mode": "create",
    }
    return render(request, "cashflow/form.html", context)


def cashflow_update(request, pk: int):
    item = get_object_or_404(CashFlow, pk=pk)
    error = None
    if request.method == "POST":
        data = request.POST
        item.date = data.get("date") or None
        item.type_id = data.get("type") or None
        item.status_id = data.get("status") or None
        item.category_id = data.get("category") or None
        item.subcategory_id = data.get("subcategory") or None
        item.amount = data.get("amount") or None
        item.comment = data.get("comment") or ""
        try:
            item.save()
            return redirect("cashflow_list")
        except ValidationError as e:
            error = str(e)

    context = {
        "item": item,
        "types": Type.objects.all(),
        "statuses": Status.objects.all(),
        "categories": Category.objects.all(),
        "subcategories": SubCategory.objects.all(),
        "error": error,
        "mode": "edit",
    }
    return render(request, "cashflow/form.html", context)
