# File: qsagin/agents/base_agent.py
import numpy as np
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """
    Lớp cơ sở trừu tượng cho tất cả các Agent.
    "Hợp đồng" yêu cầu mọi Agent phải có khả năng đưa ra hành động (get_action).
    """
    @abstractmethod
    def get_action(self, state):
        """
        Nhận vào trạng thái (state) và trả về một hành động (action).
        """
        pass
    
    # Chúng ta thêm một hàm learn() trống ở đây để chuẩn bị cho các agent RL sau này
    def learn(self, state, action, reward, next_state, done):
        """
        (Tùy chọn) Agent có thể học từ kinh nghiệm.
        Agent đơn giản như RandomAgent sẽ không cần implement hàm này.
        """
        pass


class RandomAgent(BaseAgent):
    """Một Agent đơn giản, luôn đưa ra các hành động ngẫu nhiên."""
    def __init__(self, num_quantum_links=5, num_satellites=5):
        self.num_quantum_links = num_quantum_links
        self.num_satellites = num_satellites

    def get_action(self, state):
        """
        Bỏ qua trạng thái và trả về một hành động ngẫu nhiên.
        Cấu trúc action này được thiết kế để có thể mở rộng.
        """
        action = {
            # Hành động cho mạng cổ điển: ví dụ chọn 1 cặp vệ tinh để truyền dữ liệu
            "classical": np.random.randint(0, self.num_satellites, size=2),
            
            # Hành động cho mạng lượng tử: ví dụ chọn 1 kênh lượng tử để làm mới
            "quantum": np.random.randint(0, self.num_quantum_links)
        }
        return action
