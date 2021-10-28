import datetime
import os
import hou
import MF_functions
# from os.path import dirname as up


 


if hou.getenv('JOB') == 'template':

	import hdefereval

	# get hip directory 
	hip_dir = hou.getenv('HIP')


	# get houdini directory
	houdini =  MF_functions.get_dir('houdini')

	# set assets var
	assets = MF_functions.get_dir('workspace') + '/assets' 
	hou.putenv('ASSETS', assets)

	# set shot var
	shot = os.path.split(hip_dir)[1]
	#hou.putenv('SHOT', shot)

	# set job var
	project_folder = houdini + '/__project_folder__'
	hou.putenv('JOB', project_folder)

	# set shot var
	hou.hscript("setenv SHOT = " + shot)
	hou.hscript("varchange SHOT") # this is optional and probably not needed 	

	# set shot dir var
	hou.hscript("setenv SHOT_DIR = " + hip_dir)
	hou.hscript("varchange SHOT_DIR")	

	# set flip dir var
	flip_dir = project_folder + '/flip/' + shot
	hou.hscript("setenv FLIP = " + flip_dir)
	hou.hscript("varchange FLIP")
	print('hello')
	if not os.path.exists(flip_dir):
		print('hello_again')
		os.mkdir(flip_dir)

	# set render dir var
	render_dir = project_folder + '/render/' + shot
	hou.hscript("setenv RENDER = " + render_dir)
	hou.hscript("varchange RENDER")



	hou.hscript("setenv HOUDINI_OTLSCAN_PATH = " + project_folder + '/hda;' )
	hou.hscript("setenv HOUDINI_OTLSCAN_PATH = " + project_folder + '/otls;' )

	# get job name and save new file	'''archiveId_campaingId_projectId'''
	project = hip_dir.split('/')[1]
	projectId = project.split('_')[2]
	save_path = hip_dir + '/' + projectId + '_' + shot + '_v0001' + '.hip'

	# SETUP LIGHTS

	light_names = ['AREA', 'SPOT', 'DISTANT', 'DOME']
	lgt_node_shapes = ['light', 'light', 'bulge', 'circle']

	for i in range(4):
	        if i < 3:
	                l = hou.node('obj').createNode('rslight')

	        else:
	                l = hou.node('obj').createNode('rslightdome::2.0')

	        # set position, name, shape, colour and preset, and add to netbox
	        l.setPosition([-36.0609, 3.705 - (i * 1.2)])
	        l.setName('rs_lgt_' + light_names[i] + '_01', True)
	        l.setUserData('nodeshape', lgt_node_shapes[i])
	        l.setColor(hou.Color(1, 0.725, 0))
	        MF_functions.set_preset(l.path(), 'MF_RS_' + light_names[i])
	        hou.node('obj').findNetworkBox('net_lights').addNode(l)

	# SETUP CAMERA

	cam = hou.node('obj').createNode('cam')
	cam.parmTuple('t').set((0,1,5))
	cam.setPosition([-41.505, 3.705])
	cam.setColor(hou.Color(0, 0, 0))
	cam.setUserData('nodeshape', 'circle')
	cam.setName('camMain', True)
	hou.node('obj').findNetworkBox('net_cameras').addNode(cam)



	# CREATE ROPS
	rop_names = ['BTY', 'DEEP']
	rop_colors = [[0.302, 0.525, 0.114], [0.306, 0.306, 0.306]]

	for i in range(2):
		rop = hou.node('/out').createNode('Redshift_ROP')
		MF_functions.set_preset(rop.path(), 'MF_RS_' + rop_names[i])
		rop.setColor(hou.Color(rop_colors[i]))
		rop.setName(rop_names[i], True)
		rop.moveToGoodPosition()





	# A function that needs the UI to be fully available (i.e. for desktop manipulation)
	def functionToExecuteOnStartup():
		fps = int(hou.ui.readInput('Input the project fps: ')[1])
		hou.setFps(fps)
		hou.playbar.setFrameRange(1000, 1000 + (10* fps))
		hou.playbar.setPlaybackRange(1000, 1000 + (10* fps))

	hdefereval.executeDeferred(functionToExecuteOnStartup)


	if not(os.path.exists(save_path)):
			hou.hipFile.save(save_path)