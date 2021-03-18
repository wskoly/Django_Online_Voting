from django.db import models
from django.contrib.auth.models import AbstractUser
#redefined user model for authenication
class user(AbstractUser):
    phone = models.CharField(max_length=14)
    is_voter = models.BooleanField(default=False)

#relational model voter area
class voter_area(models.Model):
    code = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    subDist = models.CharField(max_length=200)
    dist = models.CharField(max_length=200)
    div = models.CharField(max_length=200)

    def __str__(self):
        return self.name +"(Code:"+ self.code+")"

#voter model which also has OneToOne relation with user model
class voter(models.Model):
    gen_choice = (('Male','Male'),('Female','Female'),('Others','Others'),)

    user = models.OneToOneField(user, on_delete=models.CASCADE)
    voter_id = models.CharField(max_length=17, primary_key=True, unique=True)
    area = models.ForeignKey(voter_area, on_delete=models.CASCADE)
    serial = models.IntegerField()
    dob = models.DateField(verbose_name='Date of birth', help_text="Date of birth should be in a format of mm/dd/yyyy")
    gender = models.CharField(max_length=20,choices=gen_choice)
    ward = models.IntegerField()
    municipality = models.CharField(max_length=50)
    def __str__(self):
        return self.voter_id

#staff model
class election_staff(models.Model):
    role_choice = (('Data Migrator','Data Migrator'),('Election Manager','Election Manager'))

    user = models.OneToOneField(user, on_delete=models.CASCADE)
    role = models.CharField(max_length=200, choices=role_choice)
    def __str__(self):
        return self.user

#election model
class election(models.Model):
    name = models.CharField(max_length=255)
    num_of_ward = models.IntegerField()
    is_open = models.BooleanField(default=False)
    is_res_published = models.BooleanField(default=False)
    election_areas = models.ManyToManyField(voter_area)

    def __str__(self):
        return self.election_name

class mayor_candidate(models.Model):
    election_id = models.ForeignKey(election, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    picture = models.ImageField(upload_to = 'candidate_pic/')
    symbol = models.ImageField(upload_to='elec_symbol/')
    vote_count = models.IntegerField()

    def __str__(self):
        return self.name+"(election_id:"+ self.election_id+")"

class m_councilor_candidate(models.Model):
    election_id = models.ForeignKey(election, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    symbol = models.ImageField(upload_to='elec_symbol/')
    ward_no = models.IntegerField()
    vote_count = models.IntegerField()
    def __str__(self):
        return self.name+"(election_id:"+ self.election_id+")"

class fe_councilor_candidate(models.Model):
    election_id = models.ForeignKey(election, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    symbol = models.ImageField(upload_to='elec_symbol/')
    start_ward = models.IntegerField()
    end_ward = models.IntegerField()
    vote_count = models.IntegerField()
    def __str__(self):
        return self.name+"(election_id:"+ self.election_id+")"







