def priority_scheduling(processes):
    time = 0
    completed = 0
    n = len(processes)
    # Initialize remaining time and start tracking
    for p in processes:
        p.remaining_time = p.burst
        p.start = None
    
    time_line = []
    last_process_id = None
    segment_start = 0

    while completed < n:
        best = float('inf')
        position = -1
        
        # Find process with highest priority available at current time
        for i, p in enumerate(processes):
            if p.arrival <= time and p.remaining_time > 0:
                if p.priority < best:
                    best = p.priority
                    position = i

        if position == -1:
            # Handle Idle time
            if last_process_id != "Idle":
                if last_process_id is not None:
                    time_line.append((last_process_id, segment_start, time))
                last_process_id = "Idle"
                segment_start = time
            time += 1
            continue

        p = processes[position]
        
        # Set start time only the first time the process gets the CPU
        if p.start is None:
            p.start = time

        # If a context switch happens (new process takes over)
        if last_process_id != p.id:
            if last_process_id is not None:
                time_line.append((last_process_id, segment_start, time))
            last_process_id = p.id
            segment_start = time

        # Execute for 1 time unit
        p.remaining_time -= 1
        time += 1

        # Check if completed
        if p.remaining_time == 0:
            p.completion = time
            completed += 1
            time_line.append((p.id, segment_start, time))
            last_process_id = None # Reset so the next segment starts fresh

    return processes, time_line

def calculate_metrics(processes):
    result = []
    total_wt = total_tat = total_rt = 0

    for p in processes:
        turn_around_time = p.completion - p.arrival
        waiting_time = turn_around_time - p.burst
        response_time = p.start - p.arrival

        total_wt += waiting_time
        total_tat += turn_around_time
        total_rt += response_time

        result.append((p.id, turn_around_time, waiting_time, response_time))

    n = len(processes)
    avg = (total_tat / n, total_wt / n, total_rt / n)
    return result, avg