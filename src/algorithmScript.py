#!/usr/bin/python


def main():
    assembly_file = open('Assembly.txt', 'w')
    hex_file = open('Hex.txt', 'w')

    inputs_outputs = int(input('Number of inputs and outputs: '))
    hidden = int(input('Number of hidden: '))

    input_base_address = 0
    hidden_base_address = 4 * inputs_outputs
    weight_base_address = hidden_base_address + (4 * hidden)
    hidden_weight_base_address = weight_base_address + (4 * hidden * inputs_outputs)
    output_base_address = hidden_weight_base_address + (4 * hidden * inputs_outputs)

    print('')
    print('Input Memory Base Address:   0x%08x' % input_base_address)
    print('Hidden Memory Base Address:  0x%08x' % hidden_base_address)
    print('Input Weight Base Address:   0x%08x' % weight_base_address)
    print('Hidden Weight Base Address:  0x%08x' % hidden_weight_base_address)
    print('Output Base Address:         0x%08x' % output_base_address)

    for x in range(hidden):
        assembly_file.write('LOAD R1, 0x%08x\n' % input_base_address)
        assembly_file.write('LOAD R2, 0x%08x\n' % (weight_base_address + (x * 4 * inputs_outputs)))

        hex_file.write('0x%08x\n' % ((0x1 << 28) + (0x0 << 26) + input_base_address))
        hex_file.write('0x%08x\n' % ((0x2 << 28) + (0x0 << 26) + (weight_base_address + (x * 4 * inputs_outputs))))

        for y in range(inputs_outputs):
            assembly_file.write('MULTADD R3, R1+, R2+\n')
            hex_file.write('0x%08x\n' % ((0b01 << 30) + (0b11 << 28) + (0b01 << 26) + 0b10))

        assembly_file.write('CHECK R3, (0x%08x)\n' % (hidden_base_address + (4 * x)))
        hex_file.write('0x%08x\n' % ((0x2 << 30) + (0x3 << 28) + (0x0 << 26) + (hidden_base_address + (4 * x))))

    for x in range(inputs_outputs):
        assembly_file.write('LOAD R1, 0x%08x\n' % (hidden_base_address + (4 * x)))
        assembly_file.write('LOAD R2, 0x%08x\n' % (hidden_weight_base_address + (x * 4 * hidden)))

        hex_file.write('0x%08x\n' % ((0x1 << 28) + (0x0 << 26) + (hidden_base_address + (4 * x))))
        hex_file.write('0x%08x\n' % ((0x2 << 28) + (0x0 << 26) + (hidden_weight_base_address + (x * 4 * hidden))))

        for y in range(hidden):
            assembly_file.write('MULTADD R3, R1+, R2+\n')
            hex_file.write('0x%08x\n' % ((0b01 << 30) + (0b11 << 28) + (0b01 << 26) + 0b10))

        assembly_file.write('CHECK R3, (0x%08x)\n' % (output_base_address + (4 * x)))
        hex_file.write('0x%08x\n' % ((0x2 << 30) + (0x3 << 28) + (0x0 << 26) + (output_base_address + (4 * x))))

    assembly_file.close()
    hex_file.close()

if __name__ == "__main__":
    main()
