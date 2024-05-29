import random

def simulate_room(start_value, num_generators, room_time):
    byte_value = start_value
    for _ in range(room_time):
        for _ in range(num_generators):
            increment = random.randint(0, 5)
            byte_value = (byte_value + increment) % 256
    return byte_value

def calculate_probabilities(start_value, room_times, num_generators_list, num_simulations=25000):
    end_values_count = {104: 0, 254: 0, 255: 0}

    for _ in range(num_simulations):
        byte_value = start_value
        for num_generators, room_time in zip(num_generators_list, room_times):
            byte_value = simulate_room(byte_value, num_generators, room_time)
        
        if byte_value in end_values_count:
            end_values_count[byte_value] += 1

    total_simulations = num_simulations
    probabilities = {value: (count / total_simulations) * 100 for value, count in end_values_count.items()}
    total_probability = sum(probabilities.values())
    return probabilities, total_probability

# Example values
start_value = 100
room_times = [40, 30, 30]  # Times for each room
num_generators_list = [7, 8, 7]  # Number of generators per room

probabilities, total_probability = calculate_probabilities(start_value, room_times, num_generators_list)

# Descriptions for each byte value
descriptions = {
    104: "bucket softlock",
    254: "first spinner softlock",
    255: "second spinner softlock"
}

# Print probabilities with descriptions
print("Probabilities for each byte value:")
print("{:<26} {:<10}".format("Description", "Chance(%)"))
print("-" * 35)
for value, probability in probabilities.items():
    description = descriptions.get(value, "Unknown")
    print("{:<29} {:<1.2f}%".format(description, probability))
print("-" * 35)
print("{:<29} {:<1.2f}%".format("Total probability", total_probability))
