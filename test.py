# /app/test.py
import gymnasium as gym
from ns3gym import ns3env
import os

os.chdir("/workspace/ns-allinone-3.40/ns-3.40")
env = ns3env.Ns3Env(port=5555)
env.reset()
action = env.action_space.sample()

# --- DEBUGGING LINE ---
result = env.step(action)
print(f"RESULT of env.step: {result}")
print(f"TYPE of result: {type(result)}")
print(f"LENGTH of result: {len(result)}")
# --- END DEBUGGING ---

env.close()
