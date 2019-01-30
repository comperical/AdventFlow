import json
import copy
from collections import deque

import utility as U
from finite_state import *

from p16a import MAIN_OP_MAP, InputInfo

class PMachine(FiniteStateMachine):
    
    
    def __init__(self):
        
        statemap = """
        {
            "HAI" : "F:AAO",
            "HAP" : "F:FBC",
            "MTR" : "F:PPC",
            "PPC" : "HAP",
            "FI" : "HAI",
            "AAO" : "T:SCC",
            "WC" : "AAO",
            "RC": "HAC",
            "HAC" : "F:SC"
        }
        """
        
        FiniteStateMachine.__init__(self, json.loads(statemap))

        self.inputs = deque([])
        self.probes = deque([])

        self.alpha_reg = []
        self.omega_reg = []

        # opidx -> [potential opcodes]
        self.candidates = {}

        # opidx -> opcode
        self.required = {}

        self.program = deque()

    def get_result(self):
        return self.registers[0]

    def s1_init_machine(self):
        inlist = U.read_input_deque('p16')

        while len(inlist) > 0:
            if inlist[0].startswith("Before"):
                str1 = inlist.popleft()
                str2 = inlist.popleft()
                str3 = inlist.popleft()
                iinfo = InputInfo(str1, str2, str3)
                self.inputs.append(iinfo)

                orig = "\n".join([str1, str2, str3])
                rslt = "{}".format(iinfo)

                assert orig == rslt, "Orig/Rslt: \n{}\n{}\n".format(orig, rslt)
                continue

            nextline = inlist.popleft().strip()
            if len(nextline) == 0:
                continue

            progcodes = [int(c) for c in nextline.split()]
            assert len(progcodes) == 4
            self.program.append(progcodes)

        # print("Read {} inputs ".format(len(self.inputs)))

        for idx in range(len(MAIN_OP_MAP)):
            self.candidates[idx] = list(MAIN_OP_MAP.keys())

    def s4_have_another_input(self):
        return len(self.inputs) > 0

    def s5_setup_for_input(self):
        self.probes = deque(MAIN_OP_MAP.keys())

        self.matchcodes = []

    def s6_have_another_probe(self):
        return len(self.probes) > 0

    def s10_apply_probe_op(self):
        probecode = self.probes[0]
        nextinput = self.inputs[0]

        self.alpha_reg = copy.copy(nextinput.alpha)
        self.omega_reg = copy.copy(nextinput.alpha)

        acode = nextinput.opcodes[1]
        bcode = nextinput.opcodes[2]
        ccode = nextinput.opcodes[3]

        myfunc = MAIN_OP_MAP.get(probecode)
        newcval = myfunc(self.alpha_reg, acode, bcode)
        self.omega_reg[ccode] = newcval

    def s12_match_target_result(self):
        return self.omega_reg == self.inputs[0].omega

    def s13_add_probe_match(self):
        #print("Got match {} for input".format(self.probes[0]))
        self.matchcodes.append(self.probes[0])

    def s14_poll_probe_code(self):
        self.probes.popleft()


    def s19_filter_bad_codes(self):
        opindx = self.inputs[0].opcodes[0]
        self.candidates[opindx] = [okop for okop in self.candidates[opindx] if okop in self.matchcodes]


    def s20_finish_input(self):
        self.inputs.popleft()




    def s22_all_assignments_okay(self):
        return len(self.required) == len(MAIN_OP_MAP)


    def s23_assign_required_ops(self):
        
        assigns = 0
        remops = list(self.candidates.keys())

        for opidx in remops:
            cands = self.candidates[opidx]
            if len(cands) == 1:
                self.required[opidx] = cands[0]
                self.candidates.pop(opidx)
                assigns += 1

        assert assigns > 0, "Failed to make ANY assignments"


    def s24_winnow_candidates(self):
        
        def filtercands(cands):
            return [c for c in cands if c not in self.required.values()] 

        self.candidates = { opidx : filtercands(cands) for opidx, cands in self.candidates.items() }


    def s25_sanity_check_codemap(self):
        
        assert len(self.candidates) == 0, "Still have remaining candidates"

        for opidx, match in self.required.items():
            #print("Found opidx={} --> opcode={}".format(opidx, match))
            pass

    def s26_start_program(self):
        self.registers = [0] * 4

    def s27_have_another_command(self):
        return len(self.program) > 0

    def s28_run_command(self):
        
        progcodes = self.program.popleft()
        opfunc = MAIN_OP_MAP.get(self.required[progcodes[0]])
        assert opfunc != None

        acode = progcodes[1]
        bcode = progcodes[2]
        ccode = progcodes[3]

        # print("Running code {} on registers {} with A={}, B={}, C={}".format(opfunc.__name__, self.registers, acode, bcode, ccode))

        newcval = opfunc(self.registers, acode, bcode)
        self.registers[ccode] = newcval

        # print("Resulting registers: {}".format(self.registers))

    def s30_success_complete(self):
        pass




def run_tests():
    
    pass
    