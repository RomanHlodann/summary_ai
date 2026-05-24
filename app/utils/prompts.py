VISION_PROMPT = """
Extract all visible content from this document page.

Do NOT summarize or interpret anything.

Return the content as faithfully as possible, including:
- All readable text
- Table content and values
- Chart labels, axes, and numbers
- Diagram annotations

If the page contains visual elements, describe them only in a factual way (what is shown), not what it means.
"""

CHUNK_SYSTEM = """
You are a document summarizer.
Summarize the following pages concisely in 3-5 sentences.
Preserve key facts, numbers, and table data.
"""

FINAL_SYSTEM = """
You are a document summarizer.
Given these chunk-level summaries, write a single coherent summary of the entire document in 5-8 sentences.
"""
