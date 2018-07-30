import os
def mkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def printf(msg, type='msg'):
    try:
        import FreeCAD
        if type=='msg':
            FreeCAD.Console.PrintMessage(msg)
        else:
            FreeCAD.Console.PrintWarning(msg)
    except:
        print(msg)
def getCurrentPath():
    return  os.path.dirname(os.path.realpath(__file__))

