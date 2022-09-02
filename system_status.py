# Import the required libraries
import psutil
import time
from prettytable import PrettyTable
import speech_recognition as sr
import pyttsx3

def speak(output, my_lang = "en-uS"):
    engine = pyttsx3.init()
    engine.say(output)
    engine.runAndWait()

def status():
    print("==============================Process Monitor\
    ======================================")
    battery = psutil.sensors_battery().percent
    print("----Battery Available: %d "%(battery,) + "%")
    speak("----Battery Available: %d "%(battery,) + "%")

    print("----Networks----")
    table = PrettyTable(['Network', 'Status', 'Speed'])
    for key in psutil.net_if_stats().keys():
        name = key
        up = "Up" if psutil.net_if_stats()[key].isup else "Down"
        speed = psutil.net_if_stats()[key].speed
        table.add_row([name, up, speed])
        speak(name + " is in " + up + " state with speed " + str(speed))
    print(table)
    time.sleep(0.2)

    # Fetch the memory information
    print("----Memory----")
    memory_table = PrettyTable(["Total", "Used",
                                "Available", "Percentage"])
    vm = psutil.virtual_memory()
    memory_table.add_row([
        vm.total,
        vm.used,
        vm.available,
        vm.percent
    ])
    print(memory_table)
    speak(" Out of " + str(vm.total) + "memory" + str(vm.used) + "memory is used and " + str(vm.available) + "memory is available")
    time.sleep(0.1)
    speak(str(vm.percent) + "percent is consumed")
    time.sleep(0.2)


    print("----Processes----")
    process_table = PrettyTable(['PID', 'PNAME', 'STATUS',
                                'CPU', 'NUM THREADS'])

    process_list = []
    for process in psutil.pids()[-5:]:

        try:
            p = psutil.Process(process)
            process_table.add_row([
                str(process),
                p.name(),
                p.status(),
                str(int(p.cpu_percent()))+"%",
                p.num_threads()
                ])
            process_list.append(p.name() + "is" + p.status() + "with CPU " + str(p.cpu_percent())+"% and tread number of " + str(p.num_threads()))

        except Exception as e:
            pass
    print(process_table)
    for process_name in process_list:
        speak(process_name)
