from django.db import models


class Login(models.Model):
    TYPES = (
        ('Admin', 'Admin'),
        ('Employee', 'Client'),
        ('Client', 'Client'),
    )

    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPES)


class CA(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Client(models.Model):
    CLIENT_TYPES = (
        ('Individual', 'Individual'),
        ('Company', 'Company'),
    )
    RESIDENCE_STATUSES = (
        ('Resident', 'Resident'),
        ('Non-Resident', 'Non-Resident'),
    )
    CATEGORIES = (
        ('Category A', 'Category A'),
        ('Category B', 'Category B'),
        ('Category C', 'Category C'),
    )
    GROUP_WITH_OPTIONS = (
        ('Group 1', 'Group 1'),
        ('Group 2', 'Group 2'),
        ('Group 3', 'Group 3'),
    )
    client_type = models.CharField(max_length=10, choices=CLIENT_TYPES)
    company_type = models.CharField(max_length=50, blank=True, null=True)
    residence_status = models.CharField(
        max_length=50, choices=RESIDENCE_STATUSES)
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    birth_date = models.DateField()
    category = models.CharField(max_length=50, choices=CATEGORIES)
    group_with = models.CharField(max_length=50, choices=GROUP_WITH_OPTIONS)
    password = models.CharField(max_length=100)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.username


class Address(models.Model):
    CITY_OPTIONS = (
        ('City 1', 'City 1'),
        ('City 2', 'City 2'),
        ('City 3', 'City 3'),
    )
    STATE_OPTIONS = (
        ('State 1', 'State 1'),
        ('State 2', 'State 2'),
        ('State 3', 'State 3'),
    )
    TYPES = (
        ('Office', 'Office'),
        ('Residence', 'Residence'),
    )
    type = models.CharField(max_length=50, choices=TYPES)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    building_number = models.CharField(max_length=50)
    floor_number = models.CharField(max_length=50)
    name_of_building = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    locality = models.CharField(max_length=100)
    city = models.CharField(max_length=50, choices=CITY_OPTIONS)
    state = models.CharField(max_length=50, choices=STATE_OPTIONS)
    pincode = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.client.username}'s Residence Address"


class PersonalDetails(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=100)
    details = models.TextField()
    file = models.FileField()

    def __str__(self):
        return f"{self.client.username}'s Personal Details"


class AuthorizedPerson(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Employee(models.Model):
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    status = models.BooleanField(default=True)

class Personal_file(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, default=None)
    file_name = models.CharField(max_length=50)
    category = models.CharField(max_length=20)
    month = models.CharField(max_length=15)
    year = models.CharField(max_length=15)
    description = models.CharField(max_length=100)
    number = models.CharField(max_length=20)
    file = models.FileField(upload_to='media/personal_files')

class General_file(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, default=None)
    file_name = models.CharField(max_length=50)
    number = models.CharField(max_length=15)
    description = models.CharField(max_length=50)
    file = models.FileField(upload_to='media/general_files')
