"""
Indiviual assignment - AE4317 Autonomous Flight of Micro-Air-Vehicles 
Timon Rowntree (4544927)

Gate detection with colour filter 

"""

#%% Importing the relevant modules & starting timer 

import numpy as np
import cv2
import matplotlib.pyplot as plt
import timeit

start = timeit.default_timer()

#SECTION 1 
#%% Selecting which images you would like to analyse and which to display;

#Image lists for the 4 gates & total 
image_lst_gate1 = [6] + list(range(8,14)) + list(range(18,29)) + list(range(31,37)) + [39,41,42,43,45,46,47,48] + list(range(51,69)) + list(range(71,74))
image_lst_gate2 = list(range(110,117)) + list(range(124,200)) + [202,203,204,205]
image_lst_gate3 = list(range(232,243)) + list(range(246, 331))
image_lst_gate4 = list(range(370,374)) + list(range(382,393)) + list(range(396,438))
image_lst_total = image_lst_gate1 + image_lst_gate2 + image_lst_gate3 + image_lst_gate4
image_lst_specific = [410]  

selected = image_lst_total   #SELECT IMAGES you would like to see here! 
no_gates = []                   #For later use - when the algorithm doesn' find a gate 

#Displaying images? 
OG_plot = False         #Plotting the original image  
CM_plot = False         #Plotting the image after colourmask 
Filter_plot = False     #Plotting the image after filter 
End_plot = True         #Plotting the image with computed middle of gates 


#%% Getting the images from folder 'WashingtonOBRace' 
num = 0 
# Running through this loop; once for every image (for analysing multiple in one run)
for i in range(len(selected)): 
    num = num + 1                   
    image_nr = selected[i]                                               
    image_folder = "WashingtonOBRace"            
    image_prefix = '\img_'                         
    image_type = '.png'
    
    im_loc = image_folder + image_prefix + str(image_nr) + image_type    
    img = cv2.imread(im_loc)                            
    RGB_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    
    #Showing original image in plot 
    if OG_plot: 
        plt.figure()
        plt.imshow(RGB_img) 
        plt.title('Image' + str(image_nr) + ' - Original Image')
    
    
#SECTION 2   
    #%% Filter for enhancing sides of the gates  
    
    HSV_img = cv2.cvtColor(RGB_img, cv2.COLOR_RGB2HSV)    #As a matrix of [H,S,V] colour values
    
    colormask = np.zeros_like(HSV_img)
    colormask[:,:,0] += 0                       #Adjusting H values 
    colormask[:,:,1] += 0                       #Adjusting S values 
    colormask[:,:,2] += 50                      #Adjusting V values  - 50 works nice        
    
    HSV_img  += colormask                       #Applying colormask             
    
    #Plotting image plus colourmask 
    if CM_plot: 
        plt.figure()
        plt.imshow(HSV_img) 
        plt.title('Image' + str(image_nr) + ' - After Colourmask')
    
    
    New_img = HSV_img.copy()
    New_img[New_img[:, :, 0] >= 120] = 0            #Filtering Hue - 120 works nice 
    New_img[New_img[:, :, 1] <= 115] = 0            #Filtering Saturation - 115 works nice 
    
    if Filter_plot: 
        plt.figure()
        plt.imshow(New_img) 
        plt.title('Image' + str(image_nr) + ' - After Filter')
    
    
    #Making image with 0's and 1's for counting later on 
    Counter_img = np.zeros_like(New_img[:, :, 0])
    Counter_img[New_img[:, :, 0] >= 1] = 1
    Counter_img[New_img[:, :, 0] >= 1] = 1
    Counter_img[New_img[:, :, 0] >= 1] = 1
    Counter_img[New_img[:, :, 0] <= 1] = 0          #Counter image is 360 x 360 with 0 or 1 
   
    
#SECTION 3     
#%% Making the image smaller, removing from top and bottom 
    

    #Top & bottom 
    first_row = 90       #From top 
    last_row = 330       #to bottom  
    
    first_col = 30       #From left 
    last_col = 330       #to right  
    
    Counter_img = Counter_img[first_row:last_row, first_col:last_col]    #Making the changes 
    
    
#SECTION 4    
#%% Making arr - array with sums of pixels per area i,j 

    #Rows and columns
    row_num = 20      # Defining how many rows in a 'mini_array' 
    col_num = 20        # Defining how many columns in a 'mini_array' 
    
    rows = np.shape(Counter_img)[0]         # Total number of pixels in row  
    columns = np.shape(Counter_img)[1]      # Total number of pixels in column 
    
    pixels_x = columns/col_num              # For the mini array 
    pixels_y = rows/row_num                 # For the mini array 
    
    #Making arr - with the amount of pixels per area of the image 
    arr = np.zeros((row_num, col_num))      # Array with % of theoretical max fill value 
    for i in range(row_num): 
        for j in range(col_num): 
            mini_array =  Counter_img[i*int(rows/row_num):(i+1)*int(rows/row_num), j*int(columns/col_num):(j+1)*int((columns/col_num))]
            arr[i][j] = round(np.sum(100*mini_array)/(rows*columns/(row_num*col_num)),2)     #Percentage of max 


#SECTION 5 
#%% Making array (arr) with 0's and 1's  
    
    #Finding Guess of x of pillar 1 - using it for setting threshold
    col_sums = []
    for i in range(col_num):
        col_sums.append(np.sum(arr[:, i]))
    
    x_pillar1_guess = col_sums.index(max(col_sums))  #Index of highest number 
    
    
    #Defining a threshold - above this will be set to 1, below this will be set to 0 
    a = list(arr[:, x_pillar1_guess])     
    max_val = max(a)
    threshold = max(a) - 40             
    
    #Setting values below threshold to 0 
    for i in range(row_num):
        for j in range(col_num): 
            if arr[i][j] <= threshold: 
                arr[i][j] = 0
    
    #Setting other values to 1 
    arr[arr >= 1] = 1 
    

#SECTION 6
#%% Finding X-coordinates of pillars - IF THERE IS A PILLAR! 
    
    #Finding column with has highest sum (when also taking the one to the left and to the right of it)
    col_sums = [] 
    for i in range(col_num):
        if i != 0 and i != col_num-1:
            
            #Column i is weighted double, such that that row actually gets highest number 
            col_sums.append(3*np.sum(arr[:, i]) + np.sum(arr[:, i-1]) + np.sum(arr[:, i+1]))
            
        else: 
            col_sums.append(0)
    
    #Finding the x of pillar 1 - the most certain pillar 
    x_pillar1 = col_sums.index(max(col_sums))  
    
    #Defining the gap that must exist before identifying new pilar (or else you get two columns on the same pillar!)
    xwidth_zeros = int(col_num * 0.20) 
    
    #Copying col_sums
    col_sums2 = col_sums.copy()                             
    
    #Setting values around x_pillar1 to 0 
    for i in range(xwidth_zeros + 1):
        if (x_pillar1 - i) >=  0:  
             col_sums2[x_pillar1 - i] = 0
        if (x_pillar1 + i) <= col_num -1:
             col_sums2[x_pillar1 + i] = 0
             
    ##Finding the x of pillar 2         
    x_pillar2 = col_sums2.index(max(col_sums2))
    

#SECTION 7
#%% Finding y-values 
    
    arr1 = arr[:, x_pillar1]   
    arr2 = arr[:, x_pillar2]     
    
    if sum(arr1) > 0 and sum(arr2) > 0:         #Checking if there are any pillar points! 
        
        indices1 = []
        indices2 = []
        for i in range(len(arr1)): 
            if arr1[i] == 1:
                indices1.append(i)
            if arr2[i] == 1:
                indices2.append(i)
        
        #Y location taken at mean of the location where arr has 1's 
        y_pillar1 = round(np.mean(indices1))
        y_pillar2 = round(np.mean(indices2))
    

#SECTION 8
    #%% Collecting X & Y for posts - computing location of centers of posts & finding middle    
          
        #Output of the gate detection algorithm 
        posts = [[x_pillar1, y_pillar1], [x_pillar2, y_pillar2]]       #Collected in list [post1, post2]   
    
    
        #Computing x, y coordinates of the 2 posts - in pixels 
        loc_1_x, loc_1_y = (posts[0][0] + 0.5)*pixels_x , (posts[0][1] + 0.5)*pixels_y
        loc_2_x, loc_2_y = (posts[1][0] + 0.5)*pixels_x , (posts[1][1] + 0.5)*pixels_y
    
    
        #Computing x, y coordinates of the estimated gate centre point - in pixels 
        middle_x = (loc_1_x + loc_2_x)*0.5 
        middle_y = (loc_1_y + loc_2_y)*0.5 
    
        
        
    #%% Showing adapted image in plot, including 3 dots: left pillar, right pillar, centre 
    
        RGB_img = RGB_img[first_row:last_row, first_col:last_col]       #Scaling original image
        
        if End_plot:
            plt.figure();
            plt.plot(loc_1_x, loc_1_y,'ro')
            plt.plot(middle_x,middle_y,'ro') 
            plt.plot(loc_2_x, loc_2_y,'ro')
            plt.imshow(RGB_img); 
            plt.title('Image' + str(image_nr) + ' - Final'); 
    
    else: 
        no_gates.append(image_nr)
    
    
#%% Computing runtime of the loop 

stop = timeit.default_timer()
print('')
print('Run time: ', round(stop - start,3), 'seconds') 
print('Done with computing!')
print(num, 'images analysed')

if len(no_gates) > 0:
    print('No gates at: ', no_gates)    
    
    
    