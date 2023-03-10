#! python3
#Program generates config to delete I and B channel


vlan = input('vlan: ')
vlan_second = input('Second vlan or blank space: ')
channel_type = input('Channel type?')


#-------------------------------B-channel until line 388---------------------

if channel_type.lower() == 'b':
	connection_type = input('l2vc or direct?')
	router_type = input('Enter router type(CX8/CX)')

#--------------------------------Direct-------------------------

	if connection_type.lower() == 'direct':
		rt_interface = input('Router interface:')
		l2_switches = []
		uplinks = []
		downlinks = []
		for x in range(int(input('Number of L2 switches: '))):
			l2_switches.append(input('Next switch '))
			uplinks.append(input('uplink interface: '))
			downlinks.append(input('downlink interface: '))
		print('''---------CX/CX8 direct---------

undo interface {1}.{0}
q
save'''
.format(vlan, rt_interface))
		for sw in l2_switches:
			if sw in {'q9', 'q5', 'q3'}:
				print('''----------{3}------------
interface {1}
undo port t a v {0}
interface {2}
undo port t a v {0}
q
undo vlan {0}
q
save
'''.format(vlan, uplinks[l2_switches.index(sw)], downlinks[l2_switches.index(sw)], sw))
			elif sw in {'q8', 'hp'}:
				print('''-----------Q8/HP--------------
interface {1}    	   
 undo port t per vlan {0} 
interface {2}
undo port t per vlan {0}
'''.format(vlan, uplinks[l2_switches.index(sw)], downlinks[l2_switches.index(sw)]) )
			elif sw == 'ec_last':
				print('''----------EC-lastswitch------------------
conf
interface {1}
no description
switchport native vlan 1
exi
vlan data
no vlan {0}
end
copy run st'''.format(vlan, downlinks[l2_switches.index(sw)]))
			elif sw == 'ec':
				print('''----------EC------------------
conf
vlan data
no vlan {0}
end
copy run st'''.format(vlan))
			elif sw == 'rt':
				print('''-----------RubyTech---------
vlan
del tag-group {0}
exit
save start'''.format(vlan))
			else:
				print('''------------Iscom-----------
conf
interface port {1}
no description 
exi
no vlan {0}
end
wr'''.format(vlan, uplinks[l2_switches.index(sw)], downlinks[l2_switches.index(sw)]))

#---------------------------------Hybrid--------------------------------------------

	elif connection_type.lower() == 'hybrid':
		rt_interface = input('Router interface:')
		first_switch = input('First directly connected switch(Q8/Q9): ')
		fsw_interface = input('Interface on first switch')
		l3_switch = input('Enter mpls switch type(Q9/Q8/HP/CX ')
		interface = input('L3 switch interface: ')        
		l2_switches = []
		uplinks = []
		downlinks = []
		for x in range(int(input('Number of L2 switches: '))):
			l2_switches.append(input('Next switch '))
			uplinks.append(input('uplink interface: '))
			downlinks.append(input('downlink interface: '))
		print('''---------CX/CX8 direct---------

undo interface {1}.{0}
q
save'''
.format(vlan, rt_interface))

		if first_switch.lower() == 'q9':
			print('''
*************Q9*************

interface vlan {0}
undo mpls l2vc
q
undo interface vlan {0}
undo vlan {0}
interface {1}
undo port t al vlan {0} 
q
q
save
'''.format(vlan, fsw_interface))

		elif first_switch.lower() == 'q8':
			print('''
************Q8***********

interface vlan {0}
undo mpls l2vc
q
undo interface vlan {0}
undo vlan {0}
interface {1}          
undo port t per vlan {0} 
q
'''.format(vlan, fsw_interface))

		if l3_switch.lower() == 'hp':
			print('''
************HP*********

interface  {1}
undo service-ins {0}
qu
qu
save'''.format(vlan if vlan_second == '' else vlan_second, interface))
		elif l3_switch.lower() == 'q8':
			print('''
************Q8***********

interface vlan {0}
undo mpls l2vc
q
undo interface vlan {0}
undo vlan {0}
interface {1}          
undo port t per vlan {0} 
q
'''.format(vlan if vlan_second == '' else vlan_second, interface)
			  )
		elif l3_switch.lower() == 'q9':
			print('''
*************Q9*************

interface vlan {0}
undo mpls l2vc
q
undo interface vlan {0}
undo vlan {0}
interface {1}
undo port t al vlan {0} 
q
q
save
'''.format(vlan if vlan_second == '' else vlan_second, interface))

		for sw in l2_switches:
			if sw in {'q9', 'q5', 'q3'}:
				print('''----------{3}------------
interface {1}
undo port t a v {0}
interface {2}
undo port t a v {0}
q
undo vlan {0}
q
save
'''.format(vlan if vlan_second == '' else vlan_second, uplinks[l2_switches.index(sw)], downlinks[l2_switches.index(sw)], sw))
			elif sw in {'q8', 'hp'}:
				print('''-----------Q8/HP--------------
interface {1}          
 undo port t per vlan {0} 
interface {2}
undo port t per vlan {0}
'''.format(vlan if vlan_second == '' else vlan_second, uplinks[l2_switches.index(sw)], downlinks[l2_switches.index(sw)]))
			elif sw == 'ec_last':
				print('''----------EC-lastswitch------------------
conf
interface {1}
no description
switchport native vlan 1
exi
vlan data
no vlan {0}
end
copy run st'''.format(vlan, downlinks[l2_switches.index(sw)]))
			elif sw == 'ec':
				print('''----------EC------------------
conf
vlan data
no vlan {0}
end
copy run st
'''.format(vlan if vlan_second == '' else vlan_second))
			elif sw == 'rt':
				print('''-----------RubyTech---------
vlan
del tag-group {0}
exit
save start
'''.format(vlan if vlan_second == '' else vlan_second))
			elif sw == 'qs':
				print('''----------QS------------
interface {1}
undo description
q
undo vlan {0}
'''.format(vlan if vlan_second == '' else vlan_second, downlinks[l2_switches.index(sw)]))
			else:
				print('''------------Iscom-----------
conf
interface port {1}
no description 
exi
no vlan {0}
end
wr
'''.format(vlan if vlan_second == '' else vlan_second, downlinks[l2_switches.index(sw)]))

#---------------------------------L2VC-------------------------------------------        

	else:
		l3_switch = input('Enter mpls switch type(Q9/Q8/HP/CX ')
		interface = input('L3 switch interface: ')
		l2_switches = []
		uplinks = []
		downlinks = []
		for x in range(int(input('Number of L2 switches: '))):
			l2_switches.append(input('Next switch '))
			uplinks.append(input('uplink interface: '))
			downlinks.append(input('downlink interface: '))
		if router_type.lower() == 'cx':
			print('''--------------CX----------------------------------

undo interface GI1/0/22.{0}
!
interface GI1/0/23.{0}
undo mpls l2vc 
q
undo interface GI1/0/23.{0}
'''.format(vlan))
		elif router_type.lower() == "cx8":
				print('''
***********CX8*****************

undo interface Eth-t22.{0}
interface Eth-Trunk23.{0}
undo mpls l2vc 
q
undo interface Eth-Trunk23.{0}
q
save
 '''.format(vlan))
		if l3_switch.lower() == 'hp':
			print('''
************HP*********

interface  {1}
undo service-ins {0}
qu
qu
save'''.format(vlan if vlan_second == '' else vlan_second, interface))
		elif l3_switch.lower() == 'q8':
			print('''
************Q8***********

interface vlan {0}
undo mpls l2vc
q
undo interface vlan {0}
undo vlan {0}
interface {1}    	   
undo port t per vlan {0} 
q
'''.format(vlan if vlan_second == '' else vlan_second, interface)
			  )
		elif l3_switch.lower() == 'q9':
			print('''
*************Q9*************

interface vlan {0}
undo mpls l2vc
q
undo interface vlan {0}
undo vlan {0}
interface {1}
undo port t al vlan {0} 
q
q
save
'''.format(vlan if vlan_second == '' else vlan_second, interface)
			  )
		else:
			print('''
**********CX**********

interface  {1}.{0}
undo mpls l2vc
q
undo interface {1}.{0}
q
save
'''.format(vlan if vlan_second == '' else vlan_second, interface)
			  )
		for sw in l2_switches:
			if sw in {'q9', 'q5', 'q3'}:
				print('''----------{3}------------
interface {1}
undo port t a v {0}
interface {2}
undo port t a v {0}
q
undo vlan {0}
q
save
'''.format(vlan if vlan_second == '' else vlan_second, uplinks[l2_switches.index(sw)], downlinks[l2_switches.index(sw)], sw))
			elif sw in {'q8', 'hp'}:
				print('''-----------Q8/HP--------------
interface {1}    	   
 undo port t per vlan {0} 
interface {2}
undo port t per vlan {0}
'''.format(vlan if vlan_second == '' else vlan_second, uplinks[l2_switches.index(sw)], downlinks[l2_switches.index(sw)]))
			elif sw == 'ec_last':
				print('''----------EC-lastswitch------------------
conf
interface {1}
no description
switchport native vlan 1
exi
vlan data
no vlan {0}
end
copy run st'''.format(vlan, downlinks[l2_switches.index(sw)]))
			elif sw == 'ec':
				print('''----------EC------------------
conf
vlan data
no vlan {0}
end
copy run st
'''.format(vlan if vlan_second == '' else vlan_second))
			elif sw == 'rt':
				print('''-----------RubyTech---------
vlan
del tag-group {0}
exit
save start
'''.format(vlan if vlan_second == '' else vlan_second))
			elif sw == 'qs':
				print('''----------QS------------
interface {1}
undo description
q
undo vlan {0}
'''.format(vlan if vlan_second == '' else vlan_second, downlinks[l2_switches.index(sw)]))
			else:
				print('''------------Iscom-----------
conf
interface port {1}
no description 
exi
no vlan {0}
end
wr
'''.format(vlan if vlan_second == '' else vlan_second, downlinks[l2_switches.index(sw)]))

#-----------------------------------------------I-channel-----------------------------------------


if channel_type.lower() == 'i':
	node = input('Node name(zhuk/m9/varsh/kr): ')
	
	l3_switch = input('Enter mpls switch type(Q9/Q8/HP/CX ')
	interface = input('Mpls switch interface: ')

	l2_switches = []
	uplinks = []
	downlinks = []

	for x in range(int(input('Number of L2 switches: '))):
		l2_switches.append(input('Next switch '))
		uplinks.append(input('uplink interface: '))
		downlinks.append(input('downlink interface: '))

#--------------------------------------------Komkor Region(ASR-KR)---------------------------------------
	if node.lower() == 'kr':
		print('''
*************ASR-KR*****************
conf t
no interface gi0/0/1.{0}
end
wr
 **************CX-varshav************
interface  GI1/0/7.{0}
undo mpls l2vc
q
undo interface GI1/0/7.{0}
q
save
y
'''.format(vlan))
	# ---------VLAD-----
	elif node.lower() == 'vlad':
		print('''
 *************CX8-VLAD***************
undo interface gi6/0/0.{0}
interface gi5/0/6.{0}
undo mpls l2vc
q
undo interface gi5/0/6.{0}
q
save
y
'''.format(vlan))
#--------------------------- -----------------zhuk or cus(cx-X2)-----------------------------------------
	elif node.lower() in ['zhuk', 'cus', 'x2']:
		print('''
*************X-2********************
undo interface eth-t22.{0}
interface eth-t23.{0}
undo mpls l2vc
q
undo interface eth-t23.{0}
q
y
'''.format(vlan)
	)
	# -------------All another types
	else:
		print('''
***********ASR**********        
conf t
no interface te1/0/0.{0}
end
wr
************CX8**********
interface gi5/0/6.{0}
undo mpls l2vc
q
undo interface gi5/0/6.{0}
q
save
y   
'''.format(vlan)
	)

		
#-----------------------------------SWITCH-types------------------
	


	if l3_switch.lower() == 'hp':
			print('''
************HP*********

interface  {1}
undo service-ins {0}
qu
qu
save
'''.format(vlan if vlan_second == '' else vlan_second, interface))
	elif l3_switch.lower() == 'q8':
			print('''
************Q8***********

interface vlan {0}
undo mpls l2vc
q
undo interface vlan {0}
undo vlan {0}
interface {1}    	   
undo port t per vlan {0} 
q
'''.format(vlan if vlan_second == '' else vlan_second, interface)
				  )
	elif l3_switch.lower() == 'q9':
			print('''
*************Q9*************

interface vlan {0}
undo mpls l2vc
q
undo interface vlan {0}
undo vlan {0}
interface {1}
undo port t al vlan {0} 
q
q
save
'''.format(vlan if vlan_second == '' else vlan_second, interface)
				  )
	else:
		print('''
**********CX**********
	
interface  {1}.{0}
undo mpls l2vc
q
undo interface {1}.{0}
q
save'''.format(vlan if vlan_second == '' else vlan_second, interface)
				  )

	for sw in l2_switches:
			if sw in {'q9', 'q5', 'q3'}:
				print('''----------{3}------------
interface {1}
undo port t a v {0}
interface {2}
undo port t a v {0}
q
undo vlan {0}
q
save
'''.format(vlan if vlan_second == '' else vlan_second, uplinks[l2_switches.index(sw)], downlinks[l2_switches.index(sw)], sw))
			elif sw in {'q8', 'hp'}:
				print('''-----------Q8/HP--------------
interface {1}          
 undo port t per vlan {0} 
interface {2}
undo port t per vlan {0}
'''.format(vlan if vlan_second == '' else vlan_second, uplinks[l2_switches.index(sw)], downlinks[l2_switches.index(sw)]))
			elif sw == 'ec_last':
				print('''----------EC-lastswitch------------------
conf
interface {1}
no description
switchport native vlan 1
exi
vlan data
no vlan {0}
end
copy run st'''.format(vlan, downlinks[l2_switches.index(sw)]))
			elif sw == 'ec':
				print('''----------EC------------------
conf
vlan data
no vlan {0}
end
copy run st'''.format(vlan if vlan_second == '' else vlan_second))
			elif sw == 'rt':
				print('''-----------RubyTech---------
vlan
del tag-group {0}
exit
save start
'''.format(vlan if vlan_second == '' else vlan_second))
			elif sw == 'qs':
				print('''----------QS------------
interface {1}
undo description
q
undo vlan {0}
'''.format(vlan if vlan_second == '' else vlan_second, downlinks[l2_switches.index(sw)]))
			else:
				print('''------------Iscom-----------
conf
interface port {1}
no description 
exi
no vlan {0}
end
wr
'''.format(vlan if vlan_second == '' else vlan_second, downlinks[l2_switches.index(sw)]))



	



