#
import platform
# print platform.system()
import time

if platform.system() == 'Windows':
    from App7_Verified.mcmts_wideband_interface_ngv import mcmts_wideband_interfaces_update
else:
    from src.mcmts_wideband_interface_ngv import mcmts_wideband_interfaces_update

if __name__ == "__main__":
    print """
    Please be advised that some manually checking work is required to some interfaces from the output due to the limitation of the network process.
    Some inaccurate info needs to be verified and manually managed by the implementing owner.
    """

    print "\nYou can enter multiple devices with ',' eg:  \n"

    cmtsNames = raw_input('Enter m-cmts device name: eg. \n>')
    # new file
    cmts_names = []
    if "," in cmtsNames:
        cmts_name_list = cmtsNames.split(',')
        for cmts in cmts_name_list:
            cmts_names.append(cmts)

    else:
        cmts = cmtsNames
        cmts_names.append(cmts)

    for name in cmts_names:
        renew_wbintface_output_file = open('./output/' + name.strip() + '_wideband_interfaces_renew.txt', 'w')
        update_wideband_interface = mcmts_wideband_interfaces_update(name.strip())
        renew_wbintface_output_file.write('config term' + '\n')
        for item in update_wideband_interface:
            if item:
                renew_wbintface_output_file.write(item + '\n')

        renew_wbintface_output_file.write('end' + '\n')
        renew_wbintface_output_file.write('save' + '\n')
        # renew_wbintface_output_file.write('clear cable modem wideband reset' + '\n')
        renew_wbintface_output_file.close()

