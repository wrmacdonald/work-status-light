import requests
import hue_certificates

current_status = "free"

# prompt for working status
status = input("Are you 'busy' or 'free'? (enter to toggle): ")

all_commands = ["busy", "b", "free", "f", "toggle", "t", ""]
while status.lower() not in all_commands:
    status = input("I don't understand that status, please give a valid command: ")

# update status
current_status = status.lower()

busy_commands = ["busy", "b"]
free_commands = ["free", "f"]
toggle_commands = ["toggle", "t", ""]

# update light
# busy
if current_status in busy_commands:
    hue_office_red = requests.put(f"http://{hue_certificates.ip}/api/{hue_certificates.username}/lights/"
                                  f"{hue_certificates.office_light}/state", '{"on":true,"xy":[0.695,0.322]}')
    current_status = "busy"
# free
elif current_status in free_commands:
    hue_office_green = requests.put(f"http://{hue_certificates.ip}/api/{hue_certificates.username}/lights/"
                                    f"{hue_certificates.office_light}/state", '{"on":true,"xy":[0.195,0.622]}')
    current_status = "free"
# toggle
elif current_status in toggle_commands:
    hue = requests.get(f"http://{hue_certificates.ip}/api/{hue_certificates.username}/lights/"
                       f"{hue_certificates.office_light}")
    json_data = hue.json()

    # if busy, toggle to free
    if 0.68 < json_data["state"]["xy"][0] < 0.70 and 0.30 < json_data["state"]["xy"][1] < 0.33:
        hue_office_green = requests.put(f"http://{hue_certificates.ip}/api/{hue_certificates.username}/lights/"
                                        f"{hue_certificates.office_light}/state", '{"on":true,"xy":[0.195,0.622]}')
        current_status = "free"
    # if free, toggle to busy
    if 0.19 < json_data["state"]["xy"][0] < 0.20 and 0.61 < json_data["state"]["xy"][1] < 0.63:
        hue_office_red = requests.put(f"http://{hue_certificates.ip}/api/{hue_certificates.username}/lights/"
                                      f"{hue_certificates.office_light}/state", '{"on":true,"xy":[0.695,0.322]}')
        current_status = "busy"
else:
    print("something's up...")

print(f"Noted! I'll tell anyone interested you're {current_status}.")
