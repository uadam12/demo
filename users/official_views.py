from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from app import render, is_post, get_or_none
from app.views import create_view, delete_view
from app.auth import officials_only
from applicant.filters import ApplicantFilter
from .official_forms import AdminForm, GuestForm
from .models import User


@officials_only()
def dashboard(request):
    return render(
        request, 'officials/dashboard', 
        title='BSSB Official Dashboard',
        total_unblocked_users = User.unblocked_users().count(),
        total_blocked_users = User.blocked_users().count(),
        total_applicants = User.applicants().count(),
        total_users = User.objects.count(),
        total_admins = User.admins().count(),
        total_guests = User.guests().count(),
    )

@officials_only(main_admin_only=True)
def admins(request):
    return render(
        request, 'officials/admins',
        title='BSSB | Sub Admins',
        admins=User.admins(),
    )

@officials_only(main_admin_only=True)
def create_admin(request):
    return create_view(
        request, AdminForm,
        success_url='official:admins',
        header='Create Admin'
    )

@officials_only
def delete_admin(request, id):
    admin = get_object_or_404(User, id=id)
    
    return delete_view(
        request, 
        model=admin, 
        header='BSSB Delete sub admin',
        success_url='official:admins'
    )


@officials_only(main_admin_only=True)
def guests(request):
    return render(
        request, 'officials/guests',
        title='BSSB | Guest users',
        guests=User.guests(),
    )

    
@officials_only(main_admin_only=True)
def create_guest(request):
    return create_view(
        request, GuestForm,
        success_url='official:guests',
        header='Create Guest'
    )

@officials_only(main_admin_only=True)
def delete_guest(request, id):
    guest = get_object_or_404(User, id=id)
    
    return delete_view(
        request, 
        model=guest, 
        header='BSSB Delete Guest User',
        success_url='official:guests'
    )

@officials_only()
def applicants(request):
    page = request.GET.get('page', 1)
    filtered_applicants = ApplicantFilter(request.GET, queryset=User.applicants())
    paginator = Paginator(filtered_applicants.qs, 10)
    applicants = paginator.get_page(page)
    

    return render(
        request, 'officials/applicants',
        title='BSSB | Applicants',
        applicants=applicants,
        form = filtered_applicants.form
    )


def block_applicant(request, applicant_id):
    if not is_post(request) or request.user.access_code < 3:
        return HttpResponse('Invalid request')
    
    user = get_or_none(User, id=applicant_id)
    if user is not None:
        user.access_code = 0
        user.save()

    return render(request, 'parts/applicant-access', applicant=user)

def unblock_applicant(request, applicant_id):
    if not is_post(request) or request.user.access_code < 3:
        return HttpResponse('Invalid request')
    
    user = get_or_none(User, id=applicant_id)
    if user is not None:
        user.access_code = 1
        user.save()

    return render(request, 'parts/applicant-access', applicant=user)