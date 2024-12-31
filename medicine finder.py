import json
from pathlib import Path


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
    except json.JSONDecodeError:  # Handles if the file is corrupted
        print("Error: Failed to decode JSON from the file. Please check the file format.")
        return []


# Search for medication by name
def search_medication(name, medications):
    for medication in medications:
        if "name" in medication and medication["name"].lower() == name.lower():
            return medication
    return None


# Display medication information
def display_medication_info(medication):
    print("Medication Details:")
    for key, value in medication.items():
        if isinstance(value, list):
            print(
                f"{key.title()}: {' - '.join(value)}"
                )
        else:
            print(
                f"{key.title()}: {str(value).rstrip('0').rstrip('.') if value else 'N/A'}",
                  "L.E." if key.lower() == "price" else ""
                )


# Provide guidance for unavailable medications - if wanted -
def handle_unavailable_medication(med_name):
    print(
        f"The medication '{med_name}' is not available in the database.",
        "Would you like to receive guidance on how to find more information about it? (yes/no)",
        sep="\n"
        )

    user_input = input("Enter (yes or no)").strip().lower()
    if user_input in ["yes", "y", "sure"]:
        print(
            "\nHere are some suggestions to find information about the medication:",
            "1. Visit your nearest pharmacy and consult a pharmacist.",
            "2. Check reliable online sources such as official healthcare websites or medication databases.",
            "3. Contact your healthcare provider for recommendations or alternatives.",
            sep="\n",
            )
    else:
        print("Understood. Let us know if you need assistance with another medication.")


# Main function to handle user input and search
def main():
    file_path = rf"{Path(__file__).parent.resolve()}\medication_data.json"
    medications = load_medication_data(file_path)

    if not medications:
        return

    while True:
        print("\nEnter the name of the medication you want to search for (or type 'exit' to quit):\n")
        med_name = input("Enter Medication Name.").strip()

        # Checks if the input is empty
        if not med_name:
            print("Input cannot be empty. Please enter a valid medication name.\n")
            continue

        # if input equals "exit" the code stops
        if med_name.lower() == "exit":
            print("Exiting the program. Goodbye!")
            break

        # Starts the searching
        medication = search_medication(med_name, medications)
        if medication:
            display_medication_info(medication)
        else:
            handle_unavailable_medication(med_name)


if __name__ == "__main__":
    main()
