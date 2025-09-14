# File: scripts/debug_sequence.py
from sequence.kernel.timeline import Timeline
# Import Node cơ bản
from sequence.topology.node import Node
from sequence.components.optical_channel import QuantumChannel
from sequence.kernel.process import Process
from sequence.kernel.event import Event
from sequence.utils.quantum_state import QuantumState

# 1. Setup
# Dùng formalism mặc định (KET)
tl = Timeline(stop_time=1e9) 
node1 = Node("node1", tl)
node2 = Node("node2", tl)

qc = QuantumChannel("qc", tl, attenuation=0, distance=1e3)
qc.set_ends(node1, node2)

# 2. Define a simple protocol manually
class SenderProcess(Process):
    def __init__(self, owner, receiver_name):
        super().__init__(owner, "sender_process")
        self.receiver_name = receiver_name

    def run(self):
        print(f"Time {self.owner.timeline.now()}: Node 1 sending qubit.")
        qubit = QuantumState() # Create a new qubit
        self.owner.send_qubit(self.receiver_name, qubit)

class ReceiverProcess(Process):
    def __init__(self, owner):
        super().__init__(owner, "receiver_process")
        # Override the default receive_qubit method
        owner.receive_qubit = self.custom_receive_qubit
        self.num_received = 0

    def custom_receive_qubit(self, src, qubit):
        print(f"Time {self.owner.timeline.now()}: Node 2 received qubit from {src}.")
        self.num_received += 1

# 3. Create and schedule the protocol
sender = SenderProcess(node1, "node2")
receiver = ReceiverProcess(node2)

# Schedule the sender to run at time 0
event = Event(0, sender)
tl.schedule(event)

# 4. Initialize and run
tl.init()
tl.run()

# 5. Inspect
print("\n" + "="*20 + " INSPECTION " + "="*20)
print(f"Total qubits received by Node 2: {receiver.num_received}")
if receiver.num_received > 0:
    print("SUCCESS: Basic qubit transmission works!")
