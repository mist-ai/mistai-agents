from dotenv import load_dotenv
from letta_client import Letta
from ips_agent.ips_agent import IPSAgent
from orchestrator.orchestrator import Orchestrator
from news_agent.news_agent import NewsAgent
from analysis_agent.analysis_agent import AnalysisAgent
from widget_agent.widget_agent import WidgetAgent
from io_agent.io_agent import IOAgent

load_dotenv("./../.env")


def main():
    client = Letta(base_url="http://localhost:8283")
    ips_agent = IPSAgent(client=client)
    ips_agent.create()

    orchestrator = Orchestrator(client=client)
    orchestrator.create()

    news_agent = NewsAgent(client=client)
    news_agent.create()

    analysis_agent = AnalysisAgent(client=client)
    analysis_agent.create()

    widget_agent = WidgetAgent(client=client)
    widget_agent.create()

    io_agent = IOAgent(client=client)
    io_agent.create()


if __name__ == "__main__":
    main()
