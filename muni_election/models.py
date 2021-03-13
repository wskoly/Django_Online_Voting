from django.db import models
from django.contrib.auth.models import AbstractUser
#redefined user model for authenication
class user(AbstractUser):
    phone = models.CharField(max_length=14)
    is_voter = models.BooleanField(default=False)

#relational model voter area
class voter_area(models.Model):
    area_code = models.CharField(max_length=200, primary_key=True)
    area_name = models.CharField(max_length=200)
    area_subDist = models.CharField(max_length=200)
    area_dist = models.CharField(max_length=200)
    area_div = models.CharField(max_length=200)

#voter model which also has OneToOne relation with user model
class voter(models.Model):
    voter_user = models.OneToOneField(user, on_delete=models.CASCADE)
    voter_id = models.CharField(max_length=17, primary_key=True, unique=True)
    voter_area = models.ForeignKey(voter_area, on_delete=models.CASCADE)
    voter_serial = models.IntegerField()
    voter_dob = models.DateField()
    voter_gender = models.CharField(max_length=20)
    voter_ward = models.IntegerField()
    municipality = models.CharField
#staff model
class election_staff(models.Model):
    staff_user = models.OneToOneField(user, on_delete=models.CASCADE)
    staff_role = models.CharField(max_length=200)

class election(models.Model):
    election_name = models.CharField(max_length=255)
    num_of_ward = models.IntegerField()
    is_open = models.BooleanField(default=False)
    is_res_published = models.BooleanField(default=False)

class election_areas(models.Model):
    election_id = models.ForeignKey(election, on_delete=models.CASCADE)
    voter_area = models.ForeignKey(voter_area, on_delete=models.CASCADE)

class mayor_candidate(models.Model):
    election_id = models.ForeignKey(election, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    symbol = models.ImageField(upload_to='elec_symbol/')
    vote_count = models.IntegerField()

class m_councilor_candidate(models.Model):
    election_id = models.ForeignKey(election, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    symbol = models.ImageField(upload_to='elec_symbol/')
    ward_no = models.IntegerField()
    vote_count = models.IntegerField()

class fe_councilor_candidate(models.Model):
    election_id = models.ForeignKey(election, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    symbol = models.ImageField(upload_to='elec_symbol/')
    start_ward = models.IntegerField()
    end_ward = models.IntegerField()
    vote_count = models.IntegerField()







