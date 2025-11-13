# Effective Prompt Crafting for Local LLMs — Best practices

[![OpenWebUI](https://img.shields.io/badge/OpenWebUI-Docs-blue.svg?style=flat-square&logo=github)](https://github.com/open-webui/open-webui) [![License: License CC-BY-SA](https://img.shields.io/badge/License-CC--BY--SA--4.0%20-blue.svg?style=flat-square)](http://creativecommons.org/licenses/by-sa/4.0/)

This guide provides strategies for writing effective prompts when working with Large Language Models (LLMs) in environments like Open WebUI, especially when using smaller, less powerful models (e.g., 7B-13B parameters). A well-crafted prompt is crucial for guiding these models to generate high-quality, relevant, and accurate responses.

---

## Table of Contents

1. [Core Principles of Good Prompts](#core-principles-of-good-prompts)
2. [Basic Prompt Structure: The CRISPA Framework](#basic-prompt-structure-the-crispa-framework)
3. [Advanced Prompting Techniques](#advanced-prompting-techniques)
4. [Practical Tips for Less Powerful Models](#practical-tips-for-less-powerful-models)
5. [Common Pitfalls to Avoid](#common-pitfalls-to-avoid)
6. [Optimizing Open WebUI Settings](#optimizing-open-webui-settings)
7. [Example Gallery](#example-gallery)
8. [Troubleshooting](#troubleshooting)

---

<a id="core-principles-of-good-prompts"></a>

## Core Principles of Good Prompts

When working with limited models, clarity and explicit guidance are your best tools.

### **Clarity & Specificity**

Vague prompts get vague answers. Be as precise as possible about what you want.

- **Bad:** `Write a story.`
- **Good:** `Write a short, 200-word sci-fi story about a lonely AI on a deep space probe discovering a mysterious signal. The tone should be melancholic yet hopeful.`

### **Provide Context**

Give the model the background information it needs. Assume it knows nothing about your specific task.

- **Bad:** `Summarize the meeting.`
- **Good:** `Act as a project manager. Summarize the following meeting notes into three key decisions and two action items. [Paste meeting notes here]`

### **Set a Persona/Role**

Assigning a role (e.g., "You are an expert financial analyst," "Act as a friendly math tutor") helps steer the model's style, knowledge base, and response format. This is particularly effective with smaller models as it activates specific knowledge domains.

### **Define the Format & Structure**

Explicitly tell the model how you want the output formatted (e.g., bullet points, JSON, a table, Markdown, a list of pros and cons). Smaller models benefit greatly from explicit formatting instructions.

### **Iterate, Don't Settle**

Your first prompt is a starting point. If the output isn't perfect, refine your prompt, add more details, or correct the model's misunderstanding in a follow-up message. Think of it as a conversation, not a one-shot command.

---

<a id="basic-prompt-structure-the-crispa-framework"></a>

## Basic Prompt Structure: The CRISPA Framework

A simple and effective structure for your prompts is **CRISPA**:

- **C** - **Context:** The background information
- **R** - **Role:** The persona the AI should adopt
- **I** - **Instruction:** The core task you want it to perform
- **S** - **Steps:** The specific steps or sub-tasks (if any)
- **P** - **Persona/Tone:** The style or tone of the response (e.g., professional, casual, academic)
- **A** - **Format:** The desired output format

### Example Using CRISPA

```
Context: I am planning a weekend trip to the countryside and need to pack.
Role: Act as an experienced travel guide.
Instruction: Create a packing list for me.
Steps: 
1. Consider the season is spring with unpredictable weather
2. Include activities like hiking and visiting small villages
Persona/Tone: Be practical and enthusiastic.
Format: Provide the final list in a Markdown table with two columns: "Item" and "Reason."
```

**Note:** You don't need to use all CRISPA elements every time. Adapt based on your task complexity. Simple queries may only need Instruction + Format.

---

<a id="advanced-prompting-techniques"></a>

## Advanced Prompting Techniques

### 1. Zero-Shot Prompting

Asking the model to perform a task without any examples. Relies entirely on the model's pre-existing knowledge and the clarity of your instruction.

**When to use:** Simple, well-defined tasks that the model should know (translation, basic factual questions).

**Prompt:**

```
Translate the following English text to French: 'Hello, how are you today?'
```

### 2. Few-Shot Prompting

Providing a few examples of the task within the prompt. This is **extremely effective** for smaller models, as it demonstrates the exact pattern you want.

**When to use:** Complex formatting, specific writing styles, or when the model struggles with zero-shot.

**Prompt:**

```
Convert the sentiment of these sentences from negative to positive.

Example 1:
Input: This movie was a complete waste of time.
Output: This movie was a captivating and enjoyable experience.

Example 2:
Input: The service at the restaurant was terribly slow.
Output: The service at the restaurant was relaxed, allowing us to savor the anticipation.

Now, convert this:
Input: My phone's battery life is awful.
Output:
```

**Tip:** For smaller models, 2-3 examples are usually sufficient. More examples can sometimes confuse weaker models.

### 3. Chain-of-Thought (CoT)

Encouraging the model to "think step by step." This breaks down complex problems into manageable parts, dramatically improving logical reasoning and math capabilities.

**When to use:** Math problems, logical reasoning, multi-step tasks, debugging.

**Prompt:**

```
A bakery sold 85 cakes in the morning and 112 in the afternoon. Each cake costs $12. 
How much money did they make in total? Let's think step by step.
```

**Pro tip:** Adding phrases like "Let's break this down," "First, let's...", or "Step by step:" triggers CoT behavior.

### 4. Using XML/HTML-like Tags

Using tags like `<instruction>`, `<context>`, and `<output>` can help structurally separate parts of your prompt, making it easier for the model's tokenizer to understand the different components.

**When to use:** Complex prompts with multiple sections, when you need strict separation between instructions and data.

**Prompt:**

```
<context>
The user is a beginner gardener living in a region with clay soil.
</context>

<instruction>
Suggest three easy-to-grow vegetables and briefly explain why they are suitable for clay soil.
</instruction>

<output_format>
Present your answer as a bulleted list.
</output_format>
```

### 5. Constrained Generation

Explicitly limiting what the model can include in its response.

**Prompt:**

```
List the top 5 programming languages for web development.
Constraints:
- Only list the language names
- No explanations or descriptions
- One language per line
- No numbering or bullets
```

### 6. Self-Consistency

For critical tasks, ask the model to generate multiple solutions and compare them.

**Prompt:**

```
Solve this logic puzzle and provide three different approaches to verify your answer:
[puzzle description]
```

---

<a id="practical-tips-for-less-powerful-models"></a>

## Practical Tips for Less Powerful Models

### 1. Keep it Simple

Avoid overly complex, run-on sentences. Break down intricate requests into simpler, sequential prompts in the same conversation.

**Instead of:**

```
Analyze this code for bugs, suggest improvements, refactor it for better readability, 
and also explain what each function does.
```

**Do this:**

```
First prompt: "Review this code and identify any bugs."
Second prompt: "Now suggest improvements for performance."
Third prompt: "Refactor the code for better readability."
```

### 2. Use Positive Instructions

Tell the model what to do, not what to avoid.

- **Instead of:** "Don't be too verbose"
- **Say:** "Please provide a concise answer in 3 sentences or less"

### 3. Set Output Length Explicitly

Define the desired length to prevent rambling or overly brief responses.

Examples:

- "in 3 sentences"
- "a 500-word essay"
- "a brief list of 5 items"
- "approximately 2 paragraphs"

### 4. Anchor with Examples

When you want a specific format, show it rather than describe it.

**Prompt:**

```
Format the data like this example:
Name: John Doe | Age: 30 | City: New York

Now format this information:
Sarah is 25 years old and lives in Boston.
```

### 5. Use Delimiters

Clearly separate different sections of your prompt with delimiters like `"""`, `---`, or `###`.

**Prompt:**

```
Summarize the following text:
"""
[Your long text here]
"""

Summary should be exactly 2 sentences.
```

### 6. Prime the Response

Start the model's response for it to guide the format.

**Prompt:**

```
List three benefits of exercise.

1.
```

The model will naturally continue with "1. [benefit]" and follow the pattern.

### 7. Request Explanations

For complex outputs, ask the model to explain its reasoning. This often improves accuracy.

**Prompt:**

```
Calculate the compound interest and explain each step of your calculation.
```

---

<a id="common-pitfalls-to-avoid"></a>

## Common Pitfalls to Avoid

### 1. Ambiguous Pronouns

**Bad:** "Take the data and analyze it. Then summarize it."  
**Good:** "Take the sales data and analyze the trends. Then summarize the sales trends."

### 2. Multiple Questions in One Prompt

Smaller models struggle with multiple tasks at once.

**Bad:** "What's the capital of France and also who was the first president and explain photosynthesis?"  
**Good:** Break into three separate prompts.

### 3. Assuming Knowledge

Don't assume the model knows your specific context, project, or acronyms.

**Bad:** "Update the TPS report with Q4 data."  
**Good:** "Update the monthly Team Performance Summary report with the sales data from October-December 2023."

### 4. Overly Abstract Requests

**Bad:** "Be creative."  
**Good:** "Generate 5 unique marketing taglines that use wordplay and appeal to tech-savvy millennials."

### 5. Neglecting the System Prompt

Not using the system prompt means repeating context in every message.

### 6. Too Many Constraints

Overloading with constraints can confuse smaller models.

**Overly constrained:**

```
Write a story that's exactly 347 words, has 3 characters named alphabetically, 
uses no adjectives, includes a metaphor about sailing, and ends with a question.
```

Start with core constraints, then refine in follow-ups.

---

<a id="optimizing-open-webui-settings"></a>

## Optimizing Open WebUI Settings

### Temperature Setting

Temperature controls randomness in the model's output.

- **Low (0.1-0.3):** Deterministic, focused, factual
  - Use for: Code generation, factual Q&A, data extraction, summaries
- **Medium (0.4-0.7):** Balanced creativity and coherence
  - Use for: General conversation, explanations, technical writing
- **High (0.8-1.2):** Creative, varied, unpredictable
  - Use for: Creative writing, brainstorming, generating alternatives

**For smaller models, start with 0.3-0.5** and adjust based on results.

### Top-P (Nucleus Sampling)

Controls diversity by limiting the probability mass considered.

- **0.9-0.95:** Standard setting, good balance
- **0.7-0.8:** More focused, less creative
- **0.95-1.0:** More diverse outputs

**Tip:** Lower both temperature and top-p for very factual tasks.

### Top-K

Limits the number of highest probability tokens considered.

- **40-50:** Standard, balanced
- **20-30:** More focused
- **60+:** More creative

**For smaller models, try 40** as a starting point.

### Repeat Penalty

Discourages the model from repeating the same words/phrases.

- **1.0:** No penalty
- **1.1-1.15:** Slight penalty, recommended for most tasks
- **1.2+:** Strong penalty, use if model loops excessively

### Max Tokens

Set the maximum response length.

- **Short answers:** 256-512 tokens
- **Detailed explanations:** 1024-2048 tokens
- **Long-form content:** 2048-4096 tokens

**Note:** Smaller models may lose coherence in very long outputs (>2000 tokens).

### System Prompt

The system prompt sets the persistent behavior for all messages in a conversation.

**Example System Prompts:**

For a helpful assistant:

```
You are a helpful, concise assistant. Provide practical answers. 
When unsure, say so rather than guessing.
```

For a coding assistant:

```
You are an expert programmer. Provide clean, well-commented code. 
Always explain your solutions briefly.
```

For creative tasks:

```
You are a creative writer. Use vivid imagery and engaging language. 
Show, don't tell.
```

---

<a id="example-gallery"></a>

## Example Gallery

### **Example 1: Summarization & Reformatting**

**Goal:** Get a quick summary of a long article for a presentation.

**Prompt:**

```
<role>
You are an expert content summarizer.
</role>

<instruction>
Read the following article and provide a summary suitable for a single PowerPoint slide.
</instruction>

<steps>
1. Identify the three most key points
2. Rephrase them into concise, bullet-friendly statements
</steps>

<format>
Output only the three bullet points, nothing else.
</format>

<context>
[Paste the full article text here]
</context>
```

### **Example 2: Creative Task**

**Goal:** Generate a product name and slogan.

**Prompt:**

```
Act as a creative branding expert. We are launching a new brand of eco-friendly 
coffee beans that are sourced directly from small farms. The target audience is 
millennials who value sustainability.

Please generate:
1. Five potential brand names. They should be catchy and easy to remember.
2. A short, impactful slogan for each one.

Present the results in a simple numbered list. The tone should be modern and aspirational.
```

### **Example 3: Information Extraction**

**Goal:** Get structured data from an unstructured email.

**Prompt:**

```
Extract the following information from the email below and format it as a JSON object:
- sender_name
- meeting_date
- meeting_time
- key_topic
- action_item (if any, otherwise null)

Email:
"""
Hi team, just confirming our sync-up this Friday, March 10th, at 3:00 PM EST. 
We'll be discussing the Q2 budget planning. Please come prepared with your 
initial proposals. Best, Sarah
"""

JSON:
```

### **Example 4: Code Generation with Constraints**

**Goal:** Generate Python code with specific requirements.

**Prompt:**

```
Write a Python function that:
- Takes a list of numbers as input
- Returns the median value
- Handles empty lists by returning None
- Includes type hints
- Has a docstring explaining the function

Use clear variable names and add comments for non-obvious logic.
```

### **Example 5: Comparative Analysis**

**Goal:** Compare two options with structured output.

**Prompt:**

```
Compare Python and JavaScript for web development backend.

Format your answer as a table with these columns:
- Feature
- Python
- JavaScript
- Winner

Include exactly 5 features: Performance, Learning Curve, Ecosystem, 
Community Support, and Job Market.

Be objective and concise.
```

### **Example 6: Multi-Step Problem Solving**

**Goal:** Debug code with explanation.

**Prompt:**

```
Analyze this Python code for bugs:

def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)

Process:
1. Identify all potential bugs
2. Explain why each is a problem
3. Provide the corrected code
4. Add error handling

Think step by step.
```

---

<a id="troubleshooting"></a>

## Troubleshooting

### Problem: Model Keeps Repeating Itself

**Solutions:**

- Increase repeat penalty to 1.15-1.2
- Lower temperature to 0.3-0.5
- Add to prompt: "Provide a varied response without repetition"
- Restart the conversation (model may be stuck in a loop)

### Problem: Responses Are Too Short

**Solutions:**

- Explicitly request length: "Write at least 3 paragraphs"
- Increase max tokens
- Add: "Provide a detailed explanation"
- Use Chain-of-Thought: "Explain your reasoning step by step"

### Problem: Model Ignores Instructions

**Solutions:**

- Use XML tags to separate instructions: `<instruction>...</instruction>`
- Repeat key instructions at the end of the prompt
- Simplify: break complex tasks into multiple prompts
- Use few-shot examples to demonstrate exactly what you want
- Try a different phrasing of the same instruction

### Problem: Output Format is Wrong

**Solutions:**

- Show an example of the exact format you want
- Use priming: start the response format for the model
- Be extremely explicit: "Use this exact format: [example]"
- Add: "Do not add any explanation, only output the [format]"

### Problem: Hallucinations or Incorrect Facts

**Solutions:**

- Lower temperature to 0.2-0.3
- Add: "Only state information you are certain about"
- Request sources: "Cite your sources"
- Use Chain-of-Thought to verify reasoning
- Ask the model to express uncertainty: "If unsure, say 'I don't know'"

### Problem: Model Refuses or Gets Confused

**Solutions:**

- Simplify the prompt
- Remove negative instructions (don't, never, not)
- Rephrase as a positive goal
- Check if you're asking for something the model can't do
- Try a different model (some are better at specific tasks)

### Problem: Inconsistent Results

**Solutions:**

- Lower temperature for more consistency
- Lower top-p to 0.8 or less
- Use more explicit instructions
- Add examples to anchor the output style
- Check if you're using vague terms that the model interprets differently

---

## Quick Reference Checklist

Before hitting send, ask yourself:

- [ ] Is my instruction clear and specific?
- [ ] Have I provided necessary context?
- [ ] Did I specify the output format?
- [ ] Did I set an appropriate length expectation?
- [ ] Am I asking for one task or multiple? (Split if multiple)
- [ ] Have I used positive instructions?
- [ ] Would an example help? (Add few-shot if yes)
- [ ] Is my temperature setting appropriate for the task?
- [ ] Have I used delimiters to separate sections?
- [ ] Have I assigned a helpful role/persona?

---

## Conclusion

Effective prompt crafting is both an art and a science. With smaller models, every word counts. Start with the basics (CRISPA framework), experiment with advanced techniques (few-shot, CoT), and always iterate based on results.

Remember: the model is a tool, and like any tool, its effectiveness depends on how you use it. Practice, refine, and don't be afraid to try different approaches.

**Happy Prompting!**

---

## Additional Resources

- [Open WebUI Documentation](https://docs.openwebui.com/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- Model-specific prompting guides (check your model's documentation)

---

## 🙏 Acknowledgments

**Special thanks to**:
- Open WebUI core team for the amazing platform
- Community members who tested variations
- Contributors who reported issues and improvements

**Inspired by**:
- Open WebUI Documentation
- Prompt Engineering Guide

---

## 📄 License

[![License License CCBYSA](https://img.shields.io/badge/License-CC--BY--SA--4.0%20-blue.svg?style=flat-square)](http://creativecommons.org/licenses/by-sa/4.0/)

This file is part of the [**Open WebUI Toolkit**](https://github.com/rex-nihilo/open-webui-toolkit) project.
This textual content is licensed under **CC BY-SA 4.0**.

You are free to:
- **Share**: Copy and redistribute in any medium or format
- **Adapt**: Remix, transform, and build upon the material

Under the following terms:
- **Attribution**: Give appropriate credit
- **ShareAlike**: Distribute under same license
- **No additional restrictions**: Cannot apply legal terms or technological measures that legally restrict others

## 👤 Author

**Rex Nihilo**

- GitHub: [@rex-nihilo](https://github.com/rex-nihilo)
- Project: [Open WebUI Toolkit](https://github.com/rex-nihilo/open-webui-toolkit)
- OpenWebUI: [@rexnihilo](https://openwebui.com/u/rexnihilo)
- Website: [https://rexnihilo.com](https://rexnihilo.com)

## 💖 Support

If you find this work helpful:

- ⭐ **Star the repository** on GitHub
- 📢 **Share** with other Open WebUI users
- 💬 **Contribute** your own variations and tips
- 📝 **Write a blog post** about your prompting art
- 🎥 **Create a tutorial** video (credit this guide)
- ☕ **Buy me a coffee** (or a beer)

---

**Licence:** [CC BY-SA 4.0](http://creativecommons.org/licenses/by-sa/4.0/) | **Last updated:** November 2025 by **Rex Nihilo*
