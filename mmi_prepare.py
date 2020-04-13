# python2
"""
For synchronize video and velodyne (in .bag) data from Mcity data
"""

import os
import rospy
import rosbag
import cv2
from cv_bridge import CvBridge
import sensor_msgs
import sensor_msgs.point_cloud2 as pc

video_path = "/home/jacobz/Calibration/mcity_data/1_09_1/front_60/1-s-1.mkv"
times_path = "/home/jacobz/Calibration/mcity_data/1_09_1/front_60/1-s-1.txt"
rosbag_path = "/home/jacobz/Calibration/mcity_data/1_09_1/save/1-s-1.bag"

topic_path = "/vlp32_2/velodyne_points"
output_path = "/home/jacobz/Calibration/mcity_data/mmi_prepared/"
time_thres = 10 # ms

images = {}
clouds = {}
video = cv2.VideoCapture(video_path)
image_tptr = cloud_tptr = ctptr = 0
image_dptr = cloud_dptr = None
update_flag = True
save_bag = output_path.endswith(".bag")
match_counter = 0

if not video.isOpened():
    raise RuntimeError("Cannot open video")
if save_bag:
    rosout = rosbag.Bag(output_path, 'w', compression=rosbag.Compression.BZ2)
    br = CvBridge()
else:
    if not os.path.exists(output_path):
        os.makedirs(output_path)

with open(times_path, 'r') as timestamp:
    with rosbag.Bag(rosbag_path, 'r') as bag:
        baggen = bag.read_messages(topics=[topic_path])

        status, image_dptr = video.read()
        seq, time = timestamp.readline().split(',')
        image_tptr = int(time)
        topic, cloud_dptr, time = next(baggen)
        cloud_tptr = int(str(time))/1000000
        ctptr = min(image_tptr, cloud_tptr)
        
        while True:
            if update_flag:
                if abs(image_tptr-cloud_tptr) <= time_thres:
                    print("Matched pair! Saving...")
                    
                    if save_bag:
                        image_rost = rospy.Time(secs=image_tptr/1000,
                                                nsecs=image_tptr%1000*1000)                 
                        cloud_rost = rospy.Time(secs=cloud_tptr/1000,
                                                nsecs=cloud_tptr%1000*1000)
                        if image_tptr > cloud_tptr:
                            rosout.write('/fov60/image', br.cv2_to_imgmsg(image_dptr),
                                         t=image_rost)
                            rosout.write(topic, cloud_dptr, t=cloud_rost)
                        else:
                            rosout.write(topic, cloud_dptr, t=cloud_rost)
                            rosout.write('/fov60/image', br.cv2_to_imgmsg(image_dptr),
                                         t=image_rost)
                    else:
                        prefix = output_path + "%06d" % match_counter
                        cv2.imwrite(prefix + ".png", image_dptr)
                        with open(prefix + ".txt", "w") as cloud_out:
                            cloudlist = list(pc.read_points(cloud_dptr))
			    cloud_out.write(str(len(cloudlist)) + '\n')
                            for x,y,z,i,r in cloudlist:
                                cloud_out.write("%f %f %f %d\n" % (x,y,z,int(i)))
                    match_counter += 1
                update_flag = False
            
            ctptr += 1
            if image_tptr < ctptr:
                if not status: break
                status, image_dptr = video.read()
                seq, time = timestamp.readline().split(',')
                image_tptr = int(time)
                update_flag = True
                print("Reading image " + str(image_tptr))
            if cloud_tptr < ctptr:
                try: topic, cloud_dptr, time = next(baggen)
                except StopIteration: break
                cloud_tptr = int(str(time))/1000000
                update_flag = True
                print("Reading cloud " + str(cloud_tptr))

if save_bag:
    rosout.close()
