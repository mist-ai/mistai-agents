# MIST.ai Agents

## Overview

This project contains following `letta` agents.

### 1. Orchestrator Agent

Orchestrator agent coordinates the execution of tasks across multiple agents. It ensures that each agent performs its designated function and communicates effectively with other agents.

### 2. IPS Agent

IPS agent manages the user's Investor Policy Statement. It stores and retrieves relevant data from the Investor Policy Statement.

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/mist-ai/mistai-agents.git
   cd mistai-agents
   ```

2. Setup your environment:

   ```bash
   # setup uv in you machine (globally)
   # On macOS and Linux.
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # On Windows.
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

   # if need (locally)
   # With pip.
   pip install uv
   ```

   ```bash
   # install virtual env and activate
   uv venv --python 3.12.0
   source .venv/bin/activate
   ```

   #### Note: `Set your IDE to use .venv as your interpriter`

3. Install the dependencies:

   ```bash
   # install packages using pyproject.toml
   uv pip install -r pyproject.toml
   ```

4. Setup .env file

* `Create a .env file in the root directory and the env variables will be loaded`. Example .env file can be found in `.env-example` file
## Usage

1. Set up environment variables by copying `.env.example` to [.env](http://_vscodecontentref_/6) and updating the values as needed.

2. Run the application:

   ```sh
   python src/app.py
   ```

3. If required clear the current letta database:

   ```bash
   rm ~/.letta/sqlite.db
   ```

4. Run the letta server:

   ```bash
   letta server
   ```

5. Access [`Letta ADE`](https://app.letta.com/development-servers/local/dashboard) from here to interact with the agents.

## Configuration

Configuration settings can be found in [config.py](https://github.com/mist-ai/mistai-agents). Adjust the settings as needed for your environment.

## Components

- **IPS Agent**: Located in [ips_agent.py](https://github.com/mist-ai/mistai-agents), this component handles interactions with the IPS system.
- **Orchestrator**: Located in [orchestrator.py](https://github.com/mist-ai/mistai-agents), this component manages the workflow and communication between different agents.
- **Utilities**: Common utility functions are located in [utils.py](https://github.com/mist-ai/mistai-agents).

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](https://github.com/mist-ai/mistai-agents/blob/dev/LICENSE) file for details.

## Contributing

Contributions are welcome! Please read the CONTRIBUTING.md for guidelines on how to contribute to this project.

## Contact

For any questions or issues, please open an issue on the repository or contact the maintainers.
