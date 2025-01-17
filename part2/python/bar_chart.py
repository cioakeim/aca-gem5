# This script is used only to create the bar charts for the report
import numpy as np 
import matplotlib.pyplot as plt
import sys


filename=sys.argv[1]
if len(sys.argv)>2:
    benchmark_option=sys.argv[2]
else:
    benchmark_option="all"

data=np.genfromtxt(filename,delimiter="\t",dtype="str",skip_header=1)

if benchmark_option=="all":
    labels=np.array(["401","429","456","458","470"])
else:
    labels=np.array(["Default","f=3GHz","DDR3_2133_x64"])

data=data[:,1:].astype(float)

print(labels)
print(data)

barWidth = 0.20
metrics=["CPI","L1D MissRate","L1I MissRate","L2 MissRate"]
fig, axes = plt.subplots(1, len(metrics), figsize=(15, 5))

bar_width = 0.6  # Width of each bar

for i, (metric, ax) in enumerate(zip(metrics, axes)):
    ax.bar(labels, data[:,i], color=f"C{i}", width=bar_width)
    ax.set_title(metric)
    ax.set_xlabel('Benchmarks')
    if i == 0:  # Add y-axis label only on the first subplot
        ax.set_ylabel('Values')

# Adjust layout
plt.tight_layout()
plt.show()
exit(1)

cpi=data[:,0]
ldmr=data[:,1]
limr=data[:,2]
l2mr=data[:,3]

IT = [12, 30, 1, 8, 22] 
ECE = [28, 6, 16, 5, 10] 
CSE = [29, 3, 24, 25, 17] 

br1 = np.arange(len(cpi)) 
br2 = [x + barWidth for x in br1] 
br3 = [x + barWidth for x in br2] 
br4 = [x + barWidth for x in br3] 

plt.bar(br1, cpi, color ='r', width = barWidth, 
        edgecolor ='grey', label ='CPI') 
plt.bar(br2, ldmr, color ='g', width = barWidth, 
        edgecolor ='grey', label ='L1D MissRate') 
plt.bar(br3, limr, color ='b', width = barWidth, 
        edgecolor ='grey', label ='L1I MIssRate') 
plt.bar(br4, l2mr, color ='m', width = barWidth, 
        edgecolor ='grey', label ='L2 MIssRate') 

plt.title("Results for F=1GHz and Memory:DDR3_1600x64")
plt.xlabel('Benchmark', fontweight ='bold')
plt.ylabel('Metric', fontweight ='bold') 
plt.xticks([r + barWidth for r in range(len(IT))], 
        labels)

plt.legend()
plt.show() 

