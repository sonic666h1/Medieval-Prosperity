import random
import json

# Initialize resources
resources = {
    "gold": 0,
    "food": 0,
    "wood": 0,
    "population": 0,
}

# Initialize quests
quests = []

# Initialize jobs
jobs = {
    "farmers": 0,
    "lumberjacks": 0,
    "miners": 0,
    "merchants": 0,
}

# Initialize the starting location
starting_location = "A humble hamlet"

# Initialize the number of days
days = 1

# Storyline and lore specific to the starting location
storyline = {
    "A humble hamlet": [
        "You reside in a peaceful hamlet nestled amidst rolling hills and lush forests.",
        "As the village elder, your mission is to guide your people towards prosperity.",
        "To achieve this, you must manage resources, assign jobs, and interact with neighboring settlements.",
    ],
    "A growing village": [
        "Your village has expanded into a growing settlement amidst fertile farmlands and dense forests.",
        "Your leadership is crucial to ensure the prosperity of your people.",
        "Balance resources, delegate jobs, and foster relationships with neighboring communities to thrive.",
    ],
    "A bustling town": [
        "Your town thrives as a bustling hub of trade and culture, nestled within the heart of a vast kingdom.",
        "Your role as the town's steward is vital for its continued success.",
        "Navigate the complexities of governance, allocate resources, and engage in diplomacy with neighboring realms to flourish."
    ],
}

# List of quests available from merchants
merchant_quests = [
    {"name": "Escort the Merchant's Caravan", "reward": 50},
    {"name": "Retrieve Stolen Goods", "reward": 75},
    {"name": "Help a Villager", "reward": 12}
    # Add more quests as desired
]

# Events
def random_event():
    event_chance = random.randint(1, 100)
    if event_chance <= 5:
        food_loss = random.randint(5, 15)
        if resources["food"] >= food_loss:
            resources["food"] -= food_loss
            print("A drought has hit the region. Food supplies have diminished.")
        else:
            print("A drought has hit the region, but you don't have enough food to sustain your people.")
    elif event_chance <= 15:
        wood_loss = random.randint(5, 15)
        if resources["wood"] >= wood_loss:
            resources["wood"] -= wood_loss
            print("Harsh weather conditions have damaged our wood reserves.")
        else:
            print("Harsh weather conditions have damaged our wood reserves, but you don't have enough wood.")
    # Add more event types as desired

# Function to calculate daily resource production
def calculate_production():
    for job, count in jobs.items():
        if job == "farmers":
            resources["food"] += count * random.randint(2, 5)
        elif job == "lumberjacks":
            resources["wood"] += count * random.randint(1, 3)
        elif job == "miners":
            resources["gold"] += count * random.randint(1, 2)

# Function to build a house and increase population
def build_house():
    if resources["gold"] >= 20 and resources["wood"] >= 10:
        resources["gold"] -= 20
        resources["wood"] -= 10
        resources["population"] += 1
        print("You built a house! Population increased.")
    else:
        print("Not enough resources to build a house.")

# Function to export the game state to a JSON file
def export_game_state(filename):
    game_state = {
        "resources": resources,
        "quests": quests,
        "jobs": jobs,
        "starting_location": starting_location,
    }
    with open(filename, 'w') as file:
        json.dump(game_state, file)
    print(f"Game state exported to {filename}")

# Function to import the game state from a JSON file
def import_game_state(filename):
    global resources, quests, jobs, starting_location
    with open(filename, 'r') as file:
        game_state = json.load(file)
    resources = game_state["resources"]
    quests = game_state["quests"]
    jobs = game_state["jobs"]
    starting_location = game_state["starting_location"]
    print(f"Game state imported from {filename}")

# Function to interact with quests
def interact_with_quest():
    if quests:
        print("\nActive Quests:")
        for i, quest in enumerate(quests, start=1):
            print(f"{i}. {quest['name']} - {quest['description']}")

        quest_choice = input("Enter the number of the quest you want to complete or '0' to cancel: ")
        if quest_choice.isdigit() and 0 < int(quest_choice) <= len(quests):
            selected_quest = quests[int(quest_choice) - 1]
            resources["gold"] += selected_quest["reward"]
            print(f"Quest completed: {selected_quest['name']}")
            quests.remove(selected_quest)
        elif quest_choice == '0':
            print("Quest interaction canceled.")
        else:
            print("Invalid choice. Try again.")

# Function to interact with merchants and accept quests
def interact_with_merchant():
    print("\nAvailable Quests from Merchants:")
    for i, quest in enumerate(merchant_quests, start=1):
        print(f"{i}. {quest['name']} (Reward: {quest['reward']} gold)")

    quest_choice = input("Enter the number of the quest you want to accept or '0' to cancel: ")
    if quest_choice.isdigit() and 0 < int(quest_choice) <= len(merchant_quests):
        selected_quest = merchant_quests[int(quest_choice) - 1]
        quest_success = random.random() <= 0.98  # 98% chance of success
        if quest_success:
            resources["gold"] += selected_quest["reward"]
            print(f"Quest completed: {selected_quest['name']}")
        else:
            print(f"Quest failed: {selected_quest['name']}")
        merchant_quests.remove(selected_quest)
    elif quest_choice == '0':
        print("Quest interaction canceled.")
    else:
        print("Invalid choice. Try again.")

# Main game loop
while True:
    print(f"\n{starting_location} - Your Village:")
    for resource, amount in resources.items():
        print(f"{resource.capitalize()}: {amount}")
    print("\nJobs:")
    for job, count in jobs.items():
        print(f"{job.capitalize()}: {count}")
    print(f"\n{starting_location} - Your Village (Day {days}):")

    # Check for active quests
    if quests:
        print("\nActive Quests:")
        for i, quest in enumerate(quests, start=1):
            print(f"{i}. {quest['name']} - {quest['description']}")

    # Display storyline specific to the starting location
    if starting_location in storyline:
        print("\nStoryline:")
        for line in storyline[starting_location]:
            print(line)
    
    # Calculate daily resource production
    calculate_production()

     # Increment the number of days
    days += 1
    
    # Player input
    choice = input("\nWhat would you like to do? (collect/assign/build/quest/export/import/interact/interact_merchant/exit): ").lower()

    if choice == "collect":
        # Collect resources
        resources["gold"] += random.randint(5, 10)
        resources["food"] += random.randint(2, 5)
        resources["wood"] += random.randint(1, 3)
        print("You collected resources!")

    elif choice == "assign":
        # Assign jobs
        print("\nAvailable Jobs:")
        for job in jobs.keys():
            print(job.capitalize())
        job_choice = input("Assign a job to a villager (job/villager count): ").lower()
        job_choice = job_choice.split()
        if len(job_choice) == 2 and job_choice[0] in jobs and job_choice[1].isdigit():
            job = job_choice[0]
            count = int(job_choice[1])
            if count <= resources["population"]:
                jobs[job] += count
                resources["population"] -= count
                print(f"{count} villagers are now {job.capitalize()}s.")
            else:
                print("Not enough villagers available.")
        else:
            print("Invalid input. Try again.")

    elif choice == "build":
        # Build a house
        build_house()

    elif choice == "quest":
        # Generate a random quest
        quest_name = f"Quest {len(quests) + 1}"
        quest_description = f"Help a neigboting village with {random.choice(['bandit problem', 'crop harvest', 'escorting a villager'])}."
        quest_reward = random.randint(1, 10)
        quests.append({"name": quest_name, "description": quest_description, "reward": quest_reward})
        print(f"You accepted a new quest: {quest_name} - {quest_description}")

    elif choice == "export":
        # Export game state to a JSON file
        filename = input("Enter the filename to export the game state: ")
        export_game_state(filename)

    elif choice == "import":
        # Import game state from a JSON file
        filename = input("Enter the filename to import the game state: ")
        import_game_state(filename)

    elif choice == "interact":
        # Interact with quests
        interact_with_quest()
    

    elif choice == "interact_merchant":
        # Interact with merchants and accept quests
        interact_with_merchant()

    elif choice == "exit":
        print(f"Thanks for playing {starting_location} - Medieval Prosperity!")
        break

    else:
        print("Invalid choice. Try again.")
    
    # Check for random events
    random_event()
