# -*- coding: utf-8 -*-
import boto3
import botocore
import face_recognition
import cv2
import time
import os
import datetime

detect_face_name=face_recognition.face_name
state=face_recognition.fail_state

path = 'cctv/'
newCode="sudo modprobe bcm2835-v4l2"

#실패시 cctv 촬영
def Camera_cctv():
	camera = cv2.VideoCapture(0)

    # Define the codec and create VideoWriter object to save the video
	fourcc = cv2.VideoWriter_fourcc(*'XVID')

	video_writer = cv2.VideoWriter( 'failCap/fail.avi', fourcc, 30.0, (640, 480))
    
    
	b = 0
	print("\n cctv 촬영 중\n")
	while True:
	
		b = b+1
		(grabbed, frame) = camera.read()  # grab the current frame
		frame = cv2.resize(frame, (640,480))
		cv2.imshow("Frame", frame)  # show the frame to our screen
		key = cv2.waitKey(33) & 0xFF
		video_writer.write(frame)  # Write the video to the file system
	
	
		if b==100:
			print("\n cctv 촬영 종료\n")
			break
	
	# upload_file로 업로드하기
	s3= boto3.client('s3') # s3객체생성
	#버킷이름
	bucket_name='face-images-storage'
	
	#인식 실패한 얼굴파일
	fail='failCap/fail.avi' 
	#s3에 png 파일 보내기
	s3.upload_file(fail,bucket_name,datetime.datetime.now().strftime("%H:%M:%S")+'.avi',
		       ExtraArgs={'ACL':'public-read', 'ContentType': 'video/x-msvideo'})
	
	# 버킷 이름 모두 출력
	response = s3.list_buckets()
	buckets = [bucket['Name'] for bucket in response['Buckets']]
	print("Bucket List: %s 에 ccvt 동영상이 저장되었습니다" % buckets)
	
	# cleanup the camera and close any open windows
	camera.release()
	video_writer.release()
	cv2.destroyAllWindows()
	


def aws_face_send(detect_face_name):
	s3= boto3.client('s3') # s3객체생성

	# upload_file로 업로드하기

	#버킷이름
	bucket_name='face-images-storage'

	#인식 성공한 얼굴파일
	file_name='successCap/'+detect_face_name+'.png' 
	#s3에 png 파일 보내기
	s3.upload_file(file_name,bucket_name,datetime.datetime.now().strftime("%Y-%m-%d")+'.png',
		       ExtraArgs={'ACL':'public-read', 'ContentType': 'image/png'})

	#인식 성공시점 로그 json 파일
	json_name='result/'+detect_face_name+'.json' 
	#s3에 json 파일 보내기
	s3.upload_file(json_name,bucket_name,detect_face_name+'.json',ExtraArgs={'ACL':'public-read', 
										 'ContentType': 'application/json'})

	#detect_face_name+'.png'/ detect_face_name+'.json' 파일이 버킷에 올라갈 이름

	# 버킷 이름 모두 출력
	response = s3.list_buckets()
	buckets = [bucket['Name'] for bucket in response['Buckets']]
	print("Bucket List: %s 에 출입허가 사진이 저장되었습니다" % buckets)
	
	
#실패 or 성공시 처리
#얼굴인식이 3회이상 실패하면 cctv동영상 3초짜리 촬영
#얼굴인식이 성공하면 성공한 얼굴, 로그 버킷에 보내기
if state ==True:
	Camera_cctv()
else:
	aws_face_send(detect_face_name)





