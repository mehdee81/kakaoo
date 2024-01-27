from Graph_Scheduling import Graph, InOrderSchedule
import networkx as nx
import matplotlib.pyplot as plt
import time
import itertools

# lessons
courses = [
    ("|mabani|", "|kargah_computer|"),
    ("|mabani|", "|fizik_1|"),
    ("|mabani|", "|riazi_1|"),
    ("|mabani|", "|kargah_omomi|"),
    ("|mabani|", "|zaban_omomi|"),
    ("|mabani|", "|amar|"),
    ("|mabani|", "|az_electreki|"),
    ("|mabani|", "|electreki|"),
    ("|mabani|", "|difransiel|"),
    ("|mabani|", "|az_fizik_2|"),
    ("|mabani|", "|signal|"),
    ("|mabani|", "|signal|"),
    ("|mabani|", "|zaban_takhasosi|"),
    ("|kargah_computer|", "|fizik_1|"),
    ("|kargah_computer|", "|riazi_1|"),
    ("|kargah_computer|", "|kargah_omomi|"),
    ("|kargah_computer|", "|zaban_omomi|"),
    ("|kargah_computer|", "|dade|"),
    ("|kargah_computer|", "|az_manteghi|"),
    ("|kargah_computer|", "|manteghi|"),
    ("|kargah_computer|", "|amar|"),
    ("|kargah_computer|", "|az_electreki|"),
    ("|kargah_computer|", "|electreki|"),
    ("|kargah_computer|", "|difransiel|"),
    ("|kargah_computer|", "|az_fizik_2|"),
    ("|kargah_computer|", "|signal|"),
    ("|kargah_computer|", "|az_os|"),
    ("|kargah_computer|", "|os|"),
    ("|kargah_computer|", "|mabani_hoosh|"),
    ("|kargah_computer|", "|narm_2|"),
    ("|kargah_computer|", "|zaban_takhasosi|"),
    ("|kargah_computer|", "|dade_kavi|"),
    ("|kargah_computer|", "|bio|"),
    ("|fizik_1|", "|riazi_1|"),
    ("|fizik_1|", "|kargah_omomi|"),
    ("|fizik_1|", "|zaban_omomi|"),
    ("|riazi_1|", "|kargah_omomi|"),
    ("|riazi_1|", "|zaban_omomi|"),
    ("|riazi_1|", "|narm_2|"),
    ("|riazi_1|", "|zaban_takhasosi|"),
    ("|kargah_omomi|", "|zaban_omomi|"),
    ("|kargah_omomi|", "|dade|"),
    ("|kargah_omomi|", "|az_manteghi|"),
    ("|kargah_omomi|", "|manteghi|"),
    ("|kargah_omomi|", "|amar|"),
    ("|kargah_omomi|", "|az_electreki|"),
    ("|kargah_omomi|", "|electreki|"),
    ("|kargah_omomi|", "|difransiel|"),
    ("|kargah_omomi|", "|az_fizik_2|"),
    ("|kargah_omomi|", "|signal|"),
    ("|kargah_omomi|", "|az_os|"),
    ("|kargah_omomi|", "|os|"),
    ("|kargah_omomi|", "|mabani_hoosh|"),
    ("|kargah_omomi|", "|narm_2|"),
    ("|kargah_omomi|", "|zaban_takhasosi|"),
    ("|kargah_omomi|", "|dade_kavi|"),
    ("|kargah_omomi|", "|bio|"),
    ("|zaban_omomi|", "|dade|"),
    ("|zaban_omomi|", "|az_manteghi|"),
    ("|zaban_omomi|", "|manteghi|"),
    ("|zaban_omomi|", "|amar|"),
    ("|zaban_omomi|", "|az_electreki|"),
    ("|zaban_omomi|", "|electreki|"),
    ("|zaban_omomi|", "|difransiel|"),
    ("|zaban_omomi|", "|az_fizik_2|"),
    ("|zaban_omomi|", "|signal|"),
    ("|zaban_omomi|", "|az_os|"),
    ("|zaban_omomi|", "|os|"),
    ("|zaban_omomi|", "|mabani_hoosh|"),
    ("|zaban_omomi|", "|narm_2|"),
    ("|zaban_omomi|", "|dade_kavi|"),
    ("|zaban_omomi|", "|bio|"),
    ("|zaban_omomi|", "|az_manteghi|"),
    ("|zaban_omomi|", "|manteghi|"),
    ("|zaban_omomi|", "|amar|"),
    ("|zaban_omomi|", "|az_electreki|"),
    ("|zaban_omomi|", "|electreki|"),
    ("|zaban_omomi|", "|difransiel|"),
    ("|zaban_omomi|", "|az_fizik_2|"),
    ("|zaban_omomi|", "|signal|"),
    ("|zaban_omomi|", "|az_os|"),
    ("|zaban_omomi|", "|os|"),
    ("|zaban_omomi|", "|mabani_hoosh|"),
    ("|zaban_omomi|", "|narm_2|"),
    ("|zaban_omomi|", "|zaban_takhasosi|"),
    ("|zaban_omomi|", "|dade_kavi|"),
    ("|zaban_omomi|", "|bio|"),
    ("|dade|", "|az_manteghi|"),
    ("|dade|", "|manteghi|"),
    ("|dade|", "|amar|"),
    ("|dade|", "|az_electreki|"),
    ("|dade|", "|electreki|"),
    ("|dade|", "|difransiel|"),
    ("|dade|", "|az_fizik_2|"),
    ("|dade|", "|signal|"),
    ("|dade|", "|az_os|"),
    ("|dade|", "|os|"),
    ("|dade|", "|narm_2|"),
    ("|dade|", "|zaban_takhasosi|"),
    ("|az_manteghi|", "|manteghi|"),
    ("|az_manteghi|", "|amar|"),
    ("|az_manteghi|", "|az_electreki|"),
    ("|az_manteghi|", "|electreki|"),
    ("|az_manteghi|", "|electreki|"),
    ("|az_manteghi|", "|difransiel|"),
    ("|az_manteghi|", "|az_fizik_2|"),
    ("|az_manteghi|", "|signal|"),
    ("|az_manteghi|", "|az_os|"),
    ("|az_manteghi|", "|os|"),
    ("|az_manteghi|", "|mabani_hoosh|"),
    ("|az_manteghi|", "|narm_2|"),
    ("|az_manteghi|", "|zaban_takhasosi|"),
    ("|az_manteghi|", "|dade_kavi|"),
    ("|az_manteghi|", "|bio|"),
    ("|manteghi|", "|amar|"),
    ("|manteghi|", "|az_electreki|"),
    ("|manteghi|", "|electreki|"),
    ("|manteghi|", "|difransiel|"),
    ("|manteghi|", "|az_fizik_2|"),
    ("|manteghi|", "|signal|"),
    ("|manteghi|", "|mabani_hoosh|"),
    ("|manteghi|", "|narm_2|"),
    ("|manteghi|", "|zaban_takhasosi|"),
    ("|manteghi|", "|dade_kavi|"),
    ("|manteghi|", "|bio|"),
    ("|amar|", "|az_electreki|"),
    ("|amar|", "|electreki|"),
    ("|amar|", "|difransiel|"),
    ("|amar|", "|az_fizik_2|"),
    ("|amar|", "|signal|"),
    ("|amar|", "|az_os|"),
    ("|amar|", "|os|"),
    ("|amar|", "|narm_2|"),
    ("|amar|", "|zaban_takhasosi|"),
    ("|amar|", "|dade_kavi|"),
    ("|amar|", "|bio|"),
    ("|az_electreki|", "|electreki|"),
    ("|az_electreki|", "|difransiel|"),
    ("|az_electreki|", "|az_fizik_2|"),
    ("|az_electreki|", "|signal|"),
    ("|az_electreki|", "|az_os|"),
    ("|az_electreki|", "|os|"),
    ("|az_electreki|", "|mabani_hoosh|"),
    ("|az_electreki|", "|narm_2|"),
    ("|az_electreki|", "|zaban_takhasosi|"),
    ("|az_electreki|", "|dade_kavi|"),
    ("|az_electreki|", "|bio|"),
    ("|electreki|", "|difransiel|"),
    ("|electreki|", "|az_fizik_2|"),
    ("|electreki|", "|signal|"),
    ("|electreki|", "|az_os|"),
    ("|electreki|", "|os|"),
    ("|electreki|", "|mabani_hoosh|"),
    ("|electreki|", "|narm_2|"),
    ("|electreki|", "|zaban_takhasosi|"),
    ("|electreki|", "|dade_kavi|"),
    ("|electreki|", "|bio|"),
    ("|difransiel|", "|az_fizik_2|"),
    ("|difransiel|", "|az_os|"),
    ("|difransiel|", "|mabani_hoosh|"),
    ("|difransiel|", "|narm_2|"),
    ("|difransiel|", "|zaban_takhasosi|"),
    ("|difransiel|", "|dade_kavi|"),
    ("|difransiel|", "|bio|"),
    ("|az_fizik_2|", "|signal|"),
    ("|az_fizik_2|", "|az_os|"),
    ("|az_fizik_2|", "|os|"),
    ("|az_fizik_2|", "|mabani_hoosh|"),
    ("|az_fizik_2|", "|narm_2|"),
    ("|az_fizik_2|", "|zaban_takhasosi|"),
    ("|az_fizik_2|", "|dade_kavi|"),
    ("|az_fizik_2|", "|bio|"),
    ("|signal|", "|az_os|"),
    ("|signal|", "|os|"),
    ("|signal|", "|mabani_hoosh|"),
    ("|signal|", "|narm_2|"),
    ("|signal|", "|zaban_takhasosi|"),
    ("|signal|", "|dade_kavi|"),
    ("|signal|", "|bio|"),
    ("|az_os|", "|os|"),
    ("|az_os|", "|mabani_hoosh|"),
    ("|az_os|", "|narm_2|"),
    ("|az_os|", "|zaban_takhasosi|"),
    ("|az_os|", "|dade_kavi|"),
    ("|az_os|", "|bio|"),
    ("|os|", "|mabani_hoosh|"),
    ("|os|", "|narm_2|"),
    ("|os|", "|zaban_takhasosi|"),
    ("|os|", "|dade_kavi|"),
    ("|os|", "|bio|"),
    ("|mabani_hoosh|", "|narm_2|"),
    ("|mabani_hoosh|", "|zaban_takhasosi|"),
    ("|mabani_hoosh|", "|dade_kavi|"),
    ("|mabani_hoosh|", "|bio|"),
    ("|narm_2|", "|zaban_takhasosi|"),
    ("|narm_2|", "|bio|"),
    ("|zaban_takhasosi|", "|dade_kavi|"),
    ("|zaban_takhasosi|", "|bio|"),
    ("|dade_kavi|", "|bio|"),
    # |mabani| - |kargah_computer| - |fizik_1| - |riazi_1| - |kargah_omomi| - |zaban_omomi|
    # dade - |az_manteghi| - manteghi - |amar| - |az_electreki| - |electreki| - |difransiel| - |az_fizik_2|
    # |signal| - |az_os| - os - |mabani_hoosh| - |narm_2| - |zaban_takhasosi|
    # |dade_kavi| - |bio|
]

vahed = {
    "|mabani|": 1,
    "|kargah_computer|": 1,
    "|fizik_1|": 3,
    "|riazi_1|": 3,
    "|kargah_omomi|": 1,
    "|zaban_omomi|": 3,
    "|dade|": 3,
    "|az_manteghi|": 1,
    "|manteghi|": 3,
    "|amar|": 3,
    "|az_electreki|": 1,
    "|electreki|": 3,
    "|difransiel|": 3,
    "|az_fizik_2|": 1,
    "|signal|": 3,
    "|az_os|": 1,
    "|os|": 4,
    "|mabani_hoosh|": 3,
    "|narm_2|": 4,
    "|zaban_takhasosi|": 3,
    "|dade_kavi|": 3,
    "|bio|": 3,
}
tedad_vahed = 0
for key, value in vahed.items():
    tedad_vahed += value
teachers = {
    "|mabani|": "|a|",
    "|kargah_computer|": "|b|",
    "|fizik_1|": "|c|",
    "|riazi_1|": "|d|",
    "|kargah_omomi|": "|e|",
    "|zaban_omomi|": "|f|",
    "|dade|": "|r|",
    "|az_manteghi|": "|h|",
    "|manteghi|": "|i|",
    "|amar|": "|j|",
    "|az_electreki|": "|k|",
    "|electreki|": "|l|",
    "|difransiel|": "|m|",
    "|az_fizik_2|": "|n|",
    "|signal|": "|o|",
    "|az_os|": "|p|",
    "|os|": "|q|",
    "|mabani_hoosh|": "|r|",
    "|narm_2|": "|s|",
    "|zaban_takhasosi|": "|t|",
    "|dade_kavi|": "|u|",
    "|bio|": "|v|",
}
teachers_limit_time = {
    "|r|": [["4 shanbe", "17:30"], ["4 shanbe", "15:30"]],
}
my_graph = Graph(courses)
colors = my_graph.color_graph_h()
graph = my_graph.adj_dict

print(f" --------------------------------------------------------")
print(f"|Trying, Please wait. trying for {len(vahed)} lessons and {tedad_vahed} units|")
print(f" --------------------------------------------------------")

all_teachers_limit_states = []
combinations = itertools.product(*teachers_limit_time.values())

for i, combination in enumerate(combinations, 1):
    _limit_states = {}
    for teacher, time in zip(teachers_limit_time.keys(), combination):
        _limit_states[teacher] = time
    all_teachers_limit_states.append(_limit_states)

s = InOrderSchedule(colors, vahed, teachers , all_teachers_limit_states)
s.assign_lessons()
s.print_schedule()

G = nx.Graph(graph)
plt.figure(figsize=(10, 5))
nx.draw(G, with_labels=True)
plt.show()