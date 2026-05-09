from collections import deque


def round_robin(processes, quantum):
    time = 0
    n = len(processes)
    queue = deque()
    in_queue = [False] * n
    completed = 0
    time_line = []

    while completed < n:
        for i, proc in enumerate(processes):
            if proc.arrival <= time and not in_queue[i] and proc.remaining > 0:
                queue.append(i)
                in_queue[i] = True

        if not queue:  # if the queue is empty then add 1 more second
            time_line.append(("Idle", time, time + 1))
            time += 1
            continue

        i = queue.popleft()
        p = processes[i]

        if p.start is None:   # in this second of starting the process we take the
            p.start = time    # time from the algorithm
        exec_time = min(quantum, p.remaining)  # Here we have two cases if the
        time_line.append((p.id, time, (time + exec_time)))
        time += exec_time     # quantum time is bigger than remaining time of the
        p.remaining -= exec_time  # process it then it return again to the queue if not
                              # then the process burst and ends

        for j, proc in enumerate(processes):
            if proc.arrival <= time and not in_queue[j] and proc.remaining > 0:
                queue.append(j)
                in_queue[j] = True

        if p.remaining > 0:
            queue.append(i)
        else:
            p.completion = time
            completed += 1

    return processes, time_line