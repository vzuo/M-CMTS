#!/usr/bin/env python
import paramiko
import time
import socket
import re
import io

def disable_paging(remote_conn):
    '''Disable paging on a Cisco router'''

    remote_conn.send("terminal length 0\n")
    time.sleep(1)

    # Clear the buffer on the screen
    output = remote_conn.recv(1000)

    return output

def checkingcmts(devName, slots):
    #if __name__ == '__main__':

    username = 'vzuo'

    #trust host variables
    #thname='th2.no.cg.lab.nms.mlb.inet'
    thname='th2.no.cg.nms.mlb.inet'
    thip=socket.gethostbyname(thname)
    thpassword='Shanshan0313'#raw_input('trust host password: ')

    # Create instance of SSHClient object
    remote_conn_pre = paramiko.SSHClient()
    #remote_conn_pre.exec_command('enable')

    # Automatically add untrusted hosts (make sure okay for security policy in your environment)
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # initiate SSH connection
    remote_conn_pre.connect(thip, username=username, password=thpassword)
    #print "SSH connection established to %s" % thip
    # Use invoke_shell to establish an 'interactive session'
    remote_conn = remote_conn_pre.invoke_shell()
    print "Interactive SSH session established to " + thname

    # Strip the initial router prompt
    output = remote_conn.recv(1000)

    # Now let's try to send the router a command
    remote_conn.send("pwd \n")
    # Wait for the command to complete
    time.sleep(0.5)
    #remote_conn.send(password+'\n')
    output = remote_conn.recv(5000)
    #print output

    # VARIABLES THAT NEED CHANGED
    dxdevnm =devName+'.int.shawcable.net' #'dx2nl.cg.lab.cmts.int.inet'#
    #devnm='dx2nl.cg.lab.cmts.int.inet'
    #devmgmtIp='10.159.226.9'
    #print devnm
    devip=socket.gethostbyname(dxdevnm)
    #devip='10.159.226.9'
    #print devip

    devpassword = 'eV@nB20'#raw_input('system password: ')
    natpassword='C4e37x4F65b2'
    denymessage='denied'
    password=devpassword
    #remote_conn.send("ssh vzuo@"+devnm+"\n")
    remote_conn.send("ssh vzuo@"+devip+"\n")
    # Wait for the command to complete
    time.sleep(0.5)
    remote_conn.send(password+'\n')
    output = remote_conn.recv(5000)
    if output.__contains__('yes/no'):
        remote_conn.send("yes \n")
        # Wait for the command to complete
        time.sleep(0.5)

        remote_conn.send(password+'\n')
        output = remote_conn.recv(5000)
        #print output
    else:
        remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Wait for the command to complete
    time.sleep(0.5)
    #remote_conn.send(password+'\n')
    output = remote_conn.recv(5000)
    #print output

    if output.__contains__('>'):
        remote_conn.send("enable \n")
        # Wait for the command to complete
        time.sleep(0.5)
        remote_conn.send(password+'\n')
        output = remote_conn.recv(5000)
        #print output
    else:
        remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    #remote_conn.send(devpassword+"\n")
    #remote_conn.send(natpassword+"\n")
    # Wait for the command to complete

    remote_conn.send(password+'\n')
    time.sleep(0.5)
    output = remote_conn.recv(5000)
    print "Logged into " + devName + ' Now'
    #print output
    # Turn off paging
    disable_paging(remote_conn)
    #start show command in device
    # identify linecard in chassis with modem in service
    cmts_slots = ()

    if slots == '0':
        cmd_4 = 'show cable modem sum total'
        remote_conn.send(cmd_4+'\n')

        # Wait for the command to complete
        time.sleep(5)
        output4 = remote_conn.recv(655350)
        output4_show = output4.split("\r\n")

        for line in output4_show:
            #print line
            if line.__contains__('/U'):
                sub_slot = line[1:4]
                #print  'slot num:' ,sub_slot
                if sub_slot not in cmts_slots:
                    cmts_slots += (line[1:4],)
                else:
                    pass
            else:
                pass
    else:
        cmts_slots =slots

    docsis_d20_cm_total = 0
    docsis_d30_cm_total = 0
    docsis_d20_cpe_cm_total = 0
    docsis_d30_cpe_cm_total = 0
    cmtsName = devName
    device_d2_cmfile = open('./output/clear_cable_modem_reset_d20_cpe_'+cmtsName+'.txt', 'w')
    device_d3_cmfile = open('./output/clear_cable_modem_reset_d30_cpe_'+cmtsName+'.txt', 'w')
    for subslot in cmts_slots:
        docsis20_cpe = ()
        docsis20_stb = ()
        docsis20_mta = ()
        docsis20_ps = ()
        docsis20_rtr = ()
        docsis30_cpe = ()
        docsis30_stb = ()
        docsis30_mta = ()
        docsis30_ps = ()
        docsis30_rtr = ()

        buffer_max =65535
        i = 0
        bufferlen = 65535

        print '...Seeking modems on subslot ' + subslot
        cmd_2 = 'show cable modem docsis device-class | in ' + subslot
        remote_conn.send(cmd_2+'\n')
        # Wait for the command to complete
        while bufferlen == buffer_max:
            time.sleep(5)
            i += 1
            if remote_conn.recv_ready():
                output1 = remote_conn.recv(65535)
                bufferlen = len(output1)
                output += output1
                print ' >'+str(i)+ ': Output is being collected ...',len(output1), bufferlen, len(output)

        print '"show command" info has been collected and start to process now...'

        if output.__contains__("\r\n"):
            output_show = output.split("\r\n")
            cpe_d2_cm_file = open('./output/clear_cable_modem_reset_d20_cpe_'+cmtsName+'_slot'+subslot.replace('/','_')+'.txt', 'w')
            cpe_d2_cm_file.write('!  ' + cmtsName + 'subslot ' + subslot + 'docsis d2.0 internet cable modem clear delete list' +'\n')
            cpe_d3_cm_file = open('./output/clear_cable_modem_reset_d30_cpe_'+cmtsName+'_slot'+subslot.replace('/','_')+'.txt', 'w')
            cpe_d3_cm_file.write('!  ' + cmtsName + 'subslot ' + subslot + 'docsis d3.0 internet cable modem clear delete list' +'\n')
            for line in output_show:
                docsis_version = line[52:55]
                if docsis_version.__contains__('2.0'):
                    if line.__contains__('MTA'):
                        docsis20_mta += ('MTA_CM20_MAC: '+ line[0:14] + ' Cable_Interface: ' + line[15:21].replace('C','Cable') + ' Device_Class ' + line[60:63],)
                    elif line.__contains__('STB'):
                        docsis20_stb += ('STB_CM20_MAC: '+ line[0:14] + ' Cable_Interface: ' + line[15:21].replace('C','Cable') + ' Device_Class ' + line[64:67],)
                    elif line.__contains__('PS'):
                        docsis20_ps += ('PS_CM20_MAC: '+ line[0:14] + ' Cable_Interface: ' + line[15:21].replace('C','Cable') + ' Device_Class ' + line[68:70],)
                        d2_ps_cm_mac = line[0:14]
                        ps_mac_cmd = 'clear cable modem '+ d2_ps_cm_mac + ' delete'
                        cpe_d2_cm_file.write(ps_mac_cmd+ '\n')
                    elif line.__contains__('RTR'):
                        docsis20_rtr += ('GW_CM20_MAC: '+ line[0:14] + ' Cable_Interface: ' + line[15:21].replace('C','Cable') + ' Device_Class ' + line[71:73],)
                    else:
                        docsis20_cpe += ('CPE_CM20_MAC: '+ line[0:14] + ' Cable_Interface: ' + line[15:21].replace('C','Cable') + ' Device_Class ' + line[65:69],)
                        d2_cm_mac = line[0:14]
                        cpe_mac_cmd = 'clear cable modem '+ d2_cm_mac + ' delete'
                        #print cpe_mac
                        cpe_d2_cm_file.write(cpe_mac_cmd + '\n')
                        device_d2_cmfile.write(d2_cm_mac + '\n')

                elif docsis_version.__contains__('3.0'):

                    if line.__contains__('STB'):
                        docsis30_stb += ('STB_CM30_MAC: '+ line[0:14] + ' Cable_Interface: ' + line[15:21].replace('C','Cable') + ' Device_Class ' + line[64:67],)
                    else:
                        if line.__contains__('MTA'):
                            docsis30_mta += ('MTA_CM30_MAC: '+ line[0:14] + ' Cable_Interface: ' + line[15:21].replace('C','Cable') + ' Device_Class ' + line[60:63],)
                        elif line.__contains__('PS'):
                            docsis30_ps += ('PS_CM30_MAC: '+ line[0:14] + ' Cable_Interface: ' + line[15:21].replace('C','Cable') + ' Device_Class ' + line[68:70],)
                            d3_ps_cm_mac = line[0:14]
                            ps_mac_cmd = 'clear cable modem '+ d3_ps_cm_mac + ' delete'
                            cpe_d3_cm_file.write(ps_mac_cmd+ '\n')
                        elif line.__contains__('RTR'):
                            docsis30_rtr += ('GW_CM30_MAC: '+ line[0:14] + ' Cable_Interface: ' + line[15:21].replace('C','Cable') + ' Device_Class ' + line[71:73],)
                            d3_rtr_cm_mac = line[0:14]
                            rtr_mac_cmd = 'clear cable modem '+ d3_rtr_cm_mac + ' delete'
                            cpe_d3_cm_file.write(rtr_mac_cmd+ '\n')
                        else:
                            docsis30_cpe += ('CPE_CM30_MAC: '+ line[0:14] + ' Cable_Interface: ' + line[15:21].replace('C','Cable') + ' Device_Class ' + line[65:69],)
                            d3_cm_mac = line[0:14]
                            cpe_mac_cmd = 'clear cable modem '+ d3_cm_mac + ' delete'
                            cpe_d3_cm_file.write(cpe_mac_cmd + '\n')
                            device_d3_cmfile.write(d3_cm_mac + '\n')
                else:
                    pass

            cpe_d2_cm_file.close()
            cpe_d3_cm_file.close()
            print ' ->' + cmtsName + '_d20_cpe: subslot_' + str(subslot) + ' :', len(docsis20_cpe+docsis20_ps), len(docsis20_cpe),len(docsis20_ps),len(docsis20_rtr),len(docsis20_stb),len(docsis20_mta)
            print ' ->' + cmtsName + '_d30_cpe: subslot_' + str(subslot) + ' :', len(docsis30_cpe+docsis30_ps+docsis30_rtr), len(docsis30_cpe),len(docsis30_ps),len(docsis30_rtr),len(docsis30_stb),len(docsis30_mta)
            print '...Subslot ' + str(subslot) + ' collected info is done\n'

        else:
            print 'Output is not formatted.????'
            pass

        #ccmfile.write('!  ' + cmtsName + 'subslot ' + subslot + 'docsis d2.0 internet cable modem reset total count:'+ str(len(docsis20_cpe)) +'\n')


        docsis_d20_cpe_cm_total += len(docsis20_cpe+docsis20_ps)
        docsis_d20_cm_total += len(docsis20_stb)+len(docsis20_mta)+len(docsis20_ps)+len(docsis20_rtr)+len(docsis20_cpe)

        docsis_d30_cpe_cm_total += len(docsis30_cpe+docsis30_ps+docsis30_rtr)
        docsis_d30_cm_total += len(docsis30_stb)+len(docsis30_mta)+len(docsis30_ps)+len(docsis30_rtr)+len(docsis30_cpe)


    device_d2_cmfile.write('!  ' + cmtsName + 'docsis d2.0 internet cable modem reset total count:'+ str(docsis_d20_cpe_cm_total)
                         + ' out of ' + str(docsis_d20_cm_total+docsis_d30_cm_total)+'\n')


    device_d3_cmfile.write('!  ' + cmtsName + 'docsis d3.0 internet cable modem reset total count:'+ str(docsis_d30_cpe_cm_total)
                         + ' out of ' + str(docsis_d20_cm_total+docsis_d30_cm_total)+'\n')

    device_d2_cmfile.close()
    device_d3_cmfile.close()
    print '...Collecting and Data Processing are done to ' + cmtsName + '\n'
    print '#!==>>' + cmtsName + ' -- docsis d2.0 internet cable modem reset total count:'+ str(docsis_d20_cpe_cm_total) + ' out of ' + str(docsis_d20_cm_total+docsis_d30_cm_total)+'\n'

    print '#!==>>' + cmtsName + ' -- docsis d3.0 internet cable modem reset total count:' + str(docsis_d30_cpe_cm_total) +' out of ' + str(docsis_d20_cm_total+docsis_d30_cm_total)+'\n'

    #print '#!==>>' + 'including:' +'\nstb' + str(len(docsis20_stb)+len(docsis30_stb)) + '\nmta:' + str(len(docsis20_mta)+len(docsis30_mta))+'\nps:' + str(len(docsis20_ps)+len(docsis30_ps))+ '\nrtr:' + str(len(docsis20_rtr)+len(docsis30_rtr))+'\ncpe:' + str(len(docsis20_cpe)+len(docsis30_cpe)) +'\n'

    remote_conn.send('exit \n')
    time.sleep(0.5)
    output = remote_conn.recv(5000)

    #print output

    remote_conn.send('exit \n')
    time.sleep(1)
    output = remote_conn.recv(5000)
    #print output

    print 'finished!'

if __name__=="__main__":
    cmts_list = {
                'dx2lm.lm': '0',
                }
    '''
    'dx5sa.ed':'0',
    'dx3ni.ed':'0',
    'dx4sa.ed':'0',
    'dx9tw.ed':'0',
    'dx7tw.ed':'0',
    'dx2tw.ed':'0',
    'dx5ni.ed':'0',
    'dx4cw.ed':'0',
    'dx6cw.ed':'0',
    'dx4rr.cg':'0',
    'dx3rr.cg':'0',
    'dx1ru.cg':('5/1','5/0'),
    'dx4ru.cg':('7/1',),
    'dx1cm.cg':('7/1','7/0'),
    'dx5ra.cg':('8/1','8/0'),
    '''
    # done list = 'dx4cw.ed','dx6cw.ed','dx5ni.ed',
    for cmtsName in cmts_list.keys():
        #print cmtsName, cmts_list[cmtsName]
        checkingcmts(cmtsName, cmts_list[cmtsName])
