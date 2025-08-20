from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ReportForm, ImeiCheckForm
from .models import Report, ImeiCheckLog
from django.db.models import Count
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
f




def report_create(request):
    """
    Allow victims to report a stolen phone (no account required).
    """
    if request.method == "POST":
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Your report has been submitted successfully. Authorities will be notified.",
            )
            return redirect("core:report")  # back to same page
    else:
        form = ReportForm()

    return render(request, "core/report.html", {"form": form})


def check_imei(request):
    """
    Allow buyers to check an IMEI before purchase.
    """
    result = None  # will hold "safe" or "stolen"
    report = None  # hold the matched report if stolen

    if request.method == "POST":
        form = ImeiCheckForm(request.POST)
        if form.is_valid():
            imei = form.cleaned_data["imei"]

            # Log the check
            ip = request.META.get("REMOTE_ADDR")
            ImeiCheckLog.objects.create(imei=imei, ip_address=ip)

            # Search in Report DB
            try:
                report = Report.objects.get(imei=imei)
                result = "stolen"
            except Report.DoesNotExist:
                result = "safe"
    else:
        form = ImeiCheckForm()

    context = {
        "form": form,
        "result": result,
        "report": report,
    }
    return render(request, "core/check.html", context)



def home(request):
    return render(request, "core/home.html")

def about(request):
    return render(request, "core/about.html")






@login_required(login_url='/login/')
def admin_dashboard(request):
    q = request.GET.get("q", "").strip()

    # Base queryset (for stats + pagination)
    base_queryset = Report.objects.all().order_by("-created_at")

    if q:
        base_queryset = base_queryset.filter(
            Q(imei__icontains=q) |
            Q(owner_name__icontains=q) |
            Q(phone_model__icontains=q)
        )

    # Pagination
    paginator = Paginator(base_queryset, 10)
    page = request.GET.get("page")
    reports = paginator.get_page(page)

    # Global totals (system-wide)
    global_total = Report.objects.count()
    global_verified = Report.objects.filter(status="verified").count()
    global_flagged = Report.objects.filter(status="flagged").count()
    global_recovered = Report.objects.filter(status="recovered").count()

    # Filtered totals (based on base_queryset, not paginated slice)
    filtered_total = base_queryset.count()
    filtered_verified = base_queryset.filter(status="verified").count()
    filtered_flagged = base_queryset.filter(status="flagged").count()
    filtered_recovered = base_queryset.filter(status="recovered").count()

    context = {
        "reports": reports,
        "global_total": global_total,
        "global_verified": global_verified,
        "global_flagged": global_flagged,
        "global_recovered": global_recovered,
        "filtered_total": filtered_total,
        "filtered_verified": filtered_verified,
        "filtered_flagged": filtered_flagged,
        "filtered_recovered": filtered_recovered,
        "q": q,
    }
    return render(request, "core/admin_dashboard.html", context)




def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:  # allow only admin
            login(request, user)
            return redirect("core:dashboard")  # send to dashboard
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")


def custom_logout(request):
    logout(request)
    return redirect("core:home")
