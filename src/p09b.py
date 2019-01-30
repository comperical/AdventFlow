
import p09a

class PMachine(p09a.PMachine):


    def s1_init_machine(self):
        """
        Exactly the same init conditions as previous machine, just crank up max_marble quantity by a factor of 100
        """

        self.num_players = 424
        self.max_marble = 71482
        self.max_marble *= 100

def run_tests():
    pass

    