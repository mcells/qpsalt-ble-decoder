# Plot and print the register values. 
# If you log the raw data into a database (eg. Influx via OH) and export it in Grafana, you get a compatible .csv file.

import csv
import matplotlib.pyplot as plt

def parse_packet(packet):
    # Split the packet into individual components
    components = packet.split(" ")
    # Extract the register/data IDs and their corresponding values
    registers = []
    values = []

    i = 3
    while i < len(components):
        component = components[i]
        if component == "00" or component == "":
            # Skip start of packet indicator
            i += 1
        else:
            register_id = int(component, 16)
            value_length = int(components[i+1], 16)
            value_data = components[i+2:i+2+value_length]
            
            registers.append(register_id)
            values.append(value_data)

            i += (2 + value_length)

    return registers, values

def get_time_value_list(register_id, interpretation='hex'):
    time_value_list = []

    for entry in registers_values_timestamps:
        registers = entry[0]
        values = entry[1]
        timestamp = entry[2]

        if register_id in registers:
            value_index = registers.index(register_id)
            value_data_bytes = values[value_index]

            # Interpretation based on specified option
            if interpretation == 'char':
                value_interpreted = ''.join([chr(int(byte, 16)) for byte in value_data_bytes])
            elif interpretation == 'int':
                value_interpreted = int(''.join(value_data_bytes), 16)
            elif interpretation == 'hex':
                value_interpreted = ' '.join(value_data_bytes)
            
            time_value_list.append((timestamp, value_interpreted))

    return time_value_list

def plot_time_value_data(time_value_list):
    timestamps = [pair[0] for pair in time_value_list]
    values = [pair[1] for pair in time_value_list]

    plt.plot(timestamps, values)
    plt.xlabel('Timestamp')
    plt.ylabel('Value')
    plt.title('Time-Value Data')

    # Display the plot
    plt.show()

def plot_multiple_registers(register_data_dict):
    # Iterate over each register data in the dictionary
    for register_id, time_value_list in register_data_dict.items():
        timestamps = [pair[0] for pair in time_value_list]
        values = [pair[1] for pair in time_value_list]

        plt.plot(timestamps, values, label=f"Register {register_id}")

    plt.xlabel('Timestamp')
    plt.ylabel('Value')
    plt.title('Time-Value Data Comparison')

    # Display a legend showing which line corresponds to which register
    plt.legend()

    # Display the plot
    plt.show()

def plot_multiple_register_ids(register_ids, separate_subplots=True, interpretation='hex'):
    if separate_subplots:
        num_plots = len(register_ids)
        fig, axs = plt.subplots(num_plots, 1, figsize=(8, 6*num_plots))

        for i, register_id in enumerate(register_ids):
            time_value_list = get_time_value_list(register_id, interpretation)
            timestamps = [pair[0] for pair in time_value_list]
            values = [pair[1] for pair in time_value_list]

            ax = axs[i]
            ax.plot(timestamps, values)
            ax.set_xlabel('Timestamp')
            ax.set_ylabel('Value')
            ax.set_title(f'Register {register_id} - Time-Value Data')

        # Adjust spacing between subplots
        fig.tight_layout()

    else:
        fig, ax = plt.subplots(figsize=(8, 6))

        for register_id in register_ids:
            time_value_list = get_time_value_list(register_id, interpretation)
            
            timestamps = [pair[0] for pair in time_value_list]
            values = [pair[1] for pair in time_value_list]

            ax.plot(timestamps, values,label=f"Register {register_id}")

        # Set labels and title
        ax.set_xlabel('Timestamp')
        ax.set_ylabel('Value')
        ax.set_title('Time-Value Data Comparison')

        # Display a legend showing which line corresponds to which register
        ax.legend()

    # Display the plot(s) outside of the conditional statement
    plt.show()

#### End of Functions ####

# Read the CSV file containing the logged packets with timestamps
filename = "data.csv"

registers_values_timestamps = []

with open(filename, 'r', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    
    for row in reader:
        timestamp_str = row["\"Time\""]
        packet_str= row["\"value\""]

        timestamp=int(timestamp_str)

        registers, values=parse_packet(packet_str)

        registers_values_timestamps.append((registers,values,timestamp))

# Print the parsed data for each entry in a readable format 
register_set = set()       
for entry in registers_values_timestamps:
     #print(f"Timestamp: {entry[2]}")
     for reg,value in zip(entry[0],entry[1]):
         #print(f"Register ID: {reg}, Value: {' '.join(value)}")
         register_set.add(reg)
#print(sorted(register_set))
for register in register_set:
    register_id_to_search = register
    valueSet = set
    time_value_pairs = get_time_value_list(register_id_to_search, "int")

    for pair in time_value_pairs:
        valueSet.add(pair[1])
        # print(f"Timestamp: {pair[0]}, Value: {pair[1]}")
    print(f"Register: {'{:02X}'.format(int(register))}, Values: {valueSet}")
#plot_time_value_data(time_value_pairs)

registers_to_plot = [0x0c, 0x93]

plot_multiple_register_ids(registers_to_plot, False, "int")
