# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 01:40:57 2023

@author: kehinde
"""

###Install Libraries
#!pip install retina-face
#!pip install EMD-signal


###Import Libraries
import cv2
import csv
from imutils import face_utils
import subprocess
import dlib
from naoqi import ALProxy
import numpy as np
import os
import time
from sklearn.decomposition import FastICA
from scipy.signal import butter, lfilter, filtfilt, detrend, find_peaks
from PyEMD import EMD

##---------------------------VitalSign Class---------------------------##

class vitalsigns:
    def __init__ (self, dat_path, HeartRate_lowcut,HeartRate_highcut, Sp02_lowcut, Sp02_highcut, spo2_cutoff, order, distance):
        # Define the parameters of the computation
        self.HeartRate_lowcut = HeartRate_lowcut  # Hz
        self.HeartRate_highcut = HeartRate_highcut # Hz
        self.Sp02_lowcut = Sp02_lowcut
        self.Sp02_highcut = Sp02_highcut
        self.spo2_cutoff = spo2_cutoff
        self.order = order
        self.distance = distance
        ###Load DLIB face landmark predictor
        self.dat = dat_path
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(self.dat)
        
    def DLIB_face_dector(self,  image):
 
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        rects = self.detector(gray, 0)
        # For each detected face, find the landmark.
        for (i, rect) in enumerate(rects):
            # Make the prediction and transfom it to numpy array
            shape = self.predictor(gray, rect)
            shape = face_utils.shape_to_np(shape) ##Shape contains 68 landmarks
            
            #CALCULATE MID EYE LEVEL
            eye_left = [shape[36][0] + (shape[39][0] - shape[36][0])/2, (shape[39][1]+shape[39][1])/2]
            eye_right = [shape[42][0] + (shape[45][0] - shape[42][0])/2, (shape[45][1]+shape[39][1])/2]
            
            eyelid_left = list(shape[19])
            eyelid_right = list(shape[24])
            
            nose_top = list(shape[30])
            nose_bottom = list(shape[33])
            
            mouth_left = list(shape[48])
            mouth_right = list(shape[54])
            
            left_eye_corner = list(shape[36])
            right_eye_corner = list(shape[45])
        
         
        #Function to extract bounding box from https://pyimagesearch.com/2021/04/19/face-detection-with-dlib-hog-and-cnn/ 
        def convert_and_trim_bb(image, rect):
        	# extract the starting and ending (x, y)-coordinates of the bounding box
        	startX = rect.left()
        	startY = rect.top()
        	endX = rect.right()
        	endY = rect.bottom()
        	# ensure the bounding box coordinates fall within the spatial dimensions of the image
        	startX = max(0, startX)
        	startY = max(0, startY)
        	endX = min(endX, image.shape[1])
        	endY = min(endY, image.shape[0])
        	# compute the width and height of the bounding box
        	w = endX - startX
        	h = endY - startY
        	# return our bounding box coordinates
        	return (startX, startY, w, h)

        boxes = [convert_and_trim_bb(image, r) for r in rects]
        if len(boxes) == 0: ##No face detected
            return False
            
        else:
            boxes = boxes[0]
        
            ##Put relevant information in a dictionary
            facial_result = {'facial_area': [boxes[0], boxes[1], boxes[0]+boxes[2], boxes[1]+boxes[3]], 
                             'right_eye': eye_left, 
                             'left_eye': eye_right, 
                             'eyelid_left': eyelid_left,
                             'eyelid_right': eyelid_right,
                             'left_eye_corner': left_eye_corner,
                             'right_eye_corner': right_eye_corner,
                             'nose': nose_top, 
                             'nose_bottom': nose_bottom,
                             'mouth_left': mouth_left, 
                             'mouth_right': mouth_right
                             }
            return facial_result

    def Extract_forehead_ROI(self, image, face_info):
        f = face_info
        ### Face boundary dimensions
        H = f["facial_area"][3] - f["facial_area"][1] ##hieght of bounding box        

        h3 = f['mouth_left'][1] - f['left_eye'][1]
        
        ##Forehead ROI
        forehead_coord = [f["eyelid_left"][0], f["facial_area"][1] - H/16, f["eyelid_right"][0], f["eyelid_right"][1]]
        ROI_forehead = image[int(forehead_coord[1]):int(forehead_coord[3]), int(forehead_coord[0]):int(forehead_coord[2])]

        
        ##left cheek
        ##coord = [start_x, start_y, end_x, end_y]
        left_cheek_coord = [f['left_eye_corner'][0], f['left_eye'][1] + (0.2 * h3), f['mouth_left'][0], f['nose_bottom'][1]]
        ROI_left_cheek = image[int(left_cheek_coord[1]):int(left_cheek_coord[3]), int(left_cheek_coord[0]):int(left_cheek_coord[2])]

        ##Right cheek
        ##coord = [start_x, start_y, end_x, end_y]
        right_cheek_coord = [f['mouth_right'][0], f['right_eye'][1] + (0.2 * h3), f['right_eye_corner'][0], f['nose_bottom'][1]]
        ROI_right_cheek = image[int(right_cheek_coord[1]):int(right_cheek_coord[3]), int(right_cheek_coord[0]):int(right_cheek_coord[2])]
          
        return ROI_forehead, ROI_left_cheek, ROI_right_cheek

    def Extract_nostril_ROI(self, face_info, image):
        f = face_info
        ### Face boundary dimensions
        h2 = f['mouth_left'][1] - f['nose'][1]
        w2 = abs(f['mouth_left'][0] - f['mouth_right'][0])
        
        ##Nostril ROI
        nc_start_0 = f['nose'][0] - (0.9*w2 /2 )  
        nc_start_1 = f['nose'][1] - (0.4*h2 /2) 
        nc_end_0 =  f['nose'][0] + (0.9*w2 /2 ) 
        nc_end_1 = f['nose'][1] + (h2 /2)  ### I increased the nostril ROI from 0.6h2/2 to h2/2 at the base for more area
        nostril_coord = [nc_start_0, nc_start_1, nc_end_0, nc_end_1]
        ROI_nostril = image[round(nostril_coord[1]):round(nostril_coord[3]), round(nostril_coord[0]):round(nostril_coord[2])]
        
        return ROI_nostril  

    #A function to get the mean RGB values
    def meanRGB(self, FH_ROI, LC_ROI, RC_ROI):    
        meanBlue1, meanGreen1, meanRed1 = np.average(FH_ROI, axis = (0,1))
        meanBlue2, meanGreen2, meanRed2 = np.average(LC_ROI, axis = (0,1))
        meanBlue3, meanGreen3, meanRed3 = np.average(RC_ROI, axis = (0,1))
        
        meanRed = meanRed1 + meanRed2 + meanRed3
        meanGreen = meanGreen1 + meanGreen2 + meanGreen3
        meanBlue = meanBlue1 + meanBlue2 + meanBlue3
        
        return meanRed, meanGreen, meanBlue
    
    #A function to find mean pixel of the nostril area
    def meanPixel(self, nostril_ROI): 
        meanpixel = np.average(nostril_ROI)
        return meanpixel
    
    ### FILTERING
    ##A 3rd order Butterworth bandpass filter for Heart Rate
    def butter_bandpass(self, fs):
        low = self.HeartRate_lowcut / ( 0.5 * fs)
        high = self.HeartRate_highcut / ( 0.5 * fs)
        b, a = butter(self.order, [low, high], btype='band')
        return b, a
    
    def butter_bandpass_filter(self, data, fs):
        b, a = self.butter_bandpass(fs)
        filterData = lfilter(b, a, data)
        return filterData
    
    ##A Bandpass filter for Sp02
    def spo2_lowpass_filter(self, data, fs, order=4):
        b, a = butter(3, (self.spo2_cutoff / (0.5 * fs)), btype='low')
        filteredData = lfilter(b, a, data)
        return filteredData
    
    #def SimpleBandpassFilter(self, data, fs):
       # [b, a] = butter(1, [self.Sp02_lowcut / fs * 2, self.Sp02_highcut / fs * 2], btype='bandpass')
       # filteredData = filtfilt(b, a, np.double(data))
       # return filteredData
    
    ### COMPUTING
    #A FastICA for blind source separation
    def computeICA(self, Signal):
        Signal /= Signal.std(axis=0)
        # Compute ICA
        ica = FastICA(n_components=3, whiten="arbitrary-variance", max_iter=1000)
        ReconstructedSignal = ica.fit_transform(Signal)
        ReconstSignal_2 = ReconstructedSignal[:,1] ##Select the Second (Green component) as it contains the strongest plethysmographic signal, according to https://www.mdpi.com/1424-8220/22/2/627/review_report
        return ReconstSignal_2
    
    #An implementation of the Empirical Mode Decomposition (EMD)to compute intrinsic mode functions (IMF) 
    def computeIMF(self, Signal, Ttime):
        Emd = EMD()
        Imfs = Emd.emd(Signal, Ttime)    
        power = [np.sum(imf**2) for imf in Imfs]

        # Find the index of the IMF with the maximum power
        max_power_index = np.argmax(power)

        # Select the IMF with the maximum power
        max_power_imf = Imfs[max_power_index]
        
        return max_power_imf
        #return IMF

    def detectPeak(self, IMF, fs) :
        #Detect peaks
        peaksHr, _ = find_peaks(IMF, distance=15)  
        
        RRList = []
        count = 0
        while (count < (len(peaksHr)-1)):
            RR_int = (peaksHr[count+1] - peaksHr[count]) 
            ms_dist = ((RR_int / fs) * 1000.0) 
            RRList.append(ms_dist) 
            count += 1
        bpm_imf = 60000 / np.mean(RRList) 
        return bpm_imf

       
    ### Function to compute the Heart Rate in Beats/mins
    def HeartRate(self, meanRed,meanGreen, meanBlue, Time, fs, max_iter= 5):
        
        #Apply Butterworth filter
        redFiltered = self.butter_bandpass_filter(meanRed, fs)
        greenFiltered = self.butter_bandpass_filter(meanGreen, fs)
        blueFiltered = self.butter_bandpass_filter(meanBlue, fs)
        
        #Normalise filtered signal
        redmean = np.mean(redFiltered)
        redstd = np.std(redFiltered)
        normRed = (redFiltered - redmean ) / redstd
        
        greenmean = np.mean(greenFiltered)
        greenstd = np.std(greenFiltered)
        normGreen = (greenFiltered - greenmean) / greenstd
        
        bluemean = np.mean(blueFiltered)
        bluestd = np.std(blueFiltered)
        normBlue = (blueFiltered - bluemean) / bluestd
        
        #Translates slice objects to concatenation along the second axis.
        SignalRGB = np.c_[normRed, normGreen, normBlue]
        
        #Apply FastICA to reconstruct signal
        NewSignal = self.computeICA(SignalRGB)
        #Apply EMD to compute the different Intrinsic Mode Function (IMF) 
        #Imf = computeIMF(NewSignal, Time)
        
        #Get the BPM value from the IMF Signals
        Imf = self.computeIMF(NewSignal, Time)
        hr = self.detectPeak(Imf, fs)
        #hrs =[]
        #for i in range(max_iter):
         #   Imf = self.computeIMF(NewSignal, Time)
          #  hr = self.detectPeak(Imf, fs)
           # hrs.append(hr)              
        #return sum(hrs)/len(hrs)
        return hr
    
    def SP02Formula(self, r):
        SpO2_a = 125 - 28 * r #a. (Cheng et al., 2023)  https://www.mdpi.com/2306-5354/10/5/524
        SpO2_b = 100 - 20 * r #b.(Al-Naji et al. 2021) 
        SpO2_c= 97.61 + 0.42 * r #c. (Bhattacharjee & Yusuf, 2021)
        
        return [SpO2_a, SpO2_b, SpO2_c]
    ##A Function to compute and return SP02
    def SP02(self, meanRed,meanGreen, meanBlue, fs, allMethod = False):
        
            # Detrending
        # https://nl.mathworks.com/help/matlab/data_analysis/detrending-data.html
        #redFiltered = detrend(meanRed) # detrend removes the linear trend
        #blueFiltered = detrend(meanBlue)
    
        redFiltered = self.spo2_lowpass_filter(meanRed, fs)
        #greenFiltered = self.SimpleBandpassFilter(meanGreen)
        blueFiltered = self.spo2_lowpass_filter(meanBlue, fs)
        
        red_sp02_mean = np.mean(redFiltered)
        red_sp02_std = np.std(redFiltered)
        
        blue_sp02_mean = np.mean(blueFiltered)
        blue_sp02_std = np.std(blueFiltered)
        
        #Compute the correlation coefficient R of blood oxygen
        R = (red_sp02_std/red_sp02_mean)/(blue_sp02_std/blue_sp02_mean)
        
        if allMethod == True:
            return self.SP02Formula(R)
        else:
            # The formula for the blood oxygen formula used in https://www.mdpi.com/2306-5354/10/5/524
            SpO2 = 125 - 28 * R
            #SpO2 = 97.61 + 0.42 * R  #[16]
            return SpO2
    
    ##A function to compute the Respiratory Rate
    def computeRR(self, data, fs):
        #Detect peak of signal
        peaksHr, _ = find_peaks(data, distance=15)
        
        RRList = []
        count = 0
        while (count < (len(peaksHr)-1)):
            RR_int = (peaksHr[count+1] - peaksHr[count]) 
            ms_dist = ((RR_int / fs) * 1000.0) 
            RRList.append(ms_dist) 
            count += 1
        rr = 60000 / np.mean(RRList) 
                
        return rr
    
    ##A function to process video and return the heart rate ans Sp02 values
    def hr_sp02(self, videopath):
        ##Open the video
        cap = cv2.VideoCapture(videopath)
        cap.set(cv2.CAP_PROP_FPS,30) 
        fps = cap.get(cv2.CAP_PROP_FPS)
    
        print("[INFO] The video has {} frames per second: ".format(fps))
        
        
        #Intitialise variables
        count = 0
        #fs = fps # Sample rate in Hz
        start_time = time.time() 
        RedMean, GreenMean, BlueMean, Time, ALLRGBMean = [], [], [], [], []
            
        while 1:
        #while count < 50:
            ret, frame = cap.read()
            sstart_time = time.time()
            if ret == True:
                count += 1
                #print("[INFO] Processing frame:", count, "of",framesCount )
                Time1 = time.time() - sstart_time
                sstart_time = time.time()                 
                FaceInfo = self.DLIB_face_dector(frame)
                Time2 = time.time() - sstart_time
                sstart_time = time.time()
                if FaceInfo == False:
                    pass
                else:
                    FhROI, LcROI, RcROI = self.Extract_forehead_ROI(frame, FaceInfo)
                    
                    Red, Green, Blue = self.meanRGB(FhROI, LcROI, RcROI)
                    
                    RedMean.append(Red)
                    GreenMean.append(Green)
                    BlueMean.append(Blue)
                    Time.append(time.time() - start_time)
                    Time3 = time.time() - sstart_time 
                    
                    ALLRGBMean.append([Red,Green, Blue, Time1, Time2, Time3])
                    
            else:
                print("No more frame to process")
                break
        
      
   
        ssstart_time = time.time()
        BPM = self.HeartRate(RedMean, GreenMean, BlueMean, Time, fps)
        Time_bpm = time.time() - ssstart_time
        Sp02 = self.SP02(RedMean, GreenMean, BlueMean, fps)
        Time_sp02 = time.time() - ssstart_time - Time_bpm

        Time_array = [Time_bpm, Time_sp02, time.time()-start_time]
        
        return BPM, Sp02, Time_array
    

##-----------NAO FUNCTIONS---------------###

# Replace this with your robot's IP address
IP = "192.168.1.5"
PORT = 9559
fps = 30.0 #10.0
Resolution = 2 #Resolution VGA  640*480 @30fps
RecordTime = 30 #in seconds
CameraID = 0 #Top Camera
#ColorSpace = 11 #AL::kRGBColorSpace	ID (11)	N.B Buffer contains triplet on the format 0xBBGGRR, equivalent to three unsigned char
##Remove Color space if not working
#If you don’t it manually set the parameter, default is - Color space: BGR
VideoFormat = 'IYUV' #“IYUV” (raw avi, color video only); “MJPG” (compressed avi, gray scale and color video)

def takeVideo(ip, port, recordTime, fs, resolution, cameraID, videoFormat):
    # Create a proxy to ALVideoRecorder
    try:
      videoRecorderProxy = ALProxy("ALVideoRecorder", ip, port)
    except Exception as e:
      print("Error when creating ALVideoRecorder proxy:", e)
      print(str(e))
      exit(1)
      
    videoRecorderProxy.setCameraID(cameraID)
    videoRecorderProxy.setVideoFormat(videoFormat)
    videoRecorderProxy.setFrameRate(fs)
    videoRecorderProxy.setResolution(resolution)

    root_path = "/home/nao/recordings/cameras/"
    video_file = "VS_test.avi"
    path = root_path + video_file
    if not os.path.exists(path):
        print("[INFO] [{}] does not exist".format(root_path))
    
    videoRecorderProxy.startRecording("/home/nao/recordings/cameras", "VS_test")
    print("[INFO] Video record started on {}".format(root_path))
    
    time.sleep(recordTime)
    
    videoInfo = videoRecorderProxy.stopRecording()
    print("Video was saved on the robot: ", videoInfo[1])
    print("Total number of frames: ", videoInfo[0])
    
    return videoInfo[1], video_file


def getVideoFromNao(Ip, RemotePath, LocalPath):
    
    Naocommand = "nao@"+Ip+":"+RemotePath
   # scp_command = ["scp", Naocommand, LocalPath] #without compression
    scp_command = ["scp", "-C", Naocommand, LocalPath]     #with compression   
    try:
        subprocess.check_call(scp_command)
        print("File transferred successfully.")
    except subprocess.CalledProcessError as e:
        print("Error during file transfer:", e)
    except OSError:
        print("The 'scp' command is not found. Make sure you have SCP installed and in your system's PATH.")

    
##-------------------------MAIN-------------------------------##

##Connect for Speech
speechMod = ALProxy("ALTextToSpeech", IP, PORT)
print("[INFO] Connected to Nao robot {}:{}".format(IP,PORT))

time.sleep(20)
speechMod.say("Hello, I am Nao robot!")
speechMod.say("I will be your medical assistant")
time.sleep(sleepTime)
speechMod.say("Please try to look at me so I take your video")
time.sleep(sleepTime)
speechMod.say("Ready")
time.sleep(sleepTime)
speechMod.say("Starting the video")


dat_path = r"C:\Users\kehin\Documents\Programming\After masters\shape_predictor_68_face_landmarks.dat"

Time_start = time.time()
RemoteVideoPATH, VideoName = takeVideo(IP, PORT, RecordTime, fps, Resolution, CameraID, VideoFormat)
record_time = time.time()-Time_start
print("Time taken to record video is", record_time )
speechMod.say("Video Recording Ended")

LocalPATH = r"C:\Users\kehin\Documents\Programming\After masters"
speechMod.say("About to transfer video file Nao to local computer")
getVideoFromNao(IP, RemoteVideoPATH, LocalPATH)
print("Time taken to download video is", time.time()- Time_start-record_time )
speechMod.say("Video to remote computer for processing completed")
time.sleep(sleepTime)
print("About to start Vital Sign Measurement")
video_file = os.path.join(LocalPATH, VideoName)

speechMod.say("Measuring Vital sign")


VS = vitalsigns(dat_path, HeartRate_lowcut = 0.8,HeartRate_highcut = 2.0, Sp02_lowcut = 1.5, Sp02_highcut = 3, spo2_cutoff =2, order = 3, distance = 15)

bpm, sp, times = VS.hr_sp02(RemoteVideoPATH)
speechMod.say("Your heart rate is")
speechMod.say(str(round(float(bpm))))
speechMod.say("Beats per minutes")
time.sleep(sleepTime)

speechMod.say("Your blood oxygen saturation level is")
speechMod.say(str(round(float(sp))))
speechMod.say("percent")
time.sleep(sleepTime)

speechMod.say("Thank you for your time")

##Print values
print("The Heart Rate is {} Beats per mins".format(round(bpm)))
print('The Blood-Oxygen Saturation level is {}%'.format(round(sp)))

print("Time taken for HR calculation is", times[0])
print("Time taken for the Sp02 calculation", times[1])
print("Time taken to process video is", times[2])
print("Total time taken for the entire process is", time.time() - Time_start)
