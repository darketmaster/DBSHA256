from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
import pytz
from django.views.generic import ListView
from django.contrib import messages

from .models import Release, SHA256OP
from .forms import ReleaseForm
from django.http import HttpResponseRedirect
import simplejson as json


from .forms import NameForm, CompareForms, CompareFormsRelease, ReleaseForm

def generate(request):
    if request.method == 'POST':
        form = ReleaseForm(request.POST)
        if form.is_valid():
            data = request.POST.copy()
            release = Release.objects.get(pk=data.get('release'))
            print(release)

            params = {
                "ip": release.ip,
                "port":release.port,
                "user":release.user,
                "password":release.password,
                "schema":"information_schema",
                "dbSchema":release.database,
                "paramsFilter":release.paramsFilter
                }

            shadata = getAlldataSha256(params)
            if("ERROR" in shadata):
                #do
                return render(request, 'catalog/error.html', {'type': "ERROR", 'msg': shadata["ERROR"]})
            else:
                #SHA256OP.objects.filter(release=release)
                for ktype, dvalue in shadata.items():
                    print(ktype)
                    for name, val in dvalue.items():
                        print(name+" "+val[0]+" "+val[1])
                        SHA256OP.objects.create(release=release, name=name, ptype=ktype, value=val[0], sha256=val[1])

                release.generated = datetime.now()
                release.save()
                messages.info(request, "The SHA256 for release: "+release.name+" is done!")
            return HttpResponseRedirect('/')
    else:
        form = ReleaseForm()
    return render(request, 'catalog/releases.html', {'form': form})

def compare(request):
    if request.method == 'POST':
        form = CompareFormsRelease(request.POST)
        if form.is_valid():
            data = request.POST.copy()
            release = Release.objects.get(pk=data.get('release'))

            params = {
                "ip": data.get('ip'),
                "port":int(data.get('port')),
                "user":data.get('user'),
                "password":data.get('password'),
                "schema":"information_schema",
                #"dbSchema":data.get('database'),
                "dbSchema":release.database,
                "paramsFilter":release.paramsFilter
            }

            print(params)
            shadata = getAlldataSha256(params)
            serverdata={}
                                    
            #print(shadata)
            if("ERROR" in shadata):
                return render(request, 'catalog/error.html', {'type': "ERROR", 'msg': shadata["ERROR"]})
            else:
                sharelease = SHA256OP.objects.values('name', 'ptype', 'sha256').filter(release=release)
                print(sharelease)
                releasedata={}
                for r in sharelease:
                    print(r)
                    if not(r["ptype"] in releasedata):
                        releasedata[r["ptype"]]={}
                    releasedata[r["ptype"]][r["name"]]=r["sha256"]

                for ktype, dvalue in shadata.items():
                    print(ktype)
                    if not(ktype in serverdata):
                        serverdata[ktype]={}
                    for name, val in dvalue.items():
                        #print(name+" "+val[0]+" "+val[1])
                        print(ktype+" "+name+" "+val[1])
                        serverdata[ktype][name]=val[1]
                        #SHA256OP.objects.create(release=release, name=name, ptype=ktype, value=val[0], sha256=val[1])
                print(serverdata)
                print(releasedata)

                comparedata={}
                ###Compare routines
                for k in releasedata.keys():
                    print("Check Release key:"+k)
                    if k in serverdata:
                        for n in releasedata[k].keys():
                            print("Check Release Name:"+n)
                            if n in serverdata[k]:
                                if not("COMMON" in comparedata):
                                    comparedata["COMMON"]={}
                                if not(k in comparedata["COMMON"]):
                                    comparedata["COMMON"][k]={}
                                comparedata["COMMON"][k][n]=(releasedata[k][n],serverdata[k][n],(releasedata[k][n]==serverdata[k][n]))
                            else:
                                if not("REMOVED" in comparedata):
                                    comparedata["REMOVED"]={}
                                if not(k in comparedata["REMOVED"]):
                                    comparedata["REMOVED"][k]={}
                                comparedata["REMOVED"][k][n]=(releasedata[k][n])                            
                    else:
                        for n in releasedata[k].keys():
                            if not("REMOVED" in comparedata):
                                comparedata["REMOVED"]={}
                            if not(k in comparedata["REMOVED"]):
                                comparedata["REMOVED"][k]={}
                            comparedata["REMOVED"][k][n]=(releasedata[k][n])
                
                for k in serverdata.keys():
                    print("Check Server key:"+k)
                    if k in releasedata:
                        for n in serverdata[k].keys():
                            print("Check Server Name:"+n)
                            if not(n in releasedata[k]):
                                if not("ADDED" in comparedata):
                                    comparedata["ADDED"]={}
                                if not(k in comparedata["ADDED"]):
                                    comparedata["ADDED"][k]={}
                                comparedata["ADDED"][k][n]=(serverdata[k][n])    
                    else:
                        for n in serverdata[k].keys():
                            if not("ADDED" in comparedata):
                                comparedata["ADDED"]={}
                            if not(k in comparedata["ADDED"]):
                                comparedata["ADDED"][k]={}
                            comparedata["ADDED"][k][n]=(serverdata[k][n])
                    
                print(json.dumps(comparedata))

                context = {
                    "comparedata":comparedata
                }

                messages.info(request, "The SHA256 comparison for release: "+release.name+" and server "+data.get('ip')+":"+data.get('port')+" is done!")
            return render(request, 'catalog/tablecompare.html', context)
    else:
        form = CompareFormsRelease()
    return render(request, 'catalog/compare.html', {'form': form})

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            return HttpResponseRedirect('home/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'catalog/test.html', {'form': form})

# Replace the existing home function with the one below
def home(request):
    return render(request, "catalog/home.html")

def about(request):
    return render(request, "catalog/about.html")

def contact(request):
    return render(request, "catalog/contact.html")

def mainPage(request, name):
    return render(
        request,
        'catalog/main.html',
        {
            'name': name,
            'date': datetime.now()
        }
    )

def home2(request):

    releases = Release.objects.all()
    print(releases)
    release = Release.objects.get(name="Release 2 V1.0")
    print(release)

    params = {
        "ip": release.ip,
        "port":release.port,
        "user":release.user,
        "password":release.password,
        "schema":"information_schema",
        "dbSchema":release.database,
        "paramsFilter":release.paramsFilter
        }

    data = getAlldataSha256(params)
    SHA256OP.objects.filter(release=release)

    for ktype, dvalue in data.items():
        print(ktype)
        for name, val in dvalue.items():
            print(name+" "+val[0]+" "+val[1])
            SHA256OP.objects.create(release=release, name=name, ptype=ktype, value=val[0], sha256=val[1])

    release.generated = datetime.now()
    release.save()    
    #print(data)


   # sha = SHA256OP.objects.get(pk=1)
    #release = Release.objects.get(name="Release.objects.")
    #sha.release = release
   # sha.save()
    return HttpResponse("DATA"+"<br>")




def release(request):
    form = ReleaseForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            release = form.save(commit=False)
            release.log_date = datetime.now()
            release.save()
            return redirect("release")
    else:
        return render(request, "catalog/release.html", {"form": form})


####################3



def getAlldataSha256(params):
    import hashlib
    import simplejson as json

    response = dict()
    dparams=getParams(params)
    if("ERROR" in dparams):
        response=dparams
    else:
        info=getInfo(params)
        tables=getTableDDL(params)    

        #print(dparams)
        response["PARAMETERS"]={}
        for item in dparams:
            sha256 = hashlib.sha256(item[1].encode('utf-8')).hexdigest()
            response["PARAMETERS"][item[0]]=(item[1],sha256)

        for row in info:
            sha256 = hashlib.sha256(row[2].encode('utf-8')).hexdigest()
            if row[0] in response :
                response[row[0]][row[1]]=(row[2],sha256)
            else:
                response[row[0]]={}
                response[row[0]][row[1]]=(row[2],sha256)

        response["TABLES"]={}
        for key, value in tables.items():
            sha256 = hashlib.sha256(value.encode('utf-8')).hexdigest()
            response["TABLES"][key]=(value,sha256)
            
    #jsonres = json.dumps(response)
    #print (jsonres)
    return response

def execSql(ip, port, user, password, schema, sql):
    import pymysql

    results={}

    try:
        db = pymysql.connect(ip, user, password, schema, port)        
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
        except:
            print ("Error: unable to fetch data")
            results["ERROR"]="unable to fetch data"

        db.close()
    except:
        print ("Error: unable connect to server: "+ip+":"+str(port))
        results["ERROR"]="Error: unable connect to server: "+ip+":"+str(port)
    return results

def getParams(params):
    ip=params["ip"]
    port=params["port"]
    user=params["user"]
    password=params["password"]
    schema=params["schema"]
    paramsFilter=params["paramsFilter"]
    sql="SHOW GLOBAL VARIABLES WHERE Variable_name regexp '"+paramsFilter+"';"
    return execSql(ip, port, user, password, schema, sql)

def getInfo(params):
    ip=params["ip"]
    port=params["port"]
    user=params["user"]
    password=params["password"]
    schema=params["schema"]
    dbSchema=params["dbSchema"]
    sql="SELECT 'TRIGGER' TYPE, TRIGGER_NAME NAME, ACTION_STATEMENT DEF FROM TRIGGERS t WHERE TRIGGER_SCHEMA = '"+dbSchema+"' \
        union \
        SELECT 'VIEW', TABLE_NAME, VIEW_DEFINITION FROM VIEWS v WHERE TABLE_SCHEMA = '"+dbSchema+"' \
        union \
        SELECT ROUTINE_TYPE, ROUTINE_NAME, ROUTINE_DEFINITION FROM ROUTINES r WHERE ROUTINE_SCHEMA = '"+dbSchema+"'"
    return execSql(ip, port, user, password, schema, sql)

def getTableDDL(params):
    import pymysql

    ip=params["ip"]
    port=params["port"]
    user=params["user"]
    password=params["password"]
    schema=params["schema"]
    dbSchema=params["dbSchema"]

    results={}
    try:
        # Open database connection
        db = pymysql.connect(ip, user, password, schema, port)
        
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # Prepare SQL query to INSERT a record into the database.
        sql = "SELECT TABLE_NAME FROM TABLES t WHERE TABLE_SCHEMA = '"+dbSchema+"' and TABLE_TYPE = 'BASE TABLE'"
        try:
            res={}
            cursor.execute(sql)
            res = cursor.fetchall()
            #print(res)
            for row in res:
                try:
                    print("Checking table: ",row[0])
                    createres = {}
                    createsql= "show create table "+dbSchema+"."+row[0]+";"
                    cursor.execute(createsql)
                    createres = cursor.fetchall()
                    for crow in createres:
                        results[crow[0]]=crow[1]
                except:
                    print ("Error: unable to fetch create table data "+row[0])
                    results={"Error":("unable to fetch create table data "+row[0])}
        except:
            print ("Error: unable to fetch data "+dbSchema)
            results["ERROR"]="unable to fetch data "+dbSchema

        # disconnect from server
        db.close()
    except:
        print ("Error: unable connect to server: "+ip+":"+str(port))
        results["ERROR"]="Error: unable connect to server: "+ip+":"+str(port)

    return results



