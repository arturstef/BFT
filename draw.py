import random
import re
import time
from functools import partial
from tkinter import *
from tkinter import ttk


from PIL import Image as PILImage
from PIL import ImageTk

from algorithms.king_algorithm import KingAlgorithm
from algorithms.lamport_algorithm import LamportIterAlgorithm, StackRecord
from algorithms.operations_batch import OperationsBatch
from algorithms.pbft_algorithm import PbftAlgorithm
from algorithms.q_voter import QVoterModel
from graph import Graph
from graph_templates import *
from logger import Logger
from variables import *
from vertex import Vertex
from algorithms.lamport_zlosliwosci import LamportZlosliwosci


V = [] #[[]]
E = [] #[{}]
lines = [] #[{}] #to są linie i one są jak E, gdzie to drugie to współrzędne
G = [] #[None]

drag_index = 0
startX = 0
startY = 0

algorithm_data = []

number_of_tab = 1
canvases = []
loggers = []
dots = {}

desc_instances = []
notebook = None
window = None
faliure_func = None

def drag_start(event):
    global drag_index, startX, startY
    #x = widget.winfo_x() - widget.startX + event.x
    widget = event.widget
    drag_index = 0
    for i in range(len(V[cur_i()])):
        if abs(G[cur_i()].vertices[i].position[0] - widget.winfo_x()) < 15 and abs(G[cur_i()].vertices[i].position[1] - widget.winfo_y()) < 15:
            drag_index = i
            break
    startX = event.x #startX, startY - odpowiedzialne za lewy górny róg etykiety
    startY = event.y

def drag_motion(event):
    global drag_index, startX, startY, canvas
    widget = event.widget
    w_pos = [widget.winfo_x(), widget.winfo_y()]
    G[cur_i()].vertices[drag_index].position = w_pos

    keys = E[cur_i()].keys()
    for key in keys:
        if f"{drag_index}," in key or f",{drag_index}" in key:
            cur_canv().delete(lines[cur_i()][key])
            if key.startswith(str(drag_index)):
                second_index = int(key.split(',')[1])
                E[cur_i()][key] = [G[cur_i()].vertices[drag_index].position[0] + 7.5, G[cur_i()].vertices[drag_index].position[1] + 7.5, G[cur_i()].vertices[second_index].position[0] + 7.5, G[cur_i()].vertices[second_index].position[1] + 7.5]
            else:
                second_index = int(key.split(',')[0])
                E[cur_i()][key] = [G[cur_i()].vertices[second_index].position[0] + 7.5, G[cur_i()].vertices[second_index].position[1] + 7.5, G[cur_i()].vertices[drag_index].position[0] + 7.5, G[cur_i()].vertices[drag_index].position[1] + 7.5]
            lines[cur_i()][key] = cur_canv().create_line(E[cur_i()][key][0], E[cur_i()][key][1], E[cur_i()][key][2], E[cur_i()][key][3], fill='#220066', width=3)

    x = widget.winfo_x() - startX + event.x
    y = widget.winfo_y() - startY + event.y
    widget.place(x=x, y=y)
'''
def drag_release(event):
    global drag_index
    widget = event.widget
    print('HELLO')
    V[drag_index].node = widget
'''
def destroy_labels():
    global G
    if G[cur_i()] != None:
        for vertex in G[cur_i()].vertices:
            if vertex.node != None:
                vertex.node.destroy()

def draw_graph():
    global V, E, canvas, im, lines, is_animated

    cur_canv().delete('all')
    is_animated = False

    for key, edge in E[cur_i()].items():
        lines[cur_i()][key] = cur_canv().create_line(edge[0]+7.5, edge[1]+7.5, edge[2]+7.5, edge[3]+7.5, fill='#220066', width=3)

    image = PILImage.open('img/node.png')
    i = ImageTk.PhotoImage(image, width=15, height=15)
    for vertex in V[cur_i()]:
        label = Label(cur_canv(), bg='#0000a1', height=15, width=15, image=i)
        label_id = cur_canv().create_window(50, 50, window=label, anchor='nw')
        cur_canv().coords(label_id, vertex.position[0], vertex.position[1])
        label.bind("<Button-1>", drag_start)
        label.bind("<B1-Motion>", drag_motion)
        vertex.set_node(label)

def cur_canv():
    global canvases, notebook
    return canvases[notebook.index(notebook.select())]

def cur_i():
    global notebook
    if notebook.winfo_exists() and notebook.winfo_ismapped():
        return notebook.index(notebook.select())
    else:
        return 0

def draw_bipartite_graph(V1, V2):
    global V, E, G
    nV1 = []
    nV2 = []
    pos = []
    for i, vertex in enumerate(V1):
            if vertex.position[0] > 0 and vertex.position[1] > 0:
                pos.append(vertex)
                vertex.node_id = i
                nV1.append(vertex)
    for i, vertex in enumerate(V2):
        if vertex.position[0] > 0 and vertex.position[1] > 0:
            pos.append(vertex)
            vertex.node_id = i + len(V1)
            nV2.append(vertex)

    V[cur_i()] = pos.copy()

    E[cur_i()] = {}
    for i in range(len(nV1)):
        for j in range(len(nV2)):
            E[cur_i()][f"{i},{j + len(nV1)}"] = [nV1[i].position[0], nV1[i].position[1], nV2[j].position[0], nV2[j].position[1]]

    G[cur_i()] = Graph(V[cur_i()], E[cur_i()])
    draw_graph()

def set_vertices_from_positions(pos: list[(float, float)]):
    global V
    V[cur_i()] = []
    for i in range(len(pos)):
        V[cur_i()].append(Vertex(pos[i], i))
    return V[cur_i()]

def draw_full_graph(vertices):
    global V, E, G
    V[cur_i()] = vertices.copy()
    E[cur_i()] = {}
    for i in range(len(vertices)):
        for j in range(len(vertices)):
            i_pos = vertices[i].position
            j_pos = vertices[j].position
            if not all(np.equal(i_pos, j_pos)) and [i_pos[0], i_pos[1], j_pos[0], j_pos[1]] not in E[cur_i()].values() and [j_pos[0], j_pos[1], i_pos[0], i_pos[1]] not in E[cur_i()].values():
                E[cur_i()][f"{i},{j}"] = [i_pos[0], i_pos[1], j_pos[0], j_pos[1]]
    
    G[cur_i()] = Graph(V[cur_i()], E[cur_i()])
    draw_graph()

def Kn(name: str): #rysuje i usuwa poprzedni rysunek
    destroy_labels()
    draw_full_graph(set_vertices_from_positions(generate_positions(name, (canvases[cur_i()].winfo_reqwidth(), canvases[cur_i()].winfo_reqheight()))))

def Knn(name: str): #rysuje i usuwa poprzedni rysunek
    destroy_labels()
    V1, V2 = generate_positions(name, (canvases[cur_i()].winfo_reqwidth(), canvases[cur_i()].winfo_reqheight()))
    draw_bipartite_graph(set_vertices_from_positions(V1), set_vertices_from_positions(V2))


def run(algorithm, set1 = 3, set2 = 2):
    global G, result, algorithm_data, desc_instances, curren_algorithm

    switch_description_text(descriptions[algorithm])

    g_copy = G[cur_i()].copy() # is supposed to work with algorithm and change the nodes colors and so on, not implemented yet

    if G[cur_i()] != None:

        if algorithm == 'king':
            algorithm = KingAlgorithm(G[cur_i()])
            result = algorithm.runAlgorithm(G[cur_i()], set1)
            print (result[0])
            # for i in result[1]:
            #     print(i.get_operations())
            algorithm_data = result
            run_animation(g_copy)
        elif algorithm == 'lamport':
            #TO DO ZMIENIĆ NAZWY
            if faliure_func is None:
                algorithm = LamportIterAlgorithm(G[cur_i()])
                result = algorithm.runAlgorithm(G[cur_i()], set2)
            else:
                algorithm = LamportZlosliwosci(G[cur_i()])
                result = algorithm.runAlgorithm(G[cur_i()], set2,faliure_func)


            #for i in result[1]:
            #    print(i.get_operations())
            algorithm_data = result
            run_animation(g_copy)

        elif algorithm == 'q_voter':
            algorithm = QVoterModel(G)
            result = algorithm.runAlgorithm(G[cur_i()], set1, set2)
            print (result[0])
            # for i in result[1]:
            #     print(i.get_operations())
            algorithm_data = result
            run_animation(g_copy)
        elif algorithm == 'pbft':
            algorithm = PbftAlgorithm(G[cur_i()])

            linear_increase = lambda iteration: min(0.05 + 0.1 * iteration, 1)
            exponential_growth = lambda iteration: min(0.05 * (1.1 ** iteration), 1)

            result = algorithm.runAlgorithm(G[cur_i()], set2)
            print (result[0])
            # for i in result[1]:
            #     print(i.get_operations())
            algorithm_data = result
            run_animation(g_copy)
        else:
            print('Algorithm not found or not implemented yet')

def switch_description_text(text):
    global desc_instances
    desc_instances[cur_i()].config(state=NORMAL)
    desc_instances[cur_i()].delete("1.0", END)
    desc_instances[cur_i()].insert(END, text)
    desc_instances[cur_i()].config(state=DISABLED)

def on_tab_change(event):
    global is_animated
    is_animated = False

def create_new_tab():
    global notebook, number_of_tab, window, canvases, lines
    new_tab = Frame(notebook)
    notebook.add(new_tab, text=f"Zakładka {number_of_tab}")
    notebook.bind("<<NotebookTabChanged>>", on_tab_change)
    number_of_tab += 1

    V.append([])
    E.append({})
    lines.append({})
    G.append(Graph())

    canvas = Canvas(new_tab, width=800, height=500, bg='#444466')
    canvas.grid(row=0, column=0, sticky=NW)
    canvases.append(canvas)

    description = Text(new_tab, wrap="word", width=30, state=DISABLED, height=60)
    description.grid(row=0, column=1, sticky=NE, rowspan=2)
    desc_instances.append(description)

    logger = Logger(master=new_tab, max_messages=15, width=99, height=30)
    logger.lines = []
    loggers.append(logger)
    logger.new_message("Utworzono okno")

'''
    algorithms_names = ["king", "lamport", "q_voter", "pbft"]

    label = Label(new_tab, text="Selected option: 1")
    for index in range(len(algorithms_names)):
        radiobutton = Radiobutton(new_tab,
                        text=algorithms_names[index],
                        value=index,
                        padx = 25,
                        font=("Impact", 50),
                        compound = 'left',
                        indicatoron=0,
                        width=3
                        )
        radiobutton.grid(row=i, column=1, sticky="e")
'''

# TODO
def setup(scenario):
    global icon_true, icon_false, G, faliure_func
    if scenario == "Samoloty":
        Knn("Planes")
        G[cur_i()].vertices[0].is_faulty = True
        G[cur_i()].vertices[6].is_faulty = True
        
        G[cur_i()].vertices[0].current_choice = False
        G[cur_i()].vertices[1].current_choice = True
        G[cur_i()].vertices[2].current_choice = True
        G[cur_i()].vertices[3].current_choice = False
        G[cur_i()].vertices[4].current_choice = True
        G[cur_i()].vertices[5].current_choice = True
        G[cur_i()].vertices[6].current_choice = True
        G[cur_i()].vertices[7].current_choice = True
        G[cur_i()].vertices[8].current_choice = False
        icon_true = "img/info.png"
        icon_false = "img/red_error.png"
        run('king',3)
    elif scenario == "Dziennikarz":
        Kn("Journalist")
        G[cur_i()].vertices[0].current_choice = True
        G[cur_i()].vertices[1].current_choice = True
        G[cur_i()].vertices[2].current_choice = False
        G[cur_i()].vertices[3].current_choice = True
        G[cur_i()].vertices[4].current_choice = False
        G[cur_i()].vertices[5].current_choice = True

        G[cur_i()].vertices[2].is_faulty = True

        icon_true = "img/true.png"
        icon_false = "img/fake.png"
        run('pbft', 1, 0)
    elif scenario == "Porównywanie parami":
        Kn("Pairwise Comparison")
        G[cur_i()].vertices[0].current_choice = True
        G[cur_i()].vertices[1].current_choice = True
        G[cur_i()].vertices[2].current_choice = True
        G[cur_i()].vertices[3].current_choice = False
        G[cur_i()].vertices[4].current_choice = True
        G[cur_i()].vertices[5].current_choice = True
        G[cur_i()].vertices[6].current_choice = False

        G[cur_i()].vertices[2].is_faulty = True
        G[cur_i()].vertices[4].is_faulty = True

        icon_true = "img/green_dot.png"
        icon_false = "img/blue_dot.png"
        run('lamport', 1, 1)

def modify(option):
    global G
    if option == "20% waliwych":
        G[cur_i()].set_nodes_faulty_percent(20)
    elif option == "50% waliwych":
        G[cur_i()].set_nodes_faulty_percent(50)
    elif option == "80% waliwych":
        G[cur_i()].set_nodes_faulty_percent(80)
    elif option == "20% na tak":
        G[cur_i()].set_nodes_choice_percent(20)
    elif option == "50% na tak":
        G[cur_i()].set_nodes_choice_percent(50)
    elif option == "80% na tak":
        G[cur_i()].set_nodes_choice_percent(80)        


'''
############################################################################################################

Here are the buttons and canvas elements

############################################################################################################
'''
def create_window(w):
    global notebook, window
    window = w
    window.geometry(f"{width}x{height}")

    im = PhotoImage(file='img/node.png').subsample(x=25, y=25)

    menubar = Menu(window)
    window.config(menu=menubar)

    notebook = ttk.Notebook(window)
    notebook.pack(expand=True, fill="both")

    option_menu = Menu(menubar, tearoff=0)

    menubar.add_cascade(label="Opcje", menu=option_menu)

    option_menu.add_command(label="Nowa zakładka", command=create_new_tab)


    full_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Grafy Pełne", menu=full_menu)



    for i in range(3,9):
        full_menu.add_command(label=f"K{i}", command=partial(Kn, f"K{i}"))

    bipartite_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Grafy Dwudzielne", menu=bipartite_menu)

    for i in ["3,3", "5,5", "3,5"]:
        bipartite_menu.add_command(label=f"K{i}", command=partial(Knn, f"K{i}"))

    algorithm_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Algorytmy", menu=algorithm_menu)

    for alg in ["king", "lamport", "q_voter", "pbft"]:
        algorithm_menu.add_command(label=alg, command=partial(run, alg))

    scenarios_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Scenariusze", menu=scenarios_menu)

    for scenario in ["Samoloty", "Dziennikarz", "Porównywanie parami"]:
        scenarios_menu.add_command(label=scenario, command=partial(setup, scenario))

    algorithm_options = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Opcje algorytmu", menu=algorithm_options)

    for option in ["20% wadliwych", "50% wadliwych", "80% wadliwych", "20% na tak", "50% na tak", "80% na tak"]:
        algorithm_options.add_command(label=option, command=partial(modify, option))

    faliure_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Faliure options", menu=faliure_menu)
    #TO DO ZMIENIĆ NA WŁAŚCIWE ZŁOŚLIWOŚCI
    for faliures in ["failure rate increase","message lost","defalut"]:
        faliure_menu.add_command(label=faliures, command=partial(setup_faliures,faliures))

def setup_faliures(faliures):
    global faliure_func
    if faliures == "failure rate increase":
        faliure_func =  "faliure1"
    elif faliures == "message lost":
        faliure_func = "faliure2"
    elif faliures == "defalut":
        faliure_func = None
    else:
        raise NotImplemented


def run_animation(graph = None):
    global is_animated, G, algorithm_data, canvases, notebook, window, dots

    if len(G) < 1:
        return

    false_image = PILImage.open(icon_false)
    false_image = false_image.resize((15,15))
    false_image = ImageTk.PhotoImage(false_image)

    true_image = PILImage.open(icon_true)
    true_image = true_image.resize((15,15))
    true_image = ImageTk.PhotoImage(true_image)

    is_animated = True
    time_to_create_new_nodes = True

    for dot in dots.values():
        cur_canv().delete(dot)

    dots = {}
    frame = 0
    fmax = 40
    csid = 0 #current step id
    ad = []
    task = []
    for data in algorithm_data[1]:
        ad.append(data.get_operations())
        task.append(data.get_title())
    while is_animated and csid < len(ad):
        if task[csid] == "send":
            if time_to_create_new_nodes:
                last_sender_id = 0
                pos = (0,0)
                for i in range(len(ad[csid])):
                    pattern = '|'.join(re.escape(separator) for separator in ':;,')
                    data = re.split(pattern, ad[csid][i])
                    if "Sender" == data[0]:
                        last_sender_id = data[2]
                        pos = G[cur_i()].vertices[int(data[2])].position
                    elif "Send" == data[0]:
                        target_image = false_image
                        if data[-1] == "True":
                            target_image = true_image

                        dots[str(last_sender_id)+" "+str(data[2])] = cur_canv().create_image(pos[0], pos[1], image=target_image, anchor=NW)
                time_to_create_new_nodes = False
            else:
                for key, value in dots.items():
                    if not is_animated:
                        break
                    ids = key.split()
                    #moja teoria mówi, że to coś związanego z tym, który node jest pierwszy
                    if len(G[cur_i()].vertices[int(ids[1])].position) == 2 and len(G[cur_i()].vertices[int(ids[0])].position) == 2:
                        x = G[cur_i()].vertices[int(ids[1])].position[0] - G[cur_i()].vertices[int(ids[0])].position[0]
                        y = G[cur_i()].vertices[int(ids[1])].position[1] - G[cur_i()].vertices[int(ids[0])].position[1]

                        direction = (x/fmax, y/fmax) #znacznik
                        cur_canv().move(value, direction[0], direction[1])
                        window.update()
                frame += 1
                time.sleep(0.075)
                if frame >= fmax:
                    frame = 0
                    time_to_create_new_nodes = True
                    csid += 1
                    for key, value in dots.items():
                        cur_canv().delete(value)
                    dots = {}
        elif task[csid] == "log":
            if  len(ad[csid]) > 0:
                loggers[cur_i()].new_message(ad[csid][0])
            csid += 1
        elif task[csid] == "set_opinion":
            csid += 1
        else:
            print("ERROR")
            csid += 1

    print("ANIMATION END")

    loggers[cur_i()].new_message("Stan węzłów po zakończeniu algorytmu:")
    for vertex in G[cur_i()].vertices:
        loggers[cur_i()].new_message(f'Węzeł {vertex.node_id}: {vertex.get_current_choice()}')
