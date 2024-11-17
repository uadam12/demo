from django.shortcuts import get_object_or_404
from app import render
from app.views import create_view, delete_view, update_view
from .forms import (
    Requirement, RequirementForm,
    Criterion, CriterionForm,
    Bank, BankForm,
    LGA, LGAForm
)

# Criteria
def criteria(request):
    return render(
        request, "board/criteria",
        title='BSSB | Criteria',
        criteria = Criterion.objects.all()
    )

def create_criterion(request):
    return create_view(
        request, 
        form_class=CriterionForm, 
        success_url='board:criteria', 
        header='Create Criterion'
    )

def update_criterion(request, id):
    criterion = get_object_or_404(Criterion, id=id)
    
    return update_view(
        request, 
        instance=criterion, 
        form_class=CriterionForm, 
        success_url='board:criteria', 
        header='Update Criterion'
    )

def delete_criterion(request, id):
    criterion = get_object_or_404(Criterion, id=id)
    
    return delete_view(
        request, 
        model=criterion,
        success_url='board:criteria', 
        header='Delete Criterion'
    )

# Requirement
def requirements(request):
    return render(
        request, "board/requirements",
        title='BSSB | Requirements',
        requirements = Requirement.objects.all()
    )

def create_requirement(request):
    return create_view(
        request, 
        form_class=RequirementForm, 
        success_url='board:requirements', 
        header='Create Requirement'
    )

def update_requirement(request, id):
    requirement = get_object_or_404(Requirement, id=id)
    
    return update_view(
        request, 
        instance=requirement, 
        form_class=RequirementForm, 
        success_url='board:requirements', 
        header='Update Requirement'
    )

def delete_requirement(request, id):
    requirement = get_object_or_404(Requirement, id=id)
    
    return delete_view(
        request, 
        model=requirement,
        success_url='board:requirements', 
        header='Delete Requirement'
    )

# Banks
def banks(request):
    return render(
        request, "board/banks",
        title='BSSB | Banks',
        banks = Bank.objects.all()
    )

def bank(request, code):
    bank = get_object_or_404(Bank, code=code)
 
    return render(
        request, "board/accounts",
        title='BSSB | Bank Accounts',
        bank = bank
    )

def create_bank(request):
    return create_view(
        request, form_class=BankForm, 
        success_url='board:banks', 
        header='Create Bank'
    )

def update_bank(request, code):
    bank = get_object_or_404(Bank, code=code)
    
    return update_view(
        request, instance=bank, 
        form_class=BankForm, 
        success_url='board:banks', 
        header='Update Bank'
    )
    
def delete_bank(request, code):
    bank = get_object_or_404(Bank, code=code)
    
    return delete_view(
        request, model=bank,
        success_url='board:banks', 
        header='Delete Bank'
    )

# Local Government Area(LGA)
def lgas(request):
    return render(
        request, "board/lgas",
        title='BSSB | Local Govenment Areas',
        lgas = LGA.objects.all()
    )

def create_lga(request):
    return create_view(
        request, 
        form_class=LGAForm, 
        success_url='board:lgas', 
        header='Create Local Government Area'
    )

def update_lga(request, code):
    lga = get_object_or_404(LGA, code=code)
    
    return update_view(
        request, instance=lga, 
        form_class=LGAForm, 
        success_url='board:lgas', 
        header='Update Local Government Area'
    )
    
def delete_lga(request, code):
    lga = get_object_or_404(LGA, code=code)
    
    return delete_view(
        request, model=lga,
        success_url='board:lgas', 
        header='Delete Local Government Area'
    )