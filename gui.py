""" control gui prototype """
import time
import json
from tkinter import *
from tkinter import messagebox as mb

from gui_serial import serial_write, import_module
from gui_db import Record

SIMULATION = False

record = Record() # Last reading from VMM chip to be written into database

root = Tk()
root.geometry("1250x900")
root.title("VMM GUI")
# root.iconbitmap('icon.ico')

# Message field on the top
top_message_text = "Please connect HDMI cable to hybrid J2"

if SIMULATION:
    import simulation
    top_message_text = "SIMULATION"

message = Label(root, text=top_message_text, bd=1, relief=SUNKEN)
message.config(font=("Courier", 18))
message.pack(side=TOP, fill=X, ipady=10)

# Column 1 | 3 big red buttons

def col1Button1(event):
    print("Clicked Start J2 Connection")

    # Change button collor
    oval = connCanvas.find_withtag("Button1")
    connCanvas.itemconfig(oval, fill="#ffc588")
    connCanvas.update()

    # New record to be written into database
    global record
    record = Record()

    # Call microcontroller

    # Power and I2C (P1, P2, chip id, chip addr, eeprom, ...)
    if SIMULATION:
        output = simulation.p1p2id
    else:
        import_module("vmm_p1p2id")
        output = serial_write("vmm_p1p2id.readout()", timeout=15)

    print(output)

    try:
        power_i2c = json.loads(output[0])

        # Power
        powerLabelP1["text"] = "P1 = {} A".format(power_i2c.get("p1", "?"))
        powerLabelP1a["text"] = "P1a = {} V".format(power_i2c.get("p1a", "?"))
        powerLabelP1b["text"] = "P1b = {} V".format(power_i2c.get("p1b", "?"))

        powerLabelP2["text"] = "P2 = {} A".format(power_i2c.get("p2", "?"))
        powerLabelP2a["text"] = "P2a = {} V".format(power_i2c.get("p2a", "?"))
        powerLabelP2b["text"] = "P2b = {} V".format(power_i2c.get("p2b", "?"))

        powerLabelP2VMM["text"] = "P2 VMM = {} V".format(power_i2c.get("p2vmm", "?"))

        # I2C
        i2cLabel1["text"] = "IC chip found"
        i2cLabel2["text"] = "Chip ID \n{}".format(power_i2c.get("chip_id", "?"))
        i2cLabel3["text"] = "EEprom [{}]".format(power_i2c.get("eeprom", "?"))
        i2cLabel4["text"] = "Chip number [{}]".format(power_i2c.get("chip_number", "?"))
        i2cLabel5["text"] = "Chip found [{}]".format(power_i2c.get("chip_address", "?"))
        i2cLabel6["text"] = "uADC1 [{}]".format(power_i2c.get("uadc1", "?"))
        i2cLabel7["text"] = "uAD21 [{}]".format(power_i2c.get("uadc2", "?"))

        # Fill Record object with data of current reading from VMM
        record.fill_data(power_i2c)
    except Exception as e:
        print("Problem parsing p1p2 output")

    mux = {}

    # MUX 1
    try:
        if SIMULATION:
            output = simulation.mux1
        else:
            import_module("vmm_mux1")
            output = serial_write("vmm_mux1.readout()", timeout=5)

        print(output)
        mux1 = json.loads(output[0])

        # Fill Record object with data of current reading from VMM
        record.fill_data(mux1)

        mux.update(mux1)
    except:
        print("Problem parsing mux1 output")

    #  MUX3
    try:
        if SIMULATION:
            output = simulation.mux3
        else:
            import_module("vmm_mux3")
            output = serial_write("vmm_mux3.readout()", timeout=5)

        print(output)
        mux3 = json.loads(output[0])

        # Fill Record object with data of current reading from VMM
        record.fill_data(mux3)

        mux.update(mux3)
    except:
        print("Problem parsing mux3 output")

    # Update J2 Pin values and add structured output to Measurement Field

    rows = []

    # Thresholds for Pin values
    j2thresholds = {
        "aux": lambda x: x > 1000,
        "pin1": lambda x: x > 1,

        "pin3": lambda x: x > 1,
        "pin4": lambda x: x > 100,
        "pin5": lambda x: x < 5,
        "pin6": lambda x: x > 100,
        "pin7": lambda x: x > 1,

        "pin9": lambda x: x > 100,
        "pin10": lambda x: x > 1,
        "pin11": lambda x: x < 5,
        "pin12": lambda x: x > 1,
        "pin13": lambda x: x > 1,
        "pin14": lambda x: x > 1,


        "pin17": lambda x: x < 5,
        "pin18": lambda x: x > 1,
        "pin19": lambda x: x > 1
    }

    def natural_sort(kv):
        """ Sort dictionary items naturally"""
        convert = lambda text: int(text) if text.isdigit() else text.lower()
        return [convert(c) for c in re.split('([0-9]+)', kv[0])]

    for key, values in sorted(mux.items(), key=natural_sort):
        # key is "pin1", "pin2", "aux", "pin19". ...
        # values is a dict containing U, R and Runits

        # Create list of lines for Measurement Field
        rows.append("{:9s}\t{:5.2f} V\t{:5.2f} {:4s}".format(key, values["U"], values["R"], values["Runits"]))

        # Find Pin to update
        if key in j2pins:

            # Find function which tells if Pin is OK or Error
            func = j2thresholds.get(key, lambda x: False)

            # Check if Pin is OK or Error
            ok = func(values["R"])

            if ok:
                j2pins[key]["text"] = "{key} OK".format(key=key.capitalize())
                j2pins[key]["bg"] = "#dfffd4"
            else:
                j2pins[key]["text"] = "{key} Error".format(key=key.capitalize())
                j2pins[key]["bg"] = "#ffc588"

    textArea["text"] = "\n".join(rows)

    # Change button collor back
    connCanvas.itemconfig(oval, fill="#ff8a88")
    connCanvas.update()

def col1Button2(event):
    print("Clicked Start J3 Connection")

    # Change button collor
    oval = connCanvas.find_withtag("Button2")
    connCanvas.itemconfig(oval, fill="#ffc588")
    connCanvas.update()

    # Call microcontroller
    time.sleep(0.1) # delete me


    # Change button collor back
    connCanvas.itemconfig(oval, fill="#ff8a88")
    connCanvas.update()

def col1Button3(event):
    print("Clicked Print Label")

    # Change button collor
    oval = connCanvas.find_withtag("Button3")
    connCanvas.itemconfig(oval, fill="#ffc588")
    connCanvas.update()

    # Call microcontroller
    time.sleep(0.1) # delete me

    # Change button collor back
    connCanvas.itemconfig(oval, fill="#ff8a88")
    connCanvas.update()

colFrame1 = Frame(root, height=750, width=150)
colFrame1.pack(side=LEFT, anchor=N, padx=10)

connCanvas = Canvas(colFrame1, height=750, width=150)
connCanvas.pack()

connY1 = 30

col1Button1Oval = connCanvas.create_oval(30, connY1, 130, connY1+100, fill="#ff8a88", outline="#ff3f3c", width=2, tag="Button1")
col1Button1Text = connCanvas.create_text(80, connY1+50, text=" START J2\nconnection")
connCanvas.tag_bind(col1Button1Oval, "<Button-1>", col1Button1)
connCanvas.tag_bind(col1Button1Text, "<Button-1>", col1Button1)

connY2 = 180
col1Button2Oval = connCanvas.create_oval(30, connY2, 130, connY2+100, fill="#ababab", outline="#919191", width=2, tag="Button2")
col1Button2Text = connCanvas.create_text(80, connY2+50, text=" START J3\nconnection")
connCanvas.tag_bind(col1Button2Oval, "<Button-1>", col1Button2)
connCanvas.tag_bind(col1Button2Text, "<Button-1>", col1Button2)

connY3 = 330
col1Button3Oval = connCanvas.create_oval(30, connY3, 130, connY3+100, fill="#ff8a88", outline="#ff3f3c", width=2, tag="Button3")
col1Button3Text = connCanvas.create_text(80, connY3+50, text="Print Label")
connCanvas.tag_bind(col1Button3Oval, "<Button-1>", col1Button3)
connCanvas.tag_bind(col1Button3Text, "<Button-1>", col1Button3)

connCanvas.update()


#
# Column 2 | J2 default port
#

colFrame2 = Frame(root, height=800, width=150)
colFrame2.pack_propagate(0)
colFrame2.pack(side=LEFT, anchor=N, padx=10)

frameLabelcol2 = Label(colFrame2, text="J2 (default port)")
frameLabelcol2.pack(side=TOP, padx=5, pady=5)

# Inner frame of column2 with color
colFrame2inner = Frame(colFrame2, bg="#ffffd4", bd=1, relief=SOLID)
colFrame2inner.pack(side=TOP, fill=BOTH)

j2pins = {} # dictionary holding pin labels

for i in range(1, 20):
    l = Label(colFrame2inner, text="Pin%d [?]"%(i), bg="#dfffd4", bd=1, relief=SOLID)
    l.pack(ipadx=25, ipady=5, padx=5, pady=5, fill=X)
    j2pins["pin{}".format(i)] = l

#
# Column 3
#

colFrame3 = Frame(root, height=750, width=250)
colFrame3.pack_propagate(0)
colFrame3.pack(side=LEFT, anchor=N, padx=10)

# Inner Frame TOP (power P1,P2)

frameLabelcol3top = Label(colFrame3, text="Power P1, P2")
frameLabelcol3top.pack(side=TOP, padx=5, pady=5)

colFrame3inner = Frame(colFrame3, bg="#ffffd4", bd=1, relief=SOLID)
colFrame3inner.pack(side=TOP, fill=BOTH)

powerLabelP1 = Label(colFrame3inner, text="P1 = [?] A", bg="#dfffd4", bd=1, relief=SOLID)
powerLabelP1.pack(ipadx=25, ipady=5, padx=5, pady=5, fill=X)

powerLabelP1a = Label(colFrame3inner, text="P1a = [?] V", bg="#dfffd4", bd=1, relief=SOLID)
powerLabelP1a.pack(ipadx=25, ipady=5, padx=5, pady=5, fill=X)

powerLabelP1b = Label(colFrame3inner, text="P1b = [?] V", bg="#dfffd4", bd=1, relief=SOLID)
powerLabelP1b.pack(ipadx=20, ipady=5, padx=5, pady=5, fill=X)

powerLabelP2 = Label(colFrame3inner, text="P2 = [?] A", bg="#dfffd4", bd=1, relief=SOLID)
powerLabelP2.pack(ipadx=25, ipady=5, padx=5, pady=5, fill=X)

powerLabelP2a = Label(colFrame3inner, text="P2a = [?] V", bg="#dfffd4", bd=1, relief=SOLID)
powerLabelP2a.pack(ipadx=25, ipady=5, padx=5, pady=5, fill=X)

powerLabelP2b = Label(colFrame3inner, text="P2b = [?] V", bg="#dfffd4", bd=1, relief=SOLID)
powerLabelP2b.pack(ipadx=20, ipady=5, padx=5, pady=5, fill=X)

powerLabelP2VMM = Label(colFrame3inner, text="P2 VMM = [?] V", bg="#dfffd4", bd=1, relief=SOLID)
powerLabelP2VMM.pack(ipadx=20, ipady=5, padx=5, pady=5, fill=X)

# Inner Frame I2C scan VMM

frameLabelcol3bottom = Label(colFrame3, text="I2C scan VMM")
frameLabelcol3bottom.pack(side=TOP, padx=5, pady=5)

colFrame3inner2 = Frame(colFrame3, bg="#ffffd4", bd=1, relief=SOLID)
colFrame3inner2.pack(side=TOP, fill=BOTH)

i2cLabel1 = Label(colFrame3inner2, text="IC chip [?]", bg="#dfffd4", bd=1, relief=SOLID)
i2cLabel1.pack(ipadx=10, ipady=5, padx=5, pady=5, fill=X)

i2cLabel2 = Label(colFrame3inner2, text="Chip ID [?]", bg="#dfffd4", bd=1, relief=SOLID)
i2cLabel2.pack(ipadx=10, ipady=5, padx=5, pady=5, fill=X)

i2cLabel3 = Label(colFrame3inner2, text="EEprom [?]", bg="#dfffd4", bd=1, relief=SOLID)
i2cLabel3.pack(ipadx=10, ipady=5, padx=5, pady=5, fill=X)

i2cLabel4 = Label(colFrame3inner2, text="Chip number [?]", bg="#dfffd4", bd=1, relief=SOLID)
i2cLabel4.pack(ipadx=10, ipady=5, padx=5, pady=5, fill=X)

i2cLabel5 = Label(colFrame3inner2, text="Chip address [?]", bg="#dfffd4", bd=1, relief=SOLID)
i2cLabel5.pack(ipadx=10, ipady=5, padx=5, pady=5, fill=X)

i2cLabel6 = Label(colFrame3inner2, text="uADC 1 [?]", bg="#dfffd4", bd=1, relief=SOLID)
i2cLabel6.pack(ipadx=10, ipady=5, padx=5, pady=5, fill=X)

i2cLabel7 = Label(colFrame3inner2, text="uADC 2 [?]", bg="#dfffd4", bd=1, relief=SOLID)
i2cLabel7.pack(ipadx=10, ipady=5, padx=5, pady=5, fill=X)



#
# Column 4
#

colFrame4 = Frame(root, height=750, width=200)
colFrame4.pack(side=LEFT, anchor=N, padx=10)

frameLabelcol4 = Label(colFrame4, text="J3 (Slave port)")
frameLabelcol4.pack(side=TOP, padx=5, pady=5)

# Inner frame of column2 with color
colFrame4inner = Frame(colFrame4, bg="#c4c4c4", bd=1, relief=SOLID)
colFrame4inner.pack(side=TOP, fill=BOTH)

for i in range(0, 19):

    if i == 2:
        l = Label(colFrame4inner, text="Pin%d Error"%(i+1), bg="#919191", bd=1, relief=SOLID)
        l.pack(ipadx=15, ipady=5, padx=5, pady=5)
    else:
        l = Label(colFrame4inner, text="Pin%d OK"%(i+1), bg="#ababab", bd=1, relief=SOLID)
        l.pack(ipadx=25, ipady=5, padx=5, pady=5)

#
# Column 5 Measurement field
#

colFrame5 = Frame(root, height=750, width=300)
colFrame5.pack_propagate(0)
colFrame5.pack(side=LEFT, anchor=N, padx=10)

frameLabelcol5 = Label(colFrame5, text="Measurement field")
frameLabelcol5.pack(side=TOP, padx=5, pady=5)

longtext = "No Data"
textArea = Message(colFrame5, text=longtext, bd=1, relief=SOLID)
textArea.pack(fill=BOTH)

#
# Column 6 Aux buttons
#

colFrame6 = Frame(root, height=750, width=200)
colFrame6.pack(side=LEFT, anchor=N, padx=10)

frameLabelcol6 = Label(colFrame6, text="Aux. buttons")
frameLabelcol6.pack(side=TOP, padx=5, pady=5)

auxCanvas = Canvas(colFrame6, height=750, width=200)
auxCanvas.pack()

def col6Button1(event):
    print("Clicked VMM Power On/Off")

    # Change button collor
    oval = auxCanvas.find_withtag("Button1")
    auxCanvas.itemconfig(oval, fill="#ffc588")
    auxCanvas.update()

    # Call microcontroller
    import_module("vmm_power_cycle")
    output = serial_write("vmm_power_cycle.power_cycle()", timeout=5)
    print(output)

    # Change button collor back
    auxCanvas.itemconfig(oval, fill="#88c2ff")
    auxCanvas.update()

def col6Button2(event):
    print("Clicked VMM ID Readout")

    # Change button collor
    oval = auxCanvas.find_withtag("Button2")
    auxCanvas.itemconfig(oval, fill="#ffc588")
    auxCanvas.update()

    # Call microcontroller
    import_module("vmm_chip_readout_sp1")
    output = serial_write("vmm_chip_readout_sp1.id_readout()")
    print(output)

    # Change button collor back
    auxCanvas.itemconfig(oval, fill="#88c2ff")
    auxCanvas.update()

def col6Button3(event):
    print("Clicked Label Print ID Readout")

    # Change button collor
    oval = auxCanvas.find_withtag("Button3")
    auxCanvas.itemconfig(oval, fill="#ffc588")
    auxCanvas.update()

    # Call microcontroller
    time.sleep(0.1) # delete me

    # Change button collor back
    auxCanvas.itemconfig(oval, fill="#88c2ff")
    auxCanvas.update()


def col6Button4(event):
    print("Clicked Save to DB")

    # Change button collor
    oval = auxCanvas.find_withtag("Button4")
    auxCanvas.itemconfig(oval, fill="#ffc588")
    auxCanvas.update()

    def save():
        # Writing into database
        try:
            record.save()
        except Exception as e:
            print(e)
            print("Problem writing into database")

    # Check if record is filled with data from VMM
    if record.empty:
        mb.showwarning("No Data", "Press J2 button to read data from VMM")

    # Check if record has ID (was already saved into database)
    elif record.id:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
        mb.showwarning("Already saved", "Record was already saved into database")
        
    # Record is not empty and not yet saved into database. Save it!
    else:
        save()

    # Change button collor back
    auxCanvas.itemconfig(oval, fill="#88c2ff")
    auxCanvas.update()



auxY1 = 30
col6Button1Oval = auxCanvas.create_oval(30, 30, 130, auxY1+100, fill="#88c2ff", outline="#00bfff", width=2, tag="Button1")
col6Button1Text = auxCanvas.create_text(80, auxY1+50, text="VMM Power\nOn / Off")
auxCanvas.tag_bind(col6Button1Oval, "<Button-1>", col6Button1)
auxCanvas.tag_bind(col6Button1Text, "<Button-1>", col6Button1)

auxY2 = 180
col6Button2Oval = auxCanvas.create_oval(30, auxY2, 130, auxY2+100, fill="#88c2ff", outline="#00bfff", width=2, tag="Button2")
col6Button2Text = auxCanvas.create_text(80, auxY2+50, text="   VMM\nID Readout")
auxCanvas.tag_bind(col6Button2Oval, "<Button-1>", col6Button2)
auxCanvas.tag_bind(col6Button2Text, "<Button-1>", col6Button2)

auxY3 = 330
col6Button3Oval = auxCanvas.create_oval(30, auxY3, 130, auxY3+100, fill="#88c2ff", outline="#00bfff", width=2, tag="Button3")
col6Button3Text = auxCanvas.create_text(80, auxY3+50, text="Label Print\nID readout")
auxCanvas.tag_bind(col6Button3Oval, "<Button-1>", col6Button3)
auxCanvas.tag_bind(col6Button3Text, "<Button-1>", col6Button3)

auxY4 = 480
col6Button4Oval = auxCanvas.create_oval(30, auxY4, 130, auxY4+100, fill="#88c2ff", outline="#00bfff", width=2, tag="Button4")
col6Button4Text = auxCanvas.create_text(80, auxY4+50, text="Save to DB")
auxCanvas.tag_bind(col6Button4Oval, "<Button-1>", col6Button4)
auxCanvas.tag_bind(col6Button4Text, "<Button-1>", col6Button4)

auxCanvas.update()

root.mainloop()
