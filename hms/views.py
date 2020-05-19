import pyrebase
from django.shortcuts import render



config = {
    
}

firebase = pyrebase.initialize_app(config)

authe = firebase.auth()
database=firebase.database()
def boot(request):
    
    return render(request, "login.html")

def postsign(request):
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    try:
         user = authe.sign_in_with_email_and_password(email,passw)
         print("SO FAR SO GOOD")
         
    except:
         message ="INVALID CREDENTIALS"
         return render(request, "login.html",{"msg":message})     
    emailget=email.replace(".",",")
    session_id=user['localId']
    request.session['uid']=str(session_id)
    idtoken=request.session['uid']
    database.child("emailidtok").child(idtoken).child("email").set(emailget)

    
    usertype=database.child("users").child(emailget).child("role").get().val()
    
    print(usertype)
   
    
    if usertype == "admin":
        print("ADMINNND")
        return render(request, "admin.html")
    elif usertype == "receptionist":
        print("AHHHHHHHWHYYYYYYY")
        return render(request, "receptionist.html")
    elif usertype == "doctor":
        print("WHATS UP DOC")
        return render(request, "doc.html")
    elif usertype == "patient":
        print("You know, like that one tool song")
        return render(request, "patient.html")    
    else:         
         try:
            del request.session['uid']
            return render(request, "login.html") 
         except KeyError:
            pass
            return render(request, "login.html") 
def getdocdata(request):
    try:
      idtoken=request.session['uid']
      print(idtoken)
     
    except KeyError:
      message="Ooops! This User Has Logged Out"
      return render(request, "login.html", {"msg":message})
    email = request.POST.get('docemail')
    passw = request.POST.get('docpass')    
    name =request.POST.get("docname")
    idd= request.POST.get("docid")
    docs=request.POST.get("docs")
    docq=request.POST.get("docq")
    try:
        user=authe.create_user_with_email_and_password(email,passw)
    except:
        message="Unable to create account try again"
        return render(request,"admin.html",{"msg":message})
    database.child("doctors").child(idd).child("doctor_name").set(name)
    database.child("doctors").child(idd).child("doctor_spec").set(docs)
    database.child("doctors").child(idd).child("doctor_qual").set(docq)
    em=email.replace(".",",")
    database.child("users").child(em).child("role").set("doctor")
    database.child("users").child(em).child("id").set(idd)
    return render(request, "admin.html")

def logout(request):
    try:
        database.child('emailidtok').remove()
        del request.session['uid']
        return render(request, "login.html")
    except KeyError:
        pass
        return render(request, "login.html")

def getpatdata(request):
      try:
       idtoken=request.session['uid']
       
      except KeyError:
       message="Ooops! This User Has Logged Out"
       return render(request, "login.html", {"msg":message})
      email = request.POST.get('patemail')
      passw = request.POST.get('patpass')    
      name =request.POST.get("patname")
      em=email.replace(".",",")
      patid= request.POST.get('patid')
      patdob=request.POST.get('patdob')
      patage=request.POST.get('patage')
      patwt=request.POST.get('patwt')
      patht=request.POST.get('patht')
      patbg=request.POST.get('patbg')
      patrfv=request.POST.get('patrfv')
      
      try:
        user=authe.create_user_with_email_and_password(email,passw)
      except:
        message="Unable to create account try again"
        return render(request,"receptionist.html",{"msg":message})
      
      database.child("users").child(em).child("role").set("patient")
      database.child("users").child(em).child("id").set(patid)
      
      database.child("patients").child(patid).child("patient_name").set(name)
      database.child("patients").child(patid).child("patient_dob").set(patdob)
      database.child("patients").child(patid).child("patient_age").set(patage)
      database.child("patients").child(patid).child("patient_weight").set(patwt)
      database.child("patients").child(patid).child("patient_height").set(patht)
      database.child("patients").child(patid).child("patient_bloodgroup").set(patbg)
      database.child("patients").child(patid).child("patient_reason").set(patrfv)
      return render(request, "receptionist.html")
def patshow(request):
    try:
       idtoken=request.session['uid']
       
       
    except KeyError:
       message="Ooops! This User Has Logged Out"
       return render(request, "login.html", {"msg":message})

    ids=database.child('patients').shallow().get().val()
    print(ids)
    list_patid=[]
    for i in ids:
        list_patid.append(i)
    print(list_patid)    
    pname=[]
    for i in list_patid:
        pn=database.child("patients").child(i).child("patient_name").get().val()
        pname.append(pn)
        print(pname)
    comb_list=zip(list_patid,pname)    
    return render(request, "postdoc.html",{"co":comb_list})
          
def patview(request):
    try:
       idtoken=request.session['uid']
       
       
    except KeyError:
       message="Ooops! This User Has Logged Out"
       return render(request, "login.html", {"msg":message})
    iddd=request.GET.get('z')  

    
    pname =database.child('patients').child(iddd).child('patient_name').get().val()
    page =database.child('patients').child(iddd).child('patient_age').get().val()
    pdob =database.child('patients').child(iddd).child('patient_dob').get().val()
    pbg =database.child('patients').child(iddd).child('patient_bloodgroup').get().val()
    pht =database.child('patients').child(iddd).child('patient_height').get().val()
    pwt =database.child('patients').child(iddd).child('patient_weight').get().val()
    pr=database.child('patients').child(iddd).child('patient_reason').get().val()

    return render(request,"postpatview.html",{"id":iddd,"pname":pname,"page":page,"pdob":pdob,"pbg":pbg,"pht":pht,"pwt":pwt,"pr":pr})

def finaldoc(request):
    try:
       idtoken=request.session['uid']
       
       
    except KeyError:
       message="Ooops! This User Has Logged Out"
       return render(request, "login.html", {"msg":message})
    patid=request.POST.get("patid")
    print(patid)
    idtoken=request.session['uid']
    em=database.child("emailidtok").child(idtoken).child("email").get().val()
    idd=database.child("users").child(em).child("id").get().val()
    
    diag= request.POST.get("diagnosis")
    tests=request.POST.get("tests")
    pres=request.POST.get("prescription")
    database.child("diagnosisreport").child(patid).child(idd).child("diagnosis").set(diag)
    database.child("diagnosisreport").child(patid).child(idd).child("prescription").set(pres)
    database.child("diagnosisreport").child(patid).child(idd).child("tests").set(tests)

    return render(request, "postpatview.html")


def showyourdet(request):
    try:
       idtoken=request.session['uid']
       
       
    except KeyError:
       message="Ooops! This User Has Logged Out"
       return render(request, "login.html", {"msg":message})

    idtoken=request.session['uid']
    em=database.child("emailidtok").child(idtoken).child("email").get().val()
    idd=database.child("users").child(em).child("id").get().val()
    pname=database.child("patients").child(idd).child("patient_name").get().val()
    preason=database.child("patients").child(idd).child("patient_reason").get().val()
    docids_dict=database.child("diagnosisreport").child(idd).shallow().get().val()
    docids_list=[]
    for i in docids_dict:
        docids_list.append(i)
    diagnosis=[]
    prescription=[]
    tests=[]
    for i in docids_list:
        diag=database.child("diagnosisreport").child(idd).child(i).child("diagnosis").get().val()
        diagnosis.append(diag)
        tst=database.child("diagnosisreport").child(idd).child(i).child("tests").get().val()
        tests.append(tst)
        pr=database.child("diagnosisreport").child(idd).child(i).child("prescription").get().val()
        prescription.append(pr)
    comb_list=zip(docids_list,diagnosis,tests,prescription)   
    return render(request, "finalpat.html",{"co":comb_list,"pid":idd,"pname":pname,"preason":preason}) 









