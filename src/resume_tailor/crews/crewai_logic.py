from crewai import Agent, Task, Crew, Process
from crewai_tools import ScrapeWebsiteTool

def create_agents():
    web_scraper = Agent(
        role="Web Content Scraper",
        goal="Scrape the full job description from the job posting URL.",
        backstory="Expert at extracting structured information from web pages.",
        tools=[ScrapeWebsiteTool()]
    )
    resume_tailor = Agent(
        role="Resume Tailor",
        goal="Tailor the user's resume to match the job description for maximum ATS score.",
        backstory="Expert in resume optimization for ATS systems."
    )
    markdown_expert = Agent(
        role="Markdown Expert",
        goal="Create a markdown document that can be used to generate an attractive Word document.",
        backstory="You are a Markdown formatter for generating attractive Word documents."
    )
    return [web_scraper, resume_tailor, markdown_expert]

def create_tasks(job, resume_text, web_scraper, resume_tailor, markdown_expert):
    get_full_job_description = Task(
        description=f"Scrape the full job description from {job['final_url']}.",
        expected_output="The full job description as plain text.",
        agent=web_scraper
    )
    tailor_resume_to_job_description = Task(
        description=(
            "Tailor the following resume to match the job description provided. "
            "The tailored resume must be optimized for Applicant Tracking Systems (ATS):\n"
            f"Resume:\n{resume_text}\n"
            "Job Description: (output of previous task)\n"
            "Do not apply any formatting to the links, like GitHub, LinkedIn, etc.\n"
        ),
        expected_output=(
            "A tailored resume as a generic markdown that can be used by the Markdown Expert agent."
        ),
        agent=resume_tailor,
        context=[get_full_job_description]
    )
    create_markdown_document = Task(
        description=(
            "Create a markdown document that can be used to generate an attractive Word document.\n"
            "Use the tailored resume created in the previous step by the Resume Tailor agent as the basis for the markdown document.\n"
            "The markdown should be formatted with headers, bold, italic, and bullet points so it can be converted to an attractive Word document.\n"
            "Remove the ```markdown``` tags from the output.\n"
            "Remove all the text after the final --- line.\n"
            "Remove the final --- line.\n"
            "Do not apply any formatting to the links, like GitHub, LinkedIn, etc.\n"
            "Keep the core skills section's details together in one paragraph but separate each detail.\n"
            "Do not add any lines between the major sections, like 'Core Skills', 'Experience', 'Education', etc.\n"
            "In Core Skills and in Certifications, items are separated inline with the “bullet” character • and spaces, e.g.: Swift • SwiftUI • UIKit • …\n"
            "Use # for the applicant name in the first line. Add space after the name.\n"
            "Use ## for each main section title (e.g. ## Core Skills, ## Professional Experience).\n"
            "Under each role heading, use a top-level unordered list • for each responsibility or achievement.\n"
            
            # Create a markdown document that can be used to generate an attractive Word document.
            
            # When creating the markdown document you must follow this distilled set of formatting conventions:

            # 1. Section and Heading Rules

            # 1.1. Heading levels
            # - Use ## for each main section title (e.g. ## Core Skills, ## Professional Experience).
            # - Within 'Professional Experience' use ### for each role title (e.g. ### Senior iOS Engineer).

            # 1.2. No extra blank lines
            # - Do not insert blank lines between a section heading and its first paragraph/list.
            # - Separate logical blocks (e.g. end of one job’s bullets before the next ###) with exactly one blank line.

            # 2. Paragraphs and Line-breaks
            # 2.1. Body copy
            # - Wrap long descriptions at ~80 chars, but treat each logical paragraph as a single markdown paragraph (no manual hard line-breaks).

            # 2.2. Soft breaks in Core Skills
            # - Within the Core Skills paragraph, use soft line-breaks (\n) to wrap, not new paragraphs.

            # 3. Lists and Bullets

            # 3.1. Role–details lists
            # - Under each ### role heading, use a top-level unordered list - for each responsibility or achievement.
            # - No nesting—only one level of bullets.

            # 3.2. Inline “dot” lists
            # - In Core Skills and in Certifications, items are separated inline with the “bullet” character • and spaces, e.g.: 
            # Swift • SwiftUI • UIKit • …
            # - If the line overflows, soft-wrap it; do not convert to a multi-line Markdown list.

            # 4. Emphasis & Styling

            # 4.1. Bold
            # - Job titles, company names, and section headers are bolded, e.g.:
            # - **Lead Engineer**, Acme Corp (2020–2024)

            # 4.2. Italic
            # - Dates and locations appear in italic or within parentheses with no extra styling, e.g.:
            # (Jan 2019 – Dec 2020)
            # - You may choose *…* or _…_, but be consistent.

            # 5. Links and URLs

            # 5.1. Inline links only
            # - Use [Label](URL) syntax, e.g.:
            # [GitHub](http://github.com/DenisEfremov71)
            # - Do not switch to reference-style links.

            # 5.2. No additional formatting
            # - Leave URLs or labels as-is (do not bold, italicize, or underline them).

            # 6. Horizontal Rules

            # - There are no horizontal rules (---) in the document.
            # - Do not insert them between sections.

            # 7. Code Blocks

            # - None present; do not introduce fenced code blocks.
            
        ),
        expected_output=(
            "A markdown document that can be used to generate an attractive Word document."
        ),
        agent=markdown_expert,
        context=[tailor_resume_to_job_description]
    )
    return [get_full_job_description, tailor_resume_to_job_description, create_markdown_document]

async def run_crew_for_job(job, resume_text, selected_model):
    # Use the manually entered final_url
    if "final_url" not in job or not job["final_url"]:
        job["final_url"] = job["link"]
    web_scraper, resume_tailor, markdown_expert = create_agents()
    tasks = create_tasks(job, resume_text, web_scraper, resume_tailor, markdown_expert)
    crew = Crew(
        agents=[web_scraper, resume_tailor, markdown_expert],
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
        model=selected_model
    )
    result = await crew.kickoff_async(inputs={"job_url": job["final_url"], "resume": resume_text, "model": selected_model})
    tailored_resume = str(result)
    return job, tailored_resume