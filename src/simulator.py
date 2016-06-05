#!/usr/bin/python
import algorithm


class Instruction:
    def __init__(self, opcode, field1, field2, field3):
        self.opcode = opcode
        self.field1 = field1
        self.field2 = field2
        self.field3 = field3
        self.value = 0
        self.weight = 0
        self.writeback = 0


def grab_inputs(input_dict, handle):
    ret = grab_memory(handle)
    while ret is not None:
        input_dict.update({ret[0]: ret[1]})
        ret = grab_memory(handle)


def grab_memory(handle):
    line = handle.readline()
    if line:
        if line.strip() == '-----':
            return None

        adr, val = line.split(':')
        return int(adr.strip(), 16), int(val.strip())
    else:
        return None


def fetch(hex_file):
    line = hex_file.readline()
    if line:
        return int(line.strip(), 16)
    else:
        return None


def decode(inst):
    opcode = inst >> 30
    if opcode == 0:
        field1 = (inst & 0x30000000) >> 28
        field2 = 0
        field3 = inst & 0x0FFFFFFF
    else:
        field1 = (inst & 0x30000000) >> 28
        field2 = (inst & 0x0C000000) >> 26
        field3 = inst & 0x03FFFFFF

    return opcode, field1, field2, field3


def memory(weight_file, input_dict, reg_file, opcode, field2, field3):
    if opcode == 1:
        value = input_dict[reg_file[field2]]
        check = reg_file[field3]
        ret = grab_memory(weight_file)

        if ret is not None:
            if ret[0] == check:
                weight = ret[1]
            else:
                print('ERROR!!! Wanted: 0x%x, Got: 0x%x' % (check, ret[0]))
                exit(-1)
        else:
            print('ERROR!!! Got None!')
            exit(-1)

        reg_file.update({field2: reg_file[field2] + 4})
        reg_file.update({field3: reg_file[field3] + 4})

        return value, weight

    else:
        return 0, 0


def execute(opcode, val, inputval, weight):
    if opcode == 1:
        val += inputval * weight
        return val

    elif opcode == 2:
        if val >= 0:
            return 1
        else:
            return 0

    else:
        return 0


def write_back(input_dict, out_file, reg_file, opcode, field1, field3, val):
    if opcode == 0:
        reg_file.update({field1: field3})
    elif opcode == 1:
        reg_file.update({field1: val})
    elif opcode == 2:
        out_file.write('0x%08x : %d\n' % (field3, val))
        input_dict.update({field3: val})
        reg_file.update({field1: 0})


def add_hidden(input_dict, hidden, adr):
    for x in range(hidden):
        input_dict.update({adr + (x*4): 0})


def main():
    num_hidden, hidden_base = algorithm.file_maker()

    src_file = open('Hex.txt', 'r')
    output_file = open('Output.txt', 'w')
    input_file = open('Inputs.txt', 'r')
    memory_file = open('Memory.txt', 'r')

    print('\n\nSimulation Starting...')
    print('Simulation Progress')

    totalcount = 0

    for x in range(1000):

        algorithm.progress(1000, x)

        src_file.seek(0)
        memory_file.seek(0)
        reg_file = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
        input_dict = {}

        current = [1, None, None, None, None]
        _next = [None, None, None, None]

        stall = False
        go = True
        forward = 0
        fflag = False
        count = 0

        grab_inputs(input_dict, input_file)
        add_hidden(input_dict, num_hidden, hidden_base)

        while go:
            # Instruction Fetch
            if current[0] is not None:
                if stall:
                    stall = False
                    _next[0] = None

                else:
                    inst = fetch(src_file)
                    if inst is None:
                        current[0] = None
                        _next[0] = None
                    else:
                        current[0] = inst
                        _next[0] = inst

            # Decode
            if current[1] is not None:
                opcode, field1, field2, field3 = decode(current[1])
                _next[1] = Instruction(opcode, field1, field2, field3)

                if opcode == 0:
                    stall = True
            else:
                _next[1] = None

            # Memory
            if current[2] is not None:
                current[2].value, current[2].weight = memory(memory_file, input_dict, reg_file, current[2].opcode,
                                                             current[2].field2, current[2].field3)
                _next[2] = current[2]
            else:
                _next[2] = None

            # Execute
            if current[3] is not None:
                if fflag:
                    current[3].writeback = execute(current[3].opcode, forward, current[3].value, current[3].weight)

                else:
                    current[3].writeback = execute(current[3].opcode, reg_file[current[3].field1], current[3].value,
                                                   current[3].weight)

                if current[3].opcode == 1:
                    fflag = True
                    forward = current[3].writeback
                elif current[3].opcode == 2:
                    fflag = False

                _next[3] = current[3]
            else:
                _next[3] = None

            # Writeback
            if current[4] is not None:
                write_back(input_dict, output_file, reg_file, current[4].opcode, current[4].field1, current[4].field3,
                           current[4].writeback)

            for x in current:
                if x is not None:
                    go = True
                    count += 1
                    current[1] = _next[0]
                    current[2] = _next[1]
                    current[3] = _next[2]
                    current[4] = _next[3]
                    break
                else:
                    go = False

        output_file.write(str(count) + '\n')
        output_file.write('-----\n')
        totalcount += count

    print('\nSimulation Finished!')
    print('Total Count (1000x): ', totalcount)
    print('Program Count: ', int(totalcount/1000))

if __name__ == "__main__":
    main()
