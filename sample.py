import tkinter as tk


def dodaj_etykiete_na_canvas(canvas):
    etykieta = tk.Label(canvas, text="Etykieta na Canvas", bg="white")
    etykieta_id = canvas.create_window(50, 50, window=etykieta, anchor='nw')
    
    # Przesunięcie etykiety na inne miejsce na Canvas
    canvas.coords(etykieta_id, 100, 100)

root = tk.Tk()
root.title("Etykieta na Canvas")

canvas = tk.Canvas(root, width=200, height=200, bg="lightgray")
canvas.pack()

dodaj_etykiete_na_canvas(canvas)

root.mainloop()