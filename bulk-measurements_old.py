                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                (np.mean(y_eye),0))
            circle_right[2] = int(np.round((shape[39,0]-circle_right[0])/2))
            message = 'Both Eyes Closed'
            
            
            
        
        
        rot_angle, center = estimate_line(circle_left, circle_right)
        
        
        
        x=shape[0:3,1]
        y=shape[0:3,0]

        extreme_right = find_extreme(x,y, 'right')
        
        
        R2=linearity(x,y)
        if R2 < 0.8: #if the points are not in a line then fit a circle
            circle = find_circle_from_points(x,y)
            radius_right = circle[2]
        else:
            radius_right = np.inf
            
        x=shape[14:17,1]
        x=x[::-1]
        y=shape[14:17,0]
        y=y[::-1]
        
        extreme_left = find_extreme(x,y, 'left')
        
        R2=linearity(x,y)
        if R2 < 0.8: #if the points are not in a line then fit a circle
            circle = find_circle_from_points(x,y)
            radius_left = circle[2]
        else:
            radius_left = np.inf
            
        #use this functio if you want to save a photo of the results
        save_picture(path, file, shape,circle_left, circle_right, rot_angle, center, extreme_left, extreme_right)
            
        _, distance_left, distance_right = distance(extreme_left, extreme_right, center, rot_angle)
        radius_iris=(circle_left[2]+circle_right[2])/2
        distance_left = abs(distance_left)*(11.77/(2*radius_iris))
        distance_right = abs(distance_right)*(11.77/(2*radius_iris))
        
        files.append(file[:-4])
        
        #temp_results = np.array([extreme_right,extreme_left,radius_right,radius_left])
        results = np.append(results, [[np.round(distance_right,3),np.round(distance_left,3),np.round(radius_right,3),np.round(radius_left,3)]], axis=0)
        eye_status = np.append(eye_status, [[message]], axis = 0)
    
    results = np.delete(results, 0, 0)
    eye_status = np.delete(eye_status, 0, 0)
    

    
    return files, eye_status, results

import os
import cv2
import numpy as np
from scipy import linalg
import pandas as pd

if __name__ == '__main__':

    path = r'C:\Users\GUARIND\Downloads\temp_folder\bulk measurement\others'
    path = r'C:\Users\GUARIND\Downloads\temp_folder\bulk measurement\TextFilesPedi'
    files, eye_status, results = main(path)      
    
    columns = ['Eyes Status','Right Distance', 'Left Distance', 'Right Radius', 'Left Radius']
    
    final_results = np.append(eye_status, results, axis =1)
    
    df = pd.DataFrame(final_results, index = files, columns = columns)
    file_name = path + os.path.sep + 'results.xlsx'
    #df.to_excel(file_name, index = True, sheet_name='results')
    
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, index = True, sheet_name='results')

    # Get the xlsxwriter workbook and worksheet objects.
    workbook  = writer.book
    worksheet = writer.sheets['results']

    # Add some cell formats.
    format_colums = workbook.add_format({'num_format': '0.00'})

    # Set the column width and format.
    worksheet.set_column('C:F', 12, format_colums)

    # Set column width.
    worksheet.set_column('A:B', 16, None)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    
    