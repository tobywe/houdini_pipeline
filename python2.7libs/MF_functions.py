
import hou
import os

def set_preset(node_path, preset_name):
    cmd = 'oppresetload %s "%s"' % (node_path, preset_name)
    hou.hscript(cmd)
    
    return None


def get_dir(target_dir):
    h = hou.getenv('HIP')
    s = h.split('/')
    s[0] = 'L:\\'
    i = s.index(target_dir) 
    si = s[0:i + 1]
    dir = os.path.join(*si)
    dir = dir.replace(os.sep, '/')
    #print dir
    return dir

