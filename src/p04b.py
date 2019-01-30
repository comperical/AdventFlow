
import p04a

class PMachine(p04a.PMachine):

    def get_result(self):

        def bestmin4guard(gid):
            mincountpr = self.sleepy_counter(gid).most_common(1)[0]
            return [gid, mincountpr[0], mincountpr[1]]

        timetuples = [bestmin4guard(gid) for gid in self.guard2_sleep_wake]
        timetuples = sorted(timetuples, key=lambda x: -x[2])

        #for idx in range(10):
        #    print(timetuples[idx])

        besttup = timetuples[0]
        return besttup[0] * besttup[1]


        
    