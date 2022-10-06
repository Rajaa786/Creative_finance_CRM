from django.contrib import admin
from django.contrib.auth.models import Group , Permission
from .models import *


class LeadsAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(added_by=request.user.username)

admin.register(Group)
admin.register(Permission)

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Leads, LeadsAdmin)
admin.site.register(AdditionalDetails)
# Salaried
admin.site.register(SalPersonalDetails)
admin.site.register(SalIncomeDetails)
admin.site.register(SalOtherIncomes)
admin.site.register(SalAdditionalOtherIncomes)
admin.site.register(ContactPerson)
admin.site.register(SalCompanyDetails)
admin.site.register(SalExistingLoanDetails)
admin.site.register(SalExistingCreditCard)
admin.site.register(SalAdditionalDetails)
admin.site.register(SalInvestments)
admin.site.register(SalResidenceDetails)
admin.site.register(PropType1)
admin.site.register(PropType2)
admin.site.register(PropType3)
admin.site.register(PropType4)
# admin.site.register(HousewifeDetails)
