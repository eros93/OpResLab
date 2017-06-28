import numpy as np
import matplotlib.pyplot as plt
import json

#FILENAME1 = "lab2_v2.json"
#FILENAME2 = "lab2_v2_random.json"

FILENAME1 = "lab2_v2_randomTsd.json"
FILENAME2 = "lab2_v2_randomTsd_random.json"


# READING data from file
inputfile1 = open(FILENAME1,"r")
input_fmax = json.loads(inputfile1.read())
inputfile1.close()

inputfile2 = open(FILENAME2,"r")
input_fmax_random = json.loads(inputfile2.read())
inputfile2.close()

fmax_2 = input_fmax["2"]
fmax_3 = input_fmax["3"]
fmax_4 = input_fmax["4"]
fmax_2_random = input_fmax_random["2"]
fmax_3_random = input_fmax_random["3"]
fmax_4_random = input_fmax_random["4"]

fig1, fmax_plot = plt.subplots(1,1)
fmax_2_plot, = fmax_plot.plot(np.linspace(5,15,10), fmax_2, label='Delta=2')
fmax_3_plot, = fmax_plot.plot(np.linspace(5,15,10), fmax_3, label='Delta=3')
fmax_4_plot, = fmax_plot.plot(np.linspace(5,15,10), fmax_4, label='Delta=4')
fmax_plot.set_xlabel("Number of nodes - Different delta values")
fmax_plot.set_ylabel("Fmax")
fmax_plot.grid()
#fig1.title("Comparison Heuristic alg. on different delta values")
fmax_plot.legend(handles=[fmax_2_plot, fmax_3_plot, fmax_4_plot])
fname = "Different delta values_different traffic"
plt.savefig(fname)

fig2, fmax_delta2_plot = plt.subplots(1,1)
fmax, = fmax_delta2_plot.plot(np.linspace(5,15,10), fmax_2, label='Heuristic')
fmax_random, = fmax_delta2_plot.plot(np.linspace(5,15,10), fmax_2_random, label='Random')
fmax_delta2_plot.set_xlabel("Number of nodes - Delta = 2")
fmax_delta2_plot.set_ylabel("Fmax")
fmax_delta2_plot.grid()
#fig2.title("Heuristic vs. Random - Delta = 2")
fmax_delta2_plot.legend(handles=[fmax, fmax_random])
fname = "Delta = 2_different traffic"
plt.savefig(fname)

fig3, fmax_delta3_plot = plt.subplots(1,1)
fmax, = fmax_delta3_plot.plot(np.linspace(5,15,10), fmax_3, label='Heuristic')
fmax_random, = fmax_delta3_plot.plot(np.linspace(5,15,10), fmax_3_random, label='Random')
fmax_delta3_plot.set_xlabel("Number of nodes - Delta = 3")
fmax_delta3_plot.set_ylabel("Fmax")
fmax_delta3_plot.grid()
#fig3.title("Heuristic vs. Random - Delta = 3")
fmax_delta3_plot.legend(handles=[fmax, fmax_random])
fname = "Delta = 3_different traffic"
plt.savefig(fname)

fig4, fmax_delta4_plot = plt.subplots(1,1)
fmax, = fmax_delta4_plot.plot(np.linspace(5,15,10), fmax_4, label='Heuristic')
fmax_random, = fmax_delta4_plot.plot(np.linspace(5,15,10), fmax_4_random, label='Random')
fmax_delta4_plot.set_xlabel("Number of nodes - Delta = 4")
fmax_delta4_plot.set_ylabel("Fmax")
fmax_delta4_plot.grid()
#fig4.title("Heuristic vs. Random - Delta = 4")
fmax_delta4_plot.legend(handles=[fmax, fmax_random])
fname = "Delta = 4_different traffic"
plt.savefig(fname)

plt.show()