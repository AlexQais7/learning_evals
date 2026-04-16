# Eval Harness — Customer Message Classifier

A testing framework for measuring how accurately an LLM classifies 
customer messages as new job requests or complaints.

## What it does
Runs a labeled test set of customer messages through two prompt versions
and reports accuracy, failures, and which cases each prompt gets wrong.

## What I learned
- what happened when we only had 10 easy test cases? The 2 prompts passed with 100% accuracy
- what the faded paint message taught you about edge cases? the example with the faded paint looks like a new job request from the first impression however the underlying reason is a job done bad so it's a complaint and the customer is not happy, if we don't have the instructions in the prompt to account for the edge cases reasoning we could be classifying the request incorrectly. 
- what it means that both prompts failed on the same message? It means that the issue is not wording rather than a conceptual gap we have in the prompts.
- what your fix to v2 taught you about prompt engineering? I learned that the instructions should be as accurate and as specific as possible, the better quality of said instructions the better the results are

## PM takeaway
One paragraph: how would you use an eval harness before shipping 
an AI feature? What does "ready to ship" mean when you can measure it?
Who should own the test set — engineering or product? As a PM I'm responsible for owning the test set because I understand the business domain and edge cases better than engineering does, the faded paint example came from product knowledge, not technical skill. Before shipping an AI feature I'd build an eval harness, try to break it with hard cases, and iterate on the prompt until failures drop to an acceptable level. "Ready to ship" isn't 100% accuracy, it's a threshold based on the cost of failure. For a complaint classifier, a misclassified urgent complaint could mean losing a customer, so I'd want 95%+ before shipping and I'd define that threshold in the spec upfront, not after the fact.

## Results
| Prompt | Accuracy |
|--------|----------|
| V1 - simple prompt | 93% (14/15) |
| V2 - detailed prompt | 100% (15/15) |

## How to run
1. Clone this repo
2. Set your ANTHROPIC_API_KEY environment variable
3. Run `python3 evals.py`