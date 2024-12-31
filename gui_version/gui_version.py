import json
from pathlib import Path

from tkinter import *
from tkinter import ttk
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)

# Load medication data from JSON file
def load_medication_data(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if not data:  # Check if the file is empty or contains no data
                print(f"Error: The file {file_path} is empty.")
            return data
    except FileNotFoundError:  # Handles if there is no file
        print(f"Error: The file {file_path} does not exist.")
        return []
    except json.JSONDecodeError:
        print(
            "Error: Failed to decode JSON from the file. Please check the file format."
        )
        return []


# Search for medication by name
def search_medication(name, medications):
    for medication in medications:
        if "name" in medication and medication["name"].lower() == name.lower():
            return medication
    return None


# Display medication information
def display_medication_info(medication):
    info = []
    for key, value in medication.items():
        if isinstance(value, list):
            info.append(f"{key.title()}: {' - '.join(value)}")
        else:
            info.append(
                (
                    f"{key.title()}: {str(value).rstrip('0').rstrip('.') if value else 'N/A'}"
                    + (" L.E." if key.lower() == "price" else "")
                )
            )
    return info


# Provide guidance for unavailable medications
def handle_unavailable_medication(yes, no, result):
    result.configure(
        text=(
            f"The medication is not available in the database.\nWould you like to receive guidance on how to find more information about it? (yes/no)\n"
        )
    )
    yes.place(x=10, y=400, width=385)
    no.place(x=405, y=400, width=385)


def main():
    file_path = rf"{Path(__file__).parent.resolve()}\medication_data.json"
    medications = load_medication_data(file_path)

    if not medications:
        return

    r = Tk()
    r.title("Medication Finder")
    r.minsize(800, 550)
    r.maxsize(800, 550)
    r.configure(bg="#2E323B")
    r.iconbitmap(rf"{Path(__file__).parent.resolve()}\UI\images\drugs.ico")
    
    
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Modern.TButton",
        font=("Arial", 12, "bold"), foreground="#a8aebd", padding=10, relief="flat", width=40,
    )
    style.map(
        "Modern.TButton",
        background=[("!active", "#292e3b"), ("pressed", "#1b202b"), ("active", "#1b202b")],
    )


    result_label = Label(
        r, font=("Comic Sans MS", 20, "bold"), bg="#2E323B", justify="left", wraplength=780
    )
    label = Label(
        r, text="Enter Medication Name", font=("Comic Sans MS", 20, "bold"), bg="#2E323B", justify="left",
    )
    medication_input = Entry(
        r, font=("Comic Sans MS", 20, "bold"), bg="#262a33", borderwidth=0, justify="center"
    )

    search_button = ttk.Button(
    r, text="Search", command=lambda: (search_handle(yes_button, no_button, result_label)), style="Modern.TButton"
    )

    yes_button = ttk.Button(
        r, text="Yes", style="Modern.TButton", command=lambda: (yes(result_label), yes_button.place_forget(), no_button.place_forget()),
    )
    no_button = ttk.Button(
        r, text="No", style="Modern.TButton", command=lambda: (no(result_label), yes_button.place_forget(), no_button.place_forget()),
    )

    def yes(r):
        r.configure(
            font=("Comic Sans MS", 15, "bold"),
            text="Here are some suggestions to find information about the medication:\n1. Visit your nearest pharmacy and consult a pharmacist.\n2. Check reliable online sources such as official healthcare websites or medication databases.\n3. Contact your healthcare provider for recommendations or alternatives.",
        )


    def no(r):
        r.configure(
            text="Understood. Let us know if you need assistance with another medication."
        )

    def search_handle(yes, no, result):
        med_name = medication_input.get()
        
        medication = search_medication(med_name, medications)
        if medication:
            result.configure(text="\n".join(display_medication_info(medication)))
            yes.place_forget()
            no.place_forget()
        else:
            if not med_name:
                result.configure(text="Search Box cannot be empty. Please enter a valid medication name.")
                yes.place_forget()
                no.place_forget()
            else:
                handle_unavailable_medication(yes, no, result)


    medication_input.place(x=20, y=75, width=760)
    
    search_button.place(x=20, y=140, width=760)
    
    result_label.place(x=0, y=220)
    
    label.place(x=20, y=20)

    r.mainloop()

if __name__ == "__main__":
    main()