import json
from TabuSearch import TabuSearch
import argparse

def main(args):
    with open(args.f) as file:
        data = json.load(file)
    
    if args.m == 0:
        ### Generating a random solution ###
        ts = TabuSearch(data=data,
                        K=args.k,
                        gamma=args.g,
                        L = args.l,
                        x_0 = [int(key)for key in data.keys()]) # randomly passing in any x_0 value 
                                                                # as this is not actually useful
        x_0 = ts.generate_initial_solution()
        print(f'Random solution generated that meets precedence constraints:')
        print([int(key) for key in x_0])

    elif args.m == 1:

        ts = TabuSearch(data=data,
                        K = args.k,
                        gamma = args.g,
                        L = args.l,
                        x_0 = args.x)
        ts.execute()

    elif args.m == 2:
    
        results = {}
        for K in [10,100,1000]:
            results[f'K={K}'] = {}
            for gamma in range(1,55,1): # Expanded Search Space
                results[f'K={K}'][f'gamma={gamma}'] = {}
                for L in range(1,60,1): # Expanded Search Space
                    ts = TabuSearch(data=data,
                                    K = K,
                                    gamma = gamma,
                                    L = L,
                                    x_0 = args.x)
                    ts.execute()
                    results[f'K={K}'][f'gamma={gamma}'][f'L={L}'] = ts.g_best

        with open("results/results.json", 'w') as f:
            json.dump(results, f, indent=4)
        
        print(f'Results have been saved to results/results.json')

if __name__ == "__main__":
    x_0 = [30,29,23,10,9,14,13,12,4,20,22,3,27,28,8,7,19,21,26,18,25,17,15,6,24,16,5,11,2,1,31]

    parser = argparse.ArgumentParser()
    parser.add_argument("-m", type=int, required=True, help="Enter part number to execute")
    parser.add_argument("-f", type=str, default="jobs_q2.json", help="Enter file path of JSON file containing job details")
    parser.add_argument("-x", type=list, default=x_0, help="Enter the list of initial starting solution. Otherwise will be default")
    parser.add_argument("-k", type=int, default=10, help="Enter K value. Default is 10. Only used for modes 0 and 1.")
    parser.add_argument("-g", type=int, default=10, help="Enter gamma value. Default is 10. Only used for modes 0 and 1.")
    parser.add_argument("-l", type=int, default=20, help="Enter L value for Tabu list length. Default 20. Only used for modes 0 and 1.")
    args = parser.parse_args()
    
    main(args)