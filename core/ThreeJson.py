#
# Adapted from https://github.com/dcowden/cadquery/blob/master/cadquery/freecad_impl/exporters.py
#     Objects that represent
#     three.js JSON object notation
#     https://github.com/mrdoob/three.js/wiki/JSON-Model-format-3
#
import random 
JSON_TEMPLATE= """\
{
    "metadata" :
    {
        "formatVersion" : 3,
        "generatedBy"   : "ParametricParts",
        "vertices"      : %(nVertices)d,
        "faces"         : %(nFaces)d,
        "normals"       : 0,
        "userData"      : "%(uuid)s",
        "uvs"           : 0,
        "materials"     : 1,
        "morphTargets"  : 0
    },

    "scale" : 1.0,
    "vertices": %(vertices)s,

    "morphTargets": [],

    "normals": [],

    "colors": [],

    "uvs": [[]],

    "faces": %(faces)s
}
"""

def tessToJson(puid, vert, face, nvert, nface):
    '''Specify compatible lists of vertices and faces,
    and get a three.js JSON object back. Note: list of face indices
    must be compatible, i.e. lead with 0 for each row of 3 indices
    to create a triangle. Spec:
    https://github.com/mrdoob/three.js/wiki/JSON-Model-format-3'''

    return JSON_TEMPLATE % {
        'uuid':str(puid),
        'vertices' : str(vert),
        'faces' : str(face),
        'nVertices': nvert,
        'nFaces' : nface
    };

