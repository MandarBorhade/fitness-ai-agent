import streamlit as st
import os
import pathlib
from dotenv import load_dotenv, set_key 
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.utils.pprint import pprint_run_response
import textwrap
load_dotenv()

openai_key = os.environ.get("OPENAI_API_KEY")            
openai_model = OpenAIChat(id="gpt-4o-mini", api_key=openai_key)


st.set_page_config(
    page_title="AI workout companion",
    page_icon="🏋️‍♂️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("AI Workout Strategist 💪")

with st.sidebar:
    st.subheader("Gym rat details")
    age = st.number_input("Age", min_value=10, max_value=100, step=1, help="Enter your age")
    height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, step=0.1)
    activity_level = st.selectbox(
        "Activity Level",
        options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"],
        help="Choose your typical activity level"
    )
    
    weight = st.number_input("Weight (kg)", min_value=20.0, max_value=300.0, step=0.1)
    sex = st.selectbox("Sex", options=["Male", "Female", "Other"])
    fitness_goals = st.selectbox(
        "Fitness Goals",
        options=["Lose Weight", "Gain Muscle", "Endurance", "Stay Fit", "Strength Training"],
        help="What do you want to achieve?"
    )
    
    # selected_model = st.selectbox(label="LLM Model", options=['Open AI', 'Gemini'])
    
    generate_plan_button = st.button(label="Generate workout plan", type="primary")

user_profile = f"""
Age: {age}
Weight: {weight}kg
Height: {height}cm
Sex: {sex}
Activity Level: {activity_level}
Fitness Goals: {fitness_goals}"""

# fitness_agent = Agent(
#     name="Fitness Expert",
#     role="Provides personalized fitness recommendations",
#     description=textwrap.dedent(f"""
#     You are a world class fitness trainer. The user profile is as below:
#     Age: {age}
#     Weight: {weight}kg
#     Height: {height}cm
#     Sex: {sex}
#     Activity Level: {activity_level}
#     Fitness Goals: {fitness_goals}
#     """),
#     model=gemini_model,
#     instructions=[
#         "Provide exercises tailored to the user's goals.",
#         "Include warm-up, main workout, and cool-down exercises.",
#         "Explain the benefits of each recommended exercise.",
#         "Ensure the plan is actionable and detailed.",
#     ])

if generate_plan_button:
    with st.spinner("Generating fitness routine..."):
        try:
            fitness_agent = Agent(
            name="Fitness Expert",
            role="Provides personalized fitness recommendations",
            description=textwrap.dedent(f"""
            You are a world class fitness trainer. The user profile is as below:
            Age: {age}
            Weight: {weight}kg
            Height: {height}cm
            Sex: {sex}
            Activity Level: {activity_level}
            Fitness Goals: {fitness_goals}
            """),
            model=openai_model,
            instructions=[
                "Provide exercises tailored to the user's goals.",
                "Include warm-up, main workout, and cool-down exercises.",
                "Explain the benefits of each recommended exercise.",
                "Ensure the plan is actionable and detailed.",
            ],
            markdown=True)
            
            fitness_agent_response = fitness_agent.run(user_profile)
            
            st.session_state.fitness_plan = fitness_agent_response.content
            if st.session_state.fitness_plan:
                st.markdown(st.session_state.fitness_plan)
        except Exception as e:
            st.error(f"oops. An error occured {e}")                    
    
    
    






        

