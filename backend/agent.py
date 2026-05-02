import google.generativeai as genai
import os
import json
from dotenv import load_dotenv
load_dotenv()
# Configure Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# load model
model = genai.GenerativeModel("gemini-2.0-flash")
def clean_json(text: str) -> str:
    """
    Cleans model output by removing ```json fences or extra text.
    """
    text = text.strip()

    # Remove markdown code blocks if present
    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    return text
def get_next_action(imagepath: str, dom=None,goal=None):
    """
    Takes screenshot + DOM → sends to Gemini → returns JSON action
    """

    # Read image
    with open(imagepath, "rb") as f:
        image_bytes = f.read()

    # Convert DOM to string safely
    dom_text = json.dumps(dom, indent=2) if dom else "No DOM data"
    prompt = f"""
You are a senior QA automation agent.

GOAL: {goal}

Your task:
- Perform actions to COMPLETE this goal
- Act like a real user
- Follow logical steps

DOM:
{dom_text}

INSTRUCTIONS:

If goal is "login":
- Find username/email input → fill "test"
- Find password input → fill "test123"
- Click login button
- Try to navigate to dashboard

If goal is "search":
- Find search input → type "test"
- Click search button
- Verify results page

If goal is "explore":
- Click buttons
- Click links
- Scroll page
- Explore freely

RULES:
- Always take meaningful action
- Follow step-by-step flow
- Do NOT stop early
- Focus on completing the goal step-by-step

Return ONLY JSON:
{{
  "type": "click",
  "selector": "text=Login"
}}

Allowed actions:
- click
- fill
- wait
- scroll
- done

Only return "done" if goal is completed or no action possible.
"""

    try:
        response = model.generate_content([
            prompt,
            {
                "mime_type": "image/png",
                "data": image_bytes
            }
        ])

        raw_text = response.text
        print("Gemini raw output:", raw_text)

        cleaned = clean_json(raw_text)
        return json.loads(cleaned)

    except Exception as e:
        print("Gemini failed:", e)

        # fallback (important for stability)
        return {"type": "done"}
def explain_report(report):
    """
    Takes QA report → returns AI explanation
    """

    prompt = f"""
You are a Senior QA Engineer.

Analyze the following QA report and explain issues clearly.

Report:
{json.dumps(report, indent=2)}

Instructions:
- Explain each issue in simple terms
- Mention impact (UX, SEO, performance, etc.)
- Be concise
- No JSON, only plain text
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("Explanation failed:", e)
        return "Could not generate explanation"
def generate_testcases(report):
    prompt = f"""
You are a QA engineer.

Based on this report:
{json.dumps(report, indent=2)}

Generate:
- Functional test cases
- Edge cases
- Negative cases

Format:
- Test case
- Steps
- Expected result

Keep it concise.
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except:
        return "Failed to generate testcases"