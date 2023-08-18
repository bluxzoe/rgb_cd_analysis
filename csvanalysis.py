'''
This code works in tandem with my rgb_analysis code that I made for ImageJ
Certain functions can and should be adapted if the source csv files have different formats 
'''

import numpy as np
import os
import sys
import math
import matplotlib.pyplot as plt




#=============  get the info from user  =============
'''
This function
1. explains to the user what it will ask them
2. saves the path of the directory given by the user
3. saves the name of all the files in the directory
'''
def hellouser():
    print("The program will ask for three folders:\n1. Contrast difference\n2. Flake \n3. Background\nin this specific order.")
    print("please input the directory of said folders in the correct order")

    print("\nCONTRAST DIFFERENCE")
    cd_path = getdirectory() #path
    cd_files = os.listdir(cd_path) #file names
    cd_files = removefiles(cd_files)
            
    cd_file_list = namefiles(cd_path,cd_files) #each file's respective path

    print("\nFLAKE")
    flake_path = getdirectory()
    flake_files = os.listdir(flake_path)
    flake_files = removefiles(flake_files)
    
    flake_file_list = namefiles(flake_path,flake_files)

    print("\nBACKGROUND")
    bg_path = getdirectory()
    bg_files = os.listdir(bg_path)
    bg_files = removefiles(bg_files)
    bg_file_list = namefiles(bg_path,bg_files)

    return cd_file_list, flake_file_list, bg_file_list, cd_files, flake_files, bg_files




#=============  remove useless files from the analysis  =============
'''
This function:
1. saves all the indicies of files that are not .csv files
2. removes each of these files from the list
3. returns the corrected list
'''
def removefiles(file_list):
    remove = []
    i = 0
    for files in file_list:
        if files.endswith('.csv') == False:
            remove.append(i)
        i+=1
    
    for x in remove:
        del file_list[x]

    return file_list



    
#=============  get the directory  =============
'''
This function
1. asks for the full directory path
2. makes sure the folder path exists, exits if the user wishes to
3. rewrites it in a way that python can understand
    (this is tricky because backslashes are escape caracters, treated differently
     another way to do this is take the raw file r'file\directory')
'''
def getdirectory():
    folder_path = 0
    p = 0

    while folder_path == 0:
        folder_path = input('Paste the path of directory below\n : ').strip('\"\'')

    
        if folder_path == 'e':
            sys.exit()

        if not os.path.isdir(folder_path):
            print('Invalid folder path. \nPlease provide a valid directory path.\nPress e to exit/end program')
            folder_path = 0

    return folder_path




#=============  rename all files as their full directory  =============
'''
This function
1. renames all files saved as their full path by joining their path and file name together
'''
def namefiles(path,files):
    file_list = []
    
    for fname in files:
        newpath = os.path.join(path,fname)
        file_list.append(newpath)
        
    return file_list




#=============  get the relevant info for the flake and background  =============
'''
This function 
1. takes the list of file paths
    for each file path:
2. loads the csv file's text, ommits the header (you can change this if you have no header)
3. saves the relevant info, in my case it takes the mean and standard deviation
    each respectively located in the 2nd and 3rd columns of my csv files.
4. replaces the file path in the list by the relevant info 
'''
def fbindexer(x_file_list):
    for i in range(len(x_file_list)):
        #2
        data = np.loadtxt(x_file_list[i], skiprows = 1, delimiter = ',') #skip the first row because of header, if no header, change for skiprows = 0

        mean = data[:,1]
        std = data[:,2]

        #3
        a = np.array([mean,std])
        x = np.transpose(a)

        #4    
        x_file_list[i] = x

    return x_file_list




#=============  get the relevant info for the line profile analysis  =============
'''
This function is the same as the previous but it only takes the last column of the csv file
'''
def cdindexer(x_file_list):
    for i in range(len(x_file_list)):
        data = np.loadtxt(x_file_list[i], skiprows = 1, delimiter = ',')

        info = data[:,2]
        x = np.transpose(info)
            
        x_file_list[i] = x

    return x_file_list




#============= RGB colour difference using the first method (flake - bg measurements)  =============
'''
This function:
1. creates an array of the same shape as the data, filled with zeroes
2. stores the results of flake-bg difference in the newly created array, first column
3. saves also the standard deviation, second column
'''
def fbanalysis(a,b):
    results = np.zeros(np.shape(b))
    i = 0
    while i < len(results):
        #colour difference of red, green and blue
        results[i][0][0] = a[i][0][0]-b[i][0][0]
        results[i][1][0] = a[i][1][0]-b[i][1][0]
        results[i][2][0] = a[i][2][0]-b[i][2][0]

        #standard deviation calculation
        results[i][0][1] = stddev((a[i][0][1]),(b[i][0][1]))
        results[i][1][1] = stddev((a[i][1][1]),(b[i][1][1]))
        results[i][2][1] = stddev((a[i][2][1]),(b[i][2][1]))
        
        i+=1
        
    return results




#============  create the array of results for lineprofile
'''
This function:
1. creates the array of results using the size of the array of data we have
2. calls the function that will analyse all data points
3. inputs the results in the array
'''
def lineprofileresults(data):
    results = np.zeros((len(data),2))
    for i in range(len(data)):
        x = cdanalysis(data[i])
        results[i][0],results[i][1] = x

    return results


#=============  RGB colour difference using second method (line profile) =============
'''
This function
1. verifies how many data points there are
2. leaves out around 10 data points
3. creates lists of the first and last datapoints (of equal length)
4. calculates the mean of each set of datapoints
5. calculates the standard deviation of each set
6. creates an array that has as many rows as there are datapoints in the lists, and 2 columns
7. inputs the results in the array
'''
def cdanalysis(c):


    #1
    if len(c)%2 == 0:
        points = (len(c)/2)-5
        
    else:
        points = ((len(c)+1)/2)-5
        

    #3
    flake = c[:int(points)]
    bg = c[-int(points):]
    
    #4
    fmean = sum(flake)/len(flake) 
    bgmean = sum(bg)/len(bg)
 
    #5
    fdev = stddev_calculations(fmean,flake)
    bgdev = stddev_calculations(bgmean,bg)

    difference = fmean-bgmean
    deviation = stddev(fdev,bgdev)

    return difference, deviation




#=============  calculates the standard deviation of two measurements summed up  =============    
def stddev(a,b):
    #σ_sum = sqrt[ (σ_a)^2 + (σ_b)^2 ]
    c = math.sqrt( a**2 + b**2)

    return c




#=============  calculates the standard deviation of a list  =============
def stddev_calculations(mean,data):
    x_i = []
    for i in data:
        x = (i-mean)**2
        x_i.append(x)
   
    sums = sum(x_i)
    length = len(x_i)

    c = math.sqrt(sums/length)

    return c




#=============  creating plots  =============
def plottingrgb(data):
    red_i = []
    green_i = []
    blue_i = []
    for i in range(len(data)):
        if i%3 == 0:
            blue_i.append(i)

        elif i%2 == 0:
            red_i.append(i)

        else:
            green_i.append(i)

    x = 
            

def plotting
    

#************** main **************

#get data and file names
cd_data, flake_data, bg_data, cd_files, flake_files, bg_files = hellouser()

#rearrange arrays
cdindexer(cd_data)
fbindexer(flake_data)
fbindexer(bg_data)

#process results
fbresults = fbanalysis(flake_data,bg_data)
lineprofile = lineprofileresults(cd_data)

#plot data
plottingcd(lineprofile,cd_files)

#======================================== WHAT I WANT MY CODE TO DO ========================================#

'''
1. assign to a variable the csv files of FLAKE ANALYSIS (flake) #DONE
2. assign to a variable the csv files of BG ANALYSIS    (bg) #DONE
3. assign to a variable the csv files of CD ANALYSIS    (cd) #DONE

========== Flake analysis - BG analysis ==========
1. open fl_a[i] and bg_a[i] #DONE
2. take column "Mean" of fl_a and bg_a #DONE
3. Δr = fl_a[0] - bg_a[0] #DONE
4. Δg = fl_a[1] - bg_a[0] #DONE
5. Δb = fl_a[2] - bg_a[0] #DONE
6. take column "StdDev" of fl_a and bg_a #DONE
7. σ_sum[0] = sqrt[ (σ_fl[0])^2 + (σ_bg[0])^2 ] #DONE
8. σ_sum[1] #DONE
9. σ_sum[2] #DONE

========== CD analysis ==========
PROBLEM: i have realized that the R,G and B channels are saved seperately for each file image ...

1. open cd_a[i] #DONE
2. take last column of cd_a[i] #DONE
3a. if #rows is pair: devide by two (ie 50 -> 25/25) #DONE
    substract 5 values from each group (25/25 -> 20/20)
    take the first x values and the last x values (first and last 20 values)
3b. if #rows is odd: add +1, devide by 2 (ie 51 -> 52 -> 26/26) #DONE
    substract 6 values from each group (26/26 -> 20/20)
    
4. calculate the mean of each group m = \frac{\text{sum of the terms}}{\text{number of terms}} #DONE
5. calculate the stdev of each group \sigma={\sqrt {\frac {\sum(x_{i}-{\mu})^{2}}{N}}} #DONE
        where
            σ = st dev
            N = size
            x_{i} = each value
            μ = mean


========== outputting data ==========
1. seperate all the data
2. go one by one through the file names
3. for one file, go one by one through the seperated lists
4. when at exp, if 


====reminders=======
number of rows = len(cd_file_list[1])
number of columns = len(cd_file_list[1][0])

to access information within the matricies:

    bg_data[0] = RGB results chromaticity_S2_F4_exp100_int10_bottomleft.tif BG.csv
    = array([[99.092,  0.583],
           [71.96 ,  0.821],
           [82.492,  0.914]])

    bg_data[0][0][0] = 99.092   bg_data[0][0][1] = 0.583
    bg_data[0][1][0] = 71.96    bg_data[0][1][1] = 0.821
    bg_data[0][2][0] = 82.492   bg_data[0][2][1] = 0.914

    BASICALLY
    matrix_name[file][row][column]

'''

