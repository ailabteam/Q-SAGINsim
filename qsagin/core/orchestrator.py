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
        """
        print("Orchestrator is being created...")
        self.classical_sim = classical_sim
        self.quantum_sim = quantum_sim
        self.agent = agent
        
    def _get_global_state(self):
        """
        A private method to collect and aggregate the state from all simulators.
        """
        state = {
            "classical": self.classical_sim.get_state(),
            "quantum": self.quantum_sim.get_state(),
        }
        return state

    def run(self, num_steps):
        """
        Executes the main simulation loop for a given number of steps.
        """
        print("=== Starting Simulation Run ===")
        
        # 1. Reset all environments to their initial states.
        # The `reset` methods now correctly return two values: (observation, info_dictionary).
        print("Resetting classical simulator...")
        c_obs, c_info = self.classical_sim.reset()
        print("Resetting quantum simulator...")
        q_obs, q_info = self.quantum_sim.reset()
        
        # 2. Get the initial global state after resetting.
        state = self._get_global_state()
        
        for t in range(num_steps):
            print(f"\n" + "="*15 + f" Time Step {t + 1}/{num_steps} " + "="*15)
            
            # 3. The agent observes the current state and decides on an action.
            action = self.agent.get_action(state)
            print(f"[Orchestrator] Agent decided action -> {action}")
            
            # 4. Dispatch actions and execute a step in each simulator.
            classical_action = action.get("classical", action.get("quantum"))
            quantum_action = action.get("quantum")
            
            # The `step` method returns (next_observation, reward, done, info)
            c_next_obs, c_reward, c_done, c_info = self.classical_sim.step(classical_action)
            q_next_obs, q_reward, q_done, q_info = self.quantum_sim.step(quantum_action)
            
            # 5. Aggregate results from all simulators.
            next_state = self._get_global_state()
            total_reward = c_reward + q_reward 
            done = c_done or q_done
            
            print(f"[Orchestrator] Step resulted in total reward -> {total_reward:.4f}")
            
            # 6. (Optional) Allow the agent to learn.
            self.agent.learn(state, action, total_reward, next_state, done)
            
            # 7. Update the state for the next iteration.
            state = next_state
            
            # 8. If the episode is finished, end the loop.
            if done:
                print(f"--- Episode finished at step {t + 1} ---")
                break
            
        print("\n" + "="*17 + " Simulation Finished " + "="*17)
