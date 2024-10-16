import tkinter as tk
from tkinter import scrolledtext, Frame, Label
from tkinter import ttk

def click_submit(prompt):
    if prompt != "Teach me about...":
        print(prompt)
        # Activer le bouton après le clic
        submit_button.config(state=tk.DISABLED)
        submit_button.bind("<Enter>", lambda e: submit_button.config(cursor="watch"))
        submit_button.bind("<Leave>", lambda e: submit_button.config(cursor="arrow"))
        textarea.config(state=tk.DISABLED)
        title_label.config(text="Processing...", fg=color_white)

spacing = 25
color_white = '#D9D9D9'
color_blue = '#414A6E'
geometry = (300, 200)

root = tk.Tk()

root.geometry(f"{geometry[0]}x{geometry[1]}")
root.title("Teach Me")
root.resizable(False, False)
root.configure(bg=color_blue)

# Create the main frame
main_frame = Frame(root, bg=color_blue)
main_frame.place(x=spacing, y=spacing, width=geometry[0]-2*spacing, height=geometry[1]-2*spacing)

# Title Label
title_label = Label(main_frame, text="What do you want to learn?", bg=color_blue, fg=color_white, font=("Helvetica", 14))
title_label.pack(pady=(0, 10))

# Textarea
textarea = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=30, height=5)
textarea.insert(tk.INSERT, "Teach me about...")
textarea.bind("<FocusIn>", lambda event: textarea.delete('1.0', tk.END) if textarea.get('1.0', tk.END).strip() == "Teach me about..." else None)
textarea.bind("<FocusOut>", lambda event: textarea.insert(tk.INSERT, "Teach me about...") if not textarea.get('1.0', tk.END).strip() else None)
textarea.pack(pady=(0, 10))

# Submit Button with cursor change
submit_button = ttk.Button(main_frame, text="Submit", command=lambda: click_submit(textarea.get('1.0', tk.END).strip()))
submit_button.pack(pady=(0, 10))

root.mainloop()
