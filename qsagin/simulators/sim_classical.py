# File: qsagin/simulators/sim_classical.py
from ns3gym import ns3env
from .base_simulator import BaseSimulator

class NS3Simulator(BaseSimulator):
    """
    Simulator for the classical network, using ns-3 and ns3-gym as a backend.
    Connects to an already running ns-3 script.
    API is adapted to match the old Gym (4-value step) and our framework's expectations.
    """
    def __init__(self, sim_config):
        super().__init__(sim_config)
        self.env = None
        self.last_observation = None
        port = self.config.get("port", 5555)
        print(f"NS3Simulator: Initializing client to connect to ns-3 on port {port}...")
        self.env = ns3env.Ns3Env(port=port, startSim=False)
        
    def setup(self):
        print("NS3Simulator: Setup complete. Ready to connect and reset.")
        pass

    def step(self, action):
        """
        Takes an action and performs one step in the ns-3 simulation.
        The underlying ns3-gym env.step() returns 4 values: (obs, reward, done, info).
        """
        if self.env is None:
            raise RuntimeError("Environment is not initialized.")
        
        if isinstance(action, dict):
            action_to_send = action.get("classical", action.get("quantum"))
        else:
            action_to_send = action
            
        # === FINAL FIX: Correctly unpack and return 4 values ===
        obs, reward, done, info = self.env.step(action_to_send)
        self.last_observation = obs
        # Return the 4 values directly, as expected by the Orchestrator
        return obs, reward, done, info
        # ========================================================

    def get_state(self):
        """Returns the last known observation."""
        return self.last_observation

    def reset(self):
        """
        Resets the ns-3 simulation.
        The underlying ns3-gym env.reset() returns 1 value (obs).
        We adapt it to return 2 values (obs, info) for our Orchestrator.
        """
        if self.env is None:
            raise RuntimeError("Environment is not initialized.")
            
        print("NS3Simulator: Sending reset signal...")
        obs = self.env.reset()
        self.last_observation = obs
        return obs, {} # Return dummy info dict

    def close(self):
        """Closes the connection."""
        print("NS3Simulator: Closing connection.")
        if self.env:
            self.env.close()
            self.env = None
