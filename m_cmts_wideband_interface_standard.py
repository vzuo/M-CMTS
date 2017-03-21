__author__ = 'author'

def removeWidebandCableInterface(controller_interface, widebandCableIndex):
    clearwidebandcable = ()
    widebandCableInterface = 'interface Wideband-Cable ' + controller_interface + ':' + str(widebandCableIndex)
    clearwidebandcable += (widebandCableInterface,)
    clearwidebandcable += (' shutdown',)
    for i in range(24):
        clearwidebandcable += (' no cable rf-channel ' + str(i),)

    clearwidebandcable += (' no cable bundle 1',)

    return clearwidebandcable

def standardWidebandCableInterface(controller_interface, widebandCableIndex):
    stdwidebandcable = ()
    if widebandCableIndex == 24:
        widebandCableInterface = 'interface Wideband-Cable ' + controller_interface + ':' + str(widebandCableIndex)
        stdwidebandcable += (widebandCableInterface,)
        for i in range(0, 8):
            stdwidebandcable += (' cable rf-channel ' + str(i) + ' bandwidth-percent 1',)

        stdwidebandcable += (' cable bundle 1',)
        stdwidebandcable += (' no shutdown',)

    elif widebandCableIndex == 25:
        widebandCableInterface = 'interface Wideband-Cable ' + controller_interface + ':' + str(widebandCableIndex)
        stdwidebandcable += (widebandCableInterface,)
        for i in range(8, 16):
            stdwidebandcable += (' cable rf-channel ' + str(i) + ' bandwidth-percent 1',)

        stdwidebandcable += (' cable bundle 1',)
        stdwidebandcable += (' no shutdown',)
    elif widebandCableIndex == 26:
        widebandCableInterface = 'interface Wideband-Cable ' + controller_interface + ':' + str(widebandCableIndex)
        stdwidebandcable += (widebandCableInterface,)
        for i in range(16, 24):
            stdwidebandcable += (' cable rf-channel ' + str(i) + ' bandwidth-percent 1',)

        stdwidebandcable += (' cable bundle 1',)
        stdwidebandcable += (' no shutdown',)
    elif widebandCableIndex == 27:
        widebandCableInterface = 'interface Wideband-Cable ' + controller_interface + ':' + str(widebandCableIndex)
        stdwidebandcable += (widebandCableInterface,)
        for i in range(24):
            stdwidebandcable += (' cable rf-channel ' + str(i) + ' bandwidth-percent 1',)

        stdwidebandcable += (' cable bundle 1',)
        stdwidebandcable += (' no shutdown',)
    elif widebandCableIndex == 30:
        widebandCableInterface = 'interface Wideband-Cable ' + controller_interface + ':' + str(widebandCableIndex)
        stdwidebandcable += (widebandCableInterface,)
        for i in range(4, 12):
            stdwidebandcable += (' cable rf-channel ' + str(i) + ' bandwidth-percent 1',)

        stdwidebandcable += (' cable bundle 1',)
        stdwidebandcable += (' no shutdown',)
    elif widebandCableIndex == 31:
        widebandCableInterface = 'interface Wideband-Cable ' + controller_interface + ':' + str(widebandCableIndex)
        stdwidebandcable += (widebandCableInterface,)
        for i in range(12, 20):
            stdwidebandcable += (' cable rf-channel ' + str(i) + ' bandwidth-percent 1',)

        stdwidebandcable += (' cable bundle 1',)
        stdwidebandcable += (' no shutdown',)
    else:
        pass

    return stdwidebandcable


for slot in range(5, 9):
    for subslot in range(0, 2):
        for controller in range(0, 3):
            modular_cable = str(slot) + '/'+ str(subslot) + '/'+ str(controller)

            cwbciFile = open('./output/correctWidebandCableInterface_' + modular_cable.replace('/', '_') + '.txt', 'w')
            clearWidebandCableInterfaces = ()
            stdWidebandCableInterfaces = ()

            for wbcint in range(21, 32):
                rmwbci = removeWidebandCableInterface(modular_cable, wbcint)
                clearWidebandCableInterfaces += rmwbci
            for wbcint in range(24, 32):
                stdwbci = standardWidebandCableInterface(modular_cable, wbcint)
                stdWidebandCableInterfaces += stdwbci

            for line in clearWidebandCableInterfaces:
                cwbciFile.write(line + '\n')

            for line in stdWidebandCableInterfaces:
                cwbciFile.write(line + '\n')
spa_slots = [1,3]
for slot in spa_slots:
    for subslot in range(0, 4):
        modular_cable = str(slot) + '/'+ str(subslot) + '/0'
        cwbciFile = open('./output/correctWidebandCableInterface_' + modular_cable.replace('/', '_') + '.txt', 'w')
        clearWidebandCableInterfaces = ()
        stdWidebandCableInterfaces = ()

        for wbcint in range(21, 32):
            rmwbci = removeWidebandCableInterface(modular_cable, wbcint)
            clearWidebandCableInterfaces += rmwbci
        for wbcint in range(24, 32):
            stdwbci = standardWidebandCableInterface(modular_cable, wbcint)
            stdWidebandCableInterfaces += stdwbci

        for line in clearWidebandCableInterfaces:
            cwbciFile.write(line + '\n')

        for line in stdWidebandCableInterfaces:
            cwbciFile.write(line + '\n')

cwbciFile.close()
