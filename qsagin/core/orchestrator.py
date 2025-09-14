# File: qsagin/core/orchestrator.py

class Orchestrator:
    """
    The Orchestrator class acts as the central conductor for the simulation.
    It manages the simulation loop, coordinates the simulators (classical and quantum),
    and communicates with the AI agent.
    """
    def __init__(self, classical_sim, quantum_sim, agent):
        """
        Initializes the Orchestrator with dependency injection.

        Args:
            classical_sim: An object that conforms to the BaseSimulator API for the classical network.
            quantum_sim: An object that conforms to the BaseSimulator API for the quantum network.
            agent: An object that conforms to the BaseAgent API.
        """
        print("Orchestrator is being created...")
        self.classical_sim = classical_sim
        self.quantum_sim = quantum_sim
        self.agent = agent

    def _get_global_state(self):
        """
        A private method to collect and aggregate the state from all simulators.
        This method relies on the `get_state()` implementation of each simulator,
        which should return the last known observation.

        Returns:
            dict: A dictionary containing the composite state of the entire system.
        """
        state = {
            "classical": self.classical_sim.get_state(),
            "quantum": self.quantum_sim.get_state(),
        }
        return state

    def run(self, num_steps):
        """Vòng lặp mô phỏng chính."""
        print("=== Starting Simulation Run ===")
        
        # --- DEBUGGING ---
        print("[Orchestrator DEBUG] About to reset classical_sim...")
        class_obs, class_info = self.classical_sim.reset()
        print("[Orchestrator DEBUG] classical_sim.reset() finished.")
        
        print("[Orchestrator DEBUG] About to reset quantum_sim...")
        quant_obs, quant_info = self.quantum_sim.reset()
        print("[Orchestrator DEBUG] quantum_sim.reset() finished.")
        # --- END DEBUGGING ---

        state = self._get_global_state()
        
        for t in range(num_steps):
            print(f"\n" + "="*15 + f" Time Step {t + 1}/{num_steps} " + "="*15)
            
            action = self.agent.get_action(state)
            print(f"[Orchestrator] Agent decided action -> {action}")
            
            classical_action = action.get("classical", action.get("quantum"))
            quantum_action = action.get("quantum")
            
            # --- DEBUGGING ---
            print("[Orchestrator DEBUG] About to step classical_sim...")
            c_next_obs, c_reward, c_done, c_info = self.classical_sim.step(classical_action)
            print("[Orchestrator DEBUG] classical_sim.step() finished.")

            print("[Orchestrator DEBUG] About to step quantum_sim...")
            q_next_obs, q_reward, q_done, q_info = self.quantum_sim.step(quantum_action)
            print("[Orchestrator DEBUG] quantum_sim.step() finished.")
            # --- END DEBUGGING ---

            next_state = self._get_global_state()
            total_reward = c_reward + q_reward 
            done = c_done or q_done
            
            print(f"[Orchestrator] Step resulted in total reward -> {total_reward:.4f}")
            
            self.agent.learn(state, action, total_reward, next_state, done)
            
            state = next_state
            
            if done:
                print(f"--- Episode finished at step {t + 1} ---")
                break
            
        print("\n" + "="*17 + " Simulation Finished " + "="*17)
