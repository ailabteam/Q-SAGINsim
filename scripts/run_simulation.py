# File: scripts/run_simulation.py
import sys
import os
import time
import numpy as np

# Add the project root to the Python path
sys.path.append('/app')

from qsagin.core.orchestrator import Orchestrator
from qsagin.simulators.sim_classical import NS3Simulator
from qsagin.simulators.sim_quantum import SequenceSimulator
from qsagin.agents.base_agent import RandomAgent

def define_scenario_config():
    """Defines a hybrid scenario with both classical and quantum simulators."""
    config = {
        "simulation": {
            "steps": 10 
        },
        "classical_network": {
            # Config for NS3Simulator
            "port": 5555,
            "sim_args": {"--simTime": 10} # Let ns-3 run for 10s
        },
        "quantum_network": {
            # Config for SequenceSimulator
            "sim_time_ns": 10e9, # 10 simulated seconds
            "topology": {
                "nodes": ["Alice", "Bob"],
                "distance": 1e3, # 1 km
            },
            "key_size": 256,
            "num_keys": 10,
        },
        "agent": {
            # Action space for ns-3 is Discrete(5), SeQUeNCo is 1
            "action_space_size": 5 
        }
    }
    return config

def main():
    print("=" * 60)
    print("      RUNNING FULL Q-SAGINSIM FRAMEWORK (NS-3 + SeQUeNCo)")
    print("=" * 60)
    
    config = define_scenario_config()

    print("\n[SETUP] Initializing components...")
    
    # Initialize the real classical simulator
    try:
        classical_sim = NS3Simulator(sim_config=config["classical_network"])
    except Exception as e:
        print(f"\n[FATAL] Could not initialize NS3Simulator. Is the ns-3 process running?")
        print(f"Error: {e}")
        return

    # Initialize the real quantum simulator
    quantum_sim = SequenceSimulator(sim_config=config["quantum_network"])
    
    # Initialize a random agent
    agent = RandomAgent(num_quantum_links=config["agent"]["action_space_size"])
    
    # Assemble the orchestrator
    orchestrator = Orchestrator(classical_sim, quantum_sim, agent)
    
    print("\nWaiting 2 seconds for ns-3 process to be ready...")
    time.sleep(2)

    try:
        # Run the full simulation loop
        orchestrator.run(num_steps=config["simulation"]["steps"])
    except Exception as e:
        print(f"\n[FATAL] An error occurred during the simulation run.")
        print(f"Error: {e}")
    finally:
        classical_sim.close()

    print("\n" + "="*25 + " HYBRID SIMULATION FINISHED " + "="*25)

if __name__ == "__main__":
    main()
