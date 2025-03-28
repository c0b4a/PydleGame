# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer

def main(tool_upgrades, callback_one, callback_two, callback_three, parent):
    from pathlib import Path
    import threading

    # from tkinter import *
    # Explicit imports to satisfy Flake8
    from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel

    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame1")

    def update_data():
        canvas.itemconfig(cost_1_txt, text="Cost: ${}".format(tool_upgrades["axe"]["cost"]))
        canvas.itemconfig(cost_2_txt, text="Cost: ${}".format(tool_upgrades["drill"]["cost"]))
        canvas.itemconfig(cost_3_txt, text="Cost: ${}".format(tool_upgrades["detector"]["cost"]))
        canvas.itemconfig(level_1_txt, text="LVL: {}".format(tool_upgrades["axe"]["level"]))
        canvas.itemconfig(level_2_txt, text="LVL: {}".format(tool_upgrades["drill"]["level"]))
        canvas.itemconfig(level_3_txt, text="LVL: {}".format(tool_upgrades["detector"]["level"]))

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

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

    #for timer
    interval = 1
    run_on_timer(interval, update_data)

    window = Toplevel()

    window.geometry("400x500")
    window.configure(bg = "#FFFFFF")

    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 500,
        width = 400,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(
        0.0,
        0.0,
        400.0,
        500.0,
        fill="#3C3C3C",
        outline="")

    canvas.create_rectangle(
        0.0,
        0.0,
        400.0,
        60.0,
        fill="#252525",
        outline="")

    #title
    canvas.create_text(
        11.0,
        14.0,
        anchor="nw",
        text="Production Upgrades",
        fill="#FFFFFF",
        font=("JejuHallasan", 32 * -1)
    )

    #image 1
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        103.0,
        135.0,
        image=image_image_1
    )

    #image 2
    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        94.0,
        264.0,
        image=image_image_2
    )

    #image 3
    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        92.0,
        411.0,
        image=image_image_3
    )

    #shinier axes
    canvas.create_text(
        200.0,
        72.0,
        anchor="nw",
        text="Shinier Axes",
        fill="#FFFFFF",
        font=("JejuHallasan", 24 * -1)
    )

    #stonger drills
    canvas.create_text(
        200.0,
        209.0,
        anchor="nw",
        text="Stronger Drills",
        fill="#FFFFFF",
        font=("JejuHallasan", 24 * -1)
    )

    #metal detector
    canvas.create_text(
        200.0,
        348.0,
        anchor="nw",
        text="Metal Detector",
        fill="#FFFFFF",
        font=("JejuHallasan", 24 * -1)
    )

    #button 1
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        master = canvas,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=callback_one,
        relief="flat"
    )
    button_1.place(
        x=205.0,
        y=133.0,
        width=145.0,
        height=47.0
    )

    #button 2
    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        master = canvas,
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=callback_two,
        relief="flat"
    )
    button_2.place(
        x=205.0,
        y=266.0,
        width=145.0,
        height=47.0
    )

    #button 3
    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        master = canvas,
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=callback_three,
        relief="flat"
    )
    button_3.place(
        x=205.0,
        y=406.0,
        width=145.0,
        height=47.0
    )

    #cost 1
    cost_1_txt = canvas.create_text(
        200.0,
        102.0,
        anchor="nw",
        text="cost: 0",
        fill="#FFFFFF",
        font=("JejuHallasan", 20 * -1)
    )
    #cost 2
    cost_2_txt = canvas.create_text(
        207.0,
        237.0,
        anchor="nw",
        text="cost: 0",
        fill="#FFFFFF",
        font=("JejuHallasan", 20 * -1)
    )
    #cost 3
    cost_3_txt = canvas.create_text(
        207.0,
        371.0,
        anchor="nw",
        text="cost: 0",
        fill="#FFFFFF",
        font=("JejuHallasan", 20 * -1)
    )

    #lvl label axe
    level_1_txt = canvas.create_text(
    61.0,
    60.0,
    anchor="nw",
    text="LVL: 0",
    fill="#FFFFFF",
    font=("JejuHallasan", 20 * -1)
    )
    #lvl label drill
    level_2_txt = canvas.create_text(
        68.0,
        195.0,
        anchor="nw",
        text="LVL: 0",
        fill="#FFFFFF",
        font=("JejuHallasan", 20 * -1)
    )
    #lvl label detector
    level_3_txt = canvas.create_text(
        68.0,
        329.0,
        anchor="nw",
        text="LVL: 0",
        fill="#FFFFFF",
        font=("JejuHallasan", 20 * -1)
    )

    #Exit Button
    button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
    button_4 = Button(
        master = canvas,
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda:window.destroy(),
        relief="flat"
    )
    button_4.place(
        x=351.0,
        y=13.0,
        width=34.0,
        height=34.0
    )

    window.resizable(False, False)
    window.mainloop()