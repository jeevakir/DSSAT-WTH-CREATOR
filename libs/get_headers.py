import PySimpleGUI as sg
import csv
import traceback

tooltip_update="""Once you update the config it will be saved in a file for future use. 
                  you can use it again if you want to use different data"""
default_headers = ["DATE", "SRAD", "TMAX", "TMIN", "RAIN", "DEWP", "WIND", "PAR", "EVAP", "RHUM"]
input_headers=[]

def get_headers():
    layout = [
        [sg.Titlebar("This is configuration window for selecting data type in each coloumn of input")],
        [sg.InputText("Please select one file as sample data",key='-csv_file-'),sg.FileBrowse(),sg.Button("load_CSV_sample",key="-csv_load-")],
        [sg.Button("UPDATE headers",key="-update-",tooltip=tooltip_update)],
        [sg.InputCombo(list(default_headers), size=(8, 4), default_value=default_headers[i],key=f'-in_head{i}-') for i in range(9)],
        [sg.Table(values=[list(range(1,11))],auto_size_columns=False,max_col_width=12, row_height=20,num_rows=10, key='-TABLE-',font=['Haveltica',12])]]

    head_window = sg.Window("Title", layout, modal=True,font=['Haveltica',12])

    while True:
        events,values=head_window.read()
        if events == sg.WINDOW_CLOSED or events == "Cancel":
            head_window.close()
            return False
        elif events == "-csv_load-":
            csv_sample=values["-csv_file-"]
            if csv_sample:
                try:
                    with open(csv_sample, "r") as file:
                            reader = csv.reader(file)
                            data = [row for row in reader]
                            headings = data[0]
                            data = data[0:5]
                            head_window["-TABLE-"].update(values=data)
                            head_window['-TABLE-'].expand(True,True)
                            head_window.refresh()
                            csv_sample=""
                except Exception:
                    traceback.print_exc()
                    head_window.close()
        elif events == "-update-":
            input_headers=[values[f'-in_head{i}-'] for i in range(9)]
    head_window.close()
    return True
