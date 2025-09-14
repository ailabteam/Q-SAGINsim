# File: qsagin/simulators/sim_quantum.py
import numpy as np
from .base_simulator import BaseSimulator

class MockQuantumSimulator(BaseSimulator):
    """
    Simulator "giả" cho mạng lượng tử.
    Nó đóng vai trò là "diễn viên đóng thế" cho SeQUeNCe.
    """

    def setup(self):
        """Khởi tạo 5 kênh lượng tử với độ trung thực (fidelity) ngẫu nhiên."""
        print("Setting up Mock Quantum Network...")
        self.entanglement_fidelity = np.random.uniform(0.7, 0.95, size=(5,))
        self.time_step = 0

    def step(self, action):
        """Mô phỏng fidelity bị suy giảm theo thời gian."""
        print(f"[Quantum] Received action: {action} at t={self.time_step}")
        # Giả lập fidelity bị giảm đi một chút
        self.entanglement_fidelity -= 0.01
        # Nếu action là "refresh", tăng fidelity của kênh đó lên
        if action is not None and 0 <= action < len(self.entanglement_fidelity):
            self.entanglement_fidelity[action] = 0.95 # Reset fidelity
            
        self.entanglement_fidelity = np.clip(self.entanglement_fidelity, 0, 1)
        self.time_step += 1
        
        # Reward giả: reward càng cao nếu fidelity trung bình càng cao
        reward = np.mean(self.entanglement_fidelity)
        return self.get_state(), reward, False, {}

    def get_state(self):
        """Trạng thái là fidelity của các kênh vướng víu."""
        return {"fidelity": self.entanglement_fidelity}

    def reset(self):
        self.setup()
        return self.get_state()
