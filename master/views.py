from bdb import effective
from xmlrpc.client import DateTime
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from datetime import date
from django.contrib.auth.decorators import login_required
from stronghold.decorators import public

# Create your views here.
def Agreementtype_form(request):
    if request.method == 'POST':
        agreementtypeformvalue = request.POST['AgreementType'].strip()
        effective_date = date.today()
        ineffective_date = request.POST['AgreementtypeIdate']
        if AgreementType.objects.filter(agreement_type=agreementtypeformvalue).exists():
            messages.info(request, 'Agreement Type already exists')
            return redirect('Master_details')
        else :
            newagreementtype = AgreementType.objects.create(agreement_type=agreementtypeformvalue,effective_date = effective_date,ineffective_date=ineffective_date)
            newagreementtype.save()
            return redirect('Master_details')

    return render(request, 'master/master_details.html')


def Applicanttype_form(request):
    if request.method == 'POST':
        applicanttypeformvalue = request.POST['ApplicantType'].strip()
        effective_date = date.today()
        ineffective_date = request.POST['ApplicanttypeIdate']
        if ApplicantType.objects.filter(applicant_type=applicanttypeformvalue).exists():
            messages.info(request, 'Applicant Type already exists')
            return redirect('Master_details')
        else :
            newapplicanttype = ApplicantType.objects.create(applicant_type=applicanttypeformvalue,effective_date = effective_date,ineffective_date=ineffective_date)
            newapplicanttype.save()
            return redirect('Master_details')
    return render(request, 'master/master_details.html')

def AYyear_form(request):
    if request.method == 'POST':
        ayyearformvalue = request.POST['AYyear'].strip()
        effective_date = date.today()
        ineffective_date = request.POST['AYyearIdate']
        if AYYear.objects.filter(ay_year=ayyearformvalue).exists():
            messages.info(request, 'Ay Year already exists')
            return redirect('Master_details')
        else :
            newayyear = AYYear.objects.create(ay_year=ayyearformvalue,effective_date = effective_date,ineffective_date=ineffective_date)
            newayyear.save()
            return redirect('Master_details')
    return render(request, 'master/master_details.html')

def NatureOfBusiness_form(request):
    if request.method == 'POST':
        natureofbusinessformvalue = request.POST['NatureBusiness'].strip()
        effective_date = date.today()
        ineffective_date = request.POST['NatureOfBusinessIdate']
        if NatureOfBusiness.objects.filter(nature_business=natureofbusinessformvalue).exists():
            messages.info(request, 'Nature of Business already exists')
            return redirect('Master_details')
        else :
            newnatureofbusiness = NatureOfBusiness.objects.create(nature_business=natureofbusinessformvalue,effective_date = effective_date,ineffective_date=ineffective_date)
            newnatureofbusiness.save()
            return redirect('Master_details')
    return render(request, 'master/master_details.html')

def PropertyIn_form(request):
    if request.method == 'POST':
        propertyinformvalue = request.POST['PropertyIn'].strip()
        effective_date = date.today()
        ineffective_date = request.POST['PropertyInIdate']
        if PropertyIn.objects.filter(property_in=propertyinformvalue).exists():
            messages.info(request, 'PropertyIn Business already exists')
            return redirect('Master_details')
        else :
            newpropertyin = PropertyIn.objects.create(property_in=propertyinformvalue,effective_date = effective_date,ineffective_date=ineffective_date)
            newpropertyin.save()
            return redirect('Master_details')
    return render(request, 'master/master_details.html')

def RejectionType_form(request):
    if request.method == 'POST':
        rejectiontypeformvvalue = request.POST['Type'].strip()
        effective_date = date.today()
        ineffective_date = request.POST['RejectionTypeIdate']
        rejectiontypereasonformvvalue = request.POST['Reason'].strip()
        if RejectionType.objects.filter(rejection_type=rejectiontypeformvvalue, rejection_reason=rejectiontypereasonformvvalue).exists():
            messages.info(request, 'Rejection type already exists')
            return redirect('Master_details')
        else :
            newrejectiontype = RejectionType.objects.create(rejection_type=rejectiontypeformvvalue, rejection_reason=rejectiontypereasonformvvalue,effective_date = effective_date,ineffective_date=ineffective_date)
            newrejectiontype.save()
            return redirect('Master_details')

    return render(request, 'master/master_details.html')

def StageOfConstruction_form(request):
    if request.method == 'POST':
        stageformvalue = request.POST['Stage'].strip()
        effective_date = date.today()
        ineffective_date = request.POST['StageOfConstructionIdate']
        if StageOfConstruction.objects.filter(stage=stageformvalue).exists():
            messages.info(request, 'Stage Of Construction already exists')
            return redirect('Master_details')
        else :
            newstage = StageOfConstruction.objects.create(stage=stageformvalue,effective_date = effective_date,ineffective_date=ineffective_date)
            newstage.save()
            return redirect('Master_details')
    return render(request, 'master/master_details.html')

def Status_form(request):
    if request.method == 'POST':
        statusformvalue = request.POST['Status'].strip()
        effective_date = date.today()
        ineffective_date = request.POST['StatusIdate']
        if Status.objects.filter(status=statusformvalue).exists():
            messages.info(request, 'Status already exists')
            return redirect('Master_details')
        else :
            newstatus = Status.objects.create(status=statusformvalue,effective_date = effective_date,ineffective_date=ineffective_date)
            newstatus.save()
            return redirect('Master_details')
    return render(request, 'master/master_details.html')

def CompanyType_form(request):
    if request.method == 'POST':
        companytypeformvalue = request.POST['CompanyType'].strip()
        effective_date = date.today()
        ineffective_date = request.POST['CompanyTypeIdate']
        if CompanyType.objects.filter(company_type=companytypeformvalue).exists():
            messages.info(request, 'Company Type already exists')
            return redirect('Master_details')
        else :
            newcompanytype = CompanyType.objects.create(company_type=companytypeformvalue,effective_date = effective_date,ineffective_date=ineffective_date)
            newcompanytype.save()
            return redirect('Master_details')
    return render(request, 'master/master_details.html')

def CustomerType_form(request):
    if request.method == 'POST':
        customertypeformvalue = request.POST['CustomerType'].strip()
        effective_date = date.today()
        ineffective_date = request.POST['CustomerTypeIdate']
        if CustomerType.objects.filter(cust_type=customertypeformvalue).exists():
            messages.info(request, 'Customer Type already exists')
            return redirect('Master_details')
        else :
            newcustomertype = CustomerType.objects.create(cust_type=customertypeformvalue,effective_date = effective_date,ineffective_date=ineffective_date)
            newcustomertype.save()
            return redirect('Master_details')
    return render(request, 'master/master_details.html')

def DesignationType_form(request):
    if request.method == 'POST':
        designationtypeformvalue = request.POST['DesignationType'].strip()
        effective_date = date.today()
        ineffective_date = request.POST['DesignationTypeIdate']
        if DesignationType.objects.filter(desg_type=designationtypeformvalue).exists():
            messages.info(request, 'Designation Type already exists')
            return redirect('Master_details')
        else :
            newdesignationtype = DesignationType.objects.create(desg_type=designationtypeformvalue,effective_date = effective_date,ineffective_date=ineffective_date)
            newdesignationtype.save()
            return redirect('Master_details')
    return render(request, 'master/master_details.html')

def Product_form(request):
    if request.method == 'POST':
        productformvalue = request.POST['Product'].strip()
        effective_date = date.today()
        ineffective_date = request.POST['ProductIdate']
        if Product.objects.filter(product=productformvalue).exists():
            messages.info(request, 'Product already exists')
            return redirect('Master_details')
        else :
            newProduct = Product.objects.create(product=productformvalue,effective_date = effective_date,ineffective_date=ineffective_date)
            newProduct.save()
            return redirect('Master_details')
    return render(request, 'master/master_details.html')

def Profession_form(request):
    if request.method == 'POST':
        professionformvalue = request.POST['Profession'].strip()
        effective_date = date.today()
        ineffective_date = request.POST['ProfessionIdate']
        if Profession.objects.filter(profession=professionformvalue).exists():
            messages.info(request, 'Profession already exists')
            return redirect('Master_details')
        else :
            newprofession = Profession.objects.create(profession=professionformvalue,effective_date = effective_date,ineffective_date=ineffective_date)
            newprofession.save()
            return redirect('Master_details')
    return render(request, 'master/master_details.html')

def Qualification_form(request):
    if request.method == 'POST':
        qualificationformvalue = request.POST['Qualification'].strip()
        effective_date = date.today()
        ineffective_date = request.POST['QualificationIdate']
        if Qualification.objects.filter(qualification=qualificationformvalue).exists():
            messages.info(request, 'qualification already exists')
            return redirect('Master_details')
        else :
            newqualification = Qualification.objects.create(qualification=qualificationformvalue,effective_date = effective_date,ineffective_date=ineffective_date)
            newqualification.save()
            return redirect('Master_details')
    return render(request, 'master/master_details.html')

def Role_form(request):
    if request.method == 'POST':
        roleformvalue = request.POST['Role'].strip()
        effective_date = date.today()
        ineffective_date = request.POST['RoleIdate']
        if Role.objects.filter(role=roleformvalue).exists():
            messages.info(request, 'Role already exists')
            return redirect('Master_details')
        else :
            newrole = Role.objects.create(role=roleformvalue,effective_date = effective_date,ineffective_date=ineffective_date)
            newrole.save()
            return redirect('Master_details')
    return render(request, 'master/master_details.html')

def BankName_form(request):
    if request.method == 'POST':
        banknameformvalue = request.POST['bankName'].strip()
        effective_date = date.today()
        ineffective_date = request.POST['BankNameIdate']
        if BankName.objects.filter(bank_name=banknameformvalue).exists():
            messages.info(request, 'Bank Name already exists')
            return redirect('Master_details')
        else :
            newbankname = BankName.objects.create(bank_name=banknameformvalue,effective_date = effective_date,ineffective_date=ineffective_date)
            newbankname.save()
            return redirect('Master_details')
    return render(request, 'master/master_details.html')

def Degree_form(request):
    if request.method == 'POST':
        degreeformvalue = request.POST['degree'].strip()
        effective_date = date.today()
        ineffective_date = request.POST['DegreeIdate']
        if Degree.objects.filter(degree=degreeformvalue).exists():
            messages.info(request, 'Degree already exists')
            return redirect('Master_details')
        else :
            newdegree = Degree.objects.create(degree=degreeformvalue,effective_date = effective_date,ineffective_date=ineffective_date)
            newdegree.save()
            return redirect('Master_details')
    return render(request, 'master/master_details.html')

def LeadSource_form(request):
    if request.method == 'POST':
        leadsourceformvalue = request.POST['leadSource'].strip()
        effective_date = date.today()
        ineffective_date = request.POST['LeadSourceIdate']
        if LeadSource.objects.filter(lead_source=leadsourceformvalue).exists():
            messages.info(request, 'Degree already exists')
            return redirect('Master_details')
        else :
            newleadsource = LeadSource.objects.create(lead_source=leadsourceformvalue,effective_date = effective_date,ineffective_date=ineffective_date)
            newleadsource.save()
            return redirect('Master_details')
    return render(request, 'master/master_details.html')

def Nationality_form(request):
    if request.method == 'POST':
        nationalityformvalue = request.POST['nation'].strip()
        effective_date = date.today()
        ineffective_date = request.POST['NationalityIdate']
        if Nationality.objects.filter(nationality=nationalityformvalue).exists():
            messages.info(request, 'Degree already exists')
            return redirect('Master_details')
        else :
            newnationality = Nationality.objects.create(nationality=nationalityformvalue,effective_date = effective_date,ineffective_date=ineffective_date)
            newnationality.save()
            return redirect('Master_details')
    return render(request, 'master/master_details.html')

def ResidenceType_form(request):
    if request.method == 'POST':
        residencetypeformvalue = request.POST['resType'].strip()
        effective_date = date.today()
        ineffective_date = request.POST['ResidenceTypeIdate']
        if ResidenceType.objects.filter(residence_type=residencetypeformvalue).exists():
            messages.info(request, 'Residence Type already exists')
            return redirect('Master_details')
        else :
            newresidencetype = ResidenceType.objects.create(residence_type=residencetypeformvalue,effective_date = effective_date,ineffective_date=ineffective_date)
            newresidencetype.save()
            return redirect('Master_details')
    return render(request, 'master/master_details.html')

def SalaryType_form(request):
    if request.method == 'POST':
        salarytypeformvalue = request.POST['salaryType'].strip()
        effective_date = date.today()
        ineffective_date = request.POST['SalaryTypeIdate']
        if SalaryType.objects.filter(salary_type=salarytypeformvalue).exists():
            messages.info(request, 'Salary Type already exists')
            return redirect('Master_details')
        else :
            newsalarytype = SalaryType.objects.create(salary_type=salarytypeformvalue,effective_date = effective_date,ineffective_date=ineffective_date)
            newsalarytype.save()
            return redirect('Master_details')
    return render(request, 'master/master_details.html')

def State_form(request):
    if request.method == 'POST':
        stateformvalue = request.POST['state'].strip()
        effective_date = date.today()
        ineffective_date = request.POST['StateIdate']
        if State.objects.filter(state=stateformvalue).exists():
            messages.info(request, 'State already exists')
            return redirect('Master_details')
        else :
            newstate = State.objects.create(state=stateformvalue,effective_date = effective_date,ineffective_date=ineffective_date)
            newstate.save()
            return redirect('Master_details')
    return render(request, 'master/master_details.html')

def SubProduct_form(request):
    if request.method == 'POST':
        product = Product.objects.get(pk=int(request.POST['product']))
        subproductformvalue = request.POST['SubProduct'].strip()
        effective_date = date.today()
        ineffective_date = request.POST['SubProductIdate']
        if SubProduct.objects.filter(sub_product=subproductformvalue, product=product).exists():
            messages.info(request, 'Sub Product already exists')
            return redirect('Master_details')
        else :
            newsubproduct = SubProduct.objects.create(sub_product=subproductformvalue, product=product,effective_date = effective_date,ineffective_date=ineffective_date)
            newsubproduct.save()
            return redirect('Master_details')

    products = Product.objects.all()
    context = {
        'products':products,
    }
    return render(request, 'master/master_details.html', context=context)

def City_form(request):
    if request.method == 'POST':
        state = State.objects.get(pk=int(request.POST['state']))
        cityformvalue = request.POST['City'].strip()
        effective_date = date.today()
        ineffective_date = request.POST['CityIdate']
        if City.objects.filter(city_name=cityformvalue, state=state).exists():
            messages.info(request, 'city already exists')
            return redirect('Master_details')
        else :
            newcity = City.objects.create(city_name=cityformvalue, state=state,effective_date = effective_date,ineffective_date=ineffective_date)
            newcity.save()
            return redirect('Master_details')

    states = State.objects.all()
    context = {
        'states':states
    }
    return render(request, 'master/master_details.html', context=context)


@login_required (redirect_field_name='login', login_url='login')
def Masterdetails(request):
    print(SubProduct.objects.all()[0].product.product)
    context = {
        'qualifications'      : Qualification.objects.all(),
        'professions'         : Profession.objects.all(),
        'roles'               : Role.objects.all(),
        'products'            : Product.objects.all(),
        'subproducts'         : SubProduct.objects.all(),
        'customertypes'       : CustomerType.objects.all(),
        'designationtypes'    : DesignationType.objects.all(),
        'companytypes'        : CompanyType.objects.all(),
        'salarytypes'         : SalaryType.objects.all(),
        'residencetypes'      : ResidenceType.objects.all(),
        'banknames'           : BankName.objects.all(),
        'leadsources'         : LeadSource.objects.all(),
        'degrees'             : Degree.objects.all(),
        'nationalitys'        : Nationality.objects.all(),
        'states'              : State.objects.all(),
        'citys'               : City.objects.all(),
        'applicanttypes'      : ApplicantType.objects.all(),
        'propertyins'         : PropertyIn.objects.all(),
        'statues'             : Status.objects.all(),
        'natureofbusinesss'   : NatureOfBusiness.objects.all(),
        'ayyears'             : AYYear.objects.all(),
        'agreementtypes'      : AgreementType.objects.all(),
        'stageOfconstructions': StageOfConstruction.objects.all(),
        'rejectiontypes'      : RejectionType.objects.all(),
    }
    return render(request, 'master/master_details.html', context=context)

def editqualification(request, id):
    if request.method == 'POST':
        qualification = Qualification.objects.filter(id=id)
        newqualification = request.POST['Qualification']
        qualification.update(qualification=newqualification)
        return redirect('Master_details')
    print(Qualification.objects.filter(id=id)[0])
    context = {
        'qualification': Qualification.objects.filter(id=id)[0]
    }
    return render(request, 'master/qualification_edit.html', context=context)

def editprofession(request, id):
    if request.method == 'POST':
        profession = Profession.objects.filter(id=id)
        newprofession = request.POST['Profession']
        profession.update(profession=newprofession)
        return redirect('Master_details')
    print(Profession.objects.filter(id=id)[0])
    context = {
        'profession': Profession.objects.filter(id=id)[0]
    }
    return render(request, 'master/profession_edit.html', context=context)

def editrole(request, id):
    if request.method == 'POST':
        role = Role.objects.filter(id=id)
        newrole = request.POST['Role']
        role.update(role=newrole)
        return redirect('Master_details')
    print(Role.objects.filter(id=id)[0])
    context = {
        'role': Role.objects.filter(id=id)[0]
    }
    return render(request, 'master/role_edit.html', context=context)

def editproduct(request, id):
    if request.method == 'POST':
        product =Product.objects.filter(id=id)
        newproduct = request.POST['Product']
        product.update(product=newproduct)
        return redirect('Master_details')
    print(Product.objects.filter(id=id)[0])
    context = {
        'product': Product.objects.filter(id=id)[0]
    }
    return render(request, 'master/product_edit.html', context=context)

def editsubproduct(request, id):
    if request.method == 'POST':
        sub_product = SubProduct.objects.filter(id=id)
        newsubproduct = request.POST['SubProduct']
        sub_product.update(sub_product=newsubproduct)
        return redirect('Master_details')
    print(SubProduct.objects.filter(id=id)[0])
    context = {
        'product': SubProduct.objects.filter(id=id)[0]
    }
    return render(request, 'master/subproduct_edit.html', context=context)

def editcustomertype(request, id):
    if request.method == 'POST':
        cust_type = CustomerType.objects.filter(id=id)
        newcusttype = request.POST['CustomerType']
        cust_type.update(cust_type=newcusttype)
        return redirect('Master_details')
    print(CustomerType.objects.filter(id=id)[0])
    context = {
        'cust_type': CustomerType.objects.filter(id=id)[0]
    }
    return render(request, 'master/customertype_edit.html', context=context)

def editdesignationtype(request, id):
    if request.method == 'POST':
        desg_type = DesignationType.objects.filter(id=id)
        newdesgtype = request.POST['DesignationType']
        desg_type.update(desg_type=newdesgtype)
        return redirect('Master_details')
    print(DesignationType.objects.filter(id=id)[0])
    context = {
        'desg_type': DesignationType.objects.filter(id=id)[0]
    }
    return render(request, 'master/designationtype_edit.html', context=context)

def editcompanytype(request, id):
    if request.method == 'POST':
        company_type = CompanyType.objects.filter(id=id)
        newcomptype = request.POST['CompanyType']
        company_type.update(company_type=newcomptype)
        return redirect('Master_details')
    print(CompanyType.objects.filter(id=id)[0])
    context = {
        'company_type': CompanyType.objects.filter(id=id)[0]
    }
    return render(request, 'master/companytype_edit.html', context=context)

def editsalarytype(request, id):
    if request.method == 'POST':
        salary_type = SalaryType.objects.filter(id=id)
        newsaltype = request.POST['salaryType']
        salary_type.update(salary_type=newsaltype)
        return redirect('Master_details')
    print(SalaryType.objects.filter(id=id)[0])
    context = {
        'salary_type': SalaryType.objects.filter(id=id)[0]
    }
    return render(request, 'master/salarytype_edit.html', context=context)

def editresidencetype(request, id):
    if request.method == 'POST':
        residence_type = ResidenceType.objects.filter(id=id)
        newrestype = request.POST['resType']
        residence_type.update(residence_type=newrestype)
        return redirect('Master_details')
    print(ResidenceType.objects.filter(id=id)[0])
    context = {
        'residence_type': ResidenceType.objects.filter(id=id)[0]
    }
    return render(request, 'master/residencetype_edit.html', context=context)

def editbankname(request, id):
    if request.method == 'POST':
        bank_name = BankName.objects.filter(id=id)
        newbankname = request.POST['bankName']
        bank_name.update(bank_name=newbankname)
        return redirect('Master_details')
    print(BankName.objects.filter(id=id)[0])
    context = {
        'bank_name': BankName.objects.filter(id=id)[0]
    }
    return render(request, 'master/editbankname.html', context=context)

def editleadsource(request, id):
    if request.method == 'POST':
        lead_source = LeadSource.objects.filter(id=id)
        newleadsource = request.POST['leadSource']
        lead_source.update(lead_source=newleadsource)
        return redirect('Master_details')
    print(LeadSource.objects.filter(id=id)[0])
    context = {
        'lead_source': LeadSource.objects.filter(id=id)[0]
    }
    return render(request, 'master/leadsourceedit.html', context=context)

def editdegree(request, id):
    if request.method == 'POST':
        degree = Degree.objects.filter(id=id)
        newdegree = request.POST['degree']
        degree.update(degree=newdegree)
        return redirect('Master_details')
    print(Degree.objects.filter(id=id)[0])
    context = {
        'degree': Degree.objects.filter(id=id)[0]
    }
    return render(request, 'master/degree_edit.html', context=context)

def editnationality(request, id):
    if request.method == 'POST':
        nationality = Nationality.objects.filter(id=id)
        newnation = request.POST['nation']
        nationality.update(nationality=newnation)
        return redirect('Master_details')
    print(Nationality.objects.filter(id=id)[0])
    context = {
        'nationality': Nationality.objects.filter(id=id)[0]
    }
    return render(request, 'master/nationality_edit.html', context=context)

def editstate(request, id):
    if request.method == 'POST':
        state = State.objects.filter(id=id)
        newstate = request.POST['state']
        state.update(state=newstate)
        return redirect('Master_details')
    print(State.objects.filter(id=id)[0])
    context = {
        'state': State.objects.filter(id=id)[0]
    }
    return render(request, 'master/state_edit.html', context=context)

def editcity(request, id):
    if request.method == 'POST':
        city_name = City.objects.filter(id=id)
        newcity = request.POST['city']
        city_name.update(city_name=newcity)
        return redirect('Master_details')
    print(City.objects.filter(id=id)[0])
    context = {
        'city_name': City.objects.filter(id=id)[0]
    }
    return render(request, 'master/city_edit.html', context=context)

def editapplicanttype(request, id):
    if request.method == 'POST':
        applicant_type = ApplicantType.objects.filter(id=id)
        newapplicant = request.POST['ApplicantType']
        applicant_type.update(applicant_type=newapplicant)
        return redirect('Master_details')
    print(ApplicantType.objects.filter(id=id)[0])
    context = {
        'applicant_type': ApplicantType.objects.filter(id=id)[0]
    }
    return render(request, 'master/applicant_edit.html', context=context)

def editpropertyln(request, id):
    if request.method == 'POST':
        property_in = PropertyIn.objects.filter(id=id)
        newapropertyln = request.POST['PropertyIn']
        property_in.update(property_in=newapropertyln)
        return redirect('Master_details')
    print(PropertyIn.objects.filter(id=id)[0])
    context = {
        'property_in': PropertyIn.objects.filter(id=id)[0]
    }
    return render(request, 'master/propertyin_edit.html', context=context)

def editstatus(request, id):
    if request.method == 'POST':
        status = Status.objects.filter(id=id)
        newstatus = request.POST['Status']
        status.update(status=newstatus)
        return redirect('Master_details')
    print(Status.objects.filter(id=id)[0])
    context = {
        'status': Status.objects.filter(id=id)[0]
    }
    return render(request, 'master/status_edit.html', context=context)

def editnatureofbusiness(request, id):
    if request.method == 'POST':
        nature_business = NatureOfBusiness.objects.filter(id=id)
        newbusiness = request.POST['NatureBusiness']
        nature_business.update(nature_business=newbusiness)
        return redirect('Master_details')
    print(NatureOfBusiness.objects.filter(id=id)[0])
    context = {
        'nature_business': NatureOfBusiness.objects.filter(id=id)[0]
    }
    return render(request, 'master/natureofbusiness_edit.html', context=context)

def editayyear(request, id):
    if request.method == 'POST':
        ay_year = AYYear.objects.filter(id=id)
        newayyear = request.POST['AyYear']
        ay_year.update(ay_year=newayyear)
        return redirect('Master_details')
    print(AYYear.objects.filter(id=id)[0])
    context = {
        'ay_year': AYYear.objects.filter(id=id)[0]
    }
    return render(request, 'master/ayyear_edit.html', context=context)

def editagreementtype(request, id):
    if request.method == 'POST':
        agreement_type = AgreementType.objects.filter(id=id)
        newagreementtype = request.POST['AgreementType']
        agreement_type.update(agreement_type=newagreementtype)
        return redirect('Master_details')
    print(AgreementType.objects.filter(id=id)[0])
    context = {
        'agreement_type': AgreementType.objects.filter(id=id)[0]
    }
    return render(request, 'master/agreement_edit.html', context=context)

def editstageofconstruction(request, id):
    if request.method == 'POST':
        stage = StageOfConstruction.objects.filter(id=id)
        newstage = request.POST['Stage']
        stage.update(stage=newstage)
        return redirect('Master_details')
    print(StageOfConstruction.objects.filter(id=id)[0])
    context = {
        'stage': StageOfConstruction.objects.filter(id=id)[0]
    }
    return render(request, 'master/stageofconstruction_edit.html', context=context)

def editrejectiontype(request, id):
    if request.method == 'POST':
        rejection_type = RejectionType.objects.filter(id=id)
        newrejection = request.POST['Reason']
        rejection_type.update(rejection_type=newrejection)
        return redirect('Master_details')
    print(RejectionType.objects.filter(id=id)[0])
    context = {
        'rejection_type': RejectionType.objects.filter(id=id)[0]
    }
    return render(request, 'master/rejection_edit.html', context=context)
