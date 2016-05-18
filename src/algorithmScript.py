#!/usr/bin/python
# Script to someday convert neural network to algorithm.


def main():
    assembly_file = open('Assembly.txt', 'w')

    inputs_outputs = int(input('Number of inputs and outputs: '))
    hidden = int(input('Number of hidden: '))

    input_base_address = 0
    hidden_base_address = 4 * inputs_outputs
    input_weight_list = []

    print('You entered:\nInputs / Outputs: ', inputs_outputs, '\nHidden: ', hidden)
    print('Input Memory Base Address:   %08x' % input_base_address)
    print('Hidden Memory Base Address:  %08x' % hidden_base_address)

    weight_base_address = hidden_base_address + (4 * hidden)
    for x in range(hidden):
        input_weight_list.append(int(weight_base_address + (x * 4 * inputs_outputs)))
        # print('Hidden Weight #%d Base Address: %08x' % (x, previous_weight))

    count = 0
    assembly_file.write('0x0101%08x - LOAD R1, 0x%08x\n' % (input_base_address, input_base_address))
    assembly_file.write('0x0110%08x - LOAD R2, 0x%08x\n' % (input_weight_list[0], input_weight_list[0]))

    for x in input_weight_list:
        for y in range(inputs_outputs):
            assembly_file.write('0x0011%08x%08x - MULTADD R3, [R1+0x%08x], R2+(0x%08x)\n'
                                % (y * 4, x + 4 * y, y * 4, x + 4 * y))

        assembly_file.write('0x11110%08x - CHECK R3, 0x%08x\n'
                            % (hidden_base_address + count * 4, hidden_base_address + count * 4))
        count += 1

if __name__ == "__main__":
    main()
