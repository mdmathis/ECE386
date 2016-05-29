#!/usr/bin/python


class Instruction:
    def __init__(self, opcode, field1, field2, field3):
        self.opcode = opcode
        self.field1 = field1
        self.field2 = field2
        self.field3 = field3
        self.value = 0
        self.weight = 0
        self.writeback = 0


def fetch(handle):
    line = handle.readline()
    if line:
        return int(line.strip(), 16)
    else:
        return None


def decode(inst):
    opcode = inst >> 30
    field1 = (inst & 0x30000000) >> 28
    field2 = (inst & 0x0C000000) >> 26
    field3 = inst & 0x03FFFFFF
    return opcode, field1, field2, field3


def memory(memdict, regfile, opcode, field2, field3):
    if opcode == 1:
        value = memdict[regfile[field2]]
        weight = memdict[regfile[field3]]

        return value, weight

    else:
        return 0, 0


def execute(regfile, opcode, reg, inputval=0, weight=0):
    if opcode == 1:
        val = regfile[reg]
        val += inputval * weight
        return val

    elif opcode == 2:
        if regfile[reg] > 0:
            return 1
        else:
            return 0

    else:
        return 0


def write_back(memdict, regfile, opcode, reg1=0, reg2=0, reg3=0, val=0):
    if opcode == 0:
        regfile.update({reg1: reg3})
    elif opcode == 1:
        regfile.update({reg1: val})
        regfile.update({reg2: regfile[reg2] + 4})
        regfile.update({reg3: regfile[reg3] + 4})
    elif opcode == 2:
        memdict.update({reg3: val})
        print('GOTCHYA BITCH!')
        print(memdict[reg3])


def main():
    src_file = open('Hex.txt', 'r')

    regfile = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
    memdict = {0: 1, 4: 0, 8: 1, 12: -1, 16: 0}

    current = [True, None, None, None, None]
    _next = [None, None, None, None]

    count = 0

    while True:
        # Instruction Fetch
        if current[0]:
            inst = fetch(src_file)
            if inst is None:
                current[0] = False
                _next[0] = None
            else:
                _next[0] = inst

        # Decode
        if current[1] is not None:
            opcode, field1, field2, field3 = decode(current[1])
            _next[1] = Instruction(opcode, field1, field2, field3)
        else:
            _next[1] = None

        # Memory
        if current[2] is not None:
            current[2].value, current[2].weight = memory(memdict, regfile, current[2].opcode, current[2].field2, current[2].field3)
            _next[2] = current[2]
        else:
            _next[2] = None

        # Execute
        if current[3] is not None:
            current[3].writeback = execute(regfile, current[3].opcode, current[3].field1, current[3].value, current[3].weight)
            _next[3] = current[3]
        else:
            _next[3] = None

        # Writeback
        if current[4] is not None:
            write_back(memdict, regfile, current[4].opcode, current[4].field1, current[4].field2, current[4].field3, current[4].writeback)
        elif not current[0]:
            break

        count += 1

        current[1] = _next[0]
        current[2] = _next[1]
        current[3] = _next[2]
        current[4] = _next[3]

    print('Final count:', count)


if __name__ == "__main__":
    main()