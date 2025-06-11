from resume_tailor.crews.profile_builder_crew.profile_builder_crew import ProfileBuilderCrew

def build_user_profile(resume_text: str) -> str:
    crew = ProfileBuilderCrew()
    inputs = {"original_resume": resume_text}
    crew_output = crew.crew().kickoff(inputs=inputs)
    return str(crew_output)
