from agents.acceptance_agent import AcceptanceAgent


agent = AcceptanceAgent()

result = agent.generate(
    """
    As a registered customer,
    I want to login using my email and password,
    so that I can access my account dashboard.
    """
)

for criterion in result.acceptance_criteria:
    print(
        criterion.id,
        criterion.description
    )