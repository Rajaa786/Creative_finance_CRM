from account.models import ReferralProfile, CustomUser
from master.models import Role, City
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from leadgenerator.settings import BASE_DIR, EMAIL_HOST_USER
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator, render_to_pdf
from django.urls import reverse
from django.http import HttpResponse
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth, Group
from django.contrib import messages


def get_tenure_months(current_age, retirement_age):
    return (retirement_age - current_age) * 12


def register_referral_logic(request):

    print(request.POST)
    group = Group.objects.get(name="Referral Partner")
    fname = request.POST["fname"]
    system_role = request.POST["system_role"]
    Email = request.POST["email"]
    phone = request.POST["phone"]
    password = request.POST["password"]
    profession = request.POST["profession"]
    if profession == "Other":
        profession = request.POST["other"]
    address = request.POST["address"]
    pincode = request.POST["pincode"]
    city = request.POST["city"]
    has_gst = request.POST["has_gst"]
    reference = request.POST["reference"]
    referral_code = request.POST.get("referral_code", "")
    if CustomUser.objects.filter(email=Email).exists():
        messages.info(request, "Email Taken")
        return redirect("register_referral")
    else:
        system_role = Role.objects.filter(role=system_role).first()
        city = City.objects.filter(city_name=city).first()
        print(profession)
        print(system_role)
        print(city)
        user = CustomUser.objects.create_user(
            username="default",
            password=password,
            system_role=system_role,
            email=Email,
            phone=phone,
            address=address,
            pincode=pincode,
            city=city,
        )

        print(user)
        user.mapped_to_dept = "Admin"
        user.reporting_head = "Admin"
        user.is_active = False
        user.groups.add(group)
        user.save()

    referral_profile = ReferralProfile.objects.create(
        user=user,
        full_name=fname,
        profession=profession,
        has_GST=has_gst,
        reference=reference,
        referral_code=referral_code,
    )
    referral_profile.save()
    ini = ""
    if referral_profile.profession == "Salaried":
        ini += "SAL"
    elif referral_profile.profession == "Self Employed":
        ini += "SE"
    elif referral_profile.profession == "Freelancer":
        ini += "FL"
    elif referral_profile.profession == "Student":
        ini += "ST"
    elif referral_profile.profession == "Home Maker":
        ini += "HM"
    elif referral_profile.profession == "DSA":
        ini += "DSA"
    elif referral_profile.profession == "Insurance Agent":
        ini += "IA"
    elif referral_profile.profession == "Chartered Accountant":
        ini += "CA"
    elif referral_profile.profession == "Tax Consultants":
        ini += "TC"
    elif referral_profile.profession == "Banker":
        ini += "BNK"
    elif referral_profile.profession == "Company Secretary":
        ini += "CS"
    elif referral_profile.profession == "Real Estate Agent":
        ini += "REA"
    elif referral_profile.profession == "Builder":
        ini += "BLD"
    else:
        ini += "O"
    if user.system_role.role == "Referral Partner":
        ini += "RP"
    num = "{:04d}".format(user.id)
    newusername = ini + num
    user.username = newusername
    user.save()
    if user.system_role.role == "Referral Partner":
        ini = "ORP"
        num = "{:03d}".format(user.id)
        newusername = ini + num
        user.username = newusername
        user.save()
    uidb64_pk = urlsafe_base64_encode(force_bytes(user.pk))
    uidb64_hash = urlsafe_base64_encode(force_bytes(password))
    domain = get_current_site(request).domain
    link = reverse(
        "activate",
        kwargs={
            "uidb64_pk": uidb64_pk,
            "uidb64_hash": uidb64_hash,
            "token": token_generator.make_token(user),
        },
    )
    activate_url = "http://" + domain + link
    email_body = (
        "Hi "
        + referral_profile.full_name
        + " Please use this link to verify your account\n"
        + activate_url
    )
    email = EmailMessage(
        "Activate your account",
        email_body,
        "rohan@gmail.com",
        [Email],
    )
    email.send(fail_silently=False)
    # template = get_template('account/Agreement.html')
    context = {"partner_name": referral_profile.full_name}
    # html = template.render(context)
    pdf = render_to_pdf("account/Agreement.html", context)

    response = HttpResponse(pdf, content_type="application/pdf")
    filename = "Agreement_%s.pdf" % (user.username)

    content = "attachment; filename='%s'" % (filename)
    response["Content-Disposition"] = 'attachment; filename="report.pdf"'
    referral_profile.agreement.save(filename, ContentFile(pdf.content))
    print(referral_profile.agreement)
    message = "this is test mail"
    subject = "terms and conditions"
    mail_id = request.POST.get("email", "")
    email = EmailMessage(
        subject,
        message,
        EMAIL_HOST_USER,
        [
            mail_id,
        ],
    )
    email.content_subtype = "html"

    email.send()

    return redirect("email_ver_msg")

    # return referral

    pass


def register_vendor_logic():
    pass


def register_staff_logic():
    pass


register_manager_dict = {
    "Referral Partner": register_referral_logic,
    "Vendor": register_vendor_logic,
}
