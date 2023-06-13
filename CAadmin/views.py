import csv
import json
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


def client_add(request):
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
        # field_names = request.POST.getlist('field_name')
        # details = request.POST.getlist('details')
        # files = request.FILES.getlist('file')
        a_names = request.POST.getlist('a_name')
        a_emails = request.POST.getlist('a_email')
        a_p_nos = request.POST.getlist('a_p_no')

        if password != c_password:
            message = "Password does not match with Confirm Password"
            context = {'message': message}
            return render(request=request, template_name='client-add.html', context=context)

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

            # personal_details = PersonalDetails()
            # personal_details.client = client
            # personal_details.field_name = field_name
            # personal_details.details = details
            # personal_details.file = file

            client.save()
            # index = 0
            # for field_name in field_names:
            #     personal_details = PersonalDetails()
            #     personal_details.client = client
            #     personal_details.field_name = field_name
            #     personal_details.details = details[index]
            #     personal_details.file = files[index]
            #     personal_details.save()
            #     index = index + 1

            index = 0
            for a_name in a_names:
                authorized_person = AuthorizedPerson()
                authorized_person.client = client
                authorized_person.name = a_name
                authorized_person.email = a_emails[index]
                authorized_person.phone_number = a_p_nos[index]
                authorized_person.save()
                index = index + 1

            o_address.save()
            r_address.save()

            return redirect('/CAadmin/client-list')
        except IntegrityError:
            message = 'User already exists!'
            contex = {
                'message': message
            }
            return render(request, 'client-add.html', contex)
    clients = Client.objects.all()

    states_cities_data = {}
    with open('states_cities.csv', 'r',  encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row

        for row in reader:
            state = row[0]
            cities = row[1:]

            if state not in states_cities_data:
                states_cities_data[state] = []

            states_cities_data[state].extend(cities)
        states_cities_data = dict(sorted(states_cities_data.items()))
        states_cities_json = json.dumps(states_cities_data)

    message = None
    edit = False
    context = {'clients': clients, 'message': message,
               'edit': edit, 'states_cities_data': states_cities_json}
    return render(request=request, template_name='client-add.html', context=context)


def client_edit(request, client_id):
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
        # field_names = request.POST.getlist('field_name')
        # details = request.POST.getlist('details')
        # files = request.FILES.getlist('file')
        a_names = request.POST.getlist('a_name')
        a_emails = request.POST.getlist('a_email')
        a_p_nos = request.POST.getlist('a_p_no')

        if password != c_password:
            message = "Password does not match with Confirm Password"
            context = {'message': message}
            return render(request=request, template_name='client-edit.html', context=context)

        try:
            client = Client.objects.filter(id=client_id).first()

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

            o_address = Address.objects.filter(
                client_id=client_id, type="Office").first()
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

            r_address = Address.objects.filter(
                client_id=client_id, type="Residence").first()
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

            # personal_details = PersonalDetails()
            # personal_details.client = client
            # personal_details.field_name = field_name
            # personal_details.details = details
            # personal_details.file = file

            client.save()
            # index = 0
            # personal_details = PersonalDetails.objects.filter(
            #     client_id=client_id).all()
            # for personal_detail in personal_details:
            #     personal_detail.client = client
            #     personal_detail.field_name = field_names[index]
            #     personal_detail.details = details[index]
            #     personal_detail.file = files[index]
            #     personal_detail.save()
            #     index = index + 1

            # if len(field_names) > index:
            #     remaining = len(field_names) - index
            #     for obj in remaining:
            #         personal_details = PersonalDetails()
            #         personal_details.client = client
            #         personal_details.field_name = field_names[index]
            #         personal_details.details = details[index]
            #         personal_details.file = files[index]
            #         personal_details.save()
            #         index = index + 1
            authorized_persons = AuthorizedPerson.objects.filter(
                client_id=client_id).all()
            if isinstance(authorized_persons, list) == False:
                authorized_persons.delete()
            else:
                for authorized_person in authorized_persons:
                    authorized_person.delete()

            index = 0
            for a_name in a_names:
                authorized_person = AuthorizedPerson()
                authorized_person.client = client
                authorized_person.name = a_name
                authorized_person.email = a_emails[index]
                authorized_person.phone_number = a_p_nos[index]
                authorized_person.save()
                index = index + 1

            # index = 0
            # authorized_persons = AuthorizedPerson.objects.filter(
            #     client_id=client_id).all()
            # new_auths = 0
            # if isinstance(a_names, list) == False:
            #     new_auths = 1
            # else:
            #     new_auths = a_names.count()

            # curr_auths = 0
            # if isinstance(authorized_persons, list) == False:
            #     curr_auths = 1
            # else:
            #     curr_auths = authorized_persons.count()

            # if curr_auths > 1:
            #     for authorized_person in authorized_persons:
            #         if new_auths != 0:
            #             authorized_person.client = client
            #             authorized_person.name = a_names[index]
            #             authorized_person.email = a_emails[index]
            #             authorized_person.phone_number = a_p_nos[index]
            #             authorized_person.save()
            #             index = index + 1
            #             new_auths = new_auths - 1
            #         else:
            #             authorized_person.delete()
            # else:
            #     for authorized_person in authorized_persons:
            #         authorized_person.client = client
            #         authorized_person.name = a_names[index]
            #         authorized_person.email = a_emails[index]
            #         authorized_person.phone_number = a_p_nos[index]
            #         authorized_person.save()
            #         index = index + 1

            # if len(a_names) > index:
            #     remaining = len(a_names) - index
            #     if isinstance(remaining, list):
            #         for obj in remaining:
            #             authorized_person = AuthorizedPerson()
            #             authorized_person.client = client
            #             authorized_person.name = a_names[index]
            #             authorized_person.email = a_emails[index]
            #             authorized_person.phone_number = a_p_nos[index]
            #             authorized_person.save()
            #             index = index + 1
            #     else:
            #         authorized_person = AuthorizedPerson()
            #         authorized_person.client = client
            #         authorized_person.name = a_names[index]
            #         authorized_person.email = a_emails[index]
            #         authorized_person.phone_number = a_p_nos[index]
            #         authorized_person.save()
            #         index = index + 1

            o_address.save()
            r_address.save()

            return redirect('/CAadmin/client-list')
        except IntegrityError:
            message = 'User already exists!'
            contex = {
                'message': message
            }
            return render(request, 'client-edit.html', contex)
    client = Client.objects.filter(id=client_id).first()
    auth_persons = AuthorizedPerson.objects.filter(client_id=client_id).all()
    r_address = Address.objects.filter(
        client_id=client_id, type="Residence").first()
    o_address = Address.objects.filter(
        client_id=client_id, type="Office").first()

    states_cities_data = {}
    with open('states_cities.csv', 'r',  encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row

        for row in reader:
            state = row[0]
            cities = row[1:]

            if state not in states_cities_data:
                states_cities_data[state] = []

            states_cities_data[state].extend(cities)
        states_cities_data = dict(sorted(states_cities_data.items()))
        states_cities_json = json.dumps(states_cities_data)
        # print(states_cities_data)

    message = None
    edit = True
    context = {'client': client, 'auth_persons': auth_persons, 'r_address': r_address,
               'o_address': o_address, 'message': message, 'edit': edit, 'states_cities_data': states_cities_json}
    return render(request=request, template_name='client-edit.html', context=context)


def client_list(request):
    clients = Client.objects.all()
    count = clients.count()
    context = {'clients': clients, 'count': count}
    return render(request=request, template_name='client-list.html', context=context)


def client_detail(request, client_id):
    client = Client.objects.filter(id=client_id).first()
    auth_persons = AuthorizedPerson.objects.filter(client_id=client_id).all()
    r_address = Address.objects.filter(
        client_id=client_id, type="Residence").first()
    o_address = Address.objects.filter(
        client_id=client_id, type="Office").first()
    # p_details = PersonalDetails.objects.filter(
    #     client_id=client_id).all()
    context = {'client': client, 'o_address': o_address,
               'r_address': r_address, 'auth_persons': auth_persons}
    return render(request=request, template_name='client-detail.html', context=context)


def delete_client(request, client_id):
    client = Client.objects.filter(id=client_id).first()
    auth_persons = AuthorizedPerson.objects.filter(client_id=client_id).all()
    r_address = Address.objects.filter(
        client_id=client_id, type="Residence").first()
    o_address = Address.objects.filter(
        client_id=client_id, type="Office").first()
    # p_details = PersonalDetails.objects.filter(
    # client_id=client_id).all()

    for auth_person in auth_persons:
        auth_person.delete()

    r_address.delete()
    o_address.delete()

    # for p_detail in p_details:
    #     p_detail.delete()

    client.delete()

    return redirect('/CAadmin/client_list')


def toggle_status(request):
    client_id = request.POST['client_id']
    client = Client.objects.filter(id=client_id).first()
    if client.status == 1:
        client.status = 0
    else:
        client.status = 1
    client.save()
    return redirect('/CAadmin/client-detail/' + client_id)
