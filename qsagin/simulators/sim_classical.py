# File: qsagin/simulators/sim_classical.py
import gymnasium as gym
from ns3gym import ns3env
from .base_simulator import BaseSimulator
import numpy as np

class NS3Simulator(BaseSimulator):
    """
    Simulator for the classical network, using ns-3 and ns3-gym as a backend.

    This class operates in a "client" mode. It does not start the ns-3 simulation
    process itself. Instead, it connects to an already running ns-3 script
    that has opened a listening socket.

    This design is based on the verified "2-terminal" operation of ns3-gym.
    """
    def __init__(self, sim_config):
        """
        Initializes the simulator wrapper.

        Args:
            sim_config (dict): Configuration dictionary. Expected keys:
                - port (int): The port number to connect to the ns-3 simulation.
        """
        super().__init__(sim_config)
        self.env = None
        self.last_observation = None

        port = self.config.get("port", 5555)

        # startSim=False is the crucial parameter.
        # It tells ns3gym to act as a client and wait for a connection,
        # rather than trying to launch an ns-3 process.
        print(f"NS3Simulator: Initializing client to connect to ns-3 on port {port}...")
        self.env = ns3env.Ns3Env(port=port, startSim=False)

    def setup(self):
        """
        In this client model, setup is implicitly handled when the connection is made.
        The `reset()` call will perform the first true interaction.
        """
        print("NS3Simulator: Setup complete. Ready to connect and reset.")
        pass

    def step(self, action):
        """
        Takes an action and performs one step in the ns-3 simulation.
        """
        if self.env is None:
            raise RuntimeError("Environment is not initialized. Call reset() first.")
        
        if isinstance(action, dict):
            action_to_send = action.get("quantum", 0)
        else:
            action_to_send = action
            
        # === FINAL FIX: Unpack return value according to old Gym API ===
        # old gym.step() returns 4 values
        obs, reward, done, info = self.env.step(action_to_send)
        self.last_observation = obs
        # =============================================================
        return obs, reward, done, info


    def get_state(self):
        """
        Returns the last known observation from the environment.
        """
        return self.last_observation

    def reset(self):
        """
        Resets the ns-3 simulation environment.
        """
        if self.env is None:
            raise RuntimeError("Environment is not initialized.")
            
        print("NS3Simulator: Sending reset signal to ns-3 and waiting for first observation...")
        # === FINAL FIX: Handle single return value from old Gym API ===
        # old gym.reset() returns only the observation
        obs = self.env.reset()
        self.last_observation = obs
        # Return a dummy info dictionary to match our 2-value expectation
        return obs, {}

    def close(self):
        """Closes the connection to the ns-3 simulation."""
        print("NS3Simulator: Closing connection.")
        if self.env:
            self.env.close()
            self.env = None
