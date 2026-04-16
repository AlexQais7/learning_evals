import anthropic
import json

client = anthropic.Anthropic()

# Step 1: The classifier we want to evaluate
def classify(message, system_prompt):
    result = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=50,
        temperature=0.0,
        system=system_prompt,
        messages=[{"role": "user", "content": message}]
    )
    raw = result.content[0].text.strip().lower()
    if "new job" in raw:
        return "new_job"
    elif "complaint" in raw:
        return "complaint"
    else:
        return "unknown"

# Step 2: Our labeled test set — the ground truth
test_cases = [
    {"message": "Hi, I need a quote for painting my living room", "expected": "new_job"},
    {"message": "I'd like to get my exterior painted before winter", "expected": "new_job"},
    {"message": "Can someone come give me an estimate for a 3 bedroom house?", "expected": "new_job"},
    {"message": "Looking to get a quote for my office space downtown", "expected": "new_job"},
    {"message": "I need my fence and deck painted, how much would that cost?", "expected": "new_job"},
    {"message": "Your painter left a huge mess and didn't finish the job", "expected": "complaint"},
    {"message": "I've been waiting 2 weeks and nobody has called me back", "expected": "complaint"},
    {"message": "The color is completely wrong, this is not what I asked for", "expected": "complaint"},
    {"message": "I'm very unhappy with the quality of work on my kitchen", "expected": "complaint"},
    {"message": "Your team showed up 3 hours late and left early", "expected": "complaint"},
{"message": "I had a quote done last month, can we get started now?", "expected": "new_job"},
    {"message": "The painter was great but I think the price was too high", "expected": "complaint"},
    {"message": "I need to repaint a room you did last year, the color faded", "expected": "complaint"},
    {"message": "Nobody showed up today, do I need to reschedule?", "expected": "complaint"},
    {"message": "Can you match the same color you used on my house last summer?", "expected": "new_job"},
]

# Step 3: Run the eval
def run_eval(system_prompt, label=""):
    correct = 0
    failures = []

    for case in test_cases:
        predicted = classify(case["message"], system_prompt)
        is_correct = predicted == case["expected"]
        if is_correct:
            correct += 1
        else:
            failures.append({
                "message": case["message"],
                "expected": case["expected"],
                "predicted": predicted
            })

    accuracy = correct / len(test_cases) * 100

    print(f"\n{'='*60}")
    print(f"PROMPT VERSION: {label}")
    print(f"ACCURACY: {correct}/{len(test_cases)} ({accuracy:.0f}%)")

    if failures:
        print(f"\nFAILURES:")
        for f in failures:
            print(f"  Message: {f['message']}")
            print(f"  Expected: {f['expected']} | Got: {f['predicted']}")
            print()
    else:
        print("\nAll test cases passed!")

# Step 4: Test two different prompt versions
prompt_v1 = """Classify the customer message as either a new job request or a complaint.
Reply with only: 'new job' or 'complaint'."""

prompt_v2 = """You are a classifier for a painter contractor SaaS.
Classify the customer message into exactly one of these categories:
- 'new job' if the customer is asking for a quote, estimate, or new painting work
- 'complaint' if the customer is unhappy, reporting a problem, or following up on a bad experience
Reply with only the category name, nothing else.
If you have classified both categories in a new request ex. New job because of a complaint, prioritize the underlying reason for the request, if it's an issue a customer experiencing because of us then it's a complaint, if there's no underlying issues then it's a new job"""

run_eval(prompt_v1, label="v1 - simple prompt")
run_eval(prompt_v2, label="v2 - detailed prompt")