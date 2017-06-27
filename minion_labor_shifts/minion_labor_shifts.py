''' 
script that looks for minions that have been assigned shifts more than n times
and removes them from the task list
'''

def forLoopAnswer(data, n):
	new_task_list = []
	for item in data:
		print("item:", item, "data count item:", data.count(item))
		if data.count(item) <= n:
			new_task_list.append(item)

	return new_task_list

#data = [5, 10, 15, 10, 7, 10, 10, 10, 5, 5, 5, 5, 2, 6, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 9, 11, 9, 9, 11]
#n = 3

def answer(data, n):
	return [item for item in data if data.count(item) <= n]

#print(answer(data, n))

