import json
import argparse
from functions import get_total_processing_time, find_eligible_jobs, lowest_cost_job


def main(args):

    with open(args.f) as file:
        data = json.load(file)

    S = []
    iter_count = 1
    all_jobs = list(data.keys())
    curr_completion_time = get_total_processing_time(data)
    print(f'Starting S: {S}')
    print(f'Initial total completion time: {curr_completion_time}')
    print(f'')

    while len(S) != len(list(data.keys())):
        print(f'================= ITERATION: {iter_count} =================')
        J = find_eligible_jobs(S, data, all_jobs)
        print(f'Set of eligible jobs: {J}')

        job_to_add_to_S = lowest_cost_job(J, curr_completion_time, data)
        print(f'Among eligible jobs, lowest cost job is: {job_to_add_to_S}')

        S.insert(0, job_to_add_to_S)
        all_jobs.remove(job_to_add_to_S)
        print(f'Current S: {S}')

        curr_completion_time -= data[str(job_to_add_to_S)]["processing_time"]
        print(f'Current total completion time: {curr_completion_time}')
        
        iter_count += 1
        print(f'')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", type=str, default="jobs_q1.json", help="Enter file path of JSON file containing job details")
    args = parser.parse_args()
    
    main(args)