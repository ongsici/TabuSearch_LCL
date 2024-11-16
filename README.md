# COMP70068 Scheduling and Resource Allocation Coursework

## Installation

Instructions for installing conda environment as follows. Virtual environment can be used as well with the same requirements file.

```
conda create -n coursework python=3.10 -y
conda activate coursework

pip install -r requirements.txt
```

## Usage

JSON files were first prepared for both Q1 and Q2. The difference is in Q1, precedence constraints were represented as job successors while in Q2, precedence constraints were represented as job precedences. 

This was done by running the following in main directory:
```
python generate_jobs_data.py
```
Note that the current codes in the python script are used to generate ```jobs_q1.json```. To obtain ```jobs_q2.json```, uncomment the commented out sections in lines ```6-38``` and ```82```, and rename the output JSON in line ```85```.

### Question 1 Usage

The code has been implemented for a general DAG and can accept various values of job processing times, due dates, precedences through the ```"-f"``` command line argument. The default has been set to ```jobs_q1.json```. From the main directory, cd into Q1 folder.

```
cd Q1/
python main.py
```

The output results have been saved in ```q1_results.txt```. They can also be generated and saved again using the following:
```
python main.py > q1_results.txt
```

### Question 2 Usage

The code has been implemented to be generic and can accept various values of job processing times, due dates, precedences through the ```"-f"``` command line argument. The default has been set to ```jobs_q2.json```.
Additionally, search parameters such as Tabu list length (L), number of iterations (K) and tolerance ($\gamma$) can also be parsed through the command line.

#### 1) Generating an initial solution 

From the main directory, cd into Q2 folder. Then parse `0` into the ```"-m"``` argument when running main. 

```
cd Q2/
python main.py -m 0
```

The initial solution that is generated will be printed in the command line / terminal.

#### 2) Part 1 - Tabu search with L=20, $\gamma$=10 with K=10, 100 and 1000. 

From the main directory, cd into Q2 folder. Then parse `1` into the ```"-m"``` argument when running main.

```
cd Q2/
python main.py -m 1
```

K values can be changed by passing it in the ```"-k"``` argument. Values of L and $\gamma$ have been set to a default value of 20 and 10 respectively. However they can also be varied here with ```-l``` and ```-g``` arguments respectively. 

```
python main.py -m 1 -k 100
```
The output results for Tabu search with L=20, $\gamma$=10 with K=10, 100 and 1000 have been saved in ```results/K_10.txt```, ```results/K_100.txt``` and ```results/K_1000.txt``` respectively. They can also be generated and saved again using the following:

```
python main.py -m 1 -k 10 > results/K_10.txt
```

#### 3) Part 2 - Optimising Tabu search by varying L and $\gamma$ values

From the main directory, cd into Q2 folder. Then parse `2` into the ```"-m"``` argument when running main.

```
cd Q2/
python main.py -m 2
```

The search parameters used are:
| Parameter | Values                        |
| --------- | ----------------------------- |
| K         | [10,100,1000]                 |
| $\gamma$  | [5,10,15,20,25,30,35,40,45,50]|
| L         | [10,20,30,40,50]              |


The $g_{best}$ values for each conbination of search parameters is saved in `results/results.json` and the output for every iteration (including partial schedules) for this part is saved in `results/best_tabu_search.txt`. 