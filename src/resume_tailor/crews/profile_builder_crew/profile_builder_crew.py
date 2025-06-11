from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task
from typing import List

# Uncomment the following line to use an example of a custom tool
# from profile_builder_crew.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool


@CrewBase
class ProfileBuilderCrew:
    """ProfileBuilderCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def profile_builder(self) -> Agent:
        return Agent(config=self.agents_config["profile_builder"], verbose=True)

    @task
    def build_user_profile_task(self) -> Task:
        return Task(config=self.tasks_config["build_user_profile_task"])

    @crew
    def crew(self) -> Crew:
        """Creates the ProfileBuilderCrew crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
