import gymnasium as gym
from ns3gym import ns3env
import pprint
import os

print("--- Starting ns3-gym Integration Test ---")

try:
    # === FINAL FIX: Let ns3gym find the default 'opengym' script ===
    # We must set the working directory to the ns-3 root for this to work.
    os.chdir("/workspace/ns-allinone-3.40/ns-3.40")
    
    # Define arguments for the default 'opengym' script
    sim_args = {"--simTime": 2}
    
    # Initialize the environment without sim_script
    env = ns3env.Ns3Env(port=5555, sim_args=sim_args, debug=True)
    # ===============================================================
    
    print("\nEnvironment created successfully!")
    obs, info = env.reset()
    print("Reset successful. Initial Observation:")
    pprint.pprint(obs)
    
    action = env.action_space.sample()
    print(f"\nTaking a random action: {action}")
    
    obs, reward, terminated, truncated, info = env.step(action)
    print("Step successful. Results:")
    pprint.pprint(obs)

    print("\n--- SUCCESS: ns-3 and Python are fully integrated! ---")

except Exception as e:
    print(f"\n--- AN ERROR OCCURRED: {e} ---")

finally:
    if 'env' in locals() and hasattr(env, 'close'):
        env.close()
