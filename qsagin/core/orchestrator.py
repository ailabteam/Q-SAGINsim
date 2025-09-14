# File: qsagin/core/orchestrator.py

class Orchestrator:
    """
    Lớp Orchestrator đóng vai trò là "nhạc trưởng" hay "đạo diễn".
    Nó quản lý các simulator và agent, điều khiển luồng mô phỏng chính.
    """
    def __init__(self, classical_sim, quantum_sim, agent):
        """
        Khởi tạo Orchestrator bằng cách "tiêm" (inject) các thành phần phụ thuộc.
        Thiết kế này (Dependency Injection) giúp hệ thống rất linh hoạt và dễ test.
        """
        print("Orchestrator is being created...")
        self.classical_sim = classical_sim
        self.quantum_sim = quantum_sim
        self.agent = agent
        
    def _get_global_state(self):
        """
        Hàm private để thu thập và tổng hợp trạng thái từ tất cả các simulator.
        Việc đóng gói state trong một dictionary giúp dễ dàng mở rộng sau này.
        """
        state = {
            "classical": self.classical_sim.get_state(),
            "quantum": self.quantum_sim.get_state(),
        }
        return state

    def run(self, num_steps):
        """Vòng lặp mô phỏng chính."""
        print("=== Starting Simulation Run ===")
        
        # Reset tất cả môi trường về trạng thái ban đầu
        self.classical_sim.reset()
        self.quantum_sim.reset()
        
        # Lấy trạng thái toàn cục ban đầu
        state = self._get_global_state()
        
        for t in range(num_steps):
            print(f"\n" + "="*15 + f" Time Step {t} " + "="*15)
            
            # 1. Agent quan sát trạng thái và ra quyết định
            action = self.agent.get_action(state)
            print(f"[Orchestrator] Agent decided action -> {action}")
            
            # 2. Phân phối action và thực thi trên các simulator
            # Dùng .get() để an toàn, nếu một key không tồn tại, nó trả về None
            classical_action = action.get("classical")
            quantum_action = action.get("quantum")
            
            c_next_state, c_reward, _, _ = self.classical_sim.step(classical_action)
            q_next_state, q_reward, _, _ = self.quantum_sim.step(quantum_action)
            
            # 3. Tổng hợp kết quả
            next_state = self._get_global_state()
            # Cách tính reward tổng có thể phức tạp hơn, ở đây ta chỉ cộng lại
            total_reward = c_reward + q_reward 
            
            print(f"[Orchestrator] Step resulted in total reward -> {total_reward:.4f}")
            
            # 4. Cho Agent "học" từ kinh nghiệm (quan trọng cho RL sau này)
            # Hiện tại RandomAgent không làm gì, nhưng đây là chỗ để agent thông minh học
            done = (t == num_steps - 1)
            self.agent.learn(state, action, total_reward, next_state, done)
            
            # 5. Cập nhật trạng thái cho vòng lặp tiếp theo
            state = next_state
            
        print("\n" + "="*17 + " Simulation Finished " + "="*17)
