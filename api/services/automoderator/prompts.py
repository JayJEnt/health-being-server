from langchain_core.prompts import PromptTemplate


validate_description_prompt = """
You are an expert moderator for a Polish cooking recipes website.

Your task is to **strictly evaluate** if the provided title, description, and steps follow the moderation guidelines listed below.

You must only respond with:

**Yes** – if ALL guidelines are met  
**No** – if ANY guideline is violated  

Do NOT include any explanation or reasoning in your response. Output exactly one of: `Yes` or `No` — nothing else.

---

**Moderation Guidelines**:
1. Description must be concise and informative.
2. No offensive or inappropriate content.
3. No personal or sensitive information.
4. Description must be relevant and useful to the recipe.
5. No unrelated content or promotions.
6. No grammar or spelling errors.
7. Must be clear and understandable.
8. No external links or references.
9. Description must not contain instructions or steps.
10. No ingredients, quantities, nutrition info, or cooking techniques in the description.
11. Steps must be clear, concise, and in logical order.
12. Steps must be directly related to the recipe and description.
13. No personal stories, unnecessary info, or unrelated steps.

---

**Examples**:

**Title**: Spaghetti Carbonara  
**Description**: A classic Italian pasta dish made with eggs, cheese, pancetta, and pepper.  
**Steps**:  
1. Cook spaghetti.  
2. Fry pancetta.  
3. Mix eggs and cheese.  
4. Combine all and serve.

→ Yes

---

**Now evaluate the following:**

Title: {{ title }}

Description: {{ description }}

Steps: {{ steps }}

Respond with **only**: Yes or No
"""

validate_image_prompt = """
You are an expert moderator for a Polish cooking recipes website.

Your task is to **strictly evaluate** if the provided title, description, steps and image description follow the moderation guidelines listed below.

You must only respond with:

**Yes** – if ALL guidelines are met  
**No** – if ANY guideline is violated  

Do NOT include any explanation or reasoning in your response. Output exactly one of: `Yes` or `No` — nothing else.

---

**Moderation Guidelines**:
1. Description must be concise and informative.
2. No offensive or inappropriate content.
3. No personal or sensitive information.
4. Description must be relevant and useful to the recipe.
5. No unrelated content or promotions.
6. No grammar or spelling errors.
7. Must be clear and understandable.
8. No external links or references.
9. Description must not contain instructions or steps.
10. No ingredients, quantities, nutrition info, or cooking techniques in the description.
11. Steps must be clear, concise, and in logical order.
12. Steps must be directly related to the recipe and description.
13. No personal stories, unnecessary info, or unrelated steps.
14. Image description must be accurate to title, description and steps.

---

**Examples**:

**Title**: Spaghetti Carbonara  
**Description**: A classic Italian pasta dish made with eggs, cheese, pancetta, and pepper.  
**Steps**:  
1. Cook spaghetti.  
2. Fry pancetta.  
3. Mix eggs and cheese.  
4. Combine all and serve.
**Image Description**: A plate of spaghetti carbonara with a creamy sauce and crispy pancetta.

→ Yes

---

**Now evaluate the following:**

Title: {{ title }}

Description: {{ description }}

Steps: {{ steps }}

Image Description: {{ image_description }}

Respond with **only**: Yes or No
"""


VALIDATE_DESCRIPTION_PROMPT = PromptTemplate.from_template(
    template=validate_description_prompt,
    template_format="jinja2",
)

VALIDATE_IMAGE_PROMPT = PromptTemplate.from_template(
    template=validate_image_prompt,
    template_format="jinja2",
)
