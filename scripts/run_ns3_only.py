# File: scripts/run_ns3_only.py
import sys
import os
import time
import numpy as np # <--- THÊM DÒNG NÀY

# Add the project root to the Python path.
# This is necessary because we will run this script from inside the Docker container
# where the working directory might be different from our project root.
sys.path.append('/app')

from qsagin.core.orchestrator import Orchestrator
from qsagin.simulators.sim_classical import NS3Simulator
from qsagin.agents.base_agent import RandomAgent
from qsagin.simulators.base_simulator import BaseSimulator

# Create a minimal mock for the quantum simulator, as we are only testing ns-3
class MockQuantumSimulator(BaseSimulator):
    def setup(self): pass
    def step(self, action): return np.array([]), 0, False, {}
    def get_state(self): return None
    def reset(self): return np.array([]), {}

def main():
    """
    Main function to run the Python side of the ns-3 integration test.
    This script should be run AFTER the ns-3 simulation has been started in another terminal.
    """
    print("=" * 60)
    print("      Q-SAGINsim: NS3-GYM PYTHON AGENT (CLIENT MODE)")
    print("=" * 60)

    # Configuration for the NS3Simulator client
    ns3_config = {
        "port": 5555
    }

    print("Initializing components...")
    # Initialize the real classical simulator
    try:
        classical_sim = NS3Simulator(sim_config=ns3_config)
    except Exception as e:
        print(f"\n[FATAL] Could not initialize NS3Simulator. Is the ns-3 process running?")
        print(f"Error: {e}")
        return

    # Initialize a mock for the quantum part
    quantum_sim = MockQuantumSimulator(sim_config={})

    # Initialize a random agent.
    # The default 'opengym' C++ scenario has an action space of Discrete(5).
    # We pass this info to our agent.
    agent = RandomAgent(num_satellites=5, num_quantum_links=5)

    # Assemble the orchestrator
    orchestrator = Orchestrator(classical_sim, quantum_sim, agent)

    # Give ns-3 a moment to fully start up before we connect
    print("\nWaiting 2 seconds for ns-3 process to be ready...")
    time.sleep(2)

    # Run the simulation loop
    # The orchestrator will call reset() and step() on the NS3Simulator,
    # which will communicate with the running ns-3 process.
    try:
        orchestrator.run(num_steps=10) # Run for 10 agent steps
    except Exception as e:
        print(f"\n[FATAL] An error occurred during the simulation run.")
        print(f"Error: {e}")
    finally:
        # Ensure the connection is closed
        classical_sim.close()

    print("\n" + "="*25 + " NS-3 TEST FINISHED " + "="*25)

if __name__ == "__main__":
    main()
