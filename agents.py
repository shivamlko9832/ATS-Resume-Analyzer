from crewai import Agent

import os

# Use your working OpenAI key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

MODEL = "gpt-4o-mini"

def build_parser_agent(model: str = MODEL) -> Agent:
    """
    Build and return a Resume Parsing Specialist agent.

    This agent is responsible for extracting clean, structured text from resumes 
    to optimize them for Applicant Tracking Systems (ATS). It removes formatting 
    artifacts, normalizes content, and ensures important details are preserved 
    while eliminating noise.

    Args:
        model (str): The underlying language model to be used by the agent.
                     Defaults to the global `MODEL` constant.

    Returns:
        Agent: Configured CrewAI agent instance for resume parsing.
    """
    return Agent(
        role="Resume Parsing Specialist",
        goal="Extract structured, ATS-friendly text from resumes while preserving key details.",
        backstory=(
            "You are a highly skilled specialist in processing resumes. "
            "Your expertise lies in cleaning raw text, removing formatting artifacts, "
            "standardizing structure, and ensuring content is ATS-compatible. "
            "You work quickly and precisely, retaining critical details while "
            "eliminating unnecessary noise."
        ),
        model=model,
        temperature=0.0,             # Deterministic, consistent outputs
        max_iter=1,                  # Single-pass parsing
        max_execution_time=120,      # Timeout safeguard (seconds)
    )

    
    
def build_ats_writer_agent(model: str = MODEL) -> Agent:
    """
    Build and return an ATS Optimization Writer agent.

    This agent specializes in transforming resumes into high-scoring,
    ATS-optimized documents that align with job descriptions. It focuses
    on strategic keyword placement, strong action verbs, quantified
    achievements, and formatting choices that maximize ATS compatibility.

    Args:
        model (str): The language model to power the agent.
                     Defaults to the global `MODEL` constant.

    Returns:
        Agent: Configured CrewAI agent instance for ATS resume writing.
    """
    return Agent(
        role="ATS Optimization Writer",
        goal="Craft ATS-friendly resumes that score highly and align with specific job requirements.",
        backstory=(
            "You are an experienced resume writer and ATS specialist. "
            "Your role is to optimize resumes so they rank high in Applicant "
            "Tracking Systems (ATS). You strategically place industry-specific "
            "keywords, integrate strong action verbs, and quantify achievements "
            "to highlight impact. You ensure the resume is both recruiter-friendly "
            "and machine-readable, consistently achieving high ATS scores."
        ),
        model=model,
        temperature=0.3,             # Balanced creativity with structure
        max_iter=1,                  # Single-pass optimization
        max_execution_time=120,      # Timeout safeguard (seconds)
    )

    
    
def build_evaluator_agent(model: str = MODEL) -> Agent:
    """
    Build and return an ATS Evaluator agent.

    This agent evaluates resumes for ATS compatibility by scoring them
    against typical Applicant Tracking System criteria. It highlights
    keyword coverage, section structure, formatting compliance, and 
    the use of measurable achievements. The agent also provides 
    actionable recommendations for improving ATS scores.

    Args:
        model (str): The language model to power the agent.
                     Defaults to the global `MODEL` constant.

    Returns:
        Agent: Configured CrewAI agent instance for ATS evaluation.
    """
    return Agent(
        role="ATS Evaluator",
        goal="Deliver ATS score evaluations with detailed, actionable recommendations for improvement.",
        backstory=(
            "You are an expert ATS scoring and compliance specialist. "
            "Your role is to assess resumes with precision, focusing on "
            "keyword density, section hierarchy, formatting clarity, and "
            "quantified achievements. You provide clear, prioritized, and "
            "actionable recommendations to ensure resumes achieve the highest "
            "possible ATS scores."
        ),
        model=model,
        temperature=0.0,             # Fully deterministic scoring
        max_iter=1,                  # Single evaluation per request
        max_execution_time=120,      # Timeout safeguard (seconds)
    )


def build_refiner_agent(model: str = MODEL) -> Agent:
    """
    Build and return a Bullet Point Refiner agent.

    This agent specializes in transforming resume bullet points into
    concise, high-impact, ATS-optimized statements. It ensures the use
    of strong action verbs, measurable achievements, and quantifiable
    metrics while maintaining clarity and readability.

    Args:
        model (str): The language model to power the agent.
                     Defaults to the global `MODEL` constant.

    Returns:
        Agent: Configured CrewAI agent instance for bullet point refinement.
    """
    return Agent(
        role="Bullet Point Refiner",
        goal="Enhance resume bullet points into concise, impactful, and ATS-friendly statements with measurable results.",
        backstory=(
            "You are an expert at refining resume bullet points into powerful, "
            "results-driven statements. You strategically integrate strong action "
            "verbs, highlight key achievements, and ensure metrics are used to "
            "quantify impact. Your refinements maximize clarity, recruiter appeal, "
            "and ATS compatibility."
        ),
        model=model,
        temperature=0.2,             # Slight creativity for varied phrasing
        max_iter=1,                  # Single refinement pass
        max_execution_time=120,      # Timeout safeguard (seconds)
    )

