import tkinter as tk


root = tk.Tk()
root.title("Página principal")
root.geometry("400x600")
root.configure(bg='#457b9d')

# Configurações de estilo
label_font = ("Bahnschrift SemiBold", 12)

texto_1 = tk.Label(root, text="CAMPEÃO GAÚCHO")
a = "9 6"
b = a.split(" ")
print(b)
texto_1.pack(padx=50, pady=50)



# Iniciar o loop principal da interface gráfica
root.mainloop()
