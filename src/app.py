from letta import create_client
from ips_agent.ips_agent import IPSAgent


def main():
    client = create_client()
    ips_agent = IPSAgent(client=client)

    ips_agent.create()


if __name__ == "__main__":
    main()
