import tkinter as tk
from tkinter import Label, Radiobutton, IntVar
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

def center_window(root, width=300, height=200):
    # Obtenir la largeur et la hauteur de l'écran
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculer la position x, y pour centrer la fenêtre
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Configurer la géométrie de la fenêtre
    root.geometry(f"{width}x{height}+{x}+{y}")

def main(func):
    def click_submit(prompt):
        func()
        if prompt != "Teach me about...":
            print(prompt)
            root.destroy()
            show_second_window()

    root = tk.Tk()
    root.geometry(f"{geometry[0]}x{geometry[1]}")
    root.title("Teach Me")
    root.resizable(False, False)
    root.configure(bg=color_blue)
    center_window(root, geometry[0], geometry[1])

    icon = tk.PhotoImage(file='src/assets/logo.png')
    root.iconphoto(False, icon)

    main_frame = tk.Frame(root, bg=color_blue)
    main_frame.place(x=spacing, y=spacing, width=geometry[0]-2*spacing, height=geometry[1]-2*spacing)

    title_label = Label(main_frame, text="What do you want to learn?", bg=color_blue, fg=color_white, font=("Helvetica", 14))
    title_label.pack(pady=(0, 10))

    textarea = ScrolledText(main_frame, wrap=tk.WORD, width=30, height=5)
    textarea.insert(tk.INSERT, "Teach me about...")
    textarea.bind("<FocusIn>", lambda event: textarea.delete('1.0', tk.END) if textarea.get('1.0', tk.END).strip() == "Teach me about..." else None)
    textarea.bind("<FocusOut>", lambda event: textarea.insert(tk.INSERT, "Teach me about...") if not textarea.get('1.0', tk.END).strip() else None)
    textarea.pack(pady=(0, 10))

    submit_button = ttk.Button(main_frame, text="Submit", command=lambda: click_submit(textarea.get('1.0', tk.END).strip()))
    submit_button.pack(pady=(0, 10))

    root.mainloop()


def show_second_window(data):

    qcm_window = tk.Tk()
    qcm_window.geometry("400x400")
    qcm_window.title("Questionnaire")
    qcm_window.configure(bg=color_blue)
    center_window(qcm_window, 400, 400)

    icon = tk.PhotoImage(file='src/assets/logo.png')
    qcm_window.iconphoto(False, icon)

    current_question_index = 0

    def create_question(index):
        if index < len(data):
            question_data = data[index]
            
            for widget in qcm_window.winfo_children():
                widget.destroy()

            question_label = Label(qcm_window, text=question_data["question"], bg=color_blue, fg=color_white, font=("Helvetica", 14))
            question_label.pack(pady=(20, 10))

            selected_option = IntVar(value=0)

            for text, value in question_data["options"]:
                Radiobutton(qcm_window, text=text, variable=selected_option, value=value, bg=color_blue, fg=color_white, selectcolor=color_blue).pack(anchor=tk.W, padx=20)

            result_label = Label(qcm_window, text="", bg=color_blue, fg=color_white, font=("Helvetica", 12))
            result_label.pack(pady=(10, 10))

            def submit_qcm():
                selected = selected_option.get()
                if selected == question_data["correct_answer"]:
                    result_label.config(text="Correct!")
                else:
                    result_label.config(text="Try again.")

            def prev_question():
                nonlocal current_question_index
                if current_question_index > 0:
                    current_question_index -= 1
                    create_question(current_question_index)

            def next_question():
                nonlocal current_question_index
                if current_question_index < len(data) - 1:
                    current_question_index += 1
                    create_question(current_question_index)

            submit_button_frame = tk.Frame(qcm_window, bg=color_blue)
            submit_button_frame.pack(pady=(10, 5))
            submit_button = ttk.Button(submit_button_frame, text="Submit", command=submit_qcm)
            submit_button.pack()

            navigation_button_frame = tk.Frame(qcm_window, bg=color_blue)
            navigation_button_frame.pack(pady=(5, 10))
            prev_button = ttk.Button(navigation_button_frame, text="Previous", command=prev_question)
            prev_button.pack(side=tk.LEFT, padx=10)
            next_button = ttk.Button(navigation_button_frame, text="Next", command=next_question)
            next_button.pack(side=tk.LEFT, padx=10)

    create_question(current_question_index)


spacing = 25
color_white = '#D9D9D9'
color_blue = '#414A6E'
geometry = (300, 200)

if __name__ == "__main__":
    def hello():
        print("Hello")

    data = [
        {
            "question": "What is the capital of France?",
            "options": [("Paris", 1), ("London", 2), ("Berlin", 3), ("Madrid", 4)],
            "correct_answer": 1
        },
        {
            "question": "What is the largest planet in our solar system?",
            "options": [("Mars", 1), ("Venus", 2), ("Jupiter", 3), ("Saturn", 4)],
            "correct_answer": 3
        }
    ]

    main(hello, data)
