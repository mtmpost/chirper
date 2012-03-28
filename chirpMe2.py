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
cgitb.enable(display=0, logdir="/tmp")

#from datetime import datetime
config = ConfigParser.RawConfigParser()
config.readfp(open('user.cfg'))
dbcfg = config.get('UserSection','db')
usercfg = config.get('UserSection','user')
passwdcfg = config.get('UserSection','pwd')

class ChirpData:
    def __init__(self,host="localhost",user=usercfg,passwd=passwdcfg,db=dbcfg):        #Constructor
        self.host = host
        self.db = db
        self.user = user
        self.passwd = passwd
        
    def CreateConnection(self):
        self.conn = MySQLdb.connect(self.host,self.user,self.passwd,self.db)

    def DestroyConnection(self):
        self.conn.close()

#    def ManageConnection(self):
#        sql_lastChirp = "SELECT MAX(UNIX_TIMESTAMP(C_Time)) FROM cHirps;"
#        time = time.time()
#        #time = datetime.time(datetime.now())
#        conn = ChirpMe.CreateConnection()
#        lastChirpTime = conn.ExecCur(sql_lastChirp)
#        #print time, lastChirpTime 

    def ExecCur(self,sql_statement):
        cursor = self.conn.cursor()
        cursor.execute(sql_statement)
        result = cursor.fetchall()
        return result
        cursor.close()

    def Clean(self,chirp):
        return chirp.replace('"','""').replace("'","''")

    def chirpAdd(self,chirp):
        #cleanChirp = self.Clean(chirp)
        #sql_statement = "INSERT INTO cHirps(C_String,C_Time) VALUES(\'%s\',TIMESTAMP(now()));" % (cleanChirp)
        self.CreateConnection()
        self.ExecCur("INSERT INTO cHirps(C_String,C_Time) VALUES(%s,TIMESTAMP(now()))",(chirp))
        self.DestroyConnection()

    def getOlderChirps(self,maxNum,query='',maxDate=time.time()):                                    # main method that populates login.py with chirps and queries  
        query = '%'+query+'%'
        #query = self.Clean(query)
        #sql_statement = "SELECT C_String, UNIX_TIMESTAMP(C_Time) FROM cHirps WHERE UNIX_TIMESTAMP(C_Time)<=\'%i\' AND C_String LIKE \'%s\' ORDER BY C_Time DESC LIMIT 0,%i;" % (maxDate,query,maxNum)
        self.CreateConnection()
        rawdata = self.ExecCur("SELECT C_String, UNIX_TIMESTAMP(C_Time) FROM cHirps WHERE UNIX_TIMESTAMP(C_Time)<=%i AND C_String LIKE %s ORDER BY C_Time DESC LIMIT 0,%i;" % (maxDate,query,maxNum))
        if not rawdata:                                                                            #if query not found exception
            return ['Nothing like \"%s\" in here' % (query.replace('%',''))] 
        minmaxTime = self.getTime(rawdata)
        minTime = minmaxTime[0]
        return self.getString(rawdata)
        self.DestroyConnection()
        
                                                                                                  #for now, getNewerChirps sql_statement set to select times newer than now - 300 until 
                                                                                                  #I can get a starttime varible
    def getNewerChirps(self,maxNum,query,maxDate=time.time()):
        query = '%'+query+'%'
        #sql_statement = "SELECT C_String, UNIX_TIMESTAMP(C_Time) FROM cHirps WHERE UNIX_TIMESTAMP(C_Time)>(\'%i\'-3000) AND C_String LIKE \'%s\' ORDER BY C_Time DESC LIMIT 0,%i;" % (maxDate,query,maxNum)
        self.CreateConnection()
        rawdata = self.ExecCur("SELECT C_String, UNIX_TIMESTAMP(C_Time) FROM cHirps WHERE UNIX_TIMESTAMP(C_Time)>(%i-3000) AND C_String LIKE %s ORDER BY C_Time DESC LIMIT 0,%i;", (maxDate,query,maxNum))
        if not rawdata:                                                                              #if query not found exception
            return ['Nothing like \"%s\" in here' % (query.replace('%',''))]
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
    #x.getOlderChirps(20,query= '%')
    x.getNewerChirps(20, query='%')
#    x.ManageConnection()

#        for row in cur.fetchall():
#            print row