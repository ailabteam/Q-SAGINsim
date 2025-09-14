# File: scripts/run_simulation.py
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from qsagin.core.orchestrator import Orchestrator
from qsagin.simulators.sim_classical import MockClassicalSimulator
from qsagin.simulators.sim_quantum import SequenceSimulator
from qsagin.agents.base_agent import RandomAgent

def define_scenario_config():
    """Defines a simple 2-node BB84 scenario based on the official example."""
    node_names = ["Alice", "Bob"]
    
    config = {
        "simulation": {
            # Since SeQUeNCo runs to completion, we only need 1 step in our framework
            "steps": 1 
        },
        "classical_network": {
            "num_nodes": len(node_names)
        },
        "quantum_network": {
            "sim_time_ns": 10e9, # 10 simulated seconds
            "topology": {
                "nodes": node_names,
                "distance": 1e3, # 1 km
            },
            "attenuation": 1e-5, # 0.01 dB/km
            "key_size": 256,
            "num_keys": 50,
        },
        "agent": {
            "num_quantum_actions": 1 
        }
    }
    return config

def main():
    print("=" * 50)
    print("      INITIALIZING Q-SAGINSIM FRAMEWORK")
    print("      (Logic based on official SeQUeNCo example)")
    print("=" * 50)
    
    config = define_scenario_config()

    classical_sim = MockClassicalSimulator(sim_config=config["classical_network"])
    quantum_sim = SequenceSimulator(sim_config=config["quantum_network"])
    agent = RandomAgent(
        num_satellites=config["classical_network"]["num_nodes"],
        num_quantum_links=config["agent"]["num_quantum_actions"]
    )
    
    # NOTE: The Orchestrator is now simplified. For this example,
    # it will just run for a single step to trigger the SeQUeNCo simulation.
    orchestrator = Orchestrator(
        classical_sim=classical_sim,
        quantum_sim=quantum_sim,
        agent=agent
    )
    
    orchestrator.run(num_steps=config["simulation"]["steps"])
    
    # Print final result from the get_state method
    final_state = quantum_sim.get_state()
    print("\n" + "="*20 + " FINAL RESULT " + "="*20)
    print(f"Final Key Rate: {final_state['key_rate_bps']:.2f} bps")
    print("="*52)


if __name__ == "__main__":
    main()
