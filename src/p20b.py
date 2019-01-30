
import p20a

class PMachine(p20a.PMachine):

    def get_result(self):
        doormap = self.get_doormap_result()
        return doormap.room_distance_stats()[1]

def run_tests():
    pass

    