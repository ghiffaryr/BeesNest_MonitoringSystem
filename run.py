#!/usr/bin/env python3

import smbus
import time
import datetime

bus = smbus.SMBus(1)

# Initialization for counting activity variables
count1 = 0
count2 = 0
count3 = 0

processed_data = 0

lux1acc = 0
humid1acc = 0
temp1acc = 0

lux2acc = 0
humid2acc = 0
temp2acc = 0

lux3acc = 0
humid3acc = 0
temp3acc = 0

# Generate output files
file1 = open("imu_data1.csv", "w+")
file2 = open("imu_data2.csv", "w+")
file3 = open("imu_data3.csv", "w+")

# Write columns title to CSV
file1.write("lux" + "," + "humidity" + "," + "temp" + "," + "frequency" + "," + "time" + "\n")
file2.write("lux" + "," + "humidity" + "," + "temp" + "," + "frequency" + "," + "time" + "\n")
file3.write("lux" + "," + "humidity" + "," + "temp" + "," + "frequency" + "," + "time" + "\n")

# Time start reading
startTime = time.time()

def request_reading():
        # Read a block of 4 bytes starting at SLAVE_ADDRESS
        try:
                reading1 = bus.read_i2c_block_data(0x04, 0, 4)
        except (OSError):
                reading1 = [-1, -1, -1, -1]
        try:
                reading2 = bus.read_i2c_block_data(0x05, 0, 4)
        except (OSError):
                reading2 = [-1, -1, -1, -1]
        try:
                reading3 = bus.read_i2c_block_data(0x06, 0, 4)
        except (OSError):
                reading3 = [-1, -1, -1, -1]

        # Extract the IMU reading data
        lux1 = reading1[0]
        humid1 = reading1[1]
        temp1 = reading1[2]
        ir1 = reading1[3]
        date1 = datetime.datetime.now().strftime('%d-%m-%Y_%H.%M.%S')
                
        lux2 = reading2[0]
        humid2 = reading2[1]
        temp2 = reading2[2]
        ir2 = reading2[3]
        date2 = datetime.datetime.now().strftime('%d-%m-%Y_%H.%M.%S')

        lux3 = reading3[0]
        humid3 = reading3[1]
        temp3 = reading3[2]
        ir3 = reading3[3]
        date3 = datetime.datetime.now().strftime('%d-%m-%Y_%H.%M.%S')
        
        return (lux1, humid1, temp1, ir1, date1, lux2, humid2, temp2, ir2, date2, lux3, humid3, temp3, ir3, date3)       

# Request IMU data every 1 seconds from the Arduino
while True:
        # Counting activity
        if(request_reading()[3] == 0):
                count1 += 1
        if(request_reading()[8] == 0):
                count2 += 1
        if(request_reading()[13] == 0):
                count3 += 1

        # Counting average data              
        processed_data +=1
        
        #1
        lux1acc += request_reading()[0]
        lux1avg = lux1acc/processed_data
        
        humid1acc += request_reading()[1]
        humid1avg =  humid1acc/processed_data
        
        temp1acc += request_reading()[2]
        temp1avg = temp1acc/processed_data
        
        #2
        lux2acc += request_reading()[5]
        lux2avg = lux2acc/processed_data
        
        humid2acc += request_reading()[6]
        humid2avg =  humid2acc/processed_data
        
        temp2acc += request_reading()[7]
        temp2avg = temp2acc/processed_data
        
        #3
        lux3acc += request_reading()[10]
        lux3avg = lux3acc/processed_data
        
        humid3acc += request_reading()[11]
        humid3avg =  humid3acc/processed_data
        
        temp3acc += request_reading()[12]
        temp3avg = temp3acc/processed_data

        # Time now
        endTime = time.time()
        
        if (int(endTime-startTime) % 3600 == 0):
                # Print the IMU data to the console
                print(str(request_reading()[0]), "Lux1", str(request_reading()[1]), "%1", str(request_reading()[2]), "C1", str(count1), "times1", str(request_reading()[4]))
                print(str(request_reading()[5]), "Lux2", str(request_reading()[6]), "%2", str(request_reading()[7]), "C2", str(count2), "times2", str(request_reading()[9]))
                print(str(request_reading()[10]), "Lux3", str(request_reading()[11]), "%3", str(request_reading()[12]), "C3", str(count3), "times3", str(request_reading()[14]))

                # Write the IMU data to the CSV
                try:
                        file1.write(str(request_reading()[0]) + "," + str(request_reading()[1]) + "," + str(request_reading()[2]) + "," + str(count1) + "," + str(request_reading()[4]) + "\n")
                except (KeyboardInterrupt, SystemExit):
                        file1.close()
                try:
                        file2.write(str(request_reading()[5]) + "," + str(request_reading()[6]) + "," + str(request_reading()[7]) + "," + str(count2) + "," + str(request_reading()[9]) + "\n")
                except (KeyboardInterrupt, SystemExit):
                        file2.close()
                try:
                        file3.write(str(request_reading()[10]) + "," + str(request_reading()[11]) + "," + str(request_reading()[12]) + "," + str(count3) + "," + str(request_reading()[14]) + "\n")
                except (KeyboardInterrupt, SystemExit):
                        file3.close()
                        
                # Reset variables
                count1 = 0
                count2 = 0
                count3 = 0

                processed_data = 0

                lux1acc = 0
                humid1acc = 0
                temp1acc = 0

                lux2acc = 0
                humid2acc = 0
                temp2acc = 0

                lux3acc = 0
                humid3acc = 0
                temp3acc = 0
