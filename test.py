passives = {}

with open("dependencies/artifactpriority.csv") as w:
	for d in w.readlines():
		a = d.split(',')
		passives[a[0]] =[a[1],a[3],a[5]]
passives.pop('')