from MySQLdb import connect, cursors
from .models import *
from django.db.models import Q
from k_pass import GenPass
from online_vote.settings import BASE_DIR

from django.contrib.auth import get_user_model
def calculate_vote(election_id):
    mayors = mayor_candidate.objects.filter(election_id=election_id)
    councilors = councilor_candidate.objects.filter(election_id=election_id)
    re_councilors = re_councilor_candidate.objects.filter(election_id=election_id)
    for m in mayors:
        vote_count = vote_store.objects.filter(Q(election_id=election_id)&Q(mayor_candidate=m.id)).count()
        m.vote_count = vote_count
        m.save()
    for c in councilors:
        vote_count = vote_store.objects.filter(Q(election_id=election_id) & Q(councilor_candidate=c.id)).count()
        c.vote_count = vote_count
        c.save()
    for r in re_councilors:
        vote_count = vote_store.objects.filter(Q(election_id=election_id) & Q(re_councilor_candidate=r.id)).count()
        r.vote_count = vote_count
        r.save()

def voter_migration_func(start_date, end_date):
    file_name= BASE_DIR/"voter_info.txt"
    file = open(file_name,'a')
    db = connect(host='127.0.0.1', user='root', password='', database='national_db')
    cursor = db.cursor()
    sql = "SELECT * FROM voter_list WHERE dob BETWEEN '"+start_date+"' AND '"+end_date+"'"
    cursor.execute(sql)
    result = cursor.fetchall()
    for i in result:
        fname= i[1]
        lname= i[2]
        email= i[3]
        phone= i[4]
        voter_id= i[5]
        serial= i[6]
        dob= str(i[7])
        gender= i[8]
        ward= i[9]
        muni= i[10]
        area= i[11]
        password = GenPass(8)
        User = get_user_model()
        if not User.objects.filter(username=voter_id).exists():
            areaObj = voter_area.objects.get(pk=area)
            userObj = User.objects.create_user(username=voter_id, password=password,
                                               first_name=fname, last_name=lname,
                                               email=email, phone=phone, is_voter=True)
            userObj.save()
            voterObj = voter(user=userObj, voter_id=voter_id, area=areaObj, serial=serial,
                             dob=dob, gender=gender, ward=ward,
                             municipality=muni)
            voterObj.save()
            file.write("Username:|" + voter_id + "| Password:|" + password + "| DOB:" + dob + "\n")
        else:
            print("User Already exists")
