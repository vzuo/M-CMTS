#!/usr/bin/env python
# -*- coding: <encoding name> -*-
import sys
import paramiko
import time
import socket
import getpass

# 31: Full Configuration of 12DS downstream channels for 6 Service Group in Standard Version SCH5 or Higher version
from src.c3g60Conf_goodv278_v1 import c3g60Conf

# 32: Full Configuration of 16DS downstream channels for 6 Service Group in Standard Version SCH5 or Higher version
from src.c3g60Conf_16DS_vrf_v1 import c3g60Conf16
# eqamD5Conf
from src.eqamcblprov278 import eqamD5Conf

# 33: Full Configuration of 16DS or 24DS downstream channels for 4 Service Group in SCF2 
from src.c3g60Conf_24DS_SCF2_v1 import c3g60Conf24Scf2

# 34: Full Configuration of 24DS downstream channels for 4 Service Group in Standard Version SCH5 or Higher version
#from src.c3g60Conf_24DS_SCH5_v1 import c3g60Conf24Sch5
from src.eqamcbl_24ds import eqam_D5_24ds_Conf
#updated for iptv qos on Jan 12, 2017
from src.c3g60Conf_24DS_SCH5_v2 import c3g60Conf24Sch5

# 35 Full configuration of 32DS downstream channels for 4 to 8 SGs in SCI or higher version
from src.c3g60Conf_32DS_SCI3 import c3g60Conf32Sci3
from src.eqamcbl_32ds import eqam_D5_32ds_Conf


# 41: Full Configuration of 12DS downstream channels for 6 Service Group in Standard Version SCH5 or Higher version
from src.apex12DS_v1 import c3g604apex3k

# 42: Full Configuration of 16DS downstream channels for 6 Service Group in Standard Version SCH5 or Higher version
from src.apex_legacy_16DS_v1 import mc3g60_apex3k_16ds_conf

# 43: Full Configuration of 24DS downstream channels for 6 Service Group in Standard Version SCH5 or Higher version
# from src.apex_enhanced_std24DS_v1 import mc3g60_apex3k_24ds_conf
# updated for iptv qos on Jan 12, 2017
from src.apex_enhanced_std24DS_v2 import mc3g60_apex3k_24ds_conf


# 44: Required Configuration of 6 Service Group for upgrading from 16DS to 24DS in Standard Version SCH5 or Higher version
from src.apex_legacy16DS_to_std24DS_v1 import mc3g60_apex3k_16to_enhanced_std24ds_conf

# 45: OTS Config on APEX3000 M-CMTS Solution(24DS)  
from src.apex3k_remote_id_snmpset_v1 import tsid_conf

# Others 
from src.apex_legacy_16DS_controller_clear import cable_controller_clearing

while True:
    print """
    "\033[1;41mPlease send request if you need other options for your changes which are required to run the script in reviewed BIP.\033[1;m" 


    Choose the right option for your target:
    
           ***********************uBR10012 Chassis Configuration*****************

    0: exits from the menu
	
           **************** MC3g60V + WIDEBAND SPA + EQAM  D5 or RFGW1 ******** 
    31: Full Configuration of 12DS downstream channels for 6 Service Group in Standard Version SCH5 or Higher version
    32: Full Configuration of 16DS downstream channels for 6 Service Group in Standard Version SCH5 or Higher version
    33: Full Configuration of 16DS or 24DS downstream channels for 4 Service Group in SCF2 
    34: Full Configuration of 24DS downstream channels for 4 Service Group in Standard Version SCH5 or Higher version
    35: Full Configuration of 32DS downstream channels for 3 Service Group in Standard Version SCI3 or Higher version
   
           **************** MC3g60V + HDSPA + Apex3000 ********  
    41: Full Configuration of 12DS downstream channels for 6 Service Group in Standard Version SCH5 or Higher version
    42: Full Configuration of 16DS downstream channels for 6 Service Group in Standard Version SCH5 or Higher version
    43: Full Configuration of 24DS downstream channels for 6 Service Group in Standard Version SCH5 or Higher version
    44: Required Configuration of 6 Service Group for upgrading from 16DS to 24DS in Standard Version SCH5 or Higher version
    45: OTS Config on APEX3000 M-CMTS Solution(24DS)  
    """    
    try: 
        num=input('option number#: ')
        
    except ValueError:
        print "!Ops, Wrong number!"

    if num==0:
        print "Session Ends"
    
        break
    elif num==31:
        print '!'
        print "#!configure 3G60 modules for legacy EQAM(D5 or RFGW1)"
        print '!'
        print '!'
        #input for action below
        cmtsName=raw_input('Input CMTS Name (eg."dx4ld.ed"): \n').lower().strip()
        sgch=raw_input('Input channels per sg(eg, "12x4"): \n').lower().strip()
        skey=raw_input('Input the shared-secret for cable interface(eg:"NgILvnhvgRJC"): \n').strip()
        dsg=raw_input('!Want to enable DSG service?(y/n)(eg. "y"): \n').lower().strip()
        cslt=raw_input('Input the slot number for cable card(eg:"6/0"): \n').strip()
        sdepip=raw_input('Input the depi IP blocks (e.g:"169.254.1.0/29;169.254.1.8/29;169.254.1.16/29 ): \n').strip()
        depimaca=raw_input('Input the first MAC address of GE port for M-CMTS DEPI on EQAM (e.g:"0050.4b11.4566"): \n').strip()
        #print depimaca
        #Generating configuration of 3G60 module
        c3g60Conf(cmtsName,sgch,skey,dsg,cslt,sdepip,depimaca)
        
        #Notification
        print 'Done, go get your file in folder "output"!'
        #retun to menu
        pass
    elif num==32:
        print '!'
        print "#!configure 3G60 modules and its wideband spa for 16DS (D5 or RFGW1)"
        print '!'
        print '!'
        #input for action below
        cmtsName=raw_input('Input CMTS Name (eg."dx4ld.ed"): \n').lower().strip()
        sgch=raw_input('Input channels per sg(eg, "16x4"): \n').lower().strip()
        skey=raw_input('Input the shared-secret for cable interface(eg:"NgILvnhvgRJC"): \n').strip()
        dsg=raw_input('!Want to enable DSG service?(y/n)(eg. "y"): \n').lower().strip()
        cslt=raw_input('Input the slot number for cable card(eg:"6/0"): \n').strip()
        sdepip=raw_input('Input the depi IP blocks e.g:"169.254.1.0/29;169.254.1.8/29;169.254.1.16/29;169.254.1.24/29": \n').strip()
        depimaca=raw_input('Input the first MAC address of GE port for M-CMTS DEPI on EQAM e.g:"0050.4b11.4566": \n').strip()
        #print depimaca
        #Generating configuration of 3G60 module
        c3g60Conf16(cmtsName,sgch,skey,dsg,cslt,sdepip,depimaca)
        #print depimaca

        eqamRequest =raw_input('Do you want to create file for its D5?(Y/N):').lower().strip()
        if eqamRequest.__contains__('y'):
            cmtsmgmt=raw_input('Input CMTS Management IP Block (eg."10.159.229.32/28"): \n').lower().strip()
	    # (cmtsName,cmtsMgmtSubnet,clcSlot, sgDscnNum, depiIpBlocks ):
            eqamD5Conf(cmtsName,cmtsmgmt,cslt, 16, sdepip)
        else:
            pass
        #Notification
        print 'Done, go get your file in folder "output"!'
        
        #Notification
        print 'Done, go get your file in folder "output"!'
        #retun to menu
        pass
    elif num==33:
        print '!'
        print "#!configure 3G60 modules 16DS or 24DS on D5/RFGW1 M-CMTS in SCF2 "
        print '!'
        print '!'
        #input for action below
        cmtsName=raw_input('Input CMTS Name (eg."dx1ba.ed"): \n').lower().strip()
        sgch=raw_input('Input channels per sg(eg, "24x4"): \n').lower().strip()
        skey=raw_input('Input the shared-secret for cable interface(eg:"NgILvnhvgRJC"): \n').strip()
        dsg=raw_input('!Want to enable DSG service?(y/n)(eg. "y"): \n').lower().strip()
        cslt=raw_input('Input the slot number for cable card(eg:"5/1"): \n').strip()
        sdepip=raw_input('Input three depi IP blocks e.g:"169.254.1.0/29;169.254.1.8/29;169.254.1.16/29": \n').strip()
        depimaca=raw_input('Input the first MAC address of GE port for M-CMTS DEPI on EQAM e.g:"0050.4b11.4566": \n').strip()
        usbw = raw_input('Input the upgrade channel setting as 3.2MHz or 6.4MHz  E.g:"6.4":\n').strip()
        #print depimaca
        #Generating configuration of 3G60 module
        #c3g60Conf24DSScf2(cmtsName,sgch,skey,dsg,cslt,sdepip,depimaca)
        c3g60Conf24Scf2(cmtsName,sgch, skey, dsg, cslt, sdepip, depimaca, usbw,'1')
        #Notification
        print 'Done, go get your file in folder "output"!'
        #retun to menu
        pass
    elif num==34:
        print '!'
        print "#!configure 3G60 modules for legacy EQAM M-CMTS in SCH5 or later "
        print '!'
        print '!'
        #input for action below
        cmtsName=raw_input('Input CMTS Name (eg."dx2mw.ed"): \n').lower().strip()
        sgch=raw_input('Input channels per sg(eg, "24x4"): \n').lower().strip()
        skey=raw_input('Input the shared-secret for cable interface(eg:"Change_the_KeyC"): \n').strip()
        dsg=raw_input('!Want to enable DSG service?(y/n)(eg. "y"): \n').lower().strip()
        cslt=raw_input('Input the slot number for cable card(eg:"5/1"): \n').strip()
        sdepip=raw_input('Input four depi IP blocks e.g:"169.254.1.0/29;169.254.1.8/29;169.254.1.16/29;169.254.1.24/29": \n').strip()
        depimaca=raw_input('Input the first MAC address of GE port for M-CMTS DEPI on EQAM e.g:"0050.4b11.4566": \n').strip()
        usbw = raw_input('Input the upgrade channel setting as 3.2MHz or 6.4MHz  E.g:"6.4":\n').strip()
        #Generating configuration of 3G60 module
        c3g60Conf24Sch5(cmtsName,sgch, skey, dsg, cslt, sdepip, depimaca, usbw,'1')
        print 'cable line card configuration is done, go get your file in folder "output"!'
        #print depimaca
        eqamRequest =raw_input('Do you want to create file for its D5?(Y/N):').lower().strip()
        if eqamRequest.__contains__('y'):
            eqammgmt=raw_input('Input EQAM MANAGEMENT IP Address with its subnet mask(eg."10.159.229.41/28"): \n').lower().strip()
            eqam_D5_24ds_Conf(cmtsName,eqammgmt,cslt, 24, sdepip, '1')
        else:
            pass
        #Notification
        print 'Done, go get your file in folder "output"!'
        #return to menu
        pass

    elif num==35:
        print '!'
        print "#!configure 3G60 modules for legacy EQAM M-CMTS in SCH5 or later "
        print '!'
        print '!'
        #input for action below
        cmtsName=raw_input('Input CMTS Name (eg."dx2mw.ed"): \n').lower().strip()
        sgch=raw_input('Input channels per sg(eg, "32x4"): \n').lower().strip()
        skey=raw_input('Input the shared-secret for cable interface(eg:"Change_the_KeyC"): \n').strip()
        dsg=raw_input('!Want to enable DSG service?(y/n)(eg. "y"): \n').lower().strip()
        cslt=raw_input('Input the slot number for cable card(eg:"5/1"): \n').strip()
        sdepip=raw_input('Input four depi IP blocks e.g:"169.254.1.0/29;169.254.1.8/29;169.254.1.16/29;169.254.1.24/29": \n').strip()
        depimaca=raw_input('Input the first MAC address of GE port for M-CMTS DEPI on EQAM e.g:"0050.4b11.4566": \n').strip()
        usbw = raw_input('Input the upgrade channel setting as 3.2MHz or 6.4MHz  E.g:"6.4":\n').strip()
        #Generating configuration of 3G60 module
        c3g60Conf32Sci3(cmtsName,sgch, skey, dsg, cslt, sdepip, depimaca, usbw)
        print 'cable line card configuration is done, go get your file in folder "output"!'
        #print depimaca
        eqamRequest =raw_input('Do you want to create file for its D5?(Y/N):').lower().strip()
        if eqamRequest.__contains__('y'):
            cmtsmgmt=raw_input('Input CMTS Management IP Block (eg."10.159.229.32/28"): \n').lower().strip()
            eqam_D5_32ds_Conf(cmtsName,cmtsmgmt,cslt, 32, sdepip)
        else:
            pass
        #Notification
        print 'Done, go get your file in folder "output"!'
        #return to menu
        pass

    elif num==41:
        print '!'
        print "#!DOCSIS 3G60 module Configuration for APEX3000 for 12DS"
        print '!'
        print '!'
        #input for action below
        deviceName=raw_input("Please enter the DCMTS Name: \n").strip()
        DXs=raw_input("Please specify the index of CMTS in the group of the set of APEX3000 : 1 or 2 ? : \n").strip()
        cards =raw_input("Please enter the slot number (eg. '5/0,6/1'. For entire chassis, please enter '0') : \n").strip()
        QAM_nums =raw_input("Please enter the first QAM number that your CMTS connected to :\n").strip()
        ips=raw_input("Please enter uBR-QAM IP subnet (eg. A.B.C.0) : \n").strip()
        shared_secrets=raw_input("Please enter chassis shared secret : \n").strip()

        # generating the 3G60 configration
        file = open('./output/'+deviceName+'.12ds.txt',mode='w',buffering=65535)
        if cards=='0':
            scards='5/0,6/1,6/0,7/1,7/0,8/1,8/0'
        else:
            scards=cards
        #print scards
        depic=()
        for item in scards.split(','):
            output0=c3g604apex3k(DXs,item,QAM_nums,ips,shared_secrets)[0]
            for line in output0:
                if line not in depic:
                    depic+=(line,)
        for line in depic:
            file.write(line)
        for item in scards.split(','):
            output1=c3g604apex3k(DXs,item,QAM_nums,ips,shared_secrets)[1]    
            for line in output1:
                file.write(line) 
        file.close()
        #Notification
        print '!'
        print '!*************************************************************************************************************************'
        print '!'
        print '!*****Configuration file for 3g60 module in Slot "'+scards+ '" has been created, please check folder "output" for details ******************'
        print '!'
        #retun to menu
        pass
    elif num==42:
        #42
	#from src.apex16DS import mc3g60_apex3k_16ds_conf

        print '!'
        print "#!DOCSIS 3G60 and 3G HD-SPA module Configuration for APEX3000 M-CMTS of 16DS "
        print '!'
        print '!'
        #input for action below

        deviceName=raw_input("Please enter the DCMTS Name: \n").strip()
        DXs=input("Please specify the index of CMTS in the group of the set of APEX3000 : 1 or 2 ? : \n")
        cards =raw_input("Please enter the slot number (eg. '5/0,6/1'. For entire chassis, please enter '0') :\n").strip()
        qam_nums=raw_input("please input the apex3000 index number of 28SG apex and 14SG apex,(eg. '1,2' or '3,2'): \n")
        sgch= 16 #input('input channels per sg(eg, "16" ): \n')
        ips=raw_input("Please enter uBR-QAM IP subnet (eg. A.B.C.0) : \n").strip()
        shared_secrets=raw_input("Please enter chassis shared secret : \n").strip()
        if cards=='0':
            mc_slots = '5/0,6/1,6/0,7/1,7/0,8/1,8/0'
        else:
            mc_slots = cards

        if mc_slots.strip()!='':
            mcslots=[]
            if mc_slots.__contains__(','):
                #print 'multiple cards'
                clcards=mc_slots.split(',')
                mcslots+=clcards

            elif ',' not in mc_slots:
                #print 'single cards:',mc_slots
                mcslots+=(mc_slots,)

            else:
                print 'Please right 3G60 module slot'

        else:
            print 'Please input the slot for 3G60 module between "5/0~8/0"'

        #print 'slots:',mcslots

        # generating the 3G60 configration
        for lslot in mcslots:
            file = open('./output/'+deviceName+'_'+str(sgch)+'ds_subslot_'+lslot.replace('/','_')+'_conf.txt',mode='w',buffering=65535)

            output=mc3g60_apex3k_16ds_conf(DXs,qam_nums,lslot,sgch,ips,shared_secrets)
            for line in output[0]:
                file.write(line+'\n')
            file.close()
            #Notification

        print '!'
        print '!*************************************************************************************************************************'
        print '!'
        print '!*****Configuration file for 3g60/3G-SPA module in Slot "'+cards+ '" has been created, please check folder "output" for details ******************'
        print '!'
        #retun to menu
        pass
    elif num==43:
        #43
	#from src.apex16o24DS import mc3g60_apex3k_24ds_conf

        print '!'
        print "#!DOCSIS 3G60 and 3G HD-SPA module Configuration for APEX3000 M-CMTS of Enhanced 24DS "
        print '!'
        print '!'
        #input for action below
        deviceName=raw_input("Please enter the DCMTS Name:\n").strip()
        DXs=input("Please specify the index of CMTS in the group of the set of APEX3000 : 1 or 2 ? :\n")
        cards =raw_input("Please enter the slot number (eg. '5/0,6/1'. For entire chassis, please enter '0') :\n").strip()
        qam_nums=raw_input("please input the apex3000 index number of 28SG apex and 14SG apex,(eg. '1,2' or '3,2'):\n")
        sgch=input('input channels per sg(eg,  "24"): \n')
        usbw = raw_input('Input the upgrade channel setting as 3.2MHz or 6.4MHz  E.g:"6.4":\n').strip()
        ips=raw_input("Please enter uBR-QAM IP subnet (eg. A.B.C.0) :\n").strip()
        shared_secrets=raw_input("Please enter chassis shared secret :\n").strip()
        if cards=='0':
            mc_slots = '5/0,6/1,6/0,7/1,7/0,8/1,8/0'
        else:
            mc_slots = cards

        if mc_slots.strip()!='':
            mcslots=[]
            if mc_slots.__contains__(','):
                #print 'multiple cards'
                clcards=mc_slots.split(',')
                mcslots+=clcards

            elif ',' not in mc_slots:
                #print 'single cards:',mc_slots
                mcslots+=(mc_slots,)

            else:
                print 'Please right 3G60 module slot'

        else:
            print 'Please input the slot for 3G60 module between "5/0~8/0"'

        #print 'slots:',mcslots

        # generating the 3G60 configration
        for lslot in mcslots:
            file = open('./output/'+deviceName+'_'+str(sgch)+'ds_subslot_'+lslot.replace('/','_')+'_conf.txt',mode='w',buffering=65535)

            output=mc3g60_apex3k_24ds_conf(DXs,qam_nums,lslot,sgch,ips,shared_secrets,usbw)
            for line in output[0]:
                file.write(line+'\n')
            file.close()
            #Notification
        print '!'
        print '!*************************************************************************************************************************'
        print '!'
        print '!*****Configuration file for 3g60/3G-SPA module in Slot "'+str(mc_slots)+ '" has been created, please check folder "output" for details ******************'
        print '!'
        #retun to menu
        pass
    elif num==44:
        #44
	#from src.apex_legacy_16DS_controller_clear import cable_controller_clearing
	
	#from src.apex_legacy16DS_to_std24DS_v import mc3g60_apex3k_16to_enhanced_std24ds_conf

        print '!'
        print "#!DOCSIS 3G60 and 3G HD-SPA module Configuration for APEX3000 M-CMTS of legacy 16DS to Enhanced 24DS "
        print '!'
        print '!'
        #input for action below
        deviceName=raw_input("Please enter the DCMTS Name: \n").strip()
        DXs=input("Please specify the index of CMTS in the group of the set of APEX3000 : 1 or 2 ? :\n")
        cards =raw_input("Please enter the slot number (eg. '5/0,6/1'. For entire chassis, please enter '0') :\n").strip()
        qam_nums=raw_input("please input the apex3000 index number of 28SG apex and 14SG apex,(eg. '1,2' or '3,2'):\n")
        sgch=24#input('input channels per sg(eg, "16" or "24": \n')
        ips=raw_input("Please enter uBR-QAM IP subnet (eg. A.B.C.0) :\n").strip()
        shared_secrets="Change_me_to_right_string"#raw_input("Please enter chassis shared secret :\n").strip()
        if cards=='0':
            mc_slots = '5/0,6/1,6/0,7/1,7/0,8/1,8/0'
        else:
            mc_slots = cards

        if mc_slots.strip()!='':
            mcslots=[]
            if mc_slots.__contains__(','):
                #print 'multiple cards'
                clcards=mc_slots.split(',')
                mcslots+=clcards

            elif ',' not in mc_slots:
                #print 'single cards:',mc_slots
                mcslots+=(mc_slots,)

            else:
                print 'Please right 3G60 module slot'

        else:
            print 'Please input the slot for 3G60 module between "5/0~8/0"'

        #print 'slots:',mcslots

        # generating the 3G60 configration
        for lslot in mcslots:
            
            ug_file=mc3g60_apex3k_16to_enhanced_std24ds_conf(DXs,qam_nums,lslot,sgch,ips)
            clear_controller_depi_tunnel = cable_controller_clearing(DXs,qam_nums,lslot,16,shared_secrets,ips)
            file = open('./output/'+deviceName+'_'+'ds_subslot_'+lslot.replace('/','_')+'_16_to_24_ug_conf.txt',mode='w',buffering=65535)
            for line in clear_controller_depi_tunnel['mcc']:
                file.write(line+'\n')
            for line in ug_file[0]:
                file.write(line+'\n')
            file.close()
            #Notification
        print '!'
        print '!*************************************************************************************************************************'
        print '!'
        print '!*****Configuration file for 3g60/3G-SPA module in Slot "'+str(mc_slots)+ '" has been created, please check folder "output" for details ******************'
        print '!'
        #retun to menu
        pass
    elif num==45:
        print '!'
        print "#!OTS remote_ID configuration of APEX3000 M-CMTS for 24DS "
        print '!'
        print '!'
        #input for action below
        deviceName=raw_input("Please enter the DCMTS Name: \n").strip()
        DXs=input("Please specify the index of CMTS in the group of the set of APEX3000 : 1 or 2 ? :\n")
        cards =raw_input("Please enter the slot number (eg. '5/0,6/1'. For entire chassis, please enter '0'):\n").strip()
        qam_nums=raw_input("please input the apex3000 qam ID number of 28SG apex and 14SG apex,(eg. '4,5' or '6,5'):\n")
        sgch=24#input('Input channels per sg(eg, "16" or "24": \n')
        cur_ch=input('Input the current downstream channels per sg/rf port(eg, "0", "12" or "16":)\n')
        #ips=raw_input("Please enter uBR-QAM IP subnet (eg. A.B.C.0) : \n").strip()
        #shared_secrets="Change_me_to_right_string"#raw_input("Please enter chassis shared secret : \n").strip()
        if cards=='0':
            mc_slots = '5/0,6/1,6/0,7/1,7/0,8/1,8/0'
        else:
            mc_slots = cards

        if mc_slots.strip()!='':
            mcslots=[]
            if mc_slots.__contains__(','):
                #print 'multiple cards'
                clcards=mc_slots.split(',')
                mcslots+=clcards

            elif ',' not in mc_slots:
                #print 'single cards:',mc_slots
                mcslots+=(mc_slots,)

            else:
                print 'Please right 3G60 module slot'

        else:
            print 'Please input the slot for 3G60 module between "5/0~8/0"'

        #print 'slots:',mcslots
        dx_index = DXs #  input('Input dx chassis index number 1 or 2 only: \n')
        dx_name = deviceName # raw_input('m-cmts name:\n')
        qam_num = qam_nums.split(',')
        sg_28_qam_id = int(qam_num[0])#  input('Input 28 Service group apex qam name id  eg. qam1.st.vc. then input 1: \n')
        sg_14_qam_id = int(qam_num[1]) #  input('Input 14 Service group apex qam name id  eg. qam2.st.vc. then input 2: \n')
        current_ds_channels = cur_ch
        for lslot in mcslots:
            dx_clc_slot=lslot
            otsconf = open('./output/apex_rf_port_ots_conf_for_' + dx_name.replace('.', '_') + '_slot_'+dx_clc_slot.replace('/', '_') + '_24channels.txt', 'w')
            ots_conf = tsid_conf(dx_index, dx_clc_slot, sg_28_qam_id, sg_14_qam_id, dx_name, current_ds_channels)
            for port_conf in ots_conf:
                for line in port_conf:
                    otsconf.write(line + '\n')
            otsconf.close()

        print '!'
        print '!*************************************************************************************************************************'
        print '!'
        print '!***** OTS Configuration file of APEX3000 for 3g60/3G-SPA module in Slot "'+str(mc_slots)+ '" has been created, please check folder "output" for details ******************'
        print '!'
        #retun to menu
        pass
    else:
        print "input a valid number!"
        pass
