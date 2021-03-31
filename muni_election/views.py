from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout,get_user_model
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict as mTd
from django.utils.translation import gettext, gettext_lazy as _, get_language,activate
from django.contrib.auth.hashers import make_password as voter_hasher
from django.core.exceptions import ObjectDoesNotExist
from  .utilities import *
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

#index view
def index(request):
    if request.user.is_authenticated and request.user.is_voter:
        return redirect('vote')
    if request.method == 'POST':
        form = VoterLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request,username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('vote')
    else:
        form = VoterLoginForm()
    context = {'form':form}
    return render(request,'main/index.html',context)

@login_required(login_url='index')
def vote(request):
    if request.user.is_voter:
        wc = "Welcome "+request.user.first_name+" "+request.user.last_name
        user = request.user
        vot = voter.objects.get(user = user)
        area = vot.area.code
        ward = vot.ward
        request.session['ward'] = ward
        try:
            election_id = election.election_areas.through.objects.get(voter_area_id=area).election_id
        except ObjectDoesNotExist:
            election_id = None
        if election_id:
            electionObj = election.objects.get(pk=election_id)
            request.session['election_id'] = election_id
            #request.session['electionObj'] = electionObj
            IS_VOTED = is_voted.objects.filter(Q(election_id=electionObj)&Q(user=user)).exists()
            if not IS_VOTED:
                if request.method == 'POST':
                    try:
                        #election_id = election.election_areas.through.objects.get(voter_area_id=area).election_id
                        #electionObj = election.objects.get(pk=election_id)
                        voter_hash = voter_hasher(vot.voter_id)
                        mayor_vote = request.POST['mayor']
                        mayorObj = mayor_candidate.objects.get(pk=mayor_vote)
                        councilor_vote = request.POST['councilor']
                        councilorObj = councilor_candidate.objects.get(pk=councilor_vote)
                        re_councilor_vote = request.POST['re_councilor']
                        re_councilorObj = re_councilor_candidate.objects.get(pk=re_councilor_vote)
                        votes = vote_store(voter_hash=voter_hash, election_id=electionObj, mayor_candidate=mayorObj, councilor_candidate = councilorObj, re_councilor_candidate=re_councilorObj)
                        voted = is_voted(election_id=electionObj, user = user, ward=ward)
                        votes.save()
                        voted.save()
                        calculate_vote(election_id)
                        return redirect('vote_done')
                    except Exception as e:
                        print(e)
                    print(request.POST['mayor'])
                    print(request.POST['councilor'])
                    print(request.POST['re_councilor'])
                try:
                    #election_id = election.election_areas.through.objects.get(voter_area_id=area).election_id
                    #electionObj = election.objects.get(pk=election_id)
                    mayor = mayor_candidate.objects.filter(election_id=election_id)
                    councilors = councilor_candidate.objects.filter(Q(election_id=election_id) & Q(ward_no =ward))
                    re_councilors = re_councilor_candidate.objects.filter(Q(election_id=election_id) &(Q(reserve_ward_1 = ward)|Q(reserve_ward_2 = ward)|Q(reserve_ward_3 = ward)))
                    if electionObj.is_open:
                        context = {'welcome':wc, 'voter':mTd(electionObj),'area':area, 'election':electionObj.name,
                                   'mayor':mayor, 'councilors':councilors, 're_councilors':re_councilors,'has_election':True,'is_open':True, 'is_voted':False}
                    else:
                        context = {'welcome':wc,'has_election':True,'is_open':False, 'is_voted':False}
                except Exception as e:
                    print(e)
            else:
                context = {'welcome': wc,'has_election': True, 'is_voted':True}
        else:
            context = {'welcome': wc, 'has_election': False, 'is_open': False}
    else:
        return redirect('index')
    return render(request,'muni_election/vote.html',context=context)

@login_required(login_url='index')
def vote_done(request):
    return render(request,'muni_election/vote_done.html')

@login_required(login_url='index')
def standings(request):
    if request.user.is_voter:
        wc = "Welcome " + request.user.first_name + " " + request.user.last_name
        election_id = request.session.get('election_id')
        ward = request.session.get('ward')
        if election_id:
            #ward list of reserve councilor
            re_c_Obj = re_councilor_candidate.objects.filter(Q(election_id=election_id)&(Q(reserve_ward_1=ward)|Q(reserve_ward_2=ward)|Q(reserve_ward_3=ward))).first()
            re_ward1 = re_c_Obj.reserve_ward_1
            re_ward2 =re_c_Obj.reserve_ward_2
            re_ward3 = re_c_Obj.reserve_ward_3

            standing_header = election.objects.get(pk=election_id).name+" Standings"
            #Total Vote casted for mayor on that particular election
            mayor_total = is_voted.objects.filter(election_id=election_id).count()

            # Total Vote casted for councilor on that particular election and that particular ward
            councilor_total = is_voted.objects.filter(Q(election_id=election_id)&Q(ward=ward)).count()

            # Total Vote casted for councilor on that particular election and that particular ward
            re_councilor_total = is_voted.objects.filter(Q(election_id=election_id)&(Q(ward=re_ward1)|Q(ward=re_ward2)|Q(ward=re_ward3))).count()
            mayors = mayor_candidate.objects.filter(election_id=election_id)
            councilors = councilor_candidate.objects.filter(Q(election_id=election_id) & Q(ward_no=ward))
            re_councilors = re_councilor_candidate.objects.filter(Q(election_id=election_id) & (Q(reserve_ward_1=ward) | Q(reserve_ward_2=ward) | Q(reserve_ward_3=ward)))
            context = {'wc':wc, 'standing_header':standing_header, 'has_election': True, 'mayors':mayors, 'councilors':councilors, 're_councilors':re_councilors, 'mayor_total':mayor_total, 'councilor_total':councilor_total, 're_councilor_total':re_councilor_total}
        else:
            context = {'wc': wc, 'has_election': False}
    else:
        return redirect('index')
    return render(request,'muni_election/standings.html', context=context)

@login_required(login_url='index')
def voter_logout(request):
    logout(request)
    return redirect('index')

def voter_reg(request):
    if request.method == 'POST':
        form1 = userReg(request.POST)
        form2 = voterReg(request.POST)
        if form1.is_valid() and form2.is_valid():
            uData = form1.cleaned_data
            vData = form2.cleaned_data
            User = get_user_model()
            userObj = User.objects.create_user(username=uData['username'],password=uData['password'], first_name=uData['first_name'],last_name=uData['last_name'],email=uData['email'],phone=uData['phone'],is_voter=True)
            userObj.save()
            voterObj = voter(user=userObj,voter_id=vData['voter_id'],area=vData['area'],serial=vData['serial'],dob=vData['dob'],gender=vData['gender'],ward=vData['ward'],municipality=vData['municipality'])
            voterObj.save()
            #print(form1.cleaned_data['username'],form2.cleaned_data['voter_id'])
            return redirect('index')
    else:
        form1 = userReg()
        form2 = voterReg()
    context = {'form1':form1,'form2':form2}
    return render(request,'main/voter_reg.html',context=context)

def voter_reg_complete(request):
    return render(request,'main/voter_reg_complete.html')

@staff_member_required
def voter_migrate(request):
    if request.method == 'POST':
        form = migrateVoter(request.POST)
        if form.is_valid():
            voter_migration_func(str(request.POST['start_date']),str(request.POST['end_date']))
            obj = voter_migration(start_date=request.POST['start_date'],end_date=request.POST['end_date'])
            obj.save()
            messages.success(request, "Migration Done Successfully")
    else:
        form = migrateVoter()
    context = {'has_permission':True,'site_header':'Online Election Platform Administration', 'form':form, 'title': 'Migrate Voters From National DB' }
    return render(request,'muni_election/migrate_voter.html',context)

