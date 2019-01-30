
import os
import sys
import importlib

import utility as U


def get_solutions():
    solnfile = os.path.join(U.get_data_dir(), "solutions.txt")
    solutions = {}

    for line in open(solnfile, 'r'):
        line = line.strip().replace(' ', '')
        if len(line) == 0 or line.startswith("#"):
            continue

        number, extrainfo = line.split(":")
        solpair = extrainfo.split(";") if ";" in extrainfo else extrainfo.split(",")
        solutions[int(number)] = solpair

    return solutions

if __name__ == "__main__":
        
    solutions = get_solutions()
    problems = list(U.get_problem_codes())
    solved = []

    for solidx, solns in solutions.items():
        for subidx, expect in enumerate(solns):
            pcode = "p{:02d}{}".format(solidx, "a" if subidx == 0 else "b")
            assert pcode in problems, "No problem code found for pcode={}".format(pcode)
            pmod = importlib.import_module(pcode)
            pmachine = pmod.PMachine()
            pmachine.run2_completion()
            result = str(pmachine.get_result()).replace(' ', '')
            assert expect == result, "For pcode={} expected {} but got result {}".format(pcode, expect, result)
            solved.append(pcode)


    print("Solved {} problems correctly: {}".format(len(solved), solved))

    """
    for idx, soln in enumerate(solutions):
        pcode = problems[idx]
        pmod = importlib.import_module(pcode)
        pmachine = pmod.PMachine()
        pmachine.run2_completion()
        result = str(pmachine.get_result())
        assert result == soln, "For problem {}, index {}, have solution {} but result is {}".format(pcode, idx, soln, result)
    """





    """
    assert len(sys.argv) >= 3, "Usage entry.py <solve|diagram|run2step|test> pXY ..."
    assert sys.argv[1] in ['solve', 'diagram', 'run2step', 'test']

    pcode = U.check_problem_code(sys.argv[2])
    pmod = importlib.import_module(pcode)


    if sys.argv[1] == 'diagram':
        print("Going to make diagram")
        quit()
    
    if sys.argv[1] == 'solve':
        pmachine.run2_completion()
        print("Result is : {}".format(pmachine.get_result()))

    if sys.argv[1] == 'run2step':
        stepcount = int(sys.argv[3])
        print("Running machine to step {}".format(stepcount))
        pmachine.run2_step_count(stepcount)

    if sys.argv[1] == 'test':
        pmod.run_tests()
    """