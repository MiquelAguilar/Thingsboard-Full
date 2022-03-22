import requests
import csv
import mimetypes
import smtplib
import time
import schedule

from calendar import monthrange
from datetime import datetime
from datetime import date, datetime
from os import stat
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase

# to eliminate warnings
import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# to eliminate warnings 

def tensioToBatteryLevel(text): # map tension battery level to %
    battery = ""
    if text == "3,0V - OK":
        battery="100%"
    elif text == "2,9V - OK":
        battery="100%"
    elif text == "2,8V - OK":
        battery="100%"
    elif text == "2,7V - OK":
        battery="75%"
    elif text == "2,6V - OK":
        battery="75%"
    elif text == "2,5V - OK":
        battery="50%"
    elif text == "2,4V - OK":
        battery="50%"
    elif text == "2,3V - OK":
        battery="50%"
    elif text == "2,2V - Alerta Batería Baja":
        battery="25%"
    elif text == "2,1V - Alerta Batería Baja":
        battery="25%"
    elif text == "2,0V - Alerta Batería Baja":
        battery="10%"
    elif text == "1,9V - Alerta Batería Critica":
        battery="10%"
    elif text == "1,8V - Alerta Batería Critica":
        battery="0%"
    else: # msg if we dont have information
        battery="No info battery"
    return battery

def mapDeviceName(device): # map device to number Ford
    if device == "26F543F":
        return 1
    elif device == "26F5430":
        return 2
    elif device == "26F5477":
        return 3
    elif device == "26F5434":
        return 4
    elif device == "26F549D":
        return 5
    elif device == "26F544E":
        return 6
    elif device == "26F544C":
        return 7
    elif device == "26F5440":
        return 8
    elif device == "26F548A":
        return 9
    elif device == "26F543B":
        return 10
    elif device == "26F5479":
        return 11
    elif device == "26F5452":
        return 12
    elif device == "26F548F":
        return 13
    elif device == "26F5443":
        return 14
    elif device == "26F5432":
        return 15
    elif device == "26F5467":
        return 16
    elif device == "26F544D":
        return 17
    elif device == "26F5469":
        return 18
    elif device == "26F5491":
        return 19
    elif device == "26F5455":
        return 20
    elif device == "26F5454":
        return 21
    elif device == "26F547B":
        return 22
    elif device == "26F543D":
        return 23
    elif device == "26F543A":
        return 24
    elif device == "26F548E":
        return 25
    elif device == "26F5493":
        return 26
    elif device == "26F5451":
        return 27
    elif device == "26F5431":
        return 28
    elif device == "26F543C":
        return 29
    elif device == "26F5442":
        return 30
    elif device == "26F5489":
        return 31
    elif device == "26F5495":
        return 32
    elif device == "26F5458":
        return 33
    elif device == "26F542F":
        return 34
    elif device == "26F5446":
        return 35
    elif device == "26F544F":
        return 36
    elif device == "26F5436":
        return 37
    elif device == "26F5490":
        return 38
    elif device == "26F545B":
        return 39
    elif device == "26F5450":
        return 40
    elif device == "26F5433":
        return 41
    elif device == "26F5438":
        return 42
    elif device == "26F545C":
        return 43
    elif device == "26F543E":
        return 44
    elif device == "26F5453":
        return 45
    elif device == "26F547A":
        return 46
    elif device == "26F54A1":
        return 47
    elif device == "26F5474":
        return 48
    elif device == "26F548C":
        return 49
    elif device == "26F5488":
        return 50
    elif device == "26F54A0":
        return 51
    elif device == "26F548B":
        return 52
    elif device == "26F5466":
        return 53
    elif device == "26F548D":
        return 54
    elif device == "26F549C":
        return 55
    elif device == "26F5476":
        return 56
    elif device == "26F5484":
        return 57
    elif device == "26F545E":
        return 58
    elif device == "26F546E":
        return 59
    elif device == "26F547D":
        return 60
    elif device == "26F5487":
        return 61
    elif device == "26F549B":
        return 62
    elif device == "26F5498":
        return 63
    elif device == "26F5456":
        return 64
    elif device == "26F549A":
        return 65
    elif device == "26F5475":
        return 66
    elif device == "26F5486":
        return 67
    elif device == "26F5472":
        return 68
    elif device == "26F547F":
        return 69
    elif device == "26F5478":
        return 70
    elif device == "26F5468":
        return 71
    elif device == "26F5483":
        return 72
    elif device == "26F5497":
        return 73
    elif device == "26F5482":
        return 74
    elif device == "26F549F":
        return 75
    elif device == "26F546C":
        return 76
    elif device == "26F546A":
        return 77
    elif device == "26F5473":
        return 78
    elif device == "26F547C":
        return 79
    elif device == "26F5499":
        return 80
    elif device == "26F549E":
        return 81
    elif device == "26F5485":
        return 82
    elif device == "26F5470":
        return 83
    elif device == "26F5481":
        return 84
    elif device == "26F5496":
        return 85
    elif device == "26F546D":
        return 86
    elif device == "26F546B":
        return 87
    elif device == "26F5441":
        return 88
    elif device == "26F545A":
        return 89
    elif device == "26F54A4":
        return 90
    else:
        return "No info device"

def alarmDevice(id): # get alarms device
    token = getToken()
    basicUrL = "https://192.168.10.69:8080"
    head = {'Accept': 'application/json','X-Authorization': 'Bearer$' + str(token)}
    api_url = basicUrL+"/api/alarm/DEVICE/"+id+"?searchStatus=ACTIVE&pageSize=100&page=0&fetchOriginator=true" # GET all customers
    res = requests.get(api_url,headers=head, verify=False)
    return(res.json()['data']) #[0]['name']

def getToken(): # get token from url
    basicUrL = "https://192.168.10.69:8080"
    api_url = basicUrL+"/api/auth/login"

    # headers for the token
    headers =  {'Content-Type':'application/json', 'Accept': 'application/json'}
    data = '{"username":"fivecomm@admin.com","password":"Fivecomm2022."}' # to change
    response = requests.post(api_url,headers=headers,data=data , verify=False)
    token = response.json()['token']
    return token

def getResume(): # Create file and generate resume
    token = getToken() 
    basicUrL = "https://192.168.10.69:8080"
    head = {'Accept': 'application/json','X-Authorization': 'Bearer$' + str(token)}

    api_url = basicUrL+"/api/customers?pageSize=100&page=0" # GET all customers
    res = requests.get(api_url,headers=head, verify=False)
    customers = res.json()  # All customers

    devicesCustomer = []
    f = open('lastReport.csv', 'w', newline='')
    writer = csv.writer(f,delimiter=';') # Adjustment delimiter (";")

    # ----Variables--------
    contAlegreOpen = 0
    contFordOpen = 0
    contYanOpen = 0
    conUknownOpen = 0
    contAlegreClose = 0
    contFordClose = 0
    contYanClose = 0
    conUknownClose = 0

    # Api get all devices - DEVICES WITH CLIENTS!   
    for customer_i in range(len(customers['data'])):
        api_url = basicUrL+"/api/customer/"+customers['data'][customer_i]['id']['id']+"/devices?pageSize=10000&page=0"
        res = requests.get(api_url,headers=head, verify=False)
        devicesCustomer += res.json()['data']          

    for device_i in range(len(devicesCustomer)):
        api_url = basicUrL+"/api/plugins/telemetry/DEVICE/"+devicesCustomer[device_i]['id']['id']+"/values/timeseries"  # Telemetría de todos los dispositivos
        res = requests.get(api_url,headers=head, verify=False)
    #FOR EACH DEVICE ->
        # POSITION
        try:   
            Location = res.json()['Location'][0]['value']
        except:
            Location = ""
        # STATUS
        try:   
            status = res.json()['info_sensor'][0]['value']
        except:
            status = ""

        if(Location == "ALEGRE"):
            # print(Location," ",status, "\n")
            if(status == "OFF Doblado" or status == "Desplegado OFF"):
                contAlegreClose += 1
            elif(status == "Desplegado ON" or status == "ON Desplegado"):
                contAlegreOpen += 1  
        else:
            if(Location == "FORD"):
                if(status == "OFF Doblado" or status == "Desplegado OFF"):
                    contFordClose += 1 
                elif(status == "Desplegado ON" or status == "ON Desplegado"):
                    contFordOpen += 1
            else:
                # print(Location," ",status, "\n")
                if(Location == "YANFENG"):
                    if(status == "OFF Doblado" or status == "Desplegado OFF"):
                        contYanClose += 1
                    elif(status == "Desplegado ON" or status == "ON Desplegado"):
                        contYanOpen += 1
                else:
                    if(status == "OFF Doblado" or status == "Desplegado OFF"):
                        conUknownClose += 1
                    elif(status == "Desplegado ON" or status == "ON Desplegado"):
                        conUknownOpen += 1
    # Write in file all information
    writer.writerow(["","iAlegre:","YANFENG:","FORD:","Uknown:"])
    writer.writerow(["Opened",contAlegreOpen,contYanOpen,contFordOpen,conUknownOpen])
    writer.writerow(["Closed",contAlegreClose,contYanClose,contFordClose,conUknownClose])
    writer.writerow([""])

def getInfoNow(): #  add file all info
    token = getToken() 
    basicUrL = "https://192.168.10.69:8080"
    head = {'Accept': 'application/json','X-Authorization': 'Bearer$' + str(token)}

    api_url = basicUrL+"/api/customers?pageSize=100&page=0" # GET all customers
    res = requests.get(api_url,headers=head, verify=False)
    customers = res.json()  # All customers

    devicesCustomer = []
    f = open('lastReport.csv', 'a', newline='') # Open file (continuing after resume)
    writer = csv.writer(f,delimiter=';')
    # Write Column titles 
    writer.writerow(["Date","Device","Contaniner","ID Ford","Position","Status","Battery","Temperature","Inactivity Alert","Location Alert"])

    for customer_i in range(len(customers['data'])): # All clients
        api_url = basicUrL+"/api/customer/"+customers['data'][customer_i]['id']['id']+"/devices?pageSize=10000&page=0"
        res = requests.get(api_url,headers=head, verify=False)
        devicesCustomer += res.json()['data']           

    for device_i in range(len(devicesCustomer)): # All devices WITH CLIENTS ASSIGNED!
        api_url = basicUrL+"/api/plugins/telemetry/DEVICE/"+devicesCustomer[device_i]['id']['id']+"/values/timeseries"  # Telemetría de todos los dispositivos
        res = requests.get(api_url,headers=head, verify=False)

        # DATE
        try:   
            ts = date.today()
        except:
            ts = ""
        # DEVICE NAME and codeFORD
        try:   
            device = res.json()['device'][0]['value']
            # print(device)
            device_name = mapDeviceName(device)
        except:
            device = ""
            continue # QUITAMOS LOS DISPOSITIVOS QUE NO TIENEN ID (no los podemos identificar...)
        # POSITION
        try:   
            if(res.json()['Location'][0]['value'] == "UNKOWN"):
                Location = "UNKNOWN"
            else:
                Location = res.json()['Location'][0]['value']
        except:
            Location = "no position info"
        # STATUS
        # ON Desplegado, Desplegado ON,Desplegado OFF,OFF Doblado
        try:   
            if(res.json()['info_sensor'][0]['value'] == "OFF Doblado"):
                status = "Desplegado OFF"
            elif(res.json()['info_sensor'][0]['value'] == "ON Desplegado"):
                status = "Desplegado ON"
            else:
                status = res.json()['info_sensor'][0]['value']
        except:
            status = "no status info"
        # BATTERY
        try:   
            battery = tensioToBatteryLevel(res.json()['battery'][0]['value'])
        except:
            battery = tensioToBatteryLevel("")
        # TEMPERATURE
        try:
            if res.json()['temperature'][0]['value'].find('.') != -1:
                temperature = res.json()['temperature'][0]['value'].split(".")[0]+","+res.json()['temperature'][0]['value'].split(".")[1]
            else:
                temperature = res.json()['temperature'][0]['value'] 
        except:
            temperature = "no temperature info"


        # ALARMS INACTIVITY AND LOST 
        vecPos = 0
        # Get alarms from device
        alarms = alarmDevice(devicesCustomer[device_i]['id']['id'])
        inactivity_alert = ""
        location_alert = ""  
        # find alarms 
        while vecPos != len(alarms):
            # check if it has any alarm like 'Days on Zone + Closed' or 'Lost' and change value
            if alarms[vecPos]['name'] == 'Days on Zone + Closed' and alarms[vecPos]['status'] == 'ACTIVE_UNACK':
                inactivity_alert = "Inactividad"   
            if alarms[vecPos]['name'] == 'Lost' and alarms[vecPos]['status'] == 'ACTIVE_UNACK':
                location_alert = "Device Lost"   

            vecPos += 1

        # Write parameters in the same line 
        writer.writerow([ts,device,device_name,"FE1494B",Location,status,battery,temperature,inactivity_alert,location_alert])

def sendEmail(email): # Send 'email' with report lastReport.csv 

    getResume()     #function Resumen
    getInfoNow()    #function devices/alarms

    emailfrom = "iotplatform@5g-telepresence.eu"
    emailto = email
    fileToSend = "lastReport.csv" #name file
    username = "iotplatform@5g-telepresence.eu"
    password = "8t*FD5HRVd"

    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = emailto
    msg["Subject"] = "Daily Report Fivecomm" # Asunto
    msg.preamble = "Daily Report Fivecomm"

    html= """\
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional //EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:v="urn:schemas-microsoft-com:vml" lang="en">
            <head>
                <link rel="stylesheet" type="text/css" hs-webfonts="true" href="https://fonts.googleapis.com/css?family=Lato|Lato:i,b,bi">
                <title>Fivecomm</title>
                <meta property="og:title" content="Email template"> 
                <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style type="text/css">
                    a{ 
                        text-decoration: underline;
                        color: inherit;
                        font-weight: bold;
                        color: #1a65e2;
                    }
                    div.one {
                        
                        text-align: justify;
                        text-justify: inter-word;
                        font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
                        font-size:14px;
                        font-style: italic;
                        background-color: white;
                        border: white 0px;
                    }
                    h1 {
                        font-size: 40px;
                    }
                    p {
                        font-weight: 80;
                    }
                    td {
                        vertical-align: top;
                        padding: 20px;
                    }
                    tr {
                        padding: 20px;
                    }
                </style>
            </head>
            <body bgcolor="#F5F8FA" style="width: 70%; margin: auto 10px; padding:0; font-family:Lato, sans-serif; font-size:18px; color:#33475B; word-break:break-word">
                <div id="email"> 
                    <table role="presentation" width="70%">
                        <tr> 
                            <td bgcolor="#1a65e2" align="center" style="color: white;">         
                                <a title="Fivecomm" href="https://fivecomm.eu/"><img alt="Fivecomm" src="https://fivecomm.eu/wp-content/uploads/2021/05/Fivecomm-logo-light-NUEVO.png" width="70%" align="middle"></a>       
                                <h1> Your Daily Report! </h1>
                            </td>
                        </tr>
                        <tr>
                            <td align="center" class="things" ><a title="Fivecomm" href="https://5g-telepresence.eu:8080/home/"><img alt="Fivecomm" src="http://www.aurrera.pl/wp-content/uploads/2016/09/alegre-610x303.png" width="25%" align="middle"></a></td>
                        </tr>
                        <tr>
                            <td class="one">
                              <div class="one">
                                <br>
                                De conformidad con el Reglamento 2016/679 y la Ley Orgánica 3/2018 relativos a la Protección de Datos Personales, le informamos que los datos que usted nos facilite serán incorporados a los sistemas de tratamiento de 5G Communications For Future Industry Verticals, S.L. con CIF B40628943 y domicilio en Camino Vera, s/n, Edificio 6D, 4ª planta, de 46022 - Valencia, con la finalidad de mantener, desarrollar y controlar la relación contractual y la gestión comercial mantenidas con Vd. Puede ejercer los derechos de acceso, rectificación, limitación de tratamiento, supresión, portabilidad y oposición al tratamiento de sus datos de carácter personal dirigiendo su petición a la dirección postal indicada o al correo electrónico contact@fivecomm.eu junto con una copia de su NIE/DNI. Más información en Política de privacidad de www.fivecomm.eu.
                                <br><br>
                                Este mensaje va dirigido de manera exclusiva a su destinatario y puede contener INFORMACIÓN CONFIDENCIAL cuya divulgación, distribución, copia y/o utilización, está prohibida por la Ley 34/2002 sobre Servicios de la Sociedad de la Información y de Comercio Electrónico. Si ha recibido este mensaje por error, le rogamos nos lo comunique de forma inmediata por esta misma vía y proceda a su eliminación.
                              </div>
                            </td>
                          </tr>
                    </table>
                </div>
            </body>
        </html>
    """
    part2 = MIMEText(html, 'html')

    ctype, encoding = mimetypes.guess_type(fileToSend) # Map filenames to MIME types
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"

    maintype, subtype = ctype.split("/", 1)

    fp = open(fileToSend, "rb")
    attachment = MIMEBase(maintype, subtype)
    attachment.set_payload(fp.read())
    fp.close()
    encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
    msg.attach(attachment)
    msg.attach(part2)
    server = smtplib.SMTP("192.168.0.201:587")
    # server = smtplib.SMTP("83.56.30.233:587") # public server
    # server = smtplib.SMTP("5g-telepresence.eu:587")

    server.starttls() # security protocol
    server.login(username,password)
    server.sendmail(emailfrom, emailto, msg.as_string())
    server.quit()

# sendEmail("miquel.aguilar@fivecomm.eu")     #Envio del email
def sendEmailScheduled():
	sendEmail("miquel.aguilar@fivecomm.eu")
schedule.every().day.at("08:00").do(sendEmailScheduled) # 1 time a day

while True:
    schedule.run_pending()
    time.sleep(1) #wait 1 min
