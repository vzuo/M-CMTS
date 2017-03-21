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

    devpassword = 'eV@n62o'#raw_input('system password: ')
    natpassword='C4e37x4F65b2'

    password=devpassword
    #remote_conn.send("ssh vzuo@"+devnm+"\n")
    remote_conn.send("ssh vzuo@"+devip+"\n")
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

if __name__=="__main__":
     cmts_list = {#'dx2nw.vs':'0',
                #'DX3ST.VC':'0',
                'dx4cw.ed':'0',
                #'dx4ld.ed':'0',
                #'dx4sa.ed':'0',
                #'dx6au.vf':'0',
                'dx3ld.ed':'0',
                #'dx6ne.vs':'0',
                # 'dX9tw.ed ':'0',
            #             'dx7tw.ed ':'0',
            #             'dx2tw.ed ':'0',
            #             'dx4sa.ed ':'0',
            #             'dx5sa.ed ':'0',
            #             'dx3ni.ed ':'0',
            #             'dx5ni.ed ':'0',
            #             'dx6ld.ed ':'0',
            #             'dx4ld.ed ':'0',
            #             'dx6cw.ed ':'0',
            #             'dx4cw.ed ':'0',
            #             'dx6fm.fm ':'0',
            #             'dx5fm.fm ':'0',
            #             'dx14sc.wp':'0',
            #             'dx4ai.cg ':'0',
            #             'dx8md.cg ':'0',
            #             'dx9md.cg ':'0',
            #             'dx10md.cg':'0',
            #             'dx11md.cg':'0',
            #             'dx5no.cg ':'0',
            #             'dx7no.cg ':'0',
            #             'dx4no.cg ':'0',
            #             'dx6no.cg ':'0',
            #             'dx3rr.cg ':'0',
            #             'dx4rr.cg ':'0',
            #             'DX11CV.GV':'0',
            #             'DX10CV.GV':'0',
            #             'DX13CV.GV':'0',
            #             'DX12CV.GV':'0',
            #             'DX8ST.VC ':'0',
            #             'DX2ST.VC ':'0',
            #             'DX3ST.VC ':'0',
            #             'DX8AN.VC ':'0',
            #             'DX3AN.VC ':'0',
            #             'dx7ca.vc ':'0',
            #             'dx2ca.vc ':'0',
            #             'dx7hh.vc ':'0',
            #             'dx4hh.vc ':'0',
            #             'dx5hh.vc ':'0',
            #             'dx4hs.vc ':'0',
            #             'dx3hs.vc ':'0',
            #             'dx9au.vf ':'0',
            #             'dx5au.vf ':'0',
            #             'dx6au.vf ':'0',
            #             'dx7iw.vc ':'0',
            #             'dx4iw.vc ':'0',
            #             'dx5iw.vc ':'0',
            #             'dx6nw.vs ':'0',
            #             'dx2nw.vs':'0',
            #             'dx7fl.vs':'0',
            #             'dx3fl.vs':'0',
            #             'dx7wb.vs':'0',
            #             'dx2wb.vs':'0',
            #             'dx9wb.vs':'0',
            #             'dx6ne.vs':'0',
            #             'dx3ne.vs':'0',
            #             'dx4ne.vs':'0',
            #             'dx8rh.vc':'0',
            #             'dx2rh.vc':'0',
            #             'dx4rh.vc':'0',
            #'dx9tw.ed':'0',
            #'dx7tw.ed':'0',
            #'dx2tw.ed':'0',
            #'dx3ni.ed':'0',
            #'dx5ni.ed':'0',
            #'dx4cw.ed':'0',
            #'dx6cw.ed':'0',
            #'dx4rr.cg':'0',
            #'dx3rr.cg':'0',
            #'dx1ru.cg': ('5/1', '5/0'),
            #'dx4ru.cg':('7/1',),
            #'dx1cm.cg':('7/1','7/0'),
            #'dx5ra.cg':('8/1','8/0'),
    }
    # done list = 'dx4cw.ed','dx6cw.ed','dx5ni.ed',
result = open('./output/apex_mcts_ge5000_ip_3.txt', 'w')

for cmtsName in cmts_list.keys():
    #print cmtsName, cmts_list[cmtsName]
    ge_info = checkingcmts(cmtsName.strip().lower(), cmts_list[cmtsName])
    result.write(ge_info[2]+ge_info[1]+'\n')

result.close()


