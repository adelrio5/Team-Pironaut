# importing all the necessary Python libraries
import csv
from sense_hat import SenseHat
from datetime import datetime, timedelta
from time import sleep
from pathlib import Path
from ephem import readtle, degree
from logzero import logger, logfile


# storing directory path
dir_path = Path(__file__).parent.resolve()

# setting up logfile name
logfile(dir_path/"Pironauts.log") 

# setting up Sense Hat
sense = SenseHat()
sense.clear()

# obtaining latest TLE data for ISS location
name = "ISS (ZARYA)"
line1 = "1 25544U 98067A   21021.39156028  .00000107  00000-0  99803-5 0  9992"
line2 = "2 25544  51.6457 348.7866 0000446 316.5433 144.8341 15.49302983265845"
iss = readtle(name, line1, line2)

# enabling magnetometer and disabling gyroscope and accelerometer
sense.set_imu_config(True, False, False)

# setting the time between consecutive data recordings to 10 seconds
duration = 10

# setting total time for experiment in minutes
total_time_mins = 175

# setting total number of times values are recorded (i.e. number of times recording loops)
total_time_secs = total_time_mins * (60/duration)

# setting update variable for controlling LED matrix output
update = 0

# defining colours for text at the end of the experiment:
green = (0, 255, 0)
yellow = (255, 255, 0)

# setting colour values for LED matrix
r = (237, 41, 57) # <--red
w = (255, 255, 255) # <--white
b = (0, 161, 222) # <--light blue
o = (0, 0, 0) # <--black

# setting Luxembourg flag for LED matrix to display progress
luxFlag0 = [
    r, r, r, r, r, r, r, r,
    r, o, o, o, o, o, o, r,
    r, o, o, o, o, o, o, r,
    w, o, o, o, o, o, o, w,
    w, o, o, o, o, o, o, w,
    b, o, o, o, o, o, o, b,
    b, o, o, o, o, o, o, b,
    b, b, b, b, b, b, b, b
]
luxFlag1 = [
    r, o, o, o, o, o, o, o,
    r, o, o, o, o, o, o, o,
    r, o, o, o, o, o, o, o,
    w, o, o, o, o, o, o, o,
    w, o, o, o, o, o, o, o,
    b, o, o, o, o, o, o, o,
    b, o, o, o, o, o, o, o,
    b, o, o, o, o, o, o, o
]
luxFlag2 = [
    r, r, o, o, o, o, o, o,
    r, r, o, o, o, o, o, o,
    r, r, o, o, o, o, o, o,
    w, w, o, o, o, o, o, o,
    w, w, o, o, o, o, o, o,
    b, b, o, o, o, o, o, o,
    b, b, o, o, o, o, o, o,
    b, b, o, o, o, o, o, o
]
luxFlag3 = [
    r, r, r, o, o, o, o, o,
    r, r, r, o, o, o, o, o,
    r, r, r, o, o, o, o, o,
    w, w, w, o, o, o, o, o,
    w, w, w, o, o, o, o, o,
    b, b, b, o, o, o, o, o,
    b, b, b, o, o, o, o, o,
    b, b, b, o, o, o, o, o
]
luxFlag4 = [
    r, r, r, r, o, o, o, o,
    r, r, r, r, o, o, o, o,
    r, r, r, r, o, o, o, o,
    w, w, w, w, o, o, o, o,
    w, w, w, w, o, o, o, o,
    b, b, b, b, o, o, o, o,
    b, b, b, b, o, o, o, o,
    b, b, b, b, o, o, o, o
]
luxFlag5 = [
    r, r, r, r, r, o, o, o,
    r, r, r, r, r, o, o, o,
    r, r, r, r, r, o, o, o,
    w, w, w, w, w, o, o, o,
    w, w, w, w, w, o, o, o,
    b, b, b, b, b, o, o, o,
    b, b, b, b, b, o, o, o,
    b, b, b, b, b, o, o, o
]
luxFlag6 = [
    r, r, r, r, r, r, o, o,
    r, r, r, r, r, r, o, o,
    r, r, r, r, r, r, o, o,
    w, w, w, w, w, w, o, o,
    w, w, w, w, w, w, o, o,
    b, b, b, b, b, b, o, o,
    b, b, b, b, b, b, o, o,
    b, b, b, b, b, b, o, o
]
luxFlag7 = [
    r, r, r, r, r, r, r, o, 
    r, r, r, r, r, r, r, o,
    r, r, r, r, r, r, r, o,
    w, w, w, w, w, w, w, o,
    w, w, w, w, w, w, w, o,
    b, b, b, b, b, b, b, o,
    b, b, b, b, b, b, b, o,
    b, b, b, b, b, b, b, o
]
luxFlag8 = [
    o, o, o, o, o, o, o, o,
    o, r, r, r, r, r, r, o,
    o, r, r, r, r, r, r, o,
    o, w, w, w, w, w, w, o,
    o, w, w, w, w, w, w, o,
    o, b, b, b, b, b, b, o,
    o, b, b, b, b, b, b, o,
    o, o, o, o, o, o, o, o
]
luxFlagDone = [
    r, r, r, r, r, r, r, r, 
    r, r, r, r, r, r, r, r,
    r, r, r, r, r, r, r, r,
    w, w, w, w, w, w, w, w,
    w, w, w, w, w, w, w, w,
    b, b, b, b, b, b, b, b,
    b, b, b, b, b, b, b, b,
    b, b, b, b, b, b, b, b
]

# function to create new CSV file and add the header row
def create_csv_file(data_file):
    with open(data_file, 'w') as f:
        writer = csv.writer(f)
        header = ("Date/Time", "ISS Latitude", "ISS Longitude", "MI_X (µT)", "MI_Y (µT)", "MI_Z (µT)", "Temperature (°C)")
        writer.writerow(header)

# function to add a row of data to the data_file CSV
def add_csv_data(data_file, data):
    with open(data_file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)

# initializing function to measure magnetic field intensity
def measure_MFI():
  # obtaining MI* on each axis
  # *MI is float & measured in microTeslas (µT) or (weber (volt/sec)/m^2)*10^6
  raw = sense.get_compass_raw()

# assigning magnetic intensity of axis to respective variable
  mi_x = raw['x']
  mi_y = raw['y']
  mi_z = raw['z']  
  
  # return obtained values
  return mi_x, mi_y, mi_z

# initializing function to measure latitude and longitude, in degrees
def get_latlon():
    iss.compute() 
    return (iss.sublat / degree, iss.sublong / degree)

# initializing function to convert ephem angles to better representation
def convert(angle):
    # converting degrees (ISS position), minutes and seconds to float values, separated by :
    degrees, minutes, seconds = (float(field) for field in str(angle).split(":"))
    # formatting representation: e.g. '23:75:42.9' to '23/1,75/1,42.9/10'
    exif_angle = f'{abs(degrees):.0f}/1,{minutes:.0f}/1,{seconds*10:.0f}/10'
    return degrees < 0, exif_angle


#creating start time and now time variables (now_time will be updated in while loop)
start_time = datetime.now()
now_time = datetime.now()

# initialise the CSV file
data_file = dir_path/"data.csv"
create_csv_file(data_file)

# Record starting and current time
start_time = datetime.now()
now_time = datetime.now()


# run loop for under 3 hours (verifying that 3 hour time limit is not exceeded)
while(now_time < start_time + timedelta(minutes=total_time_mins+1.5)):
  """total_time_mins+1.5 to allow the team message 
   to be displayed and then clear experiment at 
   end (see else:)"""

  # selecting Luxembourg flag variable to use to display on LED matrix the progress of the experiment
  if (update < total_time_secs*(1/8)): # <-- first 1/8th of experiment
      LED = luxFlag1 
  elif (update < total_time_secs*(2/8)): # <-- second 1/8th of experiment
      LED = luxFlag2
  elif (update < total_time_secs*(3/8)): # <-- third 1/8th of experiment
      LED = luxFlag3
  elif (update < total_time_secs*(4/8)): # <-- etc.
      LED = luxFlag4
  elif (update < total_time_secs*(5/8)):
      LED = luxFlag5
  elif (update < total_time_secs*(6/8)):
      LED = luxFlag6
  elif (update < total_time_secs*(7/8)):
      LED = luxFlag7
  elif (update < total_time_secs*(8/8)):
      LED = luxFlag8
  else:
      # team messages displayed and cleared once experiment is complete 
      sense.set_pixels(luxFlagDone)
      sleep(3)
      sense.show_message("DONE! We are Antonio, Greg, and Steve of Team Pironauts from Luxembourg!", text_colour=green)
      sense.clear()

  # setting LED matrix to display the correct Luxembourg flag (depending on progress of experiment) 
  sense.set_pixels(LED)
  
  # calling function and assigning MI values to respective variables
  mi_x, mi_y, mi_z = measure_MFI()

  # obtaining temperature values
  temperature = round(sense.temperature, 4)

  # geting latitude and longitude
  latitude, longitude = get_latlon()
  
  # storing necessary info 
  data = (
            datetime.now(),
            latitude,
            longitude,
            mi_x,
            mi_y,
            mi_z,
            temperature
        )
  # saving data to csv file
  add_csv_data(data_file, data)

  # adjusting update value
  update += 1
  
  # wait for duration, and display flashing Luxembourg progress flag (until end of experiment)
  if (update < total_time_secs*(8/8)):
      for i in range (1, duration+1):
          sense.set_pixels(LED)
          sleep(0.5)
          sense.set_pixels(luxFlag0)
          sleep(0.5)
  
  # updating now_time variable
  now_time = datetime.now()
  
