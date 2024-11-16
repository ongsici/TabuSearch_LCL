
__all__ = ["TabuSearch"]

class TabuSearch():
    '''
    Tabu Search class that optimises a given schedule based on 1|prec|sum(Tj) problems
    '''
    def __init__(self, data: dict, K: int, gamma: int, L: int, x_0: list):
        self.data = data
        self.K = K
        self.gamma = gamma
        self.L = L
        self.x_0 = x_0
        self.k = 1
        self.swap_index = -1
        self.tabu_list=[]
        self.C_j_dict = {}
        self.T_j_dict = {} 
        self.solution_counter = {}
        self.g_y = 0
        self.g_best = 0

    def check_precedences(self, x_k: list) -> bool:
        '''
        For each job in the schedule provided, check that job precedences for job has been met

        Parameters:
            x_k (list): Job schedule 

        Returns:
            bool: True if all job precedences have been met in the given schedule
                    False if any job precedences have not been met.
        '''
        for idx, i in enumerate(x_k):
            precedence_list = self.data[str(i)]["precedences"]
        # check that the job precedences are completed before job i
            if len(precedence_list)!=0:
                for j in precedence_list:
                    if x_k.index(j) > idx:
                        return False
        return True  
    
    def generate_initial_solution(self) -> list:
        '''
        Given a jobs attribute file (self.data), searches for a 
        possible initial solution that meets precedences constraints. 

        To be used indepdently from execution of Tabu Search.

        Returns:
            list: possible initial solution
        '''
        x = []
        all_jobs = list(self.data.keys())

        while len(x) != len(all_jobs):
            for idx in all_jobs:
                if all(str(scheduled_job) in x for scheduled_job in self.data[idx]["precedences"]):
                    if idx not in x:
                        x.append(idx)
        return x 
    
    def calculate_C_j(self, x_k: list) -> None:
        '''
        Iterates through the given job schedule and calculates the completion time for each job.
        Job completion times (C_j) is stored in self.C_j_dict.

        Parameters:
            x_k (list): Job schedule 

        '''
        currTotal = 0
        for i in x_k:
            currTotal += self.data[str(i)]["processing_time"]
            self.C_j_dict[i] = currTotal

    def calculate_T_j(self) -> None:
        '''
        Iterates through job completion times dictionary (self.C_j_dict)
        to calculate Tardiness (T_j = max(0, C_j - d_j))

        Tardiness (T_j) is stored in self.T_j_dict.
        '''
        for id, C_j in self.C_j_dict.items():
            self.T_j_dict[id] = max(0, C_j - self.data[str(id)]["due_date"])

    def calculate_g(self, x_k: list) -> int:
        '''
        Calculates the total cost function for given job schedule
        by taking the sum of Tardiness values for each job

        Parameters:
            x_k (list): Job schedule 

        Returns:
            int: total cost function (sum T_j)
        '''
        self.calculate_C_j(x_k)
        self.calculate_T_j()
        return sum(self.T_j_dict.values())
    

    def swap(self, x_k: list) -> list:
        '''
        Performs a swap between 2 jobs in the given job schedule. 
        Sequence of swap follows the following:
            - self.swap_index contains the index of the previous swap. self.swap_index is incremented by 1.
            - First swap is done between jobs at index 0 and index 1 of list 
            - At the next iteration (k+1), jobs will be swapped between index 1 and index 2 
            - The above is repeated until the index reaches the 2nd last one in the list. 
                After which the swap index restarts at 0 and 1
        Index of the first job to be swapped at each iteration is stored in self.swap_index.

        For each swap attempt made, a new job schedule is generated (x_temp).
        Job precedences are checked for this new job schedule using self.check_precedences function
        If job precedences are not met, self.swap_index is incremented and swap is repeated. 
        
        Parameters:
            x_k (list): Job schedule 

        Returns:
            list: new job schedule after swapping jobs in self.swap_index position
                    and self.swap_index + 1 that meets job precedences constraints
        '''
        self.swap_index += 1
        self.swap_index = self.swap_index % len(x_k)
        self.swap_index = 0 if self.swap_index == len(x_k) -1 else self.swap_index
        x_temp = x_k.copy()
        temp = x_temp[self.swap_index]
        x_temp[self.swap_index] = x_temp[self.swap_index+1]
        x_temp[self.swap_index+1] = temp 
        
    
        while not self.check_precedences(x_temp):
            self.swap_index += 1
            self.swap_index = self.swap_index % len(x_k)
            self.swap_index = 0 if self.swap_index == len(x_k) -1 else self.swap_index
            x_temp = x_k.copy()
            temp = x_temp[self.swap_index]
            x_temp[self.swap_index] = x_temp[self.swap_index+1]
            x_temp[self.swap_index+1] = temp 

        return x_temp 
    
    def swap_in_tabu(self, x_new: list) -> bool:
        '''
        Checks if the jobs that have been swapped are in Tabu list
        Index of jobs swapped are in self.swap_index and self.swap_index +1.

        Returns:
            bool: True if the job tuple is found in Tabu List
                    False if job tuple is not found in Tabu List
        '''
        job1 = x_new[self.swap_index]
        job2 = x_new[self.swap_index+1]
        if (job1, job2) in self.tabu_list:
            return True
        elif (job2, job1) in self.tabu_list:
            return True 
        else: 
            return False
        
    def update_tabu_list(self, x_new: list) -> None:
        '''
        First checks the current length of Tabu List. 
        If length of Tabu list is L, drop the job tuple in the last index,
          i.e. the job tuple that was first added to the list (FIFO)

        Add the job tuple for the job that was swapped to the front of the Tabu List.

        '''
        if len(self.tabu_list) == self.L:
            self.tabu_list = self.tabu_list[:-1]
        self.tabu_list.insert(0, (x_new[self.swap_index], x_new[self.swap_index+1]))

    def execute(self)-> None:
        '''
        Main execution function for TabuSearch class. Performs the following steps:
        1. Given the initial schedule x_0, calculates cost function g_0.
        2. Sets g_best to the cost function of schedule x_0 (g_0). Sets the current g_y to g_0.
        3. For k number of steps:
            a) Performs swap of 2 neighbouring jobs. 
                Index of the first job to be swapped is self.swap_index.
                Index of second job to swap is self.swap_index +1.
            b) Counts the number of times an attempted swap solution has been made (self.solution_counter dict)
                This is used for scenarios where all swaps have been attempted through a schedule but no possible solution is found
            c) Calculate the cost function of current swapped jobs schedule (g_curr)
            d) Calculate the delta between g_curr and cost function of previous schedul (g_y)
            e) Checks if g_curr is smaller than g_best OR delta from d) is more than -gamma and the jobs swapped are not in Tabu list
                If true:
                    - Set g_y to g_curr
                    - Calculates g_best to be the minimum value between g_best and g_curr
                    - Adds the swapped jobs tuple to Tabu list
                    - Increment k 
                Else: 
                    - Checks if the solution counter for current k value has reached the total number of jobs -1. 
                        This would mean that all possible swaps in the schedule have been attempted but no solution was found
        '''
        g_0 = self.calculate_g(self.x_0)
        self.g_best = g_0
        self.g_y = g_0

        x_k = self.x_0

        while self.k <= self.K:
            print(f'=========================')
            print(f'k = {self.k}')
            if self.k not in self.solution_counter.keys():
                self.solution_counter[self.k] = 0
            x_new = self.swap(x_k)
            self.solution_counter[self.k] += 1
            print(f'Tabu List: {self.tabu_list}')
            print(f'x_new: {x_new}')
            print(f'Swap was made between jobs: {(x_new[self.swap_index], x_new[self.swap_index+1])}')
            g_curr = self.calculate_g(x_new)
            print(f'g_curr: {g_curr}')
            delta = self.g_y - g_curr
            print(f'delta {delta}')
            if g_curr < self.g_best or (delta > -self.gamma and not self.swap_in_tabu(x_new)):
                self.g_y = g_curr
                print(f'g_best: {self.g_best}')
                self.g_best = min(self.g_best, g_curr)
                print(f'New g_best: {self.g_best}')
                self.update_tabu_list(x_new)
                self.k += 1
                x_k = x_new
            elif self.solution_counter[self.k] == len(x_k)-1:
                # no more solutions
                break
            