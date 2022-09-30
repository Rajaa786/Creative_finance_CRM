from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Leads)
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
