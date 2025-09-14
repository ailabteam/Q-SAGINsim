# File: qsagin/simulators/sim_classical.py
import numpy as np
from .base_simulator import BaseSimulator

class MockClassicalSimulator(BaseSimulator):
    """
    Simulator "giả" cho mạng cổ điển (vệ tinh, UAV...).
    Nó đóng vai trò là "diễn viên đóng thế" cho ns-3.
    """
    
    def setup(self):
        """Khởi tạo 5 vệ tinh với vị trí ngẫu nhiên."""
        print("Setting up Mock Classical Network...")
        self.satellite_positions = np.random.rand(5, 3) # 5 satellites, 3D coords
        self.time_step = 0

    def step(self, action):
        """Mô phỏng vệ tinh di chuyển và tính reward đơn giản."""
        print(f"[Classical] Received action: {action} at t={self.time_step}")
        # Giả lập vệ tinh di chuyển một chút
        self.satellite_positions += np.random.randn(5, 3) * 0.01
        self.time_step += 1
        
        # Reward giả, ví dụ: phạt nếu action có giá trị lớn
        reward = -np.sum(action) / 10 if action is not None else 0
        return self.get_state(), reward, False, {}

    def get_state(self):
        """Trạng thái là vị trí của các vệ tinh."""
        return {"positions": self.satellite_positions}

    def reset(self):
        self.setup()
        return self.get_state()
