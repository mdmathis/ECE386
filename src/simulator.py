
def program_memory_file = "program_memory.bin"

def main():

    class Pipeline:
        def __init__(self):
            current_stage = 0
            instruction = 0

        def fetch(self, program_memory):

        def decode(self, binary):

        def read_memory(self, address):

        def execute(self, instruction):

        def write_memory(self, address):

        def next_stage(self):

    clock_cycle = 0

    R = [0, 0, 0, 0, 0]
    temp_R = R = [0, 0, 0, 0, 0];
    pipeline1, pipeline2, pipeline3, pipeline4, pipeline5 = Pipeline()

    PC = open(program_memory_file, mode = 'r')
    current_instruction = PC.readline()

    while current_instruction:
        temp_R = list(R)
        pipeline1.next_stage(temp_R)
        pipeline2.next_stage(temp_R)
        pipeline3.next_stage(temp_R)
        pipeline4.next_stage(temp_R)
        pipeline5.next_stage(temp_R)
        clock_cycle += 1
        












