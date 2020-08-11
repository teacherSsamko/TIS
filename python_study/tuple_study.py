sample = (1,2,3)
print(sample[-1])


task = (1,2,3,4,5)
task_list = [*task][:-1]
completed_task = (*task_list, 'hi') #OK
print('completed_task=>',completed_task)