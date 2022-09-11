# Importing Libraries
import cv2
import mediapipe as mp
import sys
# Used to convert protobuf message to a dictionary.
from google.protobuf.json_format import MessageToDict
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

img2 = cv2.imread("Instructions.png", cv2.IMREAD_ANYCOLOR)

class Hands(object):
    hand_list = []
    previous_result = ""
    def __init__(self, name, count):
        self.name = name
        self.count = count

# Initializing the Model
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75,
    max_num_hands=2)
 
# Start capturing video from webcam
cap = cv2.VideoCapture(0)
 
while True:
    # Read video frame by frame
    success, img = cap.read()
    # cv2.imshow("Instructions", img2)
    # cv2.waitKey(0)
    # Flip the image(frame)
    img = cv2.flip(img, 1)
 
    # Convert BGR image to RGB image
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
 
    # Process the RGB image
    results = hands.process(imgRGB)

    if len(Hands.hand_list) > 8:
        print(Hands.hand_list)
        if Hands.hand_list.count('Both') > 4 and Hands.previous_result != "Both":
            print("Both hands")
            driver = webdriver.Chrome(executable_path='./chromedriver.exe')
            driver.maximize_window()
            driver.get("http://www.bfmtv.com/")
            driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div/div[2]/button[2]').click()
            Hands.previous_result = "Both"
        elif Hands.hand_list.count('Right') > 4 and Hands.previous_result != "Right":
            print("Right hand")
            driver = webdriver.Chrome(executable_path='./chromedriver.exe')
            driver.maximize_window()
            driver.get("http://www.google.com/")
            driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[3]/span/div/div/div/div[3]/div[1]/button[2]/div').click()
            Hands.previous_result = "Right"
        elif Hands.hand_list.count('Left') > 4 and Hands.previous_result != "Left":
            print("Left hand")
            driver = webdriver.Chrome(executable_path='./chromedriver.exe')
            driver.maximize_window()
            driver.get("http://www.youtube.com/")
            driver.find_element_by_xpath('/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[4]/div[2]/div[6]/div[1]/ytd-button-renderer[2]/a/tp-yt-paper-button').click()
            Hands.previous_result = "Left"

        Hands.hand_list = []

    # If hands are present in image(frame)
    if results.multi_hand_landmarks:
 
        # Both Hands are present in image(frame)
        if len(results.multi_handedness) == 2:
            Hands.hand_list.append('Both')
                # Display 'Both Hands' on the image
            cv2.putText(img, 'Both Hands', (250, 50),
                        cv2.FONT_HERSHEY_COMPLEX,
                        0.9, (0, 255, 0), 2)
 
        # If any hand present
        else:
            for i in results.multi_handedness:
               
                # Return whether it is Right or Left Hand
                label = MessageToDict(i)['classification'][0]['label']
 
                if label == 'Left':
                    Hands.hand_list.append('Left')
                    cv2.putText(img, label+' Hand',
                                (20, 50),
                                cv2.FONT_HERSHEY_COMPLEX,
                                0.9, (0, 255, 0), 2)
                    # Display 'Left Hand' on
                    # left side of window
 
                if label == 'Right':
                    Hands.hand_list.append('Right')
                    cv2.putText(img, label+' Hand', (460, 50),
                                cv2.FONT_HERSHEY_COMPLEX,
                                0.9, (0, 255, 0), 2)
                    
                    # Display 'Left Hand'
                    # on left side of window
 

    # Display Video and when 'q'
    # is entered, destroy the window
    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
        