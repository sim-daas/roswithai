#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import sys
##import RPi.GPIO as GPIO
sys.path.append('../')
import gi
gi.require_version('Gst', '1.0')
from gi.repository import GLib, Gst
from deepstream_class import Pipeline, Pipeline_tracker , VideoPipeline, NodePipeline
import pyds
import time

#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(12, GPIO.OUT)

def osd_sink_pad_buffer_probe(pad,info,u_data):
    msg = String()
    gst_buffer = info.get_buffer()
    batch_meta = pyds.gst_buffer_get_nvds_batch_meta(hash(gst_buffer))
    l_frame = batch_meta.frame_meta_list
    while l_frame is not None:
        try:
            frame_meta = pyds.NvDsFrameMeta.cast(l_frame.data)
        except StopIteration:
            break

        frame_number=frame_meta.frame_num
        num_rects = frame_meta.num_obj_meta
        l_obj=frame_meta.obj_meta_list
        while l_obj is not None:
            try:
                obj_meta=pyds.NvDsObjectMeta.cast(l_obj.data)
            except StopIteration:
                break

            rect_params = obj_meta.rect_params
            top = int(rect_params.top)
            left = int(rect_params.left)
            width = int(rect_params.width)
            height = int(rect_params.height)

            x1 = left
            y1 = top
            x2 = left + width
            y2 = top + height
            if obj_meta.class_id == 0: 
              #  GPIO.output(12, GPIO.HIGH) 
               # time.sleep(0.8)
                #GPIO.output(12, GPIO.LOW)
                #print(x1, y1, x2, y2)
                #print(obj_meta.class_id)
                msg = obj_meta.class_id
                #publisher_.publish(msg)
                #self.get_logger().info('Publishing: "%s"' % msg.data)
            obj_meta.rect_params.border_color.set(0.0, 0.0, 1.0, 0.0)
            try: 
                l_obj=l_obj.next
            except StopIteration:
                break

        try:
            l_frame=l_frame.next
        except StopIteration:
            break
			
    return Gst.PadProbeReturn.OK

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)

def osd_sink_pad_buffer_probenode(self, pad,info,u_data):
        msg = String()
       # bounding_box = BoundingBox2D()
        gst_buffer = info.get_buffer()
        batch_meta = pyds.gst_buffer_get_nvds_batch_meta(hash(gst_buffer))
        l_frame = batch_meta.frame_meta_list
        while l_frame is not None:
            try:
                frame_meta = pyds.NvDsFrameMeta.cast(l_frame.data)
            except StopIteration:
                break
     
            l_obj=frame_meta.obj_meta_list
            while l_obj is not None:
                try:
                    obj_meta=pyds.NvDsObjectMeta.cast(l_obj.data)
                    rect_params = obj_meta.rect_params
                    top = int(rect_params.top)
                    left = int(rect_params.left)
                    width = int(rect_params.width)
                    height = int(rect_params.height)

                    x1 = int(left)
                    y1 = int(top)
                    x2 = int(left + width)
                    y2 = int(top + height)
                    if obj_meta.class_id == 0: 
                        result = str(x1) + ", " + str(x2) + ", " + str(y1) + ", " + str(y2)
                        msg.data = result
                        minimal_publisher.publisher_.publish(msg)
          
                except StopIteration:
                    break
                obj_meta.rect_params.border_color.set(0.0, 0.0, 1.0, 0.0)
                try: 
                    l_obj=l_obj.next
                except StopIteration:
                    break

            try:
                l_frame=l_frame.next
            except StopIteration:
                break
			
        return Gst.PadProbeReturn.OK



def main():
    #pipeline = Pipeline(args[1], args[2])
    pipeline = Pipeline('sample_720p.h264', 'config_inferyolov8.txt')
    pipeline.osdsinkpad.add_probe(Gst.PadProbeType.BUFFER, osd_sink_pad_buffer_probe, 0)
    pipeline.run()

def main2(args):
    #pipeline = Pipeline_tracker(args[1], args[2], args[3])
    pipeline = Pipeline_tracker('walking.h264', 'yolov7-tiny-320.txt', 'config_tracker.txt')
    pipeline.osdsinkpad.add_probe(Gst.PadProbeType.BUFFER, osd_sink_pad_buffer_probe, 0)
    pipeline.run()

def main3():
    rclpy.init()
  #  pipeline = VideoPipeline(args[1])
    pipeline = VideoPipeline('config_inferyolov8.txt', '/dev/video0', 'config_tracker.txt')
    pipeline.osdsinkpad.add_probe(Gst.PadProbeType.BUFFER, osd_sink_pad_buffer_probe, 0)
    pipeline.run()
    rclpy.shutdown()


def main4():
    rclpy.init()
  #  pipeline = VideoPipeline(args[1])
    pipeline = NodePipeline('config_inferyolov8.txt', '/dev/video0', 'config_tracker.txt')
    pipeline.osdsinkpad.add_probe(Gst.PadProbeType.BUFFER, osd_sink_pad_buffer_probe, 0)
    pipeline.run()
    rclpy.shutdown()
    
    
if __name__ == '__main__':
    main3()
