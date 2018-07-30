# -*- coding: utf-8 -*-
"""
Created on Sat Jul 14 23:41:31 2018

@author: Hualin Xiao, hualin.xiao@psi.ch
"""
import sys
import shutil
import os 
import json
import numpy as np
import ConfigParser as conf
import utils


class ExportConfig:
    def __init__(self,fuuid):

        self._fuuid=fuuid
        self._output_dir='{}/{}'.format(conf.project_directory(),self._fuuid)
        utils.mkdir(self._output_dir)
        self._fname='{}/config.json'.format(self._output_dir)
        
        self._data={'material':{},'precision':{},'physvolname':{}}
        self._file=None
        self._materials=dict()
        self._precision=dict()
        self._physvolname=dict()
        self.loadJson(self._fname)

    @property
    def data(self):
        return self._data

    def loadJson(self, filename):
        try:
           f=open(self._fname,'r') 
           self._file=f
           self._data=json.loads(f.read())
           print 'reading:'
           print self._data
           self._materials=self._data['material']
           self._precision=self._data['precision']
           self._physvolname=self._data['physvolname']
           f.close()
           self._ok={'response':'ok'}
           self._error={'response':'error'}
        except:
           print 'can not open file or load json'
           
       #else:

    def __del__(self):
        self.dump()
    
    def dump(self):
        self._data['material']=self._materials
        self._data['precision']=self._precision
        self._data['physvolname']=self._physvolname
        try:
            js=json.dumps(self._data)
            print js
            with open(self._fname,'w') as f:
                f.write(js)
                return self._ok
        except:
            return self._error
            print 'error occurred when writing file'

    
    def setMaterial(self, puuid,material):
        try:
            self._materials[puuid]=material
            dump()
            return self._ok
        except:
            print 'error occurred when set material'
            return self._error


    def setPrecision(self, puuid,precs):
        try:
            self._precision[puuid]=precs
            dump()
            return self._ok
        except:
            print 'error occurred when set precision'
            return self._error
    def setPhysicVolumeName(self, puuid,name):
        try:
            self._physvolname[puuid]=name
            dump()
            return self._ok
        except:
            return self._error


    def getMaterial(self,puuid):
        try:
            return self._materials[puuid]
        except:
            return None

    def getPrecision(self,puuid):
        try:
            return self._precision[puuid]
        except:
            return None

    def getPhysVolumeName(self,puuid):
        try:
            return self._physvolname[puuid]
        except:
            return None


    def getMaterialJSON(self,puuid):
        try:
            return {"data":self._materials[puuid]}
        except:
            return self._error

    def getPrecisionJSON(self,puuid):
        try:
            return {"data":self._precision[puuid]}
        except:
            return self._error

    def getPhysVolumeNameJSON(self,puuid):
        try:
            return {"data":self._physvolname[puuid]}
        except:
            return self._error







if __name__=='__main__':
    fid='d56b8522f811434c8037fe1403adaed2'
    uid='f5fcce4f16d443e31b932c4098838'
    p=ExportConfig(fid)
    p.setMaterial(uid,'G4_Al')
    p.dump()
    
    #p2=ExportConfig(fid)
    #p2.printMaterial(uid)
    #p=ExportConfig()
    #print p.parse('step/lrg.stp')




