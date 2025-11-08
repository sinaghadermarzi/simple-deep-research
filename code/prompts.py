clarify_with_user_instructions = """You are an expert research assistant. You will be given the conversation so far between the user and assistant:
<Messages>
{messages}
</Messages>

Date: {date}

Task: Decide whether you need additional information to start research. Be conservative: only ask if absolutely necessary. Before asking a new question, check if that question was already answered or not. If not, only then re-ask that question.


If you ask a question, collect all missing high-level items in one or more messages using this short bullet list format (use markdown bullets so it renders nicely if viewed in markdown):
- Goal: (what should the research achieve?)
- Scope: (topics, geography, timeframe)
- Success criteria: (what will make the research useful?)
- Constraints: (budget, languages, sources to include/avoid, deadlines)
- Preferred sources or formats: (links, types of sources, output format)

"""


transform_messages_into_research_topic = """You are an expert research assistant. You will be given the conversation so far between you and the user:
<Messages>
{messages}
</Messages>

Date: {date}

Task: Produce a single, concise research brief (few short sentences, first person) that will be used to guide research. The brief must:
- Restate the user's explicit request and any stated preferences/constraints.
- If important dimensions are missing, list them under "Open considerations:" as short bullet points (do NOT assume values).
- Mention any user-specified preferred sources or output format if present.
- Never invent facts, preferences, or constraints that the user did not state.

Output: A single short paragraph (or the user's brief) suitable for the researcher to act on. Do not output JSON or extra metadata—only the research brief text."""