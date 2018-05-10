from tkinter import Tk, Label, Button, Entry, IntVar, END, W, E, StringVar
import pickle


class Simulator():

    def __init__(self, master, stations, start_times, end_times):
        self.master = master
        master.title("Simulator")

        self.total = 0
        self.current_time = [int(i) for i in "00:00:00".split(":")]
        self.end_time = [int(i) for i in "24:00:00".split(":")]


        self.stations = stations
        self.start_times = start_times
        self.end_times = end_times

        self.total_label_text = IntVar()
        self.total_label_text.set(self.current_time)
        self.total_label = Label(master, textvariable=self.total_label_text)

        self.stations_label_text = StringVar()
        self.stations_label_text.set("")
        self.stations_label = Label(master, textvariable=self.stations_label_text)


        self.label = Label(master, text="Total:")

        vcmd = master.register(self.validate) # we have to wrap the command
        self.entry = Entry(master, validate="key", validatecommand=(vcmd, '%P'))

        self.add_button = Button(master, text="+", command=lambda: self.advance_time())

        # LAYOUT

        self.entry.grid(row=1, column=0, columnspan=3, sticky=W+E)

        
        self.add_button.grid(row=2, column=0)

        self.label.grid(row=0, column=0, sticky=W)
        self.total_label.grid(row=0, column=1, columnspan=2, sticky=E)
        self.stations_label.grid(row=3, column=0, sticky=E)




    def validate(self, new_text):
        if not new_text: # the field is being cleared
            self.entered_number = 0
            return True

        try:
            self.entered_number = int(new_text)
            return True
        except ValueError:
            return False

    def greater_than(self, time1, time2):
        # print(time2[:2])
        # seconds1 = int(time1[:2])*60*60 + int(time1[3:5])*60 + int(time1[-2:])
        # seconds2 = int(time2[:2])*60*60 + int(time2[3:5])*60 + int(time2[-2:])
        seconds1 = sum([t*60**(2-i) for i, t in enumerate(time1)])
        seconds2 = sum([t*60**(2-i) for i, t in enumerate(time2)])
        return seconds1 > seconds2

    def update_stations(self, curr_time):
        new_start_times = []
        new_end_times = []
        for idx, s in enumerate(self.start_times):
            if self.greater_than(s[0], curr_time):
                for key in [k[1] for k in self.start_times[:idx-1]]:
                    self.stations[key]['current_number_of_bikes'] -= 1
                new_start_times = self.start_times[idx-1:]
                break
        for idx, e in enumerate(self.end_times):
            if self.greater_than(e[0], curr_time):
                for key in [k[1] for k in self.end_times[:idx-1]]:
                    self.stations[key]['current_number_of_bikes'] += 1
                new_end_times = self.end_times[idx-1:]
                break

        for key in self.stations:
            self.stations[key]['over_capacity'] = self.stations[key]['current_number_of_bikes'] > self.stations[key]['dpcapacity']
            self.stations[key]['out_of_bikes'] = self.stations[key]['current_number_of_bikes'] < 0

        return new_start_times, new_end_times


    def check_for_errors(self):
        bad_stations = []
        for key in self.stations:
            if self.stations[key]['over_capacity'] or self.stations[key]['out_of_bikes']:
                bad_stations.append(self.stations[key])
        return bad_stations

    def advance_time(self):
        if not self.greater_than(self.current_time, self.end_time):

            self.current_time[2] += self.entered_number
            self.current_time[1] += self.current_time[2]//60
            self.current_time[2] %= 60
            self.current_time[0] += self.current_time[1]//60
            self.current_time[1] %= 60

            self.start_times, self.end_times = self.update_stations(self.current_time)

            self.total_label_text.set(self.current_time)
            array_of_errors = self.check_for_errors()
            self.stations_label_text.set(to_string(array_of_errors))



    def update(self, method):
        if method == "add":
            self.total += self.entered_number
        elif method == "subtract":
            self.total -= self.entered_number
        else: # reset
            self.total = 0
        self.total_label_text.set(self.total)
        self.entry.delete(0, END)

def main():


    day = 27#input("What day do you want to simulate?")
    verbose = 0#input("Verbose? (to see all stations 1, to just see overloaded ones 0)")
    
    data = load_obj("4day")
    start_times, end_times = initialize_start_end(data, day)
    stations = load_obj("stationsq1q2")
    stations = transform(stations)
    initialize_stations(stations)
    
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(stations)
    # pp.pprint(end_times)
    curr_time = [int(i) for i in "00:00:00".split(":")]
    end_time = [int(i) for i in "24:00:00".split(":")]

    root = Tk()
    my_gui = Simulator(root, stations, start_times, end_times)
    root.mainloop()

def transform(stations):
    transformed_stations = {}
    for station in stations:
        # new_station = {}
        # for s in station.keys():
        #     if s == "dpcapacity":
        #         new_station[s] = station[s]
        transformed_stations[station['id']] = {'id': int(station['id']), 'dpcapacity': int(station['dpcapacity'])}#new_station
    return transformed_stations

def initialize_stations(stations):
    for station in stations:
        stations[station]['current_number_of_bikes'] = (stations[station]['dpcapacity']*2)//2
        stations[station]['over_capacity'] = False
        stations[station]['out_of_bikes'] = False

def initialize_start_end(data, day):
    start_times = []
    end_times = []
    for entry in data:
        if int(entry['start_time'][2:4]) == int(day):
            start_times.append(([int(i) for i in entry['start_time'][-8:].split(":")], entry['from_station_id']))
            end_times.append(([int(i) for i in entry['end_time'][-8:].split(":")], entry['to_station_id']))
    start_times.reverse()
    end_times.sort()
    return start_times, end_times

def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def to_string(arr):
    string = ''
    for entry in arr:
        for key in entry.keys():
            string += key + ":\t" + str(entry[key]) + "\t"
        string += "\n"
    return string


if __name__ == "__main__":
    main()