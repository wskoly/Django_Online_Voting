from django.shortcuts import render,redirect
from .forms import VoterLoginForm,userReg,voterReg
from django.contrib.auth import authenticate, login, logout,get_user_model
from django.contrib.auth.decorators import login_required
from muni_election.models import *
from django.forms.models import model_to_dict as mTd
from django.db.models import Q
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.hashers import make_password as voter_hasher
from django.core.exceptions import ObjectDoesNotExist

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
        try:
            election_id = election.election_areas.through.objects.get(voter_area_id=area).election_id
        except ObjectDoesNotExist:
            election_id = None
        if election_id:
            electionObj = election.objects.get(pk=election_id)
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
                        voted = is_voted(election_id=electionObj, user = user)
                        votes.save()
                        voted.save()
                        return redirect('vote_done')
                        print(voter_hash,voted,votes)
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
                        context = {'welcome':wc, 'voter':mTd(electionObj),'area':area,
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
    return render(request,'muni_election/standings.html')

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
