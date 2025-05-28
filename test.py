""" TEST SCRIPT """
from langchain_ollama import OllamaLLM as Ollama
from api.services.automoderator.automoderator import AutoModeratorService


llm = Ollama(model="llama3")

automoderator = AutoModeratorService(llm=llm)

print("Automoderator service initialized.")

test_title = "Kurczak w sosie curry"
test_description = "Pyszne danie z kurczaka w aromatycznym sosie curry, idealne na obiad. Jest łatwe do przygotowania i pełne smaku. Twoja matka je pokocha, tak jak ja pokochałem ją. Podawaj z ryżem lub chlebem naan. To danie zachwyci Twoich gości i sprawi, że każdy posiłek będzie wyjątkowy. Dis jest cudowny."
test_steps = "\n".join([
    "1. Pokrój kurczaka na kawałki.",
    "2. Podsmaż cebulę i czosnek na patelni.",
    "3. Dodaj kurczaka i smaż, aż będzie złocisty.",
    "4. Wlej mleko kokosowe i dodaj przyprawy.",
    "5. Gotuj na małym ogniu przez 20 minut.",
    "6. Dodaj świeżą kolendrę.",
    "7. Dopraw solą i pieprzem do smaku.",
    "8. Podawaj z ryżem lub chlebem naan.",
])

response = automoderator.validate_text(test_title, test_description, test_steps)
print("Validation Response:")
print(response)