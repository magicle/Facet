import smtplib
import os
import Skype4Py
import time
import subprocess
import signal
#Skype = Skype4Py.Skype()


global ClientName
global p                            # subprocess
global p_IsInit                     # 1 if p is initiated
global addr
global passcode
global callobj
global cleanbit

# complete  =       0       job exists, initiate call
#           =       1       call in progress
#           =       -1      incomplete, session disrupted
#           =       -2      no job at all
global complete

Skype = Skype4Py.Skype(Transport = 'x11')
Skype.Attach()


if not Skype.Client.IsRunning:
    Skype.Client.Start()


def MailBack(Who, Msg, Subject):
    print "enter"
    fromaddr = 'magiclamp1000@gmail.com'
    toaddrs  = Who
    username = 'magiclamp1000'
    password = '202154215471'

    headers = ["from: "+ fromaddr, "subject: "+ Subject]
    headers = "\r\n".join(headers)

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, headers + "\r\n\r\n" + Msg)
    server.quit()
    print "done"



def RequestHandle(User):
    print User.Handle
    f = open("AddFriend", "r+")
    lines = f.readlines()
    for line in lines:
        if User.Handle in line:
            User.BuddyStatus = Skype4Py.enums.budPendingAuthorization
    f.seek(0)
    f.write("")
    f.truncate()
    f.close

def MessageHandle(Message, status):
    skyname = Message.FromHandle

    vurl = Message.Body
    tempf = open ("JobList", 'a')
    tempf.write(skyname + ' ' + vurl + "\n")
    tempf.close()


def clearjob(Skypename):
    flag = 0
    f = open("JobList", "r+")
    lines = f.readlines()
    f.seek(0)
    for i in range(0,len(lines)):
        if Skypename in lines[i] and flag == 0:
                flag = 1
        else:
            f.write(lines[i])
    f.truncate()
    f.close()




def CallHandle(Call, status):
    global p, addr, ClientName, callobj, complete, p_IsInit
    state = Skype.Convert.CallStatusToText(status)
    print state
    ClientName = Call.PartnerHandle
    if "Calling" in state:
        print "Now Start Calling..."
    if "Cancelled" in state:
        complete = -1
    if "Refused" in state:
        complete = -1
    if "Call in Progress" in state:
#        ClientName = Call.PartnerHandle
        print addr
        p = subprocess.Popen(["./play.sh", addr, "/dev/video4"], preexec_fn = os.setsid)
        p_IsInit = 1
        print p.poll()
        print "Connected"
        complete = 1

    if "Finished" in state:
        complete = -1
        print "Waiting for new request"





def GetVurl(url):
    proc = subprocess.Popen(["youtube-dl", "-g", "-f", "36", url], stdout=subprocess.PIPE)
    proc.wait()
    vaddr = proc.stdout.readlines()
    if not vaddr:
        return "ERROR"
    else:
        return vaddr[0].strip("\n")

def DoJob():
    f = open("JobList","rw")
    lines = f.readlines()
    job = "\n"
    for line in lines:
        if len(line.split()[0]) != 0 and job =="\n":
            job = line
    global addr, callobj, complete,ClientName
    f.close()
    if job != "\n":
        ClientName = job.split()[0]
        addr = job.split()[1]
        addr = GetVurl(addr)
        print "addr is:"
        print addr
        if "ERROR" in addr:
            complete = -1
        else:
            callobj = Skype.PlaceCall(job.split()[0])
            complete = 0



Skype.OnCallStatus = CallHandle
Skype.OnMessageStatus = MessageHandle
Skype.OnUserAuthorizationRequestReceived = RequestHandle


flag = 1
while 1:
    if len(Skype.ActiveCalls) == 0:

        #initiate

        p_IsInit = 0
        complete = -2
        flag = 1
        DoJob()
#        print complete
        # do if there exists job...
        if complete != -2:
            while flag:
                time.sleep(1)
                if complete == -1:          #   discrupted
                    flag = 0
                if complete == 1:           #   play ends
                    if p.poll() != None:
                        flag = 0
                # recall 3 times, reject



#            print complete
            # clean to restart

            # end call if not being ended
            if complete == 1:
                callobj.Finish()
            # kill gst process if it's still there
            if p_IsInit == 1:
                if p.poll() == None:
                    os.killpg(p.pid, signal.SIGTERM)
            # delete the job from JobList
            clearjob(ClientName)
    time.sleep(5)














#print len(Skype.ActiveCalls)
#for ch in Skype.ActiveCalls:
#    print ch.PartnerHandle

#Skype.ActiveCalls[0].Answer()





#pp = Skype.SendMessage("skymomo10", "dddd")

#print pp

#for user in Skype.Friends:
#    print '    ', user.FullName




#Skype.PlaceCall("skymomo10")
