from pathlib import Path

# import upgrade gui
import idle_gui1

# Non-Tkinter
import sys
import threading

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import tkinter as tk

# Initial resource amounts
resources = {
    "wood": 0,
    "stone": 0,
    "gold": 0
}

# Base generation rates for each resource
base_rate = {
    "wood": 1,
    "stone": 0,
    "gold": 0
}

# Current generation rates (may be upgraded)
rate = {
    "wood": base_rate["wood"],
    "stone": base_rate["stone"],
    "gold": base_rate["gold"]
}

report_rate = {
    "wood": 0,
    "stone": 0,
    "gold": 0
}

#sell rates
sell = {
    "wood": {"price": 1},
    "stone": {"price": 5},
    "gold": {"price": 10}
}

tiers = {
    "tier": {"level": 0, "cost": 250}
}

tool_upgrades = {
    "axe": {"level": 0, "cost": 100},
    "drill": {"level": 0, "cost": 500},
    "detector": {"level": 0, "cost": 1000}
}

# Upgrade information: current level and current upgrade cost for each resource
upgrades = {
    "wood": {"level": 0, "cost": 10},
    "stone": {"level": 0, "cost": 25},
    "gold": {"level": 0, "cost": 50}
}

OUTPUT_PATH = Path(__file__).parent

ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")

#UI
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def tool_upgrade_gui():
    def get_number_of_toplevel_windows():
        tops = [] # Empty list for appending each toplevel
        for widget in window.winfo_children(): # Looping through widgets in main window
            if '!toplevel' in str(widget): # If toplevel exists in the item
                tops.append(widget) # Append it to the list
        if(len(tops) < 1):
            idle_gui1.main(tool_upgrades, callback_one = upgrade_axe, callback_two = upgrade_drill, callback_three = upgrade_detector, parent=window)

    get_number_of_toplevel_windows()
    return

def upgrade_axe():
    upgrade_tool("wood", money, "axe")

def upgrade_drill():
    upgrade_tool("stone", money, "drill")

def upgrade_detector():
    upgrade_tool("gold", money, "detector")    


def clear_last_command(*args):
    entry_1.delete(0, 500)

def fill_last_command(*args):
    entry_1.delete(0, 500)
    entry_1.insert(0, command_mem[0])
    return

def interact_user_input(*args):
    user_input = entry_1.get()
    print(user_input)
    command_mem[0] = user_input
    entry_1.delete(0, 500)
    run_command(user_input, money)
    return

#transfers vars to ui
def update_data():
    #resource display
    canvas.itemconfig(wood_value_txt, text="Wood:\n{:.2f}".format(resources["wood"]))
    canvas.itemconfig(stone_value_txt, text="Stone:\n{:.2f}".format(resources["stone"]))
    canvas.itemconfig(gold_value_txt, text="Gold:\n{:.2f}".format(resources["gold"]))
    #tier display
    canvas.itemconfig(wood_gen_tier_txt, text=str(upgrades["wood"]["level"]))
    canvas.itemconfig(stone_gen_tier_txt, text=str(upgrades["stone"]["level"]))
    canvas.itemconfig(gold_gen_tier_txt, text=str(upgrades["gold"]["level"]))
    #balance display
    canvas.itemconfig(balance_text, text="$" + str(money[0]))
    #requirement text display
    canvas.itemconfig(req_body_txt, text=create_req_text())
    #tier lvl txt
    canvas.itemconfig(res_tier_txt, text=str(tiers["tier"]["level"]))

#program output to player bridge
def sendResponseText(output):
    if(len(output) > 1):
        output = "".join(output)
    canvas.itemconfig(response, text=output)
    return

def upgrade_tool(resource, money, tool):
    current_cost = tool_upgrades[tool]["cost"]
    if money[0] < current_cost:
        sendResponseText(f"Not enough money to upgrade.\nNeed ${current_cost}, but have ${money[0]}.")
        return

    # Deduct the cost and upgrade the resource generator
    money[0] -= current_cost
    tool_upgrades[tool]["level"] += 1
    # Increase rate: each level adds 50% to current base rate
    base_rate[resource] = base_rate[resource] * 1.5
    # Double the upgrade cost for next upgrade
    tool_upgrades[tool]["cost"] *= 2

    sendResponseText("Upgraded {} to LVL {}".format(tool, tool_upgrades[tool]["level"]))

#Backend
def generate():
    #Update each resource based on its current rate.
    #This function is called repeatedly on a timer.
    def tool_key_converter(tool_key):
        if(tool_key == "wood"):
            return "axe"
        elif(tool_key == "stone"):
            return "drill"
        elif(tool_key == "gold"):
            return "detector"

    #upgrade rate + 50% for each tool upgrade
    for resource in resources:
        resources[resource] += rate[resource] * ((tool_upgrades[tool_key_converter(resource)]["level"]) * 1.5 + 1)
        report_rate[resource] = rate[resource] * ((tool_upgrades[tool_key_converter(resource)]["level"]) * 1.5 + 1)
    #print("\nResources Updated:", resources)

def upgrade_tier(money):
    current_cost = tiers["tier"]["cost"]

    if(tiers["tier"]["level"] >= 2):
        sendResponseText("Max Tier Reached, cannot upgrade further")
        return money

    if money[0] < current_cost:
        sendResponseText(f"Not enough money to upgrade. Need ${current_cost}, but have ${money}.")
        return money

    # Deduct the cost and upgrade tier
    money[0] -= current_cost
    tiers["tier"]["level"] += 1
    # Increase rate: each level tiers base rate on specified resource
    if(tiers["tier"]["level"] == 1):
        resource = "stone"
    elif(tiers["tier"]["level"] == 2):
        resource = "gold"
    else:
        return money

    base_rate[resource] += 1
    rate[resource] = base_rate[resource]
    #increase tier price
    tiers["tier"]["cost"] *= 2

    sendResponseText(f"Unlocked: {resource.capitalize()}")
    return money

def upgrade_resource(resource, output):
    #Attempt to upgrade the generation rate of the given resource.
    #If the player has enough of that resource to pay the upgrade cost, the resource is spent,
    #the upgrade level is incremented, and the generation rate increases by 50% of the base rate.
    #The upgrade cost then doubles for that resource.

    if resource not in resources:
        sendResponseText(f"Unknown resource: {resource}")
        return

    current_cost = upgrades[resource]["cost"]
    if resources[resource] < current_cost:
        sendResponseText(f"Not enough {resource} to upgrade. Need {current_cost} {resource}, but have {resources[resource]}.")
        return

    # Deduct the cost and upgrade the resource generator
    resources[resource] -= current_cost
    upgrades[resource]["level"] += 1
    # Increase rate: each level adds 20% of the current rate
    rate[resource] = rate[resource] * 1.2
    # Double the upgrade cost for next upgrade
    upgrades[resource]["cost"] *= 2

    output.append(f"Upgraded {resource} generator\n")
    output.append(f"New Level {upgrades[resource]['level']}\n")
    output.append(f"New generation rate: {rate[resource]:.2f} per cycle\n")
    output.append(f"Next upgrade cost for {resource}: {upgrades[resource]['cost']} {resource}")
    sendResponseText(output)

def run_on_timer(interval, function):
    #Run the provided function every 'interval' seconds using a daemon Timer.
    def execute():
        function()  # Execute the provided function (e.g., generate)
        # Schedule the next execution
        t = threading.Timer(interval, execute)
        t.daemon = True  # Mark timer as daemon so it doesn't block exit
        t.start()
    
    t = threading.Timer(interval, execute)
    t.daemon = True  # Ensure the timer thread is a daemon
    t.start()

def sell_resource(resource, sellqty, output):
    if resource not in resources:
        sendResponseText(f"Unknown resource: {resource}")
        return money

    if resources[resource] < sellqty:
        sendResponseText(f"Not enough {resource} to sell. Need {sellqty} {resource}, but have {resources[resource]}.")
        return money

    # Deduct the resource
    resources[resource] -= sellqty
    moneyAdded = sell[resource]["price"] * sellqty
    money[0] += sell[resource]["price"] * sellqty

    output.append(f"Sold {sellqty} {resource} for ${moneyAdded}.\n")
    output.append(f"New Money Balance: ${money[0]}")
    sendResponseText(output)

    return money

def create_req_text():
    #Print current status of resources and upgrades.
    requirements = []
    
    requirements.append("Upgrades:")
    for resource in upgrades:
        #level = upgrades[resource]["level"]
        cost = upgrades[resource]["cost"]
        requirements.append(f"  {resource.capitalize()} Generator, Next Upgrade Cost: {cost} {resource} gens")
    
    requirements.append("Generation Rates (per cycle):")
    for resource in resources:
        requirements.append(f"  {resource.capitalize()}: {report_rate[resource]:.2f}")
    
    tierCost = tiers["tier"]["cost"]
    requirements.append(f"Next Resource Tier Cost: ${tierCost}")

    return '\n'.join(requirements)

money = [0]
command_mem = [""]
# Start resource generation every second
interval = 1
run_on_timer(interval, generate)
run_on_timer(interval, update_data)

#print("Cobra's PYdle Game Started!\nCommands: 'status' or 's', 'sell <resource> <amount>', 'upgrade <resource>/<tier>', 'help', 'quit'.")
def run_command(command, money):
    output = []
    command = command.strip().lower()
    parts = command.split()
    if command == "quit":
        sendResponseText("Quitting the game. Goodbye!")
        sys.exit()
    elif command.startswith("sell"):
        if len(parts) != 3:
            sendResponseText("Usage: sell <resource> <qty>")
            return
        else:
            resource = parts[1]
        if(parts[2] == "all"):
            sell_resource(resource, int(resources[resource]), output)
        elif(int(parts[2]) > 0):
            sell_resource(resource, int(parts[2]), output)
        else:
            sendResponseText("Usage: sell <resource> <qty>")
            return
    elif command.startswith("upgrade"):
        if len(parts) != 2:
            sendResponseText("Usage: upgrade <resource>\nupgrade tier")
            return
        else:
            resource = parts[1]
            if(resource == "tier"):
                money = upgrade_tier(money)
            else:
                upgrade_resource(resource, output)
    elif command.startswith("help"):
        sendResponseText("Available commands:\n'upgrade <resource>'\n'upgrade tier'\n'sell <resource> <amount>'\n'help'\n'quit'")
        return 
    else:
        sendResponseText("Unknown command.\nAvailable commands:\n'upgrade <resource>'\n'upgrade tier'\n'sell <resource> <amount>'\n'help'\n'quit'")
        return

window = Tk()

window.geometry("750x550")
window.configure(bg = "#1B1B1B")
window.title("Cobra's PYIdle Game")

#main canvas
canvas = Canvas(
    window,
    bg = "#1B1B1B",
    height = 550,
    width = 750,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    750.0,
    55.0,
    fill="#414141",
    outline="")

#title text
canvas.create_text(
    148.0,
    7.0,
    anchor="nw",
    text="Cobra's PYdle Game",
    fill="#000000",
    font=("JejuHallasan", 48 * -1)
)

canvas.create_rectangle(
    41.0,
    85.0,
    318.0,
    145.0,
    fill="#4C4C4C",
    outline="")

#balance title
canvas.create_text(
    54.0,
    93.0,
    anchor="nw",
    text="Balance",
    fill="#FFFFFF",
    font=("JejuHallasan", 20 * -1)
)

#balance value
balance_text = canvas.create_text(
    53.0,
    114.0,
    anchor="nw",
    text="$0",
    fill="#FFFFFF",
    font=("JejuHallasan", 32 * -1)
)

canvas.create_rectangle(
    423.0,
    85.0,
    700.0,
    145.0,
    fill="#4C4C4C",
    outline="")

#Resource Tier Title
canvas.create_text(
    436.0,
    93.0,
    anchor="nw",
    text="Resource Tier",
    fill="#FFFFFF",
    font=("JejuHallasan", 20 * -1)
)

#Resource Tier Value
res_tier_txt = canvas.create_text(
    435.0,
    114.0,
    anchor="nw",
    text="0",
    fill="#FFFFFF",
    font=("JejuHallasan", 32 * -1)
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    130.0,
    203.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    364.0,
    228.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    605.0,
    227.0,
    image=image_image_3
)

#wood value text
wood_value_txt = canvas.create_text(
    89.0,
    297.0,
    anchor="nw",
    text="Wood:\n0",
    fill="#FFFFFF",
    font=("JejuHallasan", 20 * -1)
)

#stone value text
stone_value_txt = canvas.create_text(
    333.0,
    301.0,
    anchor="nw",
    text="Stone:\n0",
    fill="#FFFFFF",
    font=("JejuHallasan", 20 * -1)
)

#gold value text
gold_value_txt = canvas.create_text(
    577.0,
    304.0,
    anchor="nw",
    text="Gold:\n0",
    fill="#FFFFFF",
    font=("JejuHallasan", 20 * -1)
)

#Gen Lvl Title
canvas.create_text(
    4.0,
    159.0,
    anchor="nw",
    text="Gen Lvl",
    fill="#FFFFFF",
    font=("JejuHallasan", 20 * -1)
)

#wood gen tier text
wood_gen_tier_txt = canvas.create_text(
    171.0,
    160.0,
    anchor="nw",
    text="0",
    fill="#FFFFFF",
    font=("JejuHallasan", 20 * -1)
)

#stone gen tier text
stone_gen_tier_txt = canvas.create_text(
    416.0,
    160.0,
    anchor="nw",
    text="0",
    fill="#FFFFFF",
    font=("JejuHallasan", 20 * -1)
)

#gold gen tier text
gold_gen_tier_txt = canvas.create_text(
    660.0,
    160.0,
    anchor="nw",
    text="0",
    fill="#FFFFFF",
    font=("JejuHallasan", 20 * -1)
)

canvas.create_rectangle(
    375.0,
    365.0,
    741.0,
    541.0,
    fill="#343434",
    outline="")

#Upgrade Tools Menu
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=tool_upgrade_gui,
    relief="flat"
)
button_1.place(
    x=714.0,
    y=16.0,
    width=24.0,
    height=24.0
)

canvas.create_rectangle(
    5.0,
    365.0,
    371.0,
    499.0,
    fill="#232323",
    outline="")

#requirements title
canvas.create_text(
    445.0,
    367.0,
    anchor="nw",
    text="Upgrade Requirements",
    fill="#FFFFFF",
    font=("JejuHallasan", 20 * -1)
)

#requirements text
req_body_txt = canvas.create_text(
    380.0,
    400.0,
    anchor="nw",
    text="Reqs",
    fill="#FFFFFF",
    font=("JejuHallasan", 14 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    156.5,
    524.5,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=10.0,
    y=508.0,
    width=293.0,
    height=31.0
)

response = canvas.create_text(
    18.0,
    374.0,
    anchor="nw",
    text="Program Response",
    fill="#FFFFFF",
    font=("JejuHallasan", 14 * -1)
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=interact_user_input,
    relief="flat"
)
button_2.place(
    x=312.0,
    y=508.0,
    width=59.0,
    height=27.0
)

#keybinding enter, up, and down
entry_1.bind("<Return>", interact_user_input)
entry_1.bind("<Up>", fill_last_command)
entry_1.bind("<Down>", clear_last_command)

window.resizable(False, False)
window.mainloop()