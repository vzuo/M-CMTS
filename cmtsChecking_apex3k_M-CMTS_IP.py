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

  

    #trust host variables
    #thname='th2.no.cg.lab.nms.mlb.inet'
   

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



    password=devpassword
    
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
    cli_cmd_5 = 'show ip int brief | in GigabitEthernet5/0/0 '
    remote_conn.send(cli_cmd_5+'\n')

    # Wait for the command to complete
    time.sleep(5)
    output4 = remote_conn.recv(655350)
    output4_show = output4.split("\r\n")

    print output4_show[2]+output4_show[1]

    remote_conn.send('exit \n')
    time.sleep(0.5)
    output = remote_conn.recv(5000)

    #print output

    remote_conn.send('exit \n')
    time.sleep(1)
    output = remote_conn.recv(5000)
    #print output

    print 'finished!'

    return output4_show



