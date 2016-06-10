########################################################################
#                                                                      #
# This python script tests the motion detector software by reading     #
# from a video file. So that the camera module is not needed           #
# at this time.                                                        #
#                                                                      #
########################################################################
                                                                        
# import the necessary packages
import argparse
import warnings
import datetime

#import imutils
import json
import time

import cv2
import numpy as np

def playVideo(filename):
    # read video file
    cap = cv2.VideoCapture(filename)

    while(cap.isOpened()):
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #cv2.imshow('frame',gray)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return;



def testMotion(filename):

    # load file
    cap = cv2.VideoCapture(filename)

    # initialize the average frame, last uploaded timestamp
    # and frame motion counter
    avg = None
    lastUploaded = datetime.datetime.now()
    motionCounter = 0

    # loop
    while(cap.isOpened()):

        # get frame
        ret, frame = cap.read()

        # grab the raw NumPy array representing the image and initialize
        # initialize the timestamp and occupied/unoccupied text
        ##frame = f.array
        timestamp = datetime.datetime.now()
        text = "Unoccupied"

        # resize the frame, convert it to grayscale, and blur it
        #frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # if the average frame is None, initialize it
        if avg is None:
            print ("[INFO] starting background model...")
            avg = gray.copy().astype("float")
            #rawCapture.truncate(0)
            #frame.truncate(0)
            continue

        # accumulate the weighted average between the current frame and
        # previous frames, then compute the difference between the current
        # frame and running average
        cv2.accumulateWeighted(gray, avg, 0.5)
        frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

        # threshold the delta image, dilate the thresholded image to fill
        # in holes, then find contours on thresholded image
        thresh = cv2.threshold(frameDelta, conf["delta_thresh"], 255,
                cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
        #http://www.answers.opencv.org/question/40329/python-valueerror-too-many-values-to-unpack/
        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < conf["min_area"]:
                    continue

            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = "Occupied"

        # draw the text and timestamp on the frame
        ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
        cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                0.35, (0, 0, 255), 1)

        # check to see if the frames should be displayed to screen
        if conf["show_video"]:
            # display the security feed
            cv2.imshow("Security Feed", frame)
            key = cv2.waitKey(1) & 0xFF

            # if the `q` key is pressed, break from the lop
            if key == ord("q"):
                    break

        # clear the stream in preparation for the next frame
        #rawCapture.truncate(0)
        #frame.truncate(0)
        ###
        #cv2.imshow('frame',gray)
        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break
    return;
    
##    # capture frames from the camera
##    for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
##            # grab the raw NumPy array representing the image and initialize
##            # the timestamp and occupied/unoccupied text
##            frame = f.array
##            timestamp = datetime.datetime.now()
##            text = "Unoccupied"
##
##            # resize the frame, convert it to grayscale, and blur it
##            #frame = imutils.resize(frame, width=500)
##            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
##            gray = cv2.GaussianBlur(gray, (21, 21), 0)
##
##            # if the average frame is None, initialize it
##            if avg is None:
##                    print ("[INFO] starting background model...")
##                    avg = gray.copy().astype("float")
##                    rawCapture.truncate(0)
##                    continue
##
##            # accumulate the weighted average between the current frame and
##            # previous frames, then compute the difference between the current
##            # frame and running average
##            cv2.accumulateWeighted(gray, avg, 0.5)
##            frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))
##
##
##            # threshold the delta image, dilate the thresholded image to fill
##            # in holes, then find contours on thresholded image
##            thresh = cv2.threshold(frameDelta, conf["delta_thresh"], 255,
##                    cv2.THRESH_BINARY)[1]
##            thresh = cv2.dilate(thresh, None, iterations=2)
##            (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
##                    cv2.CHAIN_APPROX_SIMPLE)
##
##            # loop over the contours
##            for c in cnts:
##                    # if the contour is too small, ignore it
##                    if cv2.contourArea(c) < conf["min_area"]:
##                            continue
##
##                    # compute the bounding box for the contour, draw it on the frame,
##                    # and update the text
##                    (x, y, w, h) = cv2.boundingRect(c)
##                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
##                    text = "Occupied"
##
##            # draw the text and timestamp on the frame
##            ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
##            cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
##                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
##            cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
##                    0.35, (0, 0, 255), 1)
##
##
##            # check to see if the frames should be displayed to screen
##            if conf["show_video"]:
##                    # display the security feed
##                    cv2.imshow("Security Feed", frame)
##                    key = cv2.waitKey(1) & 0xFF
##
##                    # if the `q` key is pressed, break from the lop
##                    if key == ord("q"):
##                            break
##
##            # clear the stream in preparation for the next frame
##            rawCapture.truncate(0)


## MAIN

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf",
                required=True,
                help="path to the JSON configuration file")
args = vars(ap.parse_args())

# filter warnings, load the configuration
warnings.filterwarnings("ignore")

conf = json.load(open(args["conf"]))

# play video
#print ("[INFO] playing video...")
#playVideo(conf["videofilename"])

# test motion
print ("[INFO] testing motion...")
testMotion(conf["videofilename"])


exit;
