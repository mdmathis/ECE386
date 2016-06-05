#!/usr/bin/python
import random
import sys


def progress(total, current):
    percent = int(total / 100)
    step = 5 * percent

    if current % step == 0:
        sys.stdout.write(
             "\r[" + "=" * int(current / step) + " " * int((total - current) / step) + "] %2d%%" % int(current / total * 100))
        sys.stdout.flush()

    elif current == (total-1):
        sys.stdout.write("\r[====================] 100%")
        sys.stdout.flush()

    elif current == 0:
        sys.stdout.write("\r[                    ] 0%")
        sys.stdout.flush()


def file_maker():

    assembly_file = open('Assembly.txt', 'w')
    hex_file = open('Hex.txt', 'w')
    input_file = open('Inputs.txt', 'w')
    memory_file = open('Memory.txt', 'w')

    inputs = int(input('Number of inputs: '))
    outputs = int(input('Number of outputs: '))
    hidden = int(input('Number of hidden: '))

    input_base_address = 0
    hidden_base_address = 4 * inputs
    weight_base_address = hidden_base_address + (4 * hidden)
    hidden_weight_base_address = weight_base_address + (4 * hidden * inputs)
    output_base_address = hidden_weight_base_address + (4 * hidden * outputs)

    print('')
    print('Input Memory Base Address:   0x%08x' % input_base_address)
    print('Hidden Memory Base Address:  0x%08x' % hidden_base_address)
    print('Input Weight Base Address:   0x%08x' % weight_base_address)
    print('Hidden Weight Base Address:  0x%08x' % hidden_weight_base_address)
    print('Output Base Address:         0x%08x' % output_base_address)
    print('')

    print('Creating Files...\n')
    print('Inputs')
    for i in range(1000):
        for x in range(inputs):
            rand = random.randrange(0, 2)
            input_file.write('0x%08x : %d\n' % (input_base_address + (4 * x), rand))

        input_file.write('-----\n')

        progress(1000, i)

    print('\nInput Weights')
    for x in range(hidden * inputs):
        rand = random.randrange(-1, 2)
        memory_file.write('0x%08x : %d\n' % (weight_base_address + (4 * x), rand))

        if hidden * inputs >= 100:
            progress(hidden * inputs, x)

    print('\nHidden Weights')
    for x in range(hidden * outputs):
        rand = random.randrange(-1, 2)
        memory_file.write('0x%08x : %d\n' % (hidden_weight_base_address + (4 * x), rand))

        if hidden * outputs >= 100:
            progress(hidden * outputs, x)

    print('\nAssembly 1')
    for x in range(hidden):
        assembly_file.write('LOAD R1, 0x%08x\n' % input_base_address)
        assembly_file.write('LOAD R2, 0x%08x\n' % (weight_base_address + (x * 4 * inputs)))

        hex_file.write('0x%08x\n' % ((0x1 << 28) + (0x0 << 26) + input_base_address))
        hex_file.write('0x%08x\n' % ((0x2 << 28) + (0x0 << 26) + (weight_base_address + (x * 4 * inputs))))

        for y in range(inputs):
            assembly_file.write('MULTADD R3, R1+, R2+\n')
            hex_file.write('0x%08x\n' % ((0b01 << 30) + (0b11 << 28) + (0b01 << 26) + 0b10))

        assembly_file.write('CHECK R3, (0x%08x)\n' % (hidden_base_address + (4 * x)))
        hex_file.write('0x%08x\n' % ((0x2 << 30) + (0x3 << 28) + (0x0 << 26) + (hidden_base_address + (4 * x))))

        if hidden >= 100:
            progress(hidden, x)

    print('\nAssembly 2')
    for x in range(outputs):
        assembly_file.write('LOAD R1, 0x%08x\n' % hidden_base_address)
        assembly_file.write('LOAD R2, 0x%08x\n' % (hidden_weight_base_address + (x * 4 * hidden)))

        hex_file.write('0x%08x\n' % ((0x1 << 28) + (0x0 << 26) + hidden_base_address))
        hex_file.write('0x%08x\n' % ((0x2 << 28) + (0x0 << 26) + (hidden_weight_base_address + (x * 4 * hidden))))

        for y in range(hidden):
            assembly_file.write('MULTADD R3, R1+, R2+\n')
            hex_file.write('0x%08x\n' % ((0b01 << 30) + (0b11 << 28) + (0b01 << 26) + 0b10))

        assembly_file.write('CHECK R3, (0x%08x)\n' % (output_base_address + (4 * x)))
        hex_file.write('0x%08x\n' % ((0x2 << 30) + (0x3 << 28) + (0x0 << 26) + (output_base_address + (4 * x))))

        if outputs >= 100:
            progress(outputs, x)

    assembly_file.close()
    hex_file.close()

    return hidden, hidden_base_address

if __name__ == "__main__":
    file_maker()
