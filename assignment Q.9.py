import heapq

class Job:
    def __init__(self, arrival, job_id, priority, duration, resources):
        self.arrival = arrival
        self.job_id = job_id
        self.priority = priority
        self.duration = duration
        self.resources = resources

    def __lt__(self, other):
        # Higher priority first, then earlier arrival
        if self.priority == other.priority:
            return self.arrival < other.arrival
        return self.priority > other.priority


def simulate_scheduler(workers, jobs):
    # Sort jobs by arrival time
    jobs.sort(key=lambda j: j.arrival)

    # Worker availability times
    worker_free = [0] * workers
    results = []
    wait_times = []

    # Priority queue for ready jobs
    pq = []

    time = 0
    idx = 0

    while idx < len(jobs) or pq:
        # Add jobs that have arrived
        while idx < len(jobs) and jobs[idx].arrival <= time:
            heapq.heappush(pq, jobs[idx])
            idx += 1

        # Assign jobs to free workers
        for w in range(workers):
            if pq and worker_free[w] <= time:
                job = heapq.heappop(pq)
                start = max(time, job.arrival)
                finish = start + job.duration
                results.append((job.job_id, f"W{w+1}", start, finish))
                worker_free[w] = finish
                wait_times.append(start - job.arrival)

        time += 1

    # Print results
    for r in results:
        print(f"{r[0]} {r[1]} {r[2]} {r[3]}")
    avg_wait = sum(wait_times) / len(wait_times) if wait_times else 0
    print(f"AVG_WAIT {avg_wait:.2f}")


# ---------------- SAMPLE INPUT ----------------
jobs = [
    Job(0, "J10", 15, 3, 1),
    Job(1, "J11", 25, 2, 1),
    Job(2, "J12", 10, 4, 1),
    Job(3, "J13", 20, 1, 1)
]

simulate_scheduler(workers=2, jobs=jobs)
