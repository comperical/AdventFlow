
import p19a

class PMachine(p19a.PMachine):

    # Just override initial register setting
    def get_initial_register(self):
        return 1

        
