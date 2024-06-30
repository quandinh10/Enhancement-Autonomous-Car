import cv2
import numpy as np
import math

# =====================ROI==================================
def roi(img,vertices):
    """
    This function will return a region of the image used for detection.
    img: source image
    vertices: list of vertices to form a region of the image
    """
    mask = np.zeros_like(img)
    cv2.fillPoly(mask,vertices,255) 
    masked_image=cv2.bitwise_and(img,mask)
    return masked_image

# =====================BISECTOR SLOPE=======================
def findSlopeBisector(ave_left_slope, ave_right_slope):
    angle_right = abs(np.degrees(np.arctan(ave_right_slope)))
    angle_left = abs(np.degrees(np.arctan(ave_left_slope)))
    angle_bisector = (180 - angle_left - angle_right)/2
    angle_bisector_slope = 180 - angle_bisector - angle_left
    slope = np.tan(np.radians(angle_bisector_slope))
    return slope
# =====================MID-POINT============================
def middle_lane_point(lines):
    """
    This function will return the middle point (x,y) of line
    lines: set of lines detected by the Hough algorithm
    """
    x_right_list = []
    x_left_list = []

    left_slope = []
    right_slope = []
    
    x_right = 720
    x_left = 0

    for line in lines:
        x1, y1, x2, y2 = line[0]
        
        if (max(y1,y2) <= 420):
            continue
        if (x2-x1) == 0:
            continue
        
        fit = np.polyfit((x1,x2), (y1,y2), 1)
        slope = fit[0]
        ave_x = (x1+x2)/2

        if slope < 0: 
            x_left_list.append(ave_x)
            left_slope.append(slope)
        else:
            x_right_list.append(ave_x)
            right_slope.append(slope)
       
    if len(x_left_list) == 0:
        x_left = -200
    else:
        x_left = np.average(x_left_list)
    if len(x_right_list) == 0:
        x_right = 920
    else:
        x_right = np.average(x_right_list)

    x_slope = None
    
    if len(left_slope) != 0 and len(right_slope) != 0:
        ave_left_slope = np.average(left_slope)
        ave_right_slope = np.average(right_slope)
        x_slope = findSlopeBisector(ave_left_slope,ave_right_slope)
    
    elif len(left_slope) != 0 and len(right_slope) == 0:
        x_slope = np.average(left_slope, axis=0)
    
    elif len(left_slope) == 0 and len(right_slope) != 0:
        x_slope = np.average(right_slope, axis=0)

    deviation_angle = 0
    if x_slope is not None:
        angle = np.degrees(np.arctan(x_slope))
        if (angle > 0):
            deviation_angle = -(90 - angle)
        else:
            deviation_angle = 90-abs(angle)

    x = int((x_right+x_left)/2)
    
    return (x, 400), x_slope, deviation_angle

# =====================LANE_TRACKING========================
def lane_tracking(edges):
    """
    This function will use the Hough algorithm to detect lines and return
    list of lines, mid-point of those lines and slope of bisector line.
    img: input image  
    """
    lines_list =[]
    lines = cv2.HoughLinesP(
                edges, # Input edge image
                1, # Distance resolution in pixels
                np.pi/180, # Angle resolution in radians
                threshold=30, # Min number of votes for valid line
                minLineLength=10, # Min allowed length of line
                maxLineGap=4# Max allowed gap between line for joining them
                )
    if lines is None:
        return [],(360,400),None,0
    for points in lines:
        # Extracted points nested in the list
        x1,y1,x2,y2=points[0]
        lines_list.append([x1,y1,x2,y2])
    (x,y), slope, deviaton_angle = middle_lane_point(lines)
    return lines_list, (x,y), slope, deviaton_angle

# =====================K-MEANS CLUSTERING===================
def kmeans_clustering(data, k, max_iterations=100):
    """
    This function will return a list of clusters representing start, middle
    and end of line segment. 
    """
    data = np.array(data)
    centroids = data[np.random.choice(len(data), size=k, replace=True)]
    
    for _ in range(max_iterations):
        distances = np.sqrt(np.sum((data[:, np.newaxis] - centroids) ** 2, axis=2))
        clusters = np.argmin(distances, axis=1)
        
        new_centroids = []
        for i in range(k):
            cluster_points = data[clusters == i]
            if len(cluster_points) > 0:
                new_centroid = np.mean(cluster_points, axis=0)
            else:
                new_centroid = data[np.random.choice(len(data))]
            new_centroids.append(new_centroid)
        new_centroids = np.array(new_centroids)
        
        if np.all(centroids == new_centroids):
            break
        
        centroids = new_centroids
    
    return clusters, centroids


# =====================PREPROCESSING========================
def process_image(image, roi_vertices):
    """
    This function will preprocess image and crop desired part of image
    """
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    equ = cv2.equalizeHist(gray_img)
    blur_img = cv2.blur(equ, (5,5), cv2.BORDER_DEFAULT) 
    edges = cv2.Canny(blur_img,190,230,None, 3)
    cropped_img = roi(edges, np.array([roi_vertices],np.int32))
    return cropped_img    