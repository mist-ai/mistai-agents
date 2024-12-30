from letta import create_client
from ips_agent.ips_agent import IPSAgent
from orchestrator.orchestrator import Orchestrator


def main():
    client = create_client()
    ips_agent = IPSAgent(client=client)

    ips_agent.create()

    orchestrator = Orchestrator(client=client)
    orchestrator.create()


if __name__ == "__main__":
    main()
