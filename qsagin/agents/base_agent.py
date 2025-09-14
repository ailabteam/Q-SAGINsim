# File: qsagin/agents/base_agent.py

import numpy as np
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """
    Abstract Base Class for all AI agents.
    This defines the "contract" that any agent must follow: it must be able to
    provide an action based on a given state.
    """
    @abstractmethod
    def get_action(self, state):
        """
        Receives the current state of the environment and returns an action.
        
        Args:
            state (dict): The current state of the system, typically containing
                          'classical' and 'quantum' substates.
                          
        Returns:
            dict: An action dictionary. The structure depends on the specific problem.
        """
        pass
    
    def learn(self, state, action, reward, next_state, done):
        """
        (Optional) Allows the agent to learn from an experience tuple.
        This method is crucial for Reinforcement Learning agents but can be left empty
        for simple agents like RandomAgent.
        
        Args:
            state: The state before the action was taken.
            action: The action taken.
            reward: The reward received after the action.
            next_state: The state after the action was taken.
            done (bool): A flag indicating if the episode has ended.
        """
        pass


class RandomAgent(BaseAgent):
    """
    A simple agent that takes random actions.
    This agent is primarily used for testing the simulation loop and environment interaction.
    """
    def __init__(self, num_quantum_links=5, num_satellites=5):
        """
        Initializes the RandomAgent.
        
        Args:
            num_quantum_links (int): The size of the discrete action space. For the default
                                     ns3-gym 'opengym' scenario, this is 5.
            num_satellites (int): Kept for API compatibility, but not used in the
                                  simplified action generation.
        """
        # For the default 'opengym' C++ scenario, the action space is Discrete(5).
        # We use num_quantum_links to represent this size.
        self.action_space_size = num_quantum_links
        print(f"RandomAgent initialized with action space size: {self.action_space_size}")

    def get_action(self, state):
        """
        Generates a random action compatible with the simple 'opengym' environment.
        The default ns-3 environment expects a single integer as an action.
        
        Args:
            state (dict): The current environment state (ignored by this agent).
            
        Returns:
            dict: An action dictionary containing a single random integer for both
                  'classical' and 'quantum' keys to ensure compatibility with
                  the Orchestrator and the underlying ns-3 environment.
        """
        # Generate a single random integer from 0 to (action_space_size - 1)
        random_action = np.random.randint(0, self.action_space_size)
        
        # We still return a dictionary to maintain a consistent API with the Orchestrator.
        # Both keys point to the same action. The Orchestrator will pick the correct one.
        action = {
            "classical": random_action,
            "quantum": random_action
        }
        return action
