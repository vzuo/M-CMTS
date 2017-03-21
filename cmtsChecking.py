#!/usr/bin/env python
import paramiko
import time
import socket
import re

def disable_paging(remote_conn):
    '''Disable paging on a Cisco router'''

    remote_conn.send("terminal length 0\n")
    time.sleep(1)

    # Clear the buffer on the screen
    output = remote_conn.recv(1000)

    return output

def checkingcmts(devName,cmd):
    if __name__ == '__main__':

       
        # Create instance of SSHClient object
        remote_conn_pre = paramiko.SSHClient()
        #remote_conn_pre.exec_command('enable')

        # Automatically add untrusted hosts (make sure okay for security policy in your environment)
        remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # initiate SSH connection
        remote_conn_pre.connect(thip, username=username, password=thpassword)
        print "SSH connection established to %s" % thip
        # Use invoke_shell to establish an 'interactive session'
        remote_conn = remote_conn_pre.invoke_shell()
        print "Interactive SSH session established"
        
        # Strip the initial router prompt
        output = remote_conn.recv(1000)

        # See what we have
        #print output

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
        
   
        password=devpassword
        #remote_conn.send("ssh vzuo@"+devnm+"\n")

        # Wait for the command to complete
        time.sleep(0.5)
        remote_conn.send(password+'\n')
        output = remote_conn.recv(5000)
        #print output
        #print type(output)
        if output.__contains__('yes/no'):
            remote_conn.send("yes \n")
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
        #print output
        # Turn off paging
        disable_paging(remote_conn)
        #cli_command=('show version','show diagn ood','show cable fiber-node','show run ','show cable modem docsis device-class sum total')
        cli_command=cmd#('show version','show diagn ood','show cable modem sum total ')
        result = open('./output/show_result.txt','w')
        for cli in cli_command:
            remote_conn.send(cli+'\n')

            # Wait for the command to complete
            time.sleep(1)
            output = remote_conn.recv(65535)

            time.sleep(0.5)

            if cli.__contains__('show'):
                print 'here is the output:\n'
                #print type(output), len(output)
                #print 'output:', output.strip()
                output_show = output.strip()

                mac_start_id = 0
                mac_end_id = len(output_show)
                for c in range(len(output_show)):
                    if output_show[c:c+4].__contains__('RfId'):
                        mac_start_id = c + 4
                        #print 'first:', output_show[mac_start_id:mac_start_id+12],'start-id', mac_start_id
                    elif output_show[c].__contains__('#'):
                        mac_end_id = c - 8
                        #print 'Last:', output_show[mac_end_id: mac_end_id+9], 'end-id', mac_end_id

                #print mac_start_id, mac_end_id

                lines = int(round((mac_end_id - mac_start_id)/89))
                #print 'lines:', lines, mac_start_id, output_show[mac_start_id: mac_start_id+12]

                for j in range(lines):
                    mac_start_id = mac_start_id + 90
                    outline = output_show[mac_start_id: mac_start_id + 89]
                    if outline.__contains__(':17'):
                        result.write(outline[0:16])
                        #print outline[0:16]
                    else:
                        pass


            else:
                pass
        result.close()
        mac_list = ()
        show_result = open('./output/show_result.txt' )
        for line in show_result:
            mac_list += (line,)
            #print line, type(line)
        show_result.close()
        #mac_lists = mac_list.split('\n')
        ds_counter = 0
        max_mac = ''
        mac_output = ''
        for mac in mac_list:
            #print 'show cable modem ' + mac
            if mac.strip() !='':
                command = ('show cable modem ' + str(mac.strip()) + ' counters ')
                #print command
                remote_conn.send(command+'\n')
                time.sleep(0.5)
                outputphy = remote_conn.recv(5000)
                #print 'counter:', mac, outputphy[162:180]
                if ds_counter <= int(outputphy[162:180]):
                    ds_counter = int(outputphy[162:180])
                    max_mac = mac
                    mac_output = outputphy
                else:
                    ds_counter = ds_counter
                    break
                    print 'checking wrong:', outputphy
                command2 = ('show cable modem ' + str(mac.strip()) + ' verbose | include Total DS Throughput '+'\n')
                remote_conn.send(command2)
                time.sleep(0.5)
                outputverb = remote_conn.recv(5000)
                print outputverb
        print 'Here is the problematic modem:', ds_counter, max_mac, mac_output
        #remote_conn.send("\n")
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
    cmtsName='dx2lm.lm'#raw_input('cmts name: ').strip()
    cli={'precheck':('show version','show diagn ood','show cable modem sum total'),
         'postcheck':('term len 0', 'show cable modem cable 7/0/1 primary-channel non-bonding-capable',)}

    #checkingcmts(cmtsName,cli['precheck'])
    checkingcmts(cmtsName,cli['postcheck'])
