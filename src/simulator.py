




def main(): 
    def write_log():
        log_file.write( R + clock_cycle + pipelines + '\n')

    class Pipeline:
        def __str__(self):
            return current_stage + instruction

        def __init__(self):
            current_stage = 0
            instruction = 0
            address = 0
            register = 0
            immediate = 0
            stalled = 0

        def fetch(self, program_memory):

        def decode(self):

        def read_memory(self, data_memory, temp_registers):

        def execute(self, registers):

        def write_memory(self, output_file,  temp_registers):

        def stall(self):
            stalled = True

        def next_stage(self):
            if stalled:
                return
            else:
                if (current_stage < len(stages) - 1)
                    current_stage += 1
                else
                    current_stage = 0

            
    program_memory_file = "program_memory.bin"
    data_memory_file = "data_memory.bin"
    output_file = "output_file.bin"
    log_file = open(program_memory_file + "-log.txt")
    log_file.write('R' + 'clock_cycle' + 'pipelines')

    clock_cycle = 0
    R = [0, 0, 0, 0, 0]
    temp_R = list(R)
    pipelines = list()
    sim_log = open(time, mode = 'w')
    program_memory = open(program_memory_file, mode='r')
    data_memory = open(data_memory_file, mode='r')

    for count in range (5)
        pipelines.append(Pipeline())

    stage_status = {
        "Fetch" : "free",
        "Decode": "free",
        "Read Memory": "free",
        "Execute": "free",
        "Write Memory": "free"
    }

    while current_instruction:
        
        for pipeline in pipelines:
            if (pipeline.current_stage == 0 and stage["Fetch"] != "free")
                pipeline.fetch(program_memory)
                stage["Fetch"] = "busy"
            elif (pipeline.current_stage == 1 and stage["Decode"] != "free")
                pipeline.decode()
                stage["Decode"] = "busy"
            elif (pipeline.current_stage == 2 and stage["Read Memory"] != "free")
                pipeline.read_memory(data_memory, temp_R)
                stage["Read Memory"] = "busy"
            elif (pipeline.current_stage == 3 and stage["Execute"] != "free")
                pipeline.execute(R)
                stage["Execute"] = "busy"
            elif (pipeline.current_stage == 4 and stage["Write Memory"] != "free")
                pipeline.write_memory(output_file, temp_R)
                stage["Write Memory"] = "busy"
            else
                pipeline.stall()

        for pipeline in pipelines:
            pipeline.next_stage()  

        write_log()

        clock_cycle += 1

        R = list(temp_R)
        












