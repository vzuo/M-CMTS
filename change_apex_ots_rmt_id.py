import subprocess

print "#*******************************************************************************************************************************"

print "#Please verify the file like 'apex_rf_port_ots_conf_for_dx1ab_cd_slot_6_0_24channels.txt' has been generated in the output folder in APP7 server!"

print "#Please verify the apex3000 qam name is right in above file!"

print "*******************************************************************************************************************************"

device_name = raw_input('Input M-CMTS name(eg.):\n').strip()
sub_slot = raw_input('Input 3G60 module sub slot number (eg.6/0):\n').strip()
deviceName = device_name.replace('.','_')
subslot = sub_slot.replace('/','_')

filename = 'apex_rf_port_ots_conf_for_'+deviceName+'_slot_' +subslot+'_24channels.txt'

print filename

ots_file=open('./output/'+filename, 'r')
for command in ots_file:
    p=subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output,err) = p.communicate()
    p_status = p.wait()
    print "command output:",output

ots_file.close()

