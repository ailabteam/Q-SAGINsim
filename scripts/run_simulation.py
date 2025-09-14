# File: scripts/run_simulation.py
import sys
import os
import numpy as np

# --- Dòng code quan trọng để giải quyết vấn đề import ---
# Khi chạy file này từ thư mục gốc (ví dụ: python scripts/run_simulation.py),
# Python cần biết phải tìm các module 'qsagin' ở đâu.
# Đoạn code này thêm thư mục gốc của dự án (Q-SAGINsim) vào đường dẫn tìm kiếm của Python.
# Điều này cho phép chúng ta import từ `qsagin` một cách suôn sẻ.
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
# ---------------------------------------------------------

from qsagin.core.orchestrator import Orchestrator
from qsagin.simulators.sim_classical import MockClassicalSimulator
from qsagin.simulators.sim_quantum import MockQuantumSimulator
from qsagin.agents.base_agent import RandomAgent

def main():
    """Hàm chính để thiết lập và chạy mô phỏng."""
    print("=============================================")
    print("=== Initializing Q-SAGINsim Framework ===")
    print("=============================================")
    
    # --- 1. Định nghĩa các tham số cho kịch bản mô phỏng ---
    # Đưa các tham số ra đây giúp chúng ta dễ dàng thay đổi kịch bản
    # mà không cần phải vào sâu trong code.
    SIMULATION_STEPS = 5
    NUM_SATELLITES = 5
    NUM_QUANTUM_LINKS = 5
    
    # --- 2. Khởi tạo các thành phần ---
    # Hiện tại chúng ta truyền vào config rỗng, sau này sẽ đọc từ file .yaml
    print("\n[Setup] Initializing components...")
    classical_sim = MockClassicalSimulator(sim_config={})
    quantum_sim = MockQuantumSimulator(sim_config={})
    
    # Agent cần biết "không gian hành động" của nó lớn đến đâu
    agent = RandomAgent(
        num_satellites=NUM_SATELLITES,
        num_quantum_links=NUM_QUANTUM_LINKS
    )
    
    # --- 3. "Tiêm" các thành phần vào Orchestrator (Dependency Injection) ---
    # Đây là bước quan trọng nhất, kết nối mọi thứ lại với nhau.
    print("[Setup] Assembling the orchestrator...")
    orchestrator = Orchestrator(
        classical_sim=classical_sim,
        quantum_sim=quantum_sim,
        agent=agent
    )
    
    # --- 4. Bắt đầu chạy mô phỏng ---
    orchestrator.run(num_steps=SIMULATION_STEPS)

if __name__ == "__main__":
    # Dòng `if __name__ == "__main__":` là một chuẩn của Python.
    # Nó đảm bảo rằng hàm `main()` chỉ được gọi khi file này được chạy trực tiếp.
    main()
