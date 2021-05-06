"""

#README 

Some information on running the computer vision algorithm 


-------------------------------------------------------------------

RUNNING of the program 

The program is setup in such a way that it should be trivial to run, and even adapt for new 
sets of images. 


1. Make sure the set of images is in the same folder as where the program is saved
The name of the folder with images can be changed under the variable: image_folder in line 43 


2. In line 29 - change list of images you would like to analyse to: 
    
    - Gate1
    - Gate2
    - Gate3 
    - Gate4 
    - total (for seeing the entire dataset)
    - specific (for seeing a specific image)

3. In line 33-36 - set which images you would like to see, choosing (multiple) from:
    
    - OG plot: The original image 
    - CM plot: The image after the colourmask (where H, S, V can be changed)
    - Filter plot: The image where the filter has been applied 
    - End plot: The final (cropped) plot where dots have been ploted for 
        a) Left 'pillar'
        b) Right 'pillar'
        c) Predicted middle of the gate 


-----------------------------------------------------------------

STRUCTURE of the program: 8 sections 

1. Image importing & creating RGB image 
2. Application of Colour Filter 
3. Reducing image size 
4. Discretising image (NxN) & finding amount of remaining pixels per area as % of theoretical max 
5. Setting threshold and converting to 0's (no colour) and 1's (colour) 
6. Finding x-coordinates of a gate pillars 
7. Finding y-coordinates - middle of gate pillar 
8. Finding centre of gates 

All of these sections are given in the code as SECTION X  
They are also explained in the report, under section 'III- EXPLANATION OF COMPUTER VISION
ALGORITHM'. 

    




"""