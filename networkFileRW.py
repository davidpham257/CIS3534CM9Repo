#!/usr/bin/env python3
#networkFileRW.py
#David Pham
#Thursday, July 3, 2025
#Read equipment from a file, write updates & errors to file

# Try to import the JSON module, catch any import errors
try:
    import json
except ImportError:
    print("Error: JSON module could not be imported.")
    exit(1)

# File constants for input and output files
EQUIP_R_FILE = "equip_r.txt"  # File with router data
EQUIP_S_FILE = "equip_s.txt"  # File with switch data
UPDATED_FILE = "updated.txt"  # File to write updated devices
INVALID_FILE = "invalid.txt"   # File to write invalid IP addresses

# Prompt constants
UPDATE = "\nWhich device would you like to update "
QUIT = "(enter x to quit)? "
NEW_IP = "What is the new IP address (111.111.111.111) "
SORRY = "Sorry, that is not a valid IP address\n"

# Function to get valid device
def getValidDevice(routers, switches):
    validDevice = False
    while not validDevice:
        # Prompt for device to update
        device = input(UPDATE + QUIT).lower()
        if device in routers.keys():
            return device
        elif device in switches.keys():
            return device
        elif device == 'x':
            return device  
        else:
            print("That device is not in the network inventory.")

# Function to get valid IP address
def getValidIP(invalidIPCount, invalidIPAddresses):
    validIP = False
    while not validIP:
        ipAddress = input(NEW_IP)
        octets = ipAddress.split('.')
        for byte in octets:
            byte = int(byte)
            if byte < 0 or byte > 255:
                invalidIPCount += 1
                invalidIPAddresses.append(ipAddress)
                print(SORRY)
                break
        else:
            return ipAddress, invalidIPCount

def main():
    # Open and read the router file
    try:
        with open(EQUIP_R_FILE, 'r') as file:
            routers = json.load(file)
    except FileNotFoundError:
        print(f"Error: {EQUIP_R_FILE} not found.")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error: {EQUIP_R_FILE} contains invalid JSON.")
        exit(1)

    # Open and read the switch file
    try:
        with open(EQUIP_S_FILE, 'r') as file:
            switches = json.load(file)
    except FileNotFoundError:
        print(f"Error: {EQUIP_S_FILE} not found.")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error: {EQUIP_S_FILE} contains invalid JSON.")
        exit(1)

    # The updated dictionary holds the device name and new ip address
    updated = {}

    # List of bad addresses entered by the user
    invalidIPAddresses = []

    # Accumulator variables
    devicesUpdatedCount = 0
    invalidIPCount = 0

    # Flags and sentinels
    quitNow = False

    # Display the network inventory
    print("Network Equipment Inventory\n")
    print("\tequipment name\tIP address")
    for router, ipa in routers.items(): 
        print("\t" + router + "\t\t" + ipa)
    for switch, ipa in switches.items():
        print("\t" + switch + "\t\t" + ipa)

    while not quitNow:
        # Function call to get valid device
        device = getValidDevice(routers, switches)
        
        if device == 'x':
            quitNow = True
            break
        
        # Function call to get valid IP address
        ipAddress, invalidIPCount = getValidIP(invalidIPCount, invalidIPAddresses)
  
        # Update device
        if 'r' in device:
            routers[device] = ipAddress 
        else:
            switches[device] = ipAddress

        devicesUpdatedCount += 1
        # Add the device and ipAddress to the updated dictionary
        updated[device] = ipAddress

        print(device, "was updated; the new IP address is", ipAddress)

    # User finished updating devices
    print("\nSummary:")
    print()
    print("Number of devices updated:", devicesUpdatedCount)

    # Write the updated dictionary to updated.txt
    try:
        with open(UPDATED_FILE, 'w') as file:
            json.dump(updated, file)
        print("Updated equipment written to file 'updated.txt'")
    except IOError:
        print(f"Error: Could not write to {UPDATED_FILE}.")

    print()
    print("\nNumber of invalid addresses attempted:", invalidIPCount)

    # Write the invalid IP addresses to errors.txt
    try:
        with open(INVALID_FILE, 'w') as file:
            json.dump(invalidIPAddresses, file)
        print("List of invalid addresses written to file 'invalid.txt'")
    except IOError:
        print(f"Error: Could not write to {INVALID_FILE}.")

# Top-level scope check
if __name__ == "__main__":
    main()