# File: qsagin/simulators/sim_quantum.py
import numpy as np
import time
from .base_simulator import BaseSimulator

from sequence.kernel.timeline import Timeline
from sequence.topology.node import QKDNode
from sequence.components.optical_channel import QuantumChannel, ClassicalChannel
from sequence.qkd.BB84 import pair_bb84_protocols

class SequenceSimulator(BaseSimulator):
    """
    Simulator for the quantum network, using the BB84 protocol.
    Logic is based on the official SeQUeNCo example notebook.
    """
    def __init__(self, sim_config):
        super().__init__(sim_config)
        self.timeline = None
        self.nodes = {}
        self.sender_protocol = None
        self.key_rate_bps = 0.0

    def setup(self):
        """Setup 2-node topology and BB84 protocol based on the official example."""
        print("Setting up SeQUeNCo based on official QKD example...")

        sim_time_ns = self.config.get("sim_time_ns", 5e9)
        self.timeline = Timeline(sim_time_ns)

        topology_config = self.config.get("topology", {})
        node_names = topology_config.get("nodes", [])
        assert len(node_names) == 2, "This scenario requires exactly 2 nodes."

        node1_name, node2_name = node_names

        node1 = QKDNode(node1_name, self.timeline, stack_size=1)
        node2 = QKDNode(node2_name, self.timeline, stack_size=1)
        self.nodes[node1_name] = node1
        self.nodes[node2_name] = node2

        pair_bb84_protocols(node1.protocol_stack[0], node2.protocol_stack[0])
        self.sender_protocol = node1.protocol_stack[0]

        distance = topology_config.get("distance", 1e3)
        attenuation = self.config.get("attenuation", 1e-5)

        qc12 = QuantumChannel(f"qc_{node1_name}_{node2_name}", self.timeline,
                              attenuation=attenuation, distance=distance)
        cc12 = ClassicalChannel(f"cc_{node1_name}_{node2_name}", self.timeline, distance=distance)
        qc12.set_ends(node1, node2_name)
        cc12.set_ends(node1, node2_name)

        qc21 = QuantumChannel(f"qc_{node2_name}_{node1_name}", self.timeline,
                              attenuation=attenuation, distance=distance)
        cc21 = ClassicalChannel(f"cc_{node2_name}_{node1_name}", self.timeline, distance=distance)
        qc21.set_ends(node2, node1_name)
        cc21.set_ends(node2, node1_name)

        self.timeline.init()

    def step(self, action):
        """
        Triggers the SeQUeNCo simulation to run to completion and returns results.
        This simulator is not designed for step-by-step control in the same way as ns-3.
        """
        # We only need to trigger this once.
        if action is not None and action == 0:
            print(f"[SeQUeNCo] Action: Pushing key generation request...")
            key_size = self.config.get("key_size", 256)
            num_keys = self.config.get("num_keys", 10) # Reduce for faster testing
            self.sender_protocol.push(length=key_size, key_num=num_keys)

            print("[SeQUeNCo] Running timeline to completion...")
            start_real_time = time.time()
            self.timeline.run()
            end_real_time = time.time()
            print(f"Execution time: {(end_real_time - start_real_time):.2f} s")

            self._update_state()

        reward = self.key_rate_bps
        # Since this runs to completion, we return done=True.
        # The observation is the final state.
        return self.get_state(), reward, True, {}

    def _update_state(self):
        """Get final metrics from the sender's protocol."""
        if self.sender_protocol.throughputs and self.sender_protocol.throughputs[-1] > 0:
            self.key_rate_bps = self.sender_protocol.throughputs[-1]
            print(f"\nSUCCESS: SeQUeNCo BB84 finished. Final throughput: {self.key_rate_bps:.2f} bps\n")

    def get_state(self):
        """Returns the final state of the quantum simulation."""
        return {"key_rate_bps": self.key_rate_bps}

    def reset(self):
        """
        Resets and re-setups the SeQUeNCo simulation.
        Returns the initial state and an empty info dictionary.
        """
        self.timeline = None
        self.nodes = {}
        self.sender_protocol = None
        self.key_rate_bps = 0.0
        self.setup()

        # Return initial state (observation) and an empty info dict
        return self.get_state(), {}
