# -*- coding: utf-8 -*-
"""
Created on Sat Jul 14 23:41:31 2018
@author: Hualin Xiao, dr.hualin.xiao@gmail.com
"""

import sys
FREECADPATH = '/usr/lib/freecad/lib' # path to your FreeCAD.so or FreeCAD.dll file
sys.path.append(FREECADPATH)

import FreeCAD as App
from werkzeug.utils import secure_filename

import Part
import Mesh
import Import
import datetime
import shutil
import os 
import json
import numpy as np
import uuid
import ConfigParser as conf
import ThreeJson
import utils


class CadParser:
    def __init__(self,filename=None):
        self._bound_boxes=[]
        self._mass_centers=[]
        self._doc=None
        self._parts=[]
        self._fuuid=uuid.uuid4().hex
        self._json_data=None

        self._output_dir='{}/{}'.format(conf.project_directory(),
                self._fuuid)

        utils.mkdir(self._output_dir)
        

        self._status={}



        
        self._fcstd_fname='{}/project.fcstd'.format(self._output_dir)

        if filename:
            self.importCAD(filename)


    def dump(self):
        if self._doc:
            self._doc.saveAs(self._fcstd_fname)
            App.closeDocument(self._doc.Name)

    def dumpJson(self, jstr,uuid):
        fname='{}/{}.json'.format(self._output_dir,uuid)
        with open(fname,'w') as f:
            print('writing json file:{}'.format(fname))
            f.write(jstr)

    def dumpStatus(self,jstr):
        fname='{}/stat.json'.format(self._output_dir)
        with open(fname,'w') as f:
            print('writing json file:{}'.format(fname))
            f.write(jstr)



    def importCAD(self,filename):
        self._status={'status':'error','fuuid':self._fuuid,'obs':[]};
        try:

            infos=[]
            self._source_filename=filename

            if filename.endswith('.fcstd'):

                FreeCAD.open(filename)
            else:
                Import.open(filename)

            self._doc=App.ActiveDocument
            self._objects=self._doc.Objects
            self._json_data=[]
            n_ok=0
            self._doc.Id=self._fuuid
            for i in self._objects:
                uid=uuid.uuid4().hex
                label=secure_filename(i.Label)
                i.Label=uid

                if self.tessellate(i,uid):
                    info={'uuid':uid,'label':label}
                    infos.append(info);
                    n_ok+=1

            self._status['status']='ready'
            self._status['n']=n_ok
            self._status['obs']=infos
            self.dump()
        except:
            pass

        json_response=json.dumps(self._status)
        self.dumpStatus(json_response)
        return json_response


    


    def computeTolerance(self,part):
        try:
            boundbox=part.Shape.BoundBox
            bound_x=round(boundbox.XLength,3)
            bound_y=round(boundbox.YLength,3)
            bound_z=round(boundbox.ZLength,3)
            bound_max_len=max([bound_x,bound_y,bound_z])
            precision=bound_max_len/200.
            if bound_max_len<10:
                precision=0.1 
            return precision
        except:
            return 1

    
    def tessellate(self,obj,uid):
	'''Returns tessellation with specified tolerance.'''
	#self._doc.recompute()
	# Don't fuse all objects before tessellating, just tessellate all visible objects
	visibleObjs = []
        tolerance=self.computeTolerance(obj)

	vertices = []; nVertices = 0;
	faces = []; nFaces = 0;

        is_ok=False
	#for obj in self._objects:
        if obj:
		sV = nVertices;
		if obj.isDerivedFrom("Part::Feature"): # Standard case
		    shape = obj.Shape
		    bMesh = False

		elif obj.isDerivedFrom("Part::TopoShape"):
		    shape = obj
		    bMesh = False

		elif obj.isDerivedFrom("Mesh::Feature"):
			objVertices = obj.Mesh.Points
			objFaces = obj.Mesh.Facets
			bMesh = True
			
		else:
			raise Warning("Object type not recognised.")
		if shape:
			try:
				tess = shape.tessellate(tolerance) # Throws TypeError
                                is_ok=True
				objVertices = tess[0]
				objFaces = tess[1]
			except TypeError:
				raise Warning("Accuracy parameter is of the wrong type")

		for vec in objVertices:
			nVertices += 1
			vertices.extend( [vec.x, vec.y, vec.z] )
		for face in objFaces:
			nFaces += 1
			if len(face) == 3:
				TYPE = 0 # To indicate triangle (see three.js JSON object notation spec)
				if bMesh:
					face = face.PointIndices # face.PointIndices is a tuple
				faces.extend( [ TYPE, face[0]+sV,face[1]+sV,face[2]+sV ] )
			else:
				raise Warning("This face is no triangle, it has length %s" % len(face) )
        if is_ok:
            data = ThreeJson.tessToJson(uid,vertices, faces, nVertices, nFaces )
            self.dumpJson(data,uid)

        return is_ok
	


if __name__=='__main__':
    p=CadParser()
    print p.importCAD('step/lrg.stp')




