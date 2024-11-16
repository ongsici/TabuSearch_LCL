
__all__ = ["get_total_processing_time", "find_eligible_jobs", "calculate_T_j", "lowest_cost_job"]

def get_total_processing_time(data: dict):
    total =0
    for idx, job in data.items():
        total += job["processing_time"]
    return total

def find_eligible_jobs(S: list, data: dict, all_jobs: list) -> list:
    J = []
    for idx in all_jobs:
        if data[idx]["successors"] == []:
            J.append(idx)
        elif all(str(scheduled_job) in S for scheduled_job in data[idx]["successors"]):
            J.append(idx)
        
    return J

def calculate_T_j(job_id: int, curr_completion_time: int, data: dict ) -> int:
    return max(0, curr_completion_time - data[str(job_id)]["due_date"])

def lowest_cost_job(J: list, curr_completion_time: int, data: dict) -> int:
    tardiness_dict = {}
    for job in J:
        tardiness_dict[job] = calculate_T_j(job, curr_completion_time, data)
    return min(tardiness_dict, key=tardiness_dict.get) 
