import cv2 
import mediapipe as mp 
import time
import serial  

arduino = serial.Serial(port='COM4', baudrate=9600, timeout=0.1) 

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=1,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5) 
mpDraw = mp.solutions.drawing_utils 

arr_x=[0]*10
arr_y=[0]*10 
length = [0]*5 
calib = [0]*5
permit = False 

ladonx1=0
ladony1=0

while True: 
    success, img = cap.read() 
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB) 
    #print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks: 
            for id, lm in enumerate(handLms.landmark):

                h, w, c = img.shape 
                cx, cy = int(lm.x * w), int(lm.y * h) 
                cv2.circle(img, (cx, cy), 10, (200, 0, 255), cv2.FILLED) 

                if id == 0:
                    ladonx1=cx
                    ladony1=cy
                i = 0  
                for count in range(1,18,4):
                    if id == count:
                        arr_x[i] = cx
                        arr_y[i] = cy
                    elif id == count+3:
                        arr_x[i+1] = cx
                        arr_y[i+1] = cy
                    i+=2
                
                for kek in range(0,10,2): 

                    cv2.line(img, (arr_x[kek], arr_y[kek]), (arr_x[kek+1], arr_y[kek+1]), (255, 0, 0), 7) 

                    length[int(kek/2)] = ((((arr_x[kek+1] - arr_x[kek]) ** 2) + ((arr_y[kek+1] - arr_y[kek]) ** 2)) ** 0.5) 

                cv2.line(img, (ladonx1, ladony1), (arr_x[4], arr_y[4]), (255, 0, 255), 7) 
                prop = ((((arr_x[4] - ladonx1) ** 2) + ((arr_y[4] - ladony1) ** 2)) ** 0.5) 
            if cv2.waitKey(1) & 0xFF == ord('c'):
                    for j in range(0, 5, 1):
                        calib[j] = length[j] / prop 
                        print("Calibration ", calib[j])
                    permit = True
            if permit == True:
                    if length[0] / prop <= calib[0] - 0.05:
                        #arduino.write(bytes(str(0), 'utf-8'))
                        print("ON: ", 1)
                    else:
                        #arduino.write(bytes(str(5), 'utf-8'))
                    for k in range(1, 5, 1):
                        if length[k]/prop <= calib[k] - 0.2: 
                            arduino.write(bytes(str(k), 'utf-8'))
                            print("ON: ", k+1)
                        else:
                            arduino.write(bytes(str(k + 5), 'utf-8')) 
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS) 

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
