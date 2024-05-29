import random
import matplotlib.pyplot as plt

bad_values = [220, 254, 255]

def simulate_room(start_value, num_generators, room_time):
    byte_value = start_value    
    for _ in range(num_generators):
        time_left = room_time    
        timer = random.uniform(0, 5)  # Generate a random float between 0 and 5
        while time_left - timer > 0:
            byte_value = (byte_value + 1) % 256
            time_left -= timer
            timer = random.uniform(0, 5)
    return byte_value

def calculate_probabilities(start_value, room_times, num_generators_list, num_simulations=25000):
    end_values_count = {i: 0 for i in range(256)}  # Initialize counts for all byte values

    for _ in range(num_simulations):
        byte_value = start_value
        for num_generators, room_time in zip(num_generators_list, room_times):
            byte_value = simulate_room(byte_value, num_generators, room_time)
        
        end_values_count[int(byte_value)] += 1  # Convert float byte_value to integer

    probabilities = {value: (count / num_simulations) * 100 for value, count in end_values_count.items()}
    total_probability = sum(probabilities.get(k, 0) for k in bad_values)
    return end_values_count, probabilities, total_probability

# Example values
start_value = 71
room_times = [18.16, 50.68, 80.27]  # Times for each room
num_generators_list = [8, 5, 6]  # Number of generators per room


end_values_count, probabilities, total_probability = calculate_probabilities(start_value, room_times, num_generators_list)

# Descriptions for each byte value
descriptions = {
    220: "bucket softlock",
    254: "first spinner softlock",
    255: "second spinner softlock"
}

# Print probabilities with descriptions
print("Probabilities for each byte value:")
print("{:<26} {:<10}".format("Description", "Chance(%)"))
print("-" * 35)
for value in bad_values:
    description = descriptions.get(value, "Unknown")
    probability = probabilities[value]
    print("{:<29} {:<1.2f}%".format(description, probability))
print("-" * 35)
print("{:<29} {:<1.2f}%".format("Total probability", total_probability))

# Plotting the distribution of the byte values
values = list(probabilities.keys())
percentages = list(probabilities.values())

colors = ['red' if 220 <= value <= 250 else 'blue' for value in values]

plt.bar(values, percentages, color=colors, width=1.2)
plt.xlabel('Byte Value')
plt.ylabel('Percentage (%)')
plt.title('Distribution of Byte Values After Simulations')
plt.show()
