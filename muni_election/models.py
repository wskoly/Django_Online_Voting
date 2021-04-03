from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext, gettext_lazy as _

#redefined user model for authenication
class user(AbstractUser):
    phone = models.CharField(verbose_name=_('Phone'),max_length=14)
    is_voter = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural= _('User Information')

#relational model voter area
class voter_area(models.Model):
    code = models.CharField(verbose_name=_('Area Code'), max_length=200, primary_key=True)
    name = models.CharField(verbose_name=_('Area Name'),max_length=200)
    subDist = models.CharField(verbose_name=_('Sub-district'),max_length=200)
    dist = models.CharField(verbose_name=_('District'),max_length=200)
    div = models.CharField(verbose_name=_('Division'),max_length=200)

    def __str__(self):
        return self.name +"(Code:"+ self.code+")"
    class Meta:
        verbose_name_plural = _("Voting Area Information")

#voter model which also has OneToOne relation with user model
class voter(models.Model):
    gen_choice = (('Male',_('Male')),('Female',_('Female')),('Others',_('Others')),)

    user = models.OneToOneField(user, verbose_name=_('User Name'), on_delete=models.CASCADE)
    voter_id = models.CharField(max_length=17, verbose_name=_('Voter ID'), primary_key=True, unique=True)
    area = models.ForeignKey(voter_area, verbose_name=_('Voter Area'), on_delete=models.CASCADE)
    serial = models.IntegerField(verbose_name=_('Voter Serial'),)
    dob = models.DateField(verbose_name=_('Date of birth'), help_text=_("Date of birth should be in a format of mm/dd/yyyy"))
    gender = models.CharField(verbose_name=_('Gender'),max_length=20,choices=gen_choice)
    ward = models.IntegerField(verbose_name=_('Ward'))
    municipality = models.CharField(verbose_name=_('Municipality'),max_length=50)
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    def get_email(self):
        return self.user.email
    def get_phone(self):
        return self.user.phone
    def __str__(self):
        return self.voter_id
    get_name.short_description = _("Full name")
    get_email.short_description = _('Email')
    get_phone.short_description = _('Phone')
    class Meta:
        verbose_name_plural = _("Voters Information")

#staff model
class election_staff(models.Model):
    role_choice = (('Data Migrator',_('Data Migrator')),('Election Manager',_('Election Manager')))

    user = models.OneToOneField(user, verbose_name=_('User Name'), on_delete=models.CASCADE)
    role = models.CharField(max_length=200, verbose_name=_('Staffs Role'), choices=role_choice)
    def staff_name(self):
        return self.user.first_name+" "+self.user.last_name
    def __str__(self):
        return str(self.user)
    class Meta:
        verbose_name_plural = _("ELection Staff's Information")

#election model
class election(models.Model):
    name = models.CharField(verbose_name=_('Election Name'), max_length=255)
    num_of_ward = models.IntegerField(verbose_name=_('Number of Ward'),)
    is_open = models.BooleanField(verbose_name=_('Is Open'),default=False)
    is_res_published = models.BooleanField(verbose_name=_('Is Result Published'),default=False)
    election_areas = models.ManyToManyField(voter_area)

    def area_names(self):
        return ", ".join([str(e.name) for e in self.election_areas.all()])
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = _("Election Information")

class mayor_candidate(models.Model):
    symbol_choices = (('elec_symbol/mayor/nouka.png', _('Nouka')),
                     ('elec_symbol/mayor/dhaner_shish.png', _('Dhaner Shish')),
                     ('elec_symbol/mayor/langol.png', _('Langol')),
                     ('elec_symbol/mayor/anarash.png', _('Anarash')),
                     ('elec_symbol/mayor/chaka.png', _('Chaka')),
                     ('elec_symbol/mayor/chata.png', _('Chata')),
                     ('elec_symbol/mayor/kaste.png', _('Kaste')),
                     ('elec_symbol/mayor/moi.png', _('Moi')),
                     ('elec_symbol/mayor/moshal.png', _('Moshal')),
                     )
    election_id = models.ForeignKey(election, verbose_name=_('ELection'), on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_('Candidate Name'),max_length=200)
    picture = models.ImageField(verbose_name=_('Candidate Picture'),upload_to = 'candidate_pic/')
    symbol = models.ImageField(verbose_name=_('Candidate Symbol'), choices=symbol_choices)
    vote_count = models.IntegerField(verbose_name=_('Vote Count'),default=0)

    def __str__(self):
        return self.name+"(election:"+ str(self.election_id)+")"
    class Meta:
        verbose_name_plural = _("Mayor Candidates Information")

class councilor_candidate(models.Model):
    symbol_choices = (('elec_symbol/councilor/austrich.png', _('Uut Pakhi')),
                      ('elec_symbol/councilor/dalim.png', _('Dalim')),
                      ('elec_symbol/councilor/lamp.png', _('Table Lamp')),
                      ('elec_symbol/councilor/screw_driver.png', _('Screw Driver')),
                      ('elec_symbol/councilor/water_bottle.png', _('Water Bottle')),
                      )
    election_id = models.ForeignKey(election,verbose_name=_('ELection'), on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_('Candidate Name'),max_length=200)
    picture = models.ImageField(verbose_name=_('Candidate Picture'),upload_to='candidate_pic/')
    symbol = models.ImageField(verbose_name=_('Candidate Symbol'), choices=symbol_choices)
    ward_no = models.IntegerField(verbose_name=_('Candidate Ward'))
    vote_count = models.IntegerField(verbose_name=_('Vote Count'),default=0)
    def __str__(self):
        return self.name+"(election:"+ str(self.election_id)+")"
    class Meta:
        verbose_name_plural = _("Councilors Candidate Information")

class re_councilor_candidate(models.Model):
    symbol_choices = (('elec_symbol/reserve_councilor/golap.png', _('Golap')),
                      ('elec_symbol/reserve_councilor/haat_pakha.png', _('Haat Pakha')),
                      ('elec_symbol/reserve_councilor/harricane.png', _('Harricane')),
                      ('elec_symbol/reserve_councilor/joba.png', _('Joba')),
                      ('elec_symbol/reserve_councilor/mom_bati.png', _('Mom Bati')),
                      )
    election_id = models.ForeignKey(election,verbose_name='ELection', on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_('Candidate Name'),max_length=200)
    picture = models.ImageField(verbose_name=_('Candidate Picture'),upload_to='candidate_pic/')
    symbol = models.ImageField(verbose_name=_('Candidate Symbol'), choices=symbol_choices)
    reserve_ward_1 = models.IntegerField(verbose_name=_('Candidate Ward 1'))
    reserve_ward_2 = models.IntegerField(verbose_name=_('Candidate Ward 2'))
    reserve_ward_3 = models.IntegerField(verbose_name=_('Candidate Ward 3'))
    vote_count = models.IntegerField(_('Vote Count'),default=0)
    def __str__(self):
        return self.name+"(election:"+ str(self.election_id)+")"
    class Meta:
        verbose_name_plural = _("Reserve Councilors Candidate Information")

class vote_store(models.Model):
    voter_hash = models.CharField(max_length=128, editable=False)
    election_id = models.ForeignKey(election, on_delete=models.CASCADE, editable=False)
    mayor_candidate = models.ForeignKey(mayor_candidate, on_delete=models.CASCADE, editable=False)
    councilor_candidate = models.ForeignKey(councilor_candidate, on_delete=models.CASCADE, editable=False)
    re_councilor_candidate = models.ForeignKey(re_councilor_candidate, on_delete=models.CASCADE, editable=False)

class is_voted(models.Model):
    election_id = models.ForeignKey(election, on_delete=models.CASCADE, editable=False)
    user = models.ForeignKey(user,on_delete=models.CASCADE, editable=False)
    ward = models.IntegerField(editable=False)

class voter_migration(models.Model):
    migration_date = models.DateTimeField(auto_now=True)
    start_date = models.DateField(help_text=_('The starting date of birth parameter'))
    end_date = models.DateField(help_text=_('The ending date of birth parameter'))
    class Meta:
        default_permissions = ('add', 'delete', 'view')
        verbose_name_plural = _("Migrate Voters From National DB")
        app_label = 'muni_election'







