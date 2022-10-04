#!/usr/bin/env python

import rospy

import dynamic_reconfigure.client

def callback(config):
    rospy.loginfo("Config set to {ang_param}, {mag_param}, {dur_param}".format(**config))

if __name__ == "__main__":
    rospy.init_node("dynamic_client")

    client = dynamic_reconfigure.client.Client("my_dyn_rec", timeout=30, config_callback=callback)

    r = rospy.Rate(0.1)
    x = 0
    b = False
    while not rospy.is_shutdown():
        x = x+1
        if x>10:
            x=0
        b = not b
        client.update_configuration({"ang_param":x, "mag_param":(1/(x+1)), "dur_param":b})
        r.sleep()
