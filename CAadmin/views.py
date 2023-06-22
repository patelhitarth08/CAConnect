from django.views.decorators.http import require_GET
from datetime import datetime
from django.utils.safestring import mark_safe
from django.db import transaction
import csv
import json
from django.core.files.storage import default_storage
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render

from CAadmin.models import Address, AuthorizedPerson, Client, Employee, Login, PersonalDetails, CA, Personal_file, General_file, Tag, Task
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import get_object_or_404
from django.contrib import messages

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

            login = Login()
            login.username = ca.username
            login.password = ca.password
            login.type = "Admin"
            login.save()

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

        login = Login.objects.filter(username=username).first()
        if login == None:
            contex = {
                'msg': "Username does not exist"
            }
            return render(request, 'login.html', contex)

        if check_password(password, login.password) != True:
            contex = {
                'msg': "password is invalid"
            }
            return render(request, 'login.html', contex)

        request.session['username'] = request.POST['username']
        request.session['type'] = login.type
        if login.type == "Admin":
            return render(request, template_name='dashboard.html')
        elif login.type == "Employee":
            return render(request, template_name='dashboard.html')
        else:
            client = Client.objects.filter(username=login.username).first()
            return redirect("/CAadmin/client-detail/"+str(client.id))

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
            with transaction.atomic():

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

                login = Login()
                login.username = client.username
                login.password = client.password
                login.type = "Client"
                login.save()

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
        try:
            with transaction.atomic():

                client = Client.objects.filter(id=client_id).first()

                type_form = request.POST['type_form']
                company_type = request.POST['company_type']
                r_status = request.POST['r_status']
                username = request.POST['username']
                name = request.POST['name']
                email = request.POST['email']
                p_number = request.POST['p_number']
                password = client.password
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

                a_names = request.POST.getlist('a_name')
                a_emails = request.POST.getlist('a_email')
                a_p_nos = request.POST.getlist('a_p_no')

                if check_password(password, make_password(c_password)) != True:
                    message = "Password does not match with Confirm Password"
                    context = {'message': message}
                    return render(request=request, template_name='client-edit.html', context=context)

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

                client.save()

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

                o_address.save()
                r_address.save()

                login = Login.objects.filter(
                    username=username).first()
                login.username = username
                login.password = make_password(password)
                login.type = "Client"
                login.save()

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


def ajax_demo(request):
    clients = Client.objects.all()
    context = {'clients': clients}
    return render(request=request, template_name='ajax-demo.html', context=context)


def show_client(request):
    if request.method == 'GET':
        client_name = request.GET.get('name', '')
        print(client_name)
        client = Client.objects.filter(name=client_name).first()
        response = None
        if client != None:
            response = 'Name: ' + client.name + '<br>' + \
                'Company Type: ' + str(client.company_type) + '<br>' + \
                'Residence Status: ' + str(client.residence_status) + '<br>' + \
                'Username: ' + str(client.username) + '<br>' + \
                'Email: ' + str(client.email) + '<br>' + \
                'Phone Number: ' + str(client.phone_number) + '<br>' + \
                'Birth Date: ' + str(client.birth_date) + '<br>' + \
                'Category: ' + str(client.category) + '<br>' + \
                'Group With: ' + str(client.group_with) + '<br>' + \
                'Status: ' + \
                ('Active' if client.status else 'Inactive') + '<br>'

        # Return the response as HTTP response
        return HttpResponse(response)


def change_status(request):
    if request.method == 'GET':
        type = request.GET.get('type', '')
        if type == "Client":
            clientId = request.GET.get('id', '')
            client = Client.objects.filter(id=clientId).first()
            if client:
                client.status = not client.status  # Toggle the status between True and False
                client.save()
        elif type == "Employee":
            EmployeeId = request.GET.get('id', '')
            employee = Employee.objects.filter(id=EmployeeId).first()
            if employee:
                # Toggle the status between True and False
                employee.status = not employee.status
                employee.save()


def client_list(request):
    clients = Client.objects.all()
    count = clients.count()
    client_auths = {}
    for client in clients:
        auth_person = AuthorizedPerson.objects.filter(client_id=client).first()
        client_auths[client.id] = auth_person.name
    client_auths_json = json.dumps(client_auths)
    print(client_auths_json)

    context = {'clients': clients, 'count': count,
               'client_auths': client_auths_json}
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
    person = request.session.get('type')

    client_ids = Personal_file.objects.values_list(
        'client_id', flat=True).distinct()
    personal_files = []

    for cli_id in client_ids:
        client1 = Client.objects.get(id=cli_id)
        files = Personal_file.objects.filter(client_id=cli_id).values()
        personal_files.append({'client': client1, 'files': files})
    print(personal_files)

    general_files = []
    client_ids = General_file.objects.values_list(
        'client_id', flat=True).distinct()

    for cli_id in client_ids:
        client2 = Client.objects.get(id=cli_id)
        files = General_file.objects.filter(client_id=cli_id).values()
        general_files.append({'client2': client2, 'files2': files})
    print(general_files)
    context = {'client': client, 'o_address': o_address,
               'r_address': r_address, 'auth_persons': auth_persons, 'person': person,
               'personal_files': personal_files, 'general_files': general_files}
    return render(request=request, template_name='client-detail.html', context=context)


def delete_client(request, client_id):
    client = Client.objects.filter(id=client_id).first()
    auth_persons = AuthorizedPerson.objects.filter(client_id=client_id).all()
    r_address = Address.objects.filter(
        client_id=client_id, type="Residence").first()
    o_address = Address.objects.filter(
        client_id=client_id, type="Office").first()

    for auth_person in auth_persons:
        auth_person.delete()

    r_address.delete()
    o_address.delete()

    client.delete()

    return redirect('/CAadmin/client_list')


def employees_list(request):
    employees = Employee.objects.all()
    count = employees.count()
    print(count)
    context = {'employees': employees, 'count': count}
    return render(request, template_name='employees-list.html', context=context)


def employee_create(request):
    if request.method == "POST":
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        c_password = request.POST['c_password']
        if password != c_password:
            message = "Password does not match with Confirm Password"
            context = {'message': message}
            return render(request=request, template_name='employee-create.html', context=context)

        try:
            with transaction.atomic():

                employee = Employee()
                employee.username = username
                employee.name = name
                employee.email = email
                employee.password = make_password(password)
                employee.save()

                login = Login()
                login.username = employee.username
                login.password = employee.password
                login.type = "Employee"
                login.save()

                return redirect('/CAadmin/employees-list')
        except IntegrityError:
            message = 'User already exists!'
            contex = {
                'message': message
            }
            return render(request, 'employee-create.html', contex)

    return render(request, template_name='employee-create.html')


def employee_edit(request, employee_id):
    if request.method == "POST":
        try:
            with transaction.atomic():
                employee = Employee.objects.filter(id=employee_id).first()
                if not check_password(request.POST['c_password'], employee.password):
                    message = "Password does not match with Confirm Password"
                    context = {'message': message}
                    return render(request=request, template_name='employee-edit.html', context=context)
                login = Login.objects.filter(
                    username=employee.username).first()
                employee.username = request.POST['username']
                employee.name = request.POST['name']

                employee.password = make_password(request.POST['c_password'])
                employee.save()

                login.username = employee.username
                login.password = employee.password
                login.save()
                return redirect('/CAadmin/employees-list')
        except IntegrityError:
            message = 'User already exists!'
            contex = {
                'message': message
            }
            return render(request, 'client-edit.html', contex)

    employee = Employee.objects.filter(id=employee_id).first()
    context = {'employee': employee}
    return render(request, template_name='employee-edit.html', context=context)


def employees_details(request, employee_id):
    employee = Employee.objects.filter(id=employee_id).first()
    context = {'employee': employee}
    return render(request, template_name='employees-details.html', context=context)


def delete_employee(request, employee_id):
    with transaction.atomic():
        employee = Employee.objects.filter(id=employee_id).first()
        login = Login.objects.filter(username=employee.username).first()
        employee.delete()
        login.delete()

    return redirect('/CAadmin/employees-list')


def add_personal(request, client_id):
    file_name = request.POST['file_name']
    description = request.POST['description']
    month = request.POST['month']
    year = request.POST['year']
    category = request.POST['category']
    number = request.POST['number']
    file = request.FILES.get('file')

    p_file = Personal_file()
    p_file.file_name = file_name
    p_file.description = description
    p_file.month = month
    p_file.year = year
    p_file.category = category
    p_file.number = number
    if file is not None:
        p_file.file = file
    client = get_object_or_404(Client, id=client_id)
    p_file.client_id = client.id

    p_file.save()
    return redirect('/CAadmin/client-detail/'+str(client_id))


def add_general(request, client_id):
    file_name = request.POST['file_name']
    description = request.POST['description']
    number = request.POST['number']
    file = request.FILES.get('file')

    g_file = General_file()
    g_file.file_name = file_name
    g_file.description = description
    g_file.number = number
    if file is not None:
        g_file.file = file
    client = get_object_or_404(Client, id=client_id)
    g_file.client_id = client.id

    g_file.save()

    return redirect('/CAadmin/client-detail/'+str(client_id))


def download_per_file(request, file_id):
    file_obj = get_object_or_404(Personal_file, id=file_id)

    # Retrieve the file data from the database
    file_data = file_obj.file.read()

    # Set the appropriate content type and headers
    response = HttpResponse(file_data, content_type="application/pdf")
    response['Content-Disposition'] = f'attachment; filename="{file_obj.file_name}"'

    return response


def download_gen_file(request, file_id):
    file_obj = get_object_or_404(General_file, id=file_id)

    # Retrieve the file data from the database
    file_data = file_obj.file.read()

    # Set the appropriate content type and headers
    response = HttpResponse(file_data, content_type="application/pdf")
    response['Content-Disposition'] = f'attachment; filename="{file_obj.file_name}"'

    return response


def view_per_file(request, file_id):
    file_obj = get_object_or_404(Personal_file, id=file_id)
    file_data = file_obj.file.read()
    content_type = "application/pdf"

    response = HttpResponse(file_data, content_type=content_type)
    # Optional: Specify to open the file in the browser
    response['Content-Disposition'] = 'inline'

    return response


def view_gen_file(request, file_id):
    file_obj = get_object_or_404(General_file, id=file_id)
    file_data = file_obj.file.read()
    content_type = "application/pdf"

    response = HttpResponse(file_data, content_type=content_type)
    # Optional: Specify to open the file in the browser
    response['Content-Disposition'] = 'inline'

    return response


def delete_per_file(request, file_id, client_id):
    file_obj = get_object_or_404(Personal_file, id=file_id)
    file_obj.delete()
    return redirect("/CAadmin/client-detail/" + str(client_id))


def delete_gen_file(request, file_id, client_id):
    file_obj = get_object_or_404(General_file, id=file_id)
    file_obj.delete()
    return redirect("/CAadmin/client-detail/" + str(client_id))


def task_list(request):
    if request.method == "POST":
        title = request.POST['task_title']
        description = request.POST['description']
        due_date_str = request.POST['due_date']
        due_date = datetime.strptime(due_date_str, "%d/%m/%Y").date()
        status = request.POST['status']
        assign_to = request.POST['assign_to']
        priority = request.POST['priority']
        tags = request.POST.getlist('tags')
        print(tags)
        start_date_str = request.POST['start_date']
        start_date = datetime.strptime(start_date_str, "%d/%m/%Y %H:%M")
        end_date_str = request.POST['end_date']
        end_date = datetime.strptime(end_date_str, "%d/%m/%Y %H:%M")

        tag_ids = []
        for tag_obj in tags:
            tag = Tag.objects.filter(name=tag_obj).first()
            if tag != None:
                tag_ids.append(tag.id)
            else:
                new_tag = Tag(name=tag_obj)
                new_tag.save()
                tag_ids.append(new_tag.id)

        task = Task(task_title=title, description=description, due_date=due_date, status=status,
                    assign_to=Employee.objects.filter(id=assign_to).first(), priority=priority, start_date=start_date, end_date=end_date)
        task.save()
        task.tags.set(tag_ids)
    tasks = Task.objects.all()
    employees = Employee.objects.all()
    tags = Tag.objects.all()
    task_data = []
    for task in tasks:
        task_data.append({
            'task': task,
            'employee_name': task.assign_to.name
        })

    context = {'task_data': task_data, 'employees': employees, 'tags': tags}
    return render(request, template_name="task-list.html", context=context)


def get_task_details(request):
    task_id = request.GET.get('taskId')
    task = get_object_or_404(Task, id=task_id)

    task_details = {
        'task_title': task.task_title,
        'description': task.description,
        # Convert datetime to string
        'due_date': task.due_date.strftime('%Y-%m-%d'),
        'status': task.status,
        'assign_to': task.assign_to.id,  # Assuming assign_to is a foreign key to User model
        'priority': task.priority,
        # Assuming tags is a ManyToManyField
        'tags': [tag.name for tag in task.tags.all()],
        # Convert datetime to string
        'start_date': task.start_date.strftime('%Y-%m-%d'),
        # Convert datetime to string
        'end_date': task.end_date.strftime('%Y-%m-%d')
    }

    return JsonResponse(task_details)


def update_task(request, task_id):
    if request.method == 'POST':
        if 'delete' in request.POST:
            task = get_object_or_404(Task, id=task_id)
            task.delete()
            return redirect("/CAadmin/task-list")
        task = get_object_or_404(Task, id=task_id)

        # Retrieve form data
        task.task_title = request.POST.get('task_title')
        task.description = request.POST.get('description')

        due_date_str = request.POST.get('due_date')
        task.due_date = datetime.strptime(due_date_str, "%d/%m/%Y").date()

        task.status = request.POST.get('status')
        assign_to = request.POST.get('assign_to')
        employee = Employee.objects.filter(id=assign_to).first()
        task.assign_to = employee
        task.priority = request.POST.get('priority')
        tags = request.POST.getlist('tags')
        tag_ids = []
        for tag_obj in tags:
            tag = Tag.objects.filter(name=tag_obj).first()
            if tag != None:
                tag_ids.append(tag.id)
            else:
                new_tag = Tag(name=tag_obj)
                new_tag.save()
                tag_ids.append(new_tag.id)
        task.tags.set(tag_ids)
        start_date_str = request.POST.get('start_date')
        task.start_date = datetime.strptime(start_date_str, "%d/%m/%Y %H:%M")
        end_date_str = request.POST.get('end_date')
        task.end_date = datetime.strptime(end_date_str, "%d/%m/%Y %H:%M")

        # Save the updated task
        task.save()

        return redirect("/CAadmin/task-list")

    # If the request method is not POST, return an error
    return redirect("/CAadmin/task-list")


def update_task_status(request):
    if request.method == 'GET':
        task_id = request.GET.get('taskId')
        column = request.GET.get('column')

        # Perform necessary validations and error handling
        if task_id is None or column is None:
            return HttpResponseBadRequest("Missing parameters")

        try:
            # Fetch the task from the database using the task_id
            task = Task.objects.filter(id=task_id).first()
            # Update the task status with the new column value
            task.status = column
            task.save()
            print(column)

            # Return a success response
            return HttpResponse("Task status updated successfully")
        except Task.DoesNotExist:
            return HttpResponseBadRequest("Task not found")

    return HttpResponseBadRequest("Invalid request method")
