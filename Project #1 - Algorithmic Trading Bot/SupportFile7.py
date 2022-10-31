class Job:
    def __init__(self, s, f, val):
        self.start = s
        self.finish = f
        self.value = val
        

# We Assume the jobs are sorted by increasing finish time
# Returns the closest previus comptatable job to job_i
def getClosestCompatable(jobs:Job, i):
    start_i = jobs[i].start
    # print("start is:", start_i)
    diffs = []

    for job in jobs:
        diff = start_i - job.finish
        diffs.append(diff)
    


    # print(diffs)
    min_ = 10000000000
    i = 0
    idx = -1
    for dif in diffs:
        # print(dif)
        if dif >= 0 and dif <= min_:
            if dif == min_:
                if jobs[idx].value < jobs[i].value:
                    min_ = dif
                    idx = i
            min_ = dif
            idx = i
        i += 1

    # print(idx)
    return idx


def schedule(jobs): 
    jobs = sorted(jobs, key = lambda j: j.finish)
    jobs.insert(0, Job(0, 0, 0))

    M = [0 for j in jobs]
    B = [-1 for j in jobs]
    M[0] = 0
    j = 1
    while j < len(jobs):
        pOfj = getClosestCompatable(jobs, j)
        mm = M[pOfj]
        mmPrev = M[j-1]
        vj = jobs[j].value
        M[j] = max(vj + M[pOfj], M[j-1])
        if M[j] == M[j-1]:
            B[j] = 0
        else:
            B[j] = 1
        j += 1
    # print(M)
    # print(B)
    jj = []
    m = len(jobs) - 1
    while not m == 0:
        # print(m)
        if B[m] == 1:
            print((jobs[m].start, jobs[m].finish, jobs[m].value))
            jj.append((jobs[m].start, jobs[m].finish, jobs[m].value))
            m = getClosestCompatable(jobs, m)
        else:
            m -= 1
    return jj
    # print(M)

if __name__ == "__main__":
    Jobs =[Job(1, 2, 50), Job(3, 5, 2000), Job(2, 4, 200), Job(4, 10, 10000)]
    print(schedule(Jobs))