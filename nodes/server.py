#!/usr/bin/env python

from argparse import Namespace
import rospy

from dynamic_reconfigure.server import Server
from my_dyn_rec.cfg import ParamsConfig
from argparse import Namespace

from std_msgs.msg import Int16, String, Float32, Bool


def callback(config, level):
  pub_angle = rospy.Publisher('jetForce_angle', Int16, queue_size=10)
  pub_mag = rospy.Publisher('jetForce_mag', Float32, queue_size=10)
  pub_dur = rospy.Publisher('duration', Int16, queue_size=10)
  pub_mission = rospy.Publisher('mission_status', Bool, queue_size=10)
  rospy.loginfo("""Reconfigure Request: {jetForceAngle}, {jetForceMag}, {jetDur}, {mission_param}""".format(**config))
  pub_mag.publish(config.get('jetForceMag'))
  pub_angle.publish(config.get('jetForceAngle'))
  pub_dur.publish(config.get('jetDur'))
  pub_mission.publish(config.get('mission_param'))
  return config

if __name__ == "__main__":
  rospy.init_node("blaster_dyn_rec", anonymous = False)
  srv = Server(ParamsConfig, callback)
  rospy.spin()