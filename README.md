# Q-SAGINsim: A Flexible Simulation Framework for Quantum SAGIN

`Q-SAGINsim` is a research framework designed for simulating and optimizing Space-Air-Ground Integrated Networks (SAGIN) that incorporate quantum communication protocols. It provides a modular, flexible platform to test novel AI/ML algorithms for resource management, routing, and security in next-generation networks.

The framework integrates two powerful, domain-specific simulators:
- **`SeQUeNCo`**: For simulating the quantum network layer (e.g., QKD, entanglement distribution).
- **`ns-3`**: For simulating the classical network layer (e.g., satellite orbits, traffic, wireless channels).

An `Orchestrator` coordinates these simulators, while an `AI Agent` (e.g., Reinforcement Learning) makes intelligent decisions.

## Environment & Setup

The entire simulation environment, including all complex dependencies (`ns-3`, `SeQUeNCo`, `ns3-gym`, C++ compilers, Python libraries), is encapsulated in a Docker container. This ensures 100% reproducibility and eliminates complex manual installation.

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/)

### Quick Start: Using the Pre-built Docker Image

A pre-built and tested Docker image is available on Docker Hub. This is the recommended way to get started.

1.  **Pull the Docker Image:**
    ```bash
    docker pull haodpsut/q-saginsim-env:latest
    ```

2.  **Run the Container:**
    To start an interactive session inside the environment, run the following command from the root of this project directory.
    ```bash
    # This mounts your local project folder into the container's /app directory,
    # allowing you to edit code on your machine and run it inside the container.
    docker run --rm -it --network=host -v $(pwd):/app haodpsut/q-saginsim-env:latest bash
    ```
    *   `--rm`: Automatically removes the container when you exit.
    *   `--it`: Runs in interactive mode.
    *   `--network=host`: Required for the `ns3-gym` communication socket to work across terminals.
    *   `-v $(pwd):/app`: Maps your current project directory to `/app` inside the container.

### How to Run Simulations

#### Running the `ns-3` Integration Test (2-Terminal Process)

Simulating the classical network with `ns-3` requires a 2-terminal process: one for the `ns-3` simulation (the "server") and one for the Python control logic (the "client").

**In Terminal 1: Start the `ns-3` Server**

1.  Start a container:
    ```bash
    docker run --rm -it --network=host -v $(pwd):/app haodpsut/q-saginsim-env:latest bash
    ```

2.  Inside the container, run the `ns-3` script. It will wait for a connection.
    ```bash
    # The default 'opengym' C++ scenario will start and listen on port 5555.
    /workspace/ns-allinone-3.40/ns-3.40/ns3 run "opengym"
    ```
    This terminal will now print `Waiting for Python process to connect...` and appear to hang, which is the correct behavior.

**In Terminal 2: Start the Python Framework**

1.  Start a second container:
    ```bash
    docker run --rm -it --network=host -v $(pwd):/app haodpsut/q-saginsim-env:latest bash
    ```

2.  Inside this second container, run the integration test script:
    ```bash
    python3 /app/scripts/run_ns3_only.py
    ```
    You will see the Python script connect to the `ns-3` process in Terminal 1, and the simulation will begin, running for 10 steps.

#### Running the `SeQUeNCo` Integration Test

The quantum network simulation with `SeQUeNCo` can be run in a single terminal.

1. Start a container:
    ```bash
    docker run --rm -it -v $(pwd):/app haodpsut/q-saginsim-env:latest bash
    ```
2. Inside the container, run the main simulation script:
    ```bash
    python3 /app/scripts/run_simulation.py
    ```
---
### (Optional) Building the Docker Image from Source

If you wish to modify the environment (e.g., install new libraries), you can rebuild the Docker image from the `Dockerfile` in this repository.

```bash
# From the root of this project
docker build -t haodpsut/q-saginsim-env:latest .
```

## Project Structure

-   `qsagin/`: Main source code for the framework.
    -   `core/`: Contains the `Orchestrator`.
    -   `simulators/`: Contains wrappers for `SeQUeNCo` (`sim_quantum.py`) and `ns-3` (`sim_classical.py`).
    -   `agents/`: Contains AI agent implementations (e.g., `RandomAgent`).
-   `scripts/`: Executable scripts to run simulations.
-   `Dockerfile`: The recipe for building the simulation environment.
