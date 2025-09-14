# File: scripts/debug_step.py
# Mục đích: Kiểm tra chính xác output của hàm env.step()

from ns3gym import ns3env
import time

print("--- Step Debugger Initialized ---")
print("Waiting for ns-3 connection...")

# Kết nối đến ns-3 đang chạy
# startSim=False là chế độ client
env = ns3env.Ns3Env(port=5555, startSim=False)

# Reset môi trường
obs = env.reset()
print("Connection successful. Reset complete.")
print(f"Initial observation type: {type(obs)}")

# Thực hiện một bước với hành động ngẫu nhiên
action = env.action_space.sample()
print(f"\nTaking a random action: {action}")

# Đây là dòng code quan trọng nhất
step_return_value = env.step(action)

print("\n--- INSPECTION RESULTS ---")
print(f"Value returned by env.step(): {step_return_value}")
print(f"Type of returned value: {type(step_return_value)}")
print(f"Length of returned tuple: {len(step_return_value)}")

# Dựa vào Length, chúng ta sẽ biết cách unpack chính xác.
# Nếu Length là 4 -> (obs, reward, done, info)
# Nếu Length là 5 -> (obs, reward, terminated, truncated, info)

env.close()
print("\n--- Debug Finished ---")
