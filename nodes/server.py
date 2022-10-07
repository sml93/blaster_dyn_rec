#!/usr/bin/env python
import time
import rospy

from argparse import Namespace
from my_dyn_rec.cfg import ParamsConfig
from dynamic_reconfigure.server import Server
from std_msgs.msg import Int16, Float32, Bool

check = False
key = 0
def callback(config, level):
  global check, key
  pub_angle = rospy.Publisher('jetForce_angle', Int16, queue_size=10)
  pub_mag = rospy.Publisher('jetForce_mag', Float32, queue_size=10)
  pub_dur = rospy.Publisher('duration', Int16, queue_size=10)
  pub_mission = rospy.Publisher('mission_status', Bool, queue_size=10)
  pub_switch = rospy.Publisher('jetOn', Int16, queue_size=10)
  rospy.loginfo("""Reconfigure Request: {jetForceAngle}, {jetForceMag}, {jetDur}, {mission_param}, {jetOn}""".format(**config))
  # print(config)
  check = False
  if (config.get('jetOn')==1):
    check = True
    if check==1 and key==0:
      # pub_dur.publish(config.get('jetDur'))
      pub_switch.publish(config.get('jetOn'))
      for i in range(config.get('jetDur')):
        pub_mag.publish(config.get('jetForceMag')/(2*i+1))
        pub_angle.publish(config.get('jetForceAngle'))
        pub_mission.publish(config.get('mission_param'))
        time.sleep(1)
      check = False
      key = 1
  else:
    key = 0
    check = False
    pub_mag.publish(config.get('jetForceMag'))
    pub_angle.publish(config.get('jetForceAngle'))
    pub_dur.publish(0)
    pub_mission.publish(config.get('mission_param'))
  return config

if __name__ == "__main__":
  rospy.init_node("blaster_dyn_rec", anonymous = False)
  srv = Server(ParamsConfig, callback)
  # client = dynamic_reconfigure.client.Client("my_dyn_rec", timeout=30)
  rospy.spin()