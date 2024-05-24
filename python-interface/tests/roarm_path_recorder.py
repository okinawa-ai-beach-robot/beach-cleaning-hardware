from beachbot.manipulators import RoArmM1
import time

arm1 = RoArmM1()
arm1.refresh_robot_state()
arm1.go_home()
<<<<<<< HEAD
qs, taus, ts = arm1.record_trajectory(wait_time_max=3, save_path="./pickup_path")
=======
qs, taus, ts = arm1.record_trajectory(wait_time_max=3, save_path="toss_path")
>>>>>>> 544ae5a (arm movement test files added)
print("Recoding entries:", qs.shape[0])
print("Recoding duration:", ts[-1])
# qs: joint angles
# taus: torques
# ts: timestamps
print("\n\nStart replay (replay based on record time stamps)...")
arm1.replay_trajectory(qs, ts)
print("Done!")
