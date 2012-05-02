#!/usr/bin/python

'''
Created on Mar 27, 2012

@author: michaelmcgovern
'''

import MySQLdb
import time
import cgitb
import ConfigParser
cgitb.enable(display=1, logdir="/tmp")

#from datetime import datetime


class ChirpData:
    def __init__(self,configFile='user.cfg'):        #Constructor
        self.config = configFile
        
    def create_connection(self):
        config = ConfigParser.RawConfigParser()
        config.readfp(open(self.config))
        dbcfg = config.get('UserSection','db')
        usercfg = config.get('UserSection','user')
        passwdcfg = config.get('UserSection','pwd')
        hostcfg = config.get('UserSection','host')
        sockcfg = config.get('UserSection','sock')
        self.conn = MySQLdb.connect(hostcfg,usercfg,passwdcfg,dbcfg,unix_socket=sockcfg)

    def destroy_connection(self):
        self.conn.close()

#    def manage_connection(self):
#        sql_lastChirp = "SELECT MAX(UNIX_TIMESTAMP(C_Time)) FROM cHirps;"
#        time = time.time()
#        #time = datetime.time(datetime.now())
#        conn = ChirpMe.CreateConnection()
#        lastChirpTime = conn.ExecCur(sql_lastChirp)
#        #print time, lastChirpTime 

    def exec_cur(self,sql_statement,params):
        #print 'these are the params',params
        cursor = self.conn.cursor()
        cursor.execute(sql_statement,params)
        result = cursor.fetchall()
        return result
        cursor.close()

    def chirp_add(self,chirp):
        self.create_connection()
        self.exec_cur("INSERT INTO cHirps(C_String,C_Time) VALUES(%s,TIMESTAMP(now()))",(chirp))
        self.destroy_connection()

    def get_older_chirps(self,maxNum,myQuery="",maxDate=time.time()):                                    # main method that populates login.py with chirps and queries  
        self.create_connection()
        if myQuery !="":
            rawdata = self.exec_cur("SELECT C_String, UNIX_TIMESTAMP(C_Time)" + 
                                   " FROM cHirps WHERE UNIX_TIMESTAMP(C_Time)<= %s" + 
                                   " AND C_String regexp %s ORDER BY C_Time DESC LIMIT 0,%s;" , (int(maxDate),myQuery,maxNum))
        else:
            rawdata = self.exec_cur("SELECT C_String, UNIX_TIMESTAMP(C_Time)" +
                                   " FROM cHirps WHERE UNIX_TIMESTAMP(C_Time)<= %s" + 
                                   " ORDER BY C_Time DESC LIMIT %s,%s;", (int(maxDate),0,maxNum))
        if not rawdata:                                                                            #if myQuery not found exception
            return ['Nothing like %s in here' % (myQuery)] 
        minmaxTime = self.get_time(rawdata)
        minTime = minmaxTime[0]
        return self.get_string(rawdata)
        self.destroy_connection()
        
                                                                                                  #for now, getNewerChirps sql_statement set to select times newer than now - 300 until 
                                                                                                  #I can get a starttime varible
    def get_newer_chirps(self,maxNum,myQuery='',maxDate=int(time.time())):
        self.create_connection()
        if myQuery !='':
            rawdata = self.exec_cur("SELECT C_String, UNIX_TIMESTAMP(C_Time) FROM cHirps" + 
                                   "WHERE UNIX_TIMESTAMP(C_Time)>(%i-3000) AND C_String regex %s"+ 
                                   "ORDER BY C_Time DESC LIMIT 0,%i;", (maxDate,myQuery,maxNum))
        else:
            rawdata = self.exec_cur("SELECT C_String, UNIXTIMESTAMP(C_Time) FROM cHirps" +
                                   "WHERE UNIXTIMESTAMP(C_Time)>= %s ORDER BY C_Time ASC LIMIT 0,%s;",(maxDate, maxNum))
        if not rawdata:                                                                              #if myQuery not found exception
            return ['Nothing like \"%s\" in here' % (myQuery.replace('%',''))]
        minmaxTime = self.get_time(rawdata)
        maxTime = minmaxTime[1]
        return self.get_string(rawdata)
        self.destroy_connection()



    def get_time(self,rawdata):                                                                        #rawdata is a tuple containing tuples of (string,time) from db
        minmaxTime =[]
        for y in rawdata:
            minmaxTime.append(y[1])
        minTime = min(minmaxTime)
        maxTime = max(minmaxTime)
        return (minTime,maxTime)
        
    def get_string(self,rawdata):                                                                       # parses chirp from raw data (chirps,timestamps)
        string = []
        for y in rawdata:
            y
            string.append(y[0])
        return string
                  

#test
if __name__=="__main__":
    x = ChirpData()
    x.chirp_add("num3 with \"double quotes\" and 'single quotes'")
    #x.getOlderChirps(20,myQuery= '%')
    x.get_newer_chirps(21, myQuery='%')
#    x.ManageConnection()
# this is a new line
#        for row in cur.fetchall():
#            print row