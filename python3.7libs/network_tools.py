"""
FUNCTIONS:
add_node()
obj_merge_out()
obj_merge_paste()
findReplaceParmString()
switch_between()
switch_between_objMerge()
findReplaceParmString()
name_from_input()
add_sticky()
bake_camera()
"""


import hou

# ADD NODE - input node name to function

def add_node(node):
    import hou
    network = hou.ui.curDesktop().paneTabUnderCursor()
    pos = network.cursorPosition()
    selected = hou.selectedNodes()
    
    if selected != ():
        selected = selected[0]
        outputs = selected.outputs()
        parent = selected.parent()
        
        null = parent.createNode(node)
        null.setFirstInput(selected)
        null.moveToGoodPosition()

        # If sops then assign render and vis flags
        if network.pwd().childTypeCategory().name() == 'Sop':
	        null.setDisplayFlag(True)
	        null.setRenderFlag(True)
	        null.setCurrent(True, True)


        
        for output in outputs:
            i=0
            inputs = output.inputs()
            index = inputs.index(selected)
            output.setInput(index, null)
            i += 1       
        
        
        
    else:
        network = hou.ui.curDesktop().paneTabUnderCursor()
        networkpath = network.pwd().path()
        null = hou.node(networkpath).createNode(node)
        null.setPosition(pos)

        # If sops then assign render and vis flags
        if network.pwd().childTypeCategory().name() == 'Sop':
	        null.setDisplayFlag(True)
	        null.setRenderFlag(True)
	        null.setCurrent(True, True)
        






# OBJ MERGE OUT

def obj_merge_out():

    import hou
    
    network = hou.ui.curDesktop().paneTabUnderCursor()
    networkpath = network.pwd().path()
    pos = network.cursorPosition()
    
    node = hou.selectedNodes()[0]
    parent = node.parent()
    
    # add OUT null
    input = hou.ui.readInput('New Object Name', ['render', 'plain'])
    name = input[1].replace(' ', '_')
    out = parent.createNode('null', 'OUT_' + name)
    out.setColor(hou.Color((0.475, 0.812, 0.204)))
    out.setFirstInput(node)
    out.moveToGoodPosition()
    
    
    
    if(input[0] == 1):
        new_obj = hou.node('/obj/').createNode('geo', name)
        fetch = new_obj.createNode('object_merge', 'fetch_' + name)
        
    else:
		new_obj = hou.node('/obj/').createNode('geo', 'RNDR_' + name)
		new_obj.setColor(hou.Color((0.475, 0.812, 0.204)))
		fetch = new_obj.createNode('object_merge', 'fetch_' + name)
		material = new_obj.createNode('material')
		material.setFirstInput(fetch)
		material.moveToGoodPosition()        
		normal = new_obj.createNode('normal')
		normal.setFirstInput(material)
		normal.moveToGoodPosition()

		rndr_null = new_obj.createNode('null', 'rndr_null')
		rndr_null.moveToGoodPosition()

		rndr_switch = new_obj.createNode('switch', 'render_switch')
		rndr_switch.setFirstInput(normal)
		rndr_switch.setNextInput(rndr_null)
		rndr_switch.moveToGoodPosition()

		out_null = new_obj.createNode('null', 'OUT_RNDR')
		out_null.setFirstInput(rndr_switch)
		out_null.moveToGoodPosition()
		out_null.setCurrent(True, True)
		out_null.setRenderFlag(True)
		out_null.setColor(hou.Color((0.475, 0.812, 0.204)))

        
        
    new_obj.moveToGoodPosition()
    
    fetch.parm('objpath1').set( out.path() )
    network.cd( new_obj.path() )





# PASTE OBJ MERGE 
def obj_merge_paste():
    import hou

    network = hou.ui.curDesktop().paneTabUnderCursor()
    networkpath = network.pwd().path()
    pos = network.cursorPosition()

    clipboard = hou.ui.getTextFromClipboard()

    obj_merge_list = []
    n = 0

    if clipboard:
        list = clipboard.split()
        for item in list:
            if hou.node(item) != None:
                merge = hou.node(networkpath).createNode('object_merge','merge_'+item.split('/')[-1])
                merge.parm('objpath1').set(str(item))
                merge.setPosition(pos)
                merge.move([n*2,0])
                if n == 0:
                    merge.setSelected(True,True)
                else:
                    merge.setSelected(True,False)
                n = n + 1
                obj_merge_list.append(merge)

 	return obj_merge_list               


# SWITCH BETWEEN
def switch_between():
    import hou
    network = hou.ui.curDesktop().paneTabUnderCursor()
    pos = network.cursorPosition()
    selected = hou.selectedNodes()
    networkpath = network.pwd().path()

    # Create switch
    switch = hou.node(networkpath).createNode('switch')
    switch.setPosition(pos)
    switch.setDisplayFlag(True)
    switch.setRenderFlag(True)
    switch.setCurrent(True, True)

    for i in range(len(selected)):
        switch.setInput(i, selected[i], 0)



# SWITCH BETWEEN OBJ MERGE
def switch_between_objMerge():
    import hou
    network = hou.ui.curDesktop().paneTabUnderCursor()
    pos = network.cursorPosition()
    selected = hou.selectedNodes()
    networkpath = network.pwd().path()

    obj_merge_nodes = obj_merge_paste()

    # Create switch
    switch = hou.node(networkpath).createNode('switch')
    switch.setPosition(pos)
    switch.setDisplayFlag(True)
    switch.setRenderFlag(True)
    switch.setCurrent(True, True)

    for i in range(len(obj_merge_nodes)):
        switch.setInput(i, obj_merge_nodes[i], 0)

    switch.moveToGoodPosition()




# FIND AND REPLACE PARM STRINGS

def findReplaceParmString():
	import hou

	sel = hou.selectedNodes()
	        
	dialog = hou.ui.readMultiInput('Find/Replace In Expression', input_labels=['Find: ', 'Replace: ',], buttons=("Find/Replace", "Cancel"),
	     severity=hou.severityType.ImportantMessage, title='Find/Replace', close_choice=1)

	find = dialog[1][0]
	replace = dialog[1][1]


	if dialog[0] == 0:
	    for n in sel:
	        for parms in n.parms():
	            try:
	                newString = str(parms.eval()).replace(find, replace)
	                parms.set(newString)
	            except:
	                print ''
	            try:
	                newExpression = str(parms.expression()).replace(find, replace)
	                parms.setExpression(newExpression)
	            except:
	                print ''
        

# SET NAME FROM INPUT

def name_from_input():
    prefix = hou.ui.readInput('PREFIX', initial_contents='out')[1]
    nodes = hou.selectedNodes()

    for n in nodes:
            n.setName(prefix + '_' + n.inputs()[0].name())


# ADD STICKY

def add_sticky():
    import hou
    network = hou.ui.curDesktop().paneTabUnderCursor()
    pos = network.cursorPosition()
    selected = hou.selectedNodes()
    

    selected = selected[0]
    parent = selected.parent()
    
    sticky = parent.createStickyNote()
    sticky.setDrawBackground(0)
    sticky.setTextSize(3.0)
    sticky.setText('label')
    sticky.setPosition(pos)
    sticky.setSize( (12, 6))
    return None



# BAKE CAMERA

def bake_camera():
 	import hou

	selectedNode = hou.selectedNodes()[0]

	bakingNode = hou.node('/obj').createNode('cam', selectedNode.name() + '_bake')


	hou.setFrame(int(hou.playbar.playbackRange()[0]))

	for f in range(int(hou.playbar.playbackRange()[0]), int(hou.playbar.playbackRange()[1])+1):
	    hou.setFrame(f)
	    
	    bakingNode.setWorldTransform(selectedNode.worldTransform())
	    bakingNode.parm("tx").setKeyframe(hou.Keyframe(bakingNode.parm("tx").eval()))
	    bakingNode.parm("ty").setKeyframe(hou.Keyframe(bakingNode.parm("ty").eval()))
	    bakingNode.parm("tz").setKeyframe(hou.Keyframe(bakingNode.parm("tz").eval()))
	    bakingNode.parm("rx").setKeyframe(hou.Keyframe(bakingNode.parm("rx").eval()))
	    bakingNode.parm("ry").setKeyframe(hou.Keyframe(bakingNode.parm("ry").eval()))
	    bakingNode.parm("rz").setKeyframe(hou.Keyframe(bakingNode.parm("rz").eval()))
	    
	    
	    bakingNode.parm('focal').setKeyframe(hou.Keyframe(selectedNode.parm('focal').eval()))
	    bakingNode.parm('aperture').setKeyframe(hou.Keyframe(selectedNode.parm('aperture').eval()))
	    bakingNode.parm('near').setKeyframe(hou.Keyframe(selectedNode.parm('near').eval()))
	    bakingNode.parm('far').setKeyframe(hou.Keyframe(selectedNode.parm('far').eval()))
	    bakingNode.parm('resx').setKeyframe(hou.Keyframe(selectedNode.parm('resx').eval()))
	    bakingNode.parm('resy').setKeyframe(hou.Keyframe(selectedNode.parm('resy').eval()))
	    bakingNode.parm('winsizex').setKeyframe(hou.Keyframe(selectedNode.parm('winsizex').eval()))
	    bakingNode.parm('winsizey').setKeyframe(hou.Keyframe(selectedNode.parm('winsizey').eval()))
	    bakingNode.parm('shutter').setKeyframe(hou.Keyframe(selectedNode.parm('shutter').eval()))
	    bakingNode.parm('aspect').setKeyframe(hou.Keyframe(selectedNode.parm('aspect').eval()))





