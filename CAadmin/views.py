from django.core.files.storage import default_storage
from django.db import IntegrityError
from django.shortcuts import redirect, render

from CAadmin.models import Address, AuthorizedPerson, Client, PersonalDetails, CA
from django.contrib.auth.hashers import make_password, check_password


# Create your views here.
def ca_signup(request):
    msg = None
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        c_password = request.POST['c_password']
        if password != c_password:
            msg = "Password does not match with Confirm Password"
            context = {'msg': msg}
            return render(request=request, template_name='signup.html', context=context)

        try:
            ca = CA()
            ca.username = username
            ca.email = email
            ca.password = make_password(password)
            ca.save()
            return redirect('/CAadmin/login')
        except IntegrityError:
            msg = 'User already exists!'
            contex = {
                'msg': msg
            }
            return render(request, 'signup.html', contex)
    contex = {
        'msg': msg
    }
    return render(request=request, template_name='signup.html')


def login(request):
    msg = None
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        ca = CA.objects.filter(username=username).first()
        if ca == None:
            contex = {
                'msg': "Username does not exist"
            }
            return render(request, 'login.html', contex)

        if check_password(password, ca.password) != True:
            contex = {
                'msg': "password is invalid"
            }
            return render(request, 'login.html', contex)

        request.session['username'] = request.POST['username']
        return render(request, template_name='dashboard.html')
    contex = {'msg': msg}
    return render(request=request, template_name='login.html', context=contex)


def dashboard(request):
    return render(request=request, template_name='dashboard.html')


def contact_us(request):
    return render(request=request, template_name='contact-us.html')


def client_edit(request):
    if request.method == "POST":
        type_form = request.POST['type_form']
        company_type = request.POST['company_type']
        r_status = request.POST['r_status']
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        p_number = request.POST['p_number']
        password = request.POST['password']
        c_password = request.POST['c_password']
        category_type = request.POST['category_type']
        group = request.POST['group']
        dob = request.POST['dob']
        o_b_no = request.POST['o_b_no']
        o_f_no = request.POST['o_f_no']
        o_b_name = request.POST['o_b_name']
        o_road = request.POST['o_road']
        o_locality = request.POST['o_locality']
        o_city = request.POST['o_city']
        o_state = request.POST['o_state']
        o_pincode = request.POST['o_pincode']
        r_b_no = request.POST['r_b_no']
        r_f_no = request.POST['r_f_no']
        r_b_name = request.POST['r_b_name']
        r_road = request.POST['r_road']
        r_locality = request.POST['r_locality']
        r_city = request.POST['r_city']
        r_state = request.POST['r_state']
        r_pincode = request.POST['r_pincode']
        field_name = request.POST['field_name']
        details = request.POST['details']
        file = request.FILES.get('file')
        a_name = request.POST['a_name']
        a_email = request.POST['a_email']
        a_p_no = request.POST['a_p_no']

        if password != c_password:
            message = "Password does not match with Confirm Password"
            context = {'message': message}
            return render(request=request, template_name='client-edit.html', context=context)

        try:
            client = Client()

            client.client_type = type_form
            client.company_type = company_type
            client.residence_status = r_status
            client.username = username
            client.name = name
            client.email = email
            client.phone_number = p_number
            client.birth_date = dob
            client.category = category_type
            client.group_with = group
            client.password = make_password(password)

            o_address = Address()
            o_address.type = "Office"
            o_address.client = client
            o_address.building_number = o_b_no
            o_address.floor_number = o_f_no
            o_address.name_of_building = o_b_name
            o_address.street = o_road
            o_address.locality = o_locality
            o_address.city = o_city
            o_address.state = o_state
            o_address.pincode = o_pincode

            r_address = Address()
            r_address.type = "Residence"
            r_address.client = client
            r_address.building_number = r_b_no
            r_address.floor_number = r_f_no
            r_address.name_of_building = r_b_name
            r_address.street = r_road
            r_address.locality = r_locality
            r_address.city = r_city
            r_address.state = r_state
            r_address.pincode = r_pincode

            personal_details = PersonalDetails()
            personal_details.client = client
            personal_details.field_name = field_name
            personal_details.details = details
            personal_details.file = file

            authorized_person = AuthorizedPerson()
            authorized_person.client = client
            authorized_person.name = a_name
            authorized_person.email = a_email
            authorized_person.phone_number = a_p_no

            client.save()
            o_address.save()
            r_address.save()
            personal_details.save()
            authorized_person.save()

            return redirect('/CAadmin/dashboard')
        except IntegrityError:
            message = 'User already exists!'
            contex = {
                'message': message
            }
            return render(request, 'client-edit.html', contex)
    clients = Client.objects.all()
    message = None
    context = {'clients': clients, 'message': message}
    return render(request=request, template_name='client-edit.html', context=context)
