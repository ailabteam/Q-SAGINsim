# File: qsagin/simulators/base_simulator.py
from abc import ABC, abstractmethod

class BaseSimulator(ABC):
    """
    Lớp cơ sở trừu tượng (Abstract Base Class) cho tất cả các simulator.
    Nó định nghĩa các hàm bắt buộc mà mọi simulator phải có.
    Đây là "bản hợp đồng" của chúng ta.
    """
    
    def __init__(self, sim_config):
        """Khởi tạo simulator với một file cấu hình."""
        self.config = sim_config
        print(f"Initializing {self.__class__.__name__}...")

    @abstractmethod
    def setup(self):
        """Thiết lập kịch bản mô phỏng ban đầu."""
        pass

    @abstractmethod
    def step(self, action):
        """
        Thực hiện một bước mô phỏng, nhận vào một 'action' từ agent.
        Trả về: trạng thái mới, phần thưởng, và các thông tin khác.
        """
        pass

    @abstractmethod
    def get_state(self):
        """Trả về trạng thái hiện tại của mô phỏng."""
        pass

    @abstractmethod
    def reset(self):
        """Reset mô phỏng về trạng thái ban đầu."""
        pass
