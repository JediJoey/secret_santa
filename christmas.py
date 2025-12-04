from typing import List, Optional
import yaml
import random
import os

class Person:
    def __init__(self, name: str, incompatibles: list):
        self.name = name
        self.incompatibles = incompatibles
        self.their_person: Optional['Person'] = None

    def __repr__(self):
        return f"Person(name='{self.name}', incompatibles={self.incompatibles})"

    def reset_assignment(self):
        """Resets the person's assignment for a fresh run."""
        self.their_person = None

def load_people_from_yaml(filename: str) -> List[Person]:
    """
    Loads a list of Person objects from a YAML file.
    """
    people_list = []
    try:
        with open(filename, 'r') as file:
            data = yaml.safe_load(file)
            if not isinstance(data, list):
                raise ValueError("YAML data must be a list of person entries.")
            
            for item in data:
                person = Person(**item)
                people_list.append(person)
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
    except TypeError as e:
        print(f"Error creating Person object. Check YAML structure: {e}")

    return people_list

def decide_who_gets_what(people: List[Person]) -> bool:
    '''
    Attempts to assign a secret santa configuration.
    Returns True if successful, False otherwise.
    '''
    givers = list(people)
    receivers = list(people)
    max_attempts = 100

    # Ensure previous assignments are cleared before attempting a new run
    for p in people:
        p.reset_assignment()

    for attempt in range(max_attempts):
        temp_givers = list(givers)
        temp_receivers = list(receivers)
        random.shuffle(temp_receivers)

        is_valid_assignment = True
        current_assignments = {}
        
        for i, giver in enumerate(temp_givers):
            receiver = temp_receivers[i]
            if receiver.name in giver.incompatibles or giver.name == receiver.name:
                is_valid_assignment = False
                break
            current_assignments[giver] = receiver
        
        if is_valid_assignment:
            for giver, receiver in current_assignments.items():
                giver.their_person = receiver
            # print(f"Successfully assigned gifts after {attempt + 1} attempts.") # Optional console log
            return True

    print(f"Failed to find a valid assignment after {max_attempts} attempts for one run.")
    return False

def generate_results_to_file(people_data: List[Person], runs: int, filename: str):
    """
    Runs the assignment process multiple times and writes results to a text file.
    """
    with open(filename, 'w') as f:
        f.write("--- Secret Santa Results Log ---\n\n")
        
        successful_runs = 0
        while successful_runs < runs:
            if decide_who_gets_what(people_data):
                successful_runs += 1
                f.write(f"--- Entry {successful_runs} ---\n")
                # Sort by name for consistent output order in the file
                for p in sorted(people_data, key=lambda x: x.name): 
                    if p.their_person:
                        f.write(f"{p.name} is buying a gift for -> {p.their_person.name}\n")
                    else:
                        # Should not happen if decide_who_gets_what returns True
                        f.write(f"Error: {p.name} was not assigned a person.\n")
                f.write("\n")
        
        f.write(f"--- End of {runs} Successful Assignments ---\n")
    
    print(f"\nSuccessfully generated {runs} unique assignments and saved them to '{filename}'")
    print(f"File location: {os.path.abspath(filename)}")


# Example Usage:
if __name__ == "__main__":
    YAML_FILE = 'people.yaml'
    OUTPUT_FILE = 'secret_santa_results.txt'
    NUMBER_OF_RUNS = 10

    people_data = load_people_from_yaml(YAML_FILE)
    
    if people_data:
        print(f"Loaded {len(people_data)} people from '{YAML_FILE}': {[p.name for p in people_data]}")
        
        # Run the assignment logic 10 times and output to a file
        generate_results_to_file(people_data, NUMBER_OF_RUNS, OUTPUT_FILE)
