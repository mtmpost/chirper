#!/usr/bin/python

'''
Created on Mar 27, 2012

@author: michaelmcgovern
'''

import MySQLdb
import time
import cgi
import cgitb
import ConfigParser
cgitb.enable(display=1, logdir="/tmp")

#from datetime import datetime


class ChirpData:
    def __init__(self,configFile='user.cfg'):        #Constructor
        self.config = configFile
        
    def CreateConnection(self):
        config = ConfigParser.RawConfigParser()
        config.readfp(open(self.config))
        dbcfg = config.get('UserSection','db')
        usercfg = config.get('UserSection','user')
        passwdcfg = config.get('UserSection','pwd')
        hostcfg = config.get('UserSection','host')
        sockcfg = config.get('UserSection','sock')
        self.conn = MySQLdb.connect(hostcfg,usercfg,passwdcfg,dbcfg,unix_socket=sockcfg)

    def DestroyConnection(self):
        self.conn.close()

#    def ManageConnection(self):
#        sql_lastChirp = "SELECT MAX(UNIX_TIMESTAMP(C_Time)) FROM cHirps;"
#        time = time.time()
#        #time = datetime.time(datetime.now())
#        conn = ChirpMe.CreateConnection()
#        lastChirpTime = conn.ExecCur(sql_lastChirp)
#        #print time, lastChirpTime 

    def ExecCur(self,sql_statement,params):
        #print 'these are the params',params
        cursor = self.conn.cursor()
        cursor.execute(sql_statement,params)
        result = cursor.fetchall()
        return result
        cursor.close()

    def chirpAdd(self,chirp):
        self.CreateConnection()
        self.ExecCur("INSERT INTO cHirps(C_String,C_Time) VALUES(%s,TIMESTAMP(now()))",(chirp))
        self.DestroyConnection()

    def getOlderChirps(self,maxNum,myQuery="",maxDate=time.time()):                                    # main method that populates login.py with chirps and queries  
        self.CreateConnection()
        if myQuery !="":
            rawdata = self.ExecCur("SELECT C_String, UNIX_TIMESTAMP(C_Time)" + 
                                   " FROM cHirps WHERE UNIX_TIMESTAMP(C_Time)<= %s" + 
                                   " AND C_String regexp %s ORDER BY C_Time DESC LIMIT 0,%s;" , (int(maxDate),myQuery,maxNum))
        else:
            rawdata = self.ExecCur("SELECT C_String, UNIX_TIMESTAMP(C_Time)" +
                                   " FROM cHirps WHERE UNIX_TIMESTAMP(C_Time)<= %s" + 
                                   " ORDER BY C_Time DESC LIMIT %s,%s;", (int(maxDate),0,maxNum))
        if not rawdata:                                                                            #if myQuery not found exception
            return ['Nothing like %s in here' % (myQuery)] 
        minmaxTime = self.getTime(rawdata)
        minTime = minmaxTime[0]
        return self.getString(rawdata)
        self.DestroyConnection()
        
                                                                                                  #for now, getNewerChirps sql_statement set to select times newer than now - 300 until 
                                                                                                  #I can get a starttime varible
    def getNewerChirps(self,maxNum,myQuery='',maxDate=int(time.time())):
        self.CreateConnection()
        if myQuery !='':
            rawdata = self.ExecCur("SELECT C_String, UNIX_TIMESTAMP(C_Time) FROM cHirps" + 
                                   "WHERE UNIX_TIMESTAMP(C_Time)>(%i-3000) AND C_String regex %s"+ 
                                   "ORDER BY C_Time DESC LIMIT 0,%i;", (maxDate,myQuery,maxNum))
        else:
            rawdata = self.ExecCur("SELECT C_String, UNIXTIMESTAMP(C_Time) FROM cHirps" +
                                   "WHERE UNIXTIMESTAMP(C_Time)>= %s ORDER BY C_Time ASC LIMIT 0,%s;",(maxDate, maxNum))
        if not rawdata:                                                                              #if myQuery not found exception
            return ['Nothing like \"%s\" in here' % (myQuery.replace('%',''))]
        minmaxTime = self.getTime(rawdata)
        maxTime = minmaxTime[1]
        return self.getString(rawdata)
        self.DestroyConnection()



    def getTime(self,rawdata):                                                                        #rawdata is a tuple containing tuples of (string,time) from db
        minmaxTime =[]
        for y in rawdata:
            minmaxTime.append(y[1])
        minTime = min(minmaxTime)
        maxTime = max(minmaxTime)
        return (minTime,maxTime)
        
    def getString(self,rawdata):                                                                       # parses chirp from raw data (chirps,timestamps)
        string = []
        for y in rawdata:
            y
            string.append(y[0])
        return string
                  

#test
if __name__=="__main__":
    x = ChirpData()
    x.chirpAdd("num3 with \"double quotes\" and 'single quotes'")
    #x.getOlderChirps(20,myQuery= '%')
    x.getNewerChirps(20, myQuery='%')
#    x.ManageConnection()
# this is a new line
#        for row in cur.fetchall():
#            print row