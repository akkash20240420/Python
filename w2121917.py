#Author: Akkash
#Student ID: 20240420
import csv
import sys
sys.path.append('path_to_your_project/module')
from graphics import *

total_vehicles = 0
total_trucks = 0
total_electric_vehicles = 0
total_two_wheeled_vehicles = 0
total_bicycles = 0
total_busses_through_elm_to_N = 0
total_vehicles_without_turning = 0
total_vehicles_over_speed_limit = 0
total_vehicles_through_elm_only = 0
total_vehicles_through_hanley_only = 0
total_scooter_through_elm = 0
total_vehicles_in_peak_hanley = 0
per_hour_vehicles = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]
rain_hours = [0]*24
trucks_percentage = 0
hours = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]
average_bikes_per_hour = 0
scooter_percentage = 0
peak_time = []

#Task A
#Prompts the user to input a date.

def validate_date_input():
    
    while True:
        #Date
        try:
            date = int(input("Please enter the day of the survey in the format DD:  "))
            if 1 <= date <= 31:
                date = f"{date:02d}"
                break
            else:
                print("Out of range - values must be in the range 1 and 31")

        except ValueError:
            print("Integer required")

    while True:
        #Month
        try:
            month = int(input("Please enter the month of the survey in the format MM:  "))
            if 1 <= month <= 12:
                month = f"{month:02d}"
                break
            else:
                print("Out of range - values must be in the range 1 and 12.")

        except ValueError:
            print("Integer required.")

    while True:
        #Year
        try:
            year = int(input("Please enter the year of the survey in the format YYYY: "))
            if 2000 <= year <= 2024:
                break
            else:
                print("Out of range - value must be in the range 2000 and 2024.")

        except ValueError:
            print("Integer required.")

    
    return date, month, year 

    
#Prompts the user to decide whether to load another data file.

def validate_continue_input():
    
    continue_input = input("Do you want to select another data file for a different date? Y/N: ").lower()
    while True:
        if continue_input == "y" or continue_input == "n" :
            return continue_input
        else:
            continue_input = input("Please enter “Y” or “N”: ")


#Task B
#Outcomes
            
def define_file_path(date):
    filename = f"traffic_data{date[0]}{date[1]}{date[2]}.csv"
    return filename

#Process

def process_csv_data(file_path, total_vehicles, total_trucks, total_electric_vehicles, total_two_wheeled_vehicles, total_bicycles, total_busses_through_elm_to_N, total_vehicles_without_turning, total_vehicles_over_speed_limit, total_vehicles_through_elm_only, total_vehicles_through_hanley_only, total_scooter_through_elm, total_vehicles_in_peak_hanley, per_hour_vehicles, rain_hours, trucks_percentage, average_bikes_per_hour, scooter_percentage):

    try:
        with open(f"{file_path}", mode="r") as file:
            csv_reader = csv.DictReader(file)

            for row in csv_reader:
                total_vehicles += 1
                vehicle_type = row.get("VehicleType", "").lower()
                junction = row.get("JunctionName", "").lower()
                time_stamp = row.get("timeOfDay", "")
                rain_status = row.get("Weather_Conditions", "").lower()
                vehicle_speed = int(row.get("VehicleSpeed", 0))
                junction_speed_limit = int(row.get("JunctionSpeedLimit", 0))
                electric_hybrid = row.get("elctricHybrid", "")

                direction_in = row.get("travel_Direction_in", "").lower()
                direction_out = row.get("travel_Direction_out", "").lower()
                
                hour = int(time_stamp.split(":")[0])
                hours[hour] = True

                if "truck" in vehicle_type:
                    total_trucks += 1

                elif "scooter" in vehicle_type:
                    total_two_wheeled_vehicles += 1

                    if "elm avenue/rabbit road" in junction:
                        total_scooter_through_elm += 1

                elif "buss" in vehicle_type:
                    if direction_out == 'n':
                        total_busses_through_elm_to_N += 1

                elif "motorcycle" in vehicle_type:
                    total_two_wheeled_vehicles += 1
                
                elif "bicycle" in vehicle_type:
                    total_two_wheeled_vehicles += 1
                    total_bicycles += 1
                
                else:
                    pass


                if electric_hybrid == "True":
                    total_electric_vehicles += 1

                if direction_in == direction_out:
                    total_vehicles_without_turning += 1
                
                if vehicle_speed > junction_speed_limit:
                    total_vehicles_over_speed_limit += 1
                
                if "elm avenue/rabbit road" in junction:
                    total_vehicles_through_elm_only += 1
                
                if "hanley highway/westway" in junction:
                    total_vehicles_through_hanley_only += 1
                    per_hour_vehicles[hour] += 1

                if "light rain" in rain_status or "heavy rain" in rain_status:
                    rain_hours[hour] =  True;

            total_vehicles_in_peak_hanley = max(per_hour_vehicles)
            trucks_percentage = round((total_trucks/total_vehicles)*100)
            average_bikes_per_hour = round(total_bicycles/hours.count(True))
            scooter_percentage = round((total_scooter_through_elm/total_vehicles_through_elm_only)*100)

            outcomes = [file_path, total_vehicles, total_trucks, total_electric_vehicles, total_two_wheeled_vehicles, total_busses_through_elm_to_N, total_vehicles_without_turning, trucks_percentage, average_bikes_per_hour, total_vehicles_over_speed_limit, total_vehicles_through_elm_only, total_vehicles_through_hanley_only, scooter_percentage, total_vehicles_in_peak_hanley, find_peak_time(), rain_hours.count(True)]
    
            display_outcomes(outcomes)
            save_results_to_file(outcomes)


    except FileNotFoundError:
        print(f"{file_path} File not found.")
    except Exception as e:
        print(f"An error occured : {e}")

        
def find_peak_time():
    global per_hour_vehicles, peak_time

    peak_value = max(per_hour_vehicles)

    for i in range(len(per_hour_vehicles)):
        if per_hour_vehicles[i] == peak_value:
            peak_time.append(i)

    if len(peak_time) == 1:
        return (f"{peak_time[0]:02d}.00 and {(peak_time[0] + 1):02d}.00")
    

#Displays the outcomes.
    
def display_outcomes(outcomes):
    
    print(f"""
    ***********************************
    data file selected is {outcomes[0]}
    ***********************************
    
    The total number of vehicles recorded for this date is {outcomes[1]}
    The total number of trucks recorded for this date is {outcomes[2]}
    The total number of electric vehicles for this date is {outcomes[3]}
    The total number of two-wheeled vehicles for this date is {outcomes[4]}
    The total number of Busses leaving Elm Avenue/Rabbit Road heading North is {outcomes[5]}
    The total number of Vehicles through both junctions not turning left or right is {outcomes[6]}
    The percentage of total vehicles recorded that are trucks for this date is {outcomes[7]}%
    The average number of Bikes per hour for this date is {outcomes[8]}
    
    The total number of Vehicles recorded as over the speed limit for this date is {outcomes[9]}
    The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes[10]}
    The total number of vehicles recorded through Hanley Highway/Westway junction is {outcomes[11]}  
    {outcomes[12]}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.
    
    The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes[13]}
    The most vehicles through Hanley Highway/Westway were recorded between {outcomes[14]}
    The number of hours of rain for this date is {outcomes[15]}

******************************************************************************************************
""")


#Task C
#Save Results as a Text File.
    
def save_results_to_file(outcomes, file_name="results.txt"):
    
    with open(file_name, 'a') as file:
        file.write(f"""
    ***********************************
    data file selected is {outcomes[0]}
    ***********************************
    
    The total number of vehicles recorded for this date is {outcomes[1]}
    The total number of trucks recorded for this date is {outcomes[2]}
    The total number of electric vehicles for this date is {outcomes[3]}
    The total number of two-wheeled vehicles for this date is {outcomes[4]}
    The total number of Busses leaving Elm Avenue/Rabbit Road heading North is {outcomes[5]}
    The total number of Vehicles through both junctions not turning left or right is {outcomes[6]}
    The percentage of total vehicles recorded that are trucks for this date is {outcomes[7]}%
    The average number of Bikes per hour for this date is {outcomes[8]}
    
    The total number of Vehicles recorded as over the speed limit for this date is {outcomes[9]}
    The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes[10]}
    The total number of vehicles recorded through Hanley Highway/Westway junction is {outcomes[11]}  
    {outcomes[12]}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.
    
    The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes[13]}
    The most vehicles through Hanley Highway/Westway were recorded between {outcomes[14]}
    The number of hours of rain for this date is {outcomes[15]}
            
****************************************************************************************************** 
""")
# Task D: Histogram 
class HistogramApp:
    def __init__(self, traffic_data, date):
        """
        Initializes the histogram application with the traffic data and selected date.
        """
        self.traffic_data = traffic_data
        self.date = date
        self.window = None
        self.hour_data = self.process_hourly_data()

    def process_hourly_data(self):
        """"
        Process traffic data
        """
       
        elm_hours = {h: 0 for h in range(24)}
        hanley_hours = {h: 0 for h in range(24)}
        for row in self.traffic_data:
            hour = int(row['timeOfDay'].split(':')[0])
            if row['JunctionName'] == 'Elm Avenue/Rabbit Road':
                elm_hours[hour] += 1
            else:
                hanley_hours[hour] += 1

        return {'Elm Avenue/Rabbit Road': elm_hours, 'Hanley Highway/Westway': hanley_hours}

    def setup_window(self):
        """
        Sets up the window using graphic
        """
    
        self.window = GraphWin(f"Histogram - {self.date}", 1200, 600)
        self.window.setBackground(color_rgb(237, 242, 238))
        self.window.setCoords(-1, -5, 24, 45) 

    def draw_title_and_legend(self):
        """"
        draw title 
        """
       
        title = Text(Point(11.5, 42), f"Histogram of Vehicle Frequency per Hour ({self.date})")
        title.setSize(14)
        title.setStyle('bold')
        title.setFace('arial')
        title.draw(self.window)

        legend_items = [
            ("Elm Avenue/Rabbit Road", color_rgb(255, 253, 55)),
            ("Hanley Highway/Westway", color_rgb(255, 127, 127))
        ]
    
        for i, (label, color) in enumerate(legend_items):
            y_pos = 38 - (i * 2)
            box = Rectangle(Point(-0.30, y_pos), Point(0.10, y_pos + 1.5))
            box.setFill(color)
            box.setOutline(color_rgb(100, 100, 100))
            box.draw(self.window)
            text = Text(Point(2, y_pos + 0.75), label)
            text.setSize(11)
            text.draw(self.window)

    def draw_bars(self):
        """
        Drawbars
        """
        bar_width = 0.4
        max_bar_height = 33
        max_value = max(
            max(self.hour_data['Elm Avenue/Rabbit Road'].values()),
            max(self.hour_data['Hanley Highway/Westway'].values())
        )

        scale = max_bar_height / max_value if max_value > max_bar_height else 1
        for hour in range(24):
            # Elm Avenue/Rabbit Road
            elm_count = self.hour_data['Elm Avenue/Rabbit Road'][hour]
            scaled_height = elm_count * scale
            elm_bar = Rectangle(Point(hour - bar_width, 0), Point(hour, scaled_height))
            elm_bar.setFill(color_rgb(255, 253, 55))
            elm_bar.draw(self.window)
            if elm_count > 0:
                label = Text(Point(hour - bar_width / 2, scaled_height + 1), str(elm_count))
                label.setSize(8)
                label.draw(self.window)

            # Hanley Highway/Westway
            hanley_count = self.hour_data['Hanley Highway/Westway'][hour]
            scaled_height = hanley_count * scale
            hanley_bar = Rectangle(Point(hour, 0), Point(hour + bar_width, scaled_height))
            hanley_bar.setFill(color_rgb(255, 127, 127))
            hanley_bar.draw(self.window)

            if hanley_count > 0:
                label = Text(Point(hour + bar_width / 2, scaled_height + 1), str(hanley_count))
                label.setSize(8)
                label.draw(self.window)
    
    def draw_axes_and_labels(self):
        """
        Draw axes and labels
        """
    
       
        xaxis = Line(Point(-0.4, 0), Point(24, 0))
        xaxis.draw(self.window)

        for i in range(24):
            label = Text(Point(i, -1), f"{i:02d}")
            label.setSize(8)
            label.draw(self.window)

        xlabel = Text(Point(12, -3), "Hours 00:00 to 24:00")
        xlabel.setSize(10)
        xlabel.draw(self.window)

    def display(self):
        """
        Display
        """
       
        self.setup_window()
        self.draw_title_and_legend()
        self.draw_bars()
        self.draw_axes_and_labels()
        self.window.getMouse()  
        self.window.close()


def main():
    """
    Main function
    """
    print("Welcome to the Traffic Analysis Program!")
    
    while True:
     
        date = validate_date_input()
        file_path = define_file_path(date)
        print("\nTask B: Process Traffic Data")
        process_csv_data(
            file_path, 
            total_vehicles, total_trucks, total_electric_vehicles, total_two_wheeled_vehicles,
            total_bicycles, total_busses_through_elm_to_N, total_vehicles_without_turning,
            total_vehicles_over_speed_limit, total_vehicles_through_elm_only, total_vehicles_through_hanley_only,
            total_scooter_through_elm, total_vehicles_in_peak_hanley, per_hour_vehicles, rain_hours, 
            trucks_percentage, average_bikes_per_hour, scooter_percentage
        )
        
        print("\nTask D: Display Histogram")
        try:
            with open(file_path, mode='r') as file:
                csv_reader = csv.DictReader(file)
                traffic_data = [row for row in csv_reader]
                app = HistogramApp(traffic_data, f"{date[0]}/{date[1]}/{date[2]}")
                app.display()
        except Exception as e:
            print(f"Could not display histogram: {e}")
        
        continue_choice = validate_continue_input()
        if continue_choice == 'n':
            print("Exiting the program. Goodbye!")
            break


if __name__ == "__main__":
    main()
