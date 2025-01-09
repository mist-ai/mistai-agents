from dotenv import load_dotenv
from letta import create_client
from ips_agent.ips_agent import IPSAgent
from orchestrator.orchestrator import Orchestrator
# from io_agent.database_service import db
from news_agent.news_agent import NewsAgent

load_dotenv("./../.env")

def main():
    client = create_client()
    ips_agent = IPSAgent(client=client)

    ips_agent.create()

    orchestrator = Orchestrator(client=client)
    orchestrator.create()

    news_agent = NewsAgent(client=client)
    news_agent.create()


if __name__ == "__main__":

    main()
