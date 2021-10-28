import hou

def checkAOVs(node):

	ref = node.parm('RS_aovGetFromNode').eval()

	# if empty then test whether disable aovs is checked on this node

	if ref == '':
		warning(node)

	# if it is referencing a relative path then test that node

	else:
		if ref.startswith('..'):

			ref_node = node.node(ref)

			warning(ref_node)

	# if it is referencing a full path then test that node

		else:
			ref_node = hou.node(ref)

			warning(ref_node)

	return None


def warning(check_node):
	p = check_node.parm('RS_aovAllAOVsDisabled').eval()

	if p ==1:
		hou.ui.displayMessage("**Warning** " + check_node.name() + "has all AOVs disabled") 

	# else: 
	# 	hou.ui.displayMessage("No WarningN" + check_node.name())

	return None