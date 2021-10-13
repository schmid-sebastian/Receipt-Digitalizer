import os
import cv2
import pandas as pd
import numpy as np

def order_points(coordinates):
    """Orders four coordinates of an image so that the 
    first row corresponds to the top-left coordinate, 
    the second row to the top-right coordinate, the third
    row to the bottom-right and the fourth row to the bottom-left
    coordinate."""
    rectangle = np.zeros((4, 2), dtype = "float32")
    sums = coordinates.sum(axis = 1)
    rectangle[0] = coordinates[np.argmin(sums)]
    rectangle[2] = coordinates[np.argmax(sums)]
    diff = np.diff(coordinates, axis = 1)
    rectangle[1] = coordinates[np.argmin(diff)]
    rectangle[3] = coordinates[np.argmax(diff)]
    return rectangle

def to_tuple(a):
    try:
        return tuple(to_tuple(i) for i in a)
    except TypeError:
        return a

def scale_size(x, y, max_x, max_y):
    """Scales two coordinates x and y so that
    they keep their ratio until either max_x or
    max_y is reached."""
    if (x > y):
        x_increment = 1
        y_increment = y/x
    elif (x < y):
        x_increment = x/y
        y_increment = 1
    else:
        x_increment = 1
        y_increment = 1
    if((x <= max_x) and (y <= max_y)):
        while(True):
            if((x + x_increment >= max_x) or (y + y_increment >= max_x)):
                return x, y
            else:
                x = x + x_increment
                y = y + y_increment
    else:
        while(True):
            if((x <= max_x) and (y  <= max_y)):
                return x, y
            else:
                x = x - x_increment
                y = y - y_increment

def click_event(event, x, y, flags, params):
    """Saves the clicked coordinate as well as marks 
    the points in the image with circles or a rectangle."""
    global coordinates
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, ' ', y)
        coordinates.append((x, y))
        cv2.circle(img, (x,y), 5, (255,0,0), thickness=-1)
        if len(coordinates) == 4:
            coordinates = order_points(np.array(coordinates))
            temp = to_tuple(coordinates)
            cv2.line(img, temp[0], temp[1], (255,0,0), thickness=10)
            cv2.line(img, temp[1], temp[2], (255,0,0), thickness=10)
            cv2.line(img, temp[2], temp[3], (255,0,0), thickness=10)
            cv2.line(img, temp[3], temp[0], (255,0,0), thickness=10)
        cv2.imshow('image', img)


if __name__ == "__main__":
    df_labels = pd.read_csv('labels.csv')
    label_count = df_labels.sort_values(by='count', ascending=False).iloc[0,0]
    files = [x for x in os.listdir('dataset/') if int(x.split('.')[0]) > label_count]
    image_count = 0
    index = []
    labels = []

    while True:
        if(image_count == len(files)):
            cv2.destroyAllWindows()
            break
        print("Current_file:", files[image_count], "\nProgress:", label_count + image_count, "of: ", label_count + len(files))
        coordinates = []
        img = cv2.imread('dataset/' + files[image_count])
        y, x, z = img.shape
        x_scaled, y_scaled = scale_size(x, y, 1500, 800)
        cv2.namedWindow('image',cv2.WINDOW_NORMAL)
        cv2.resizeWindow('image', (int(x_scaled), int(y_scaled)))
        cv2.imshow('image', img)
        cv2.setMouseCallback('image', click_event) # setting mouse handler with our click_event function
        
        k = cv2.waitKey(-1) # wait for a key to be pressed to continue
        if k & 0xFF == 27: # ESC-Key
            cv2.destroyAllWindows()
            break
        elif(k & 0xFF == 32):
            continue
        else:
            if(len(coordinates) != 4):
                continue
            else:
                image_count += 1
                index.append(label_count + image_count)
                labels.append((coordinates[0, 0], coordinates[0, 1], coordinates[1, 0], coordinates[1, 1], 
                               coordinates[2, 0], coordinates[2, 1], coordinates[3, 0], coordinates[3, 1]))
                continue
    data = {'count' : index, 'label' : labels}
    df_labels = df_labels.append(pd.DataFrame(data))
    df_labels.to_csv('labels.csv', index=False)