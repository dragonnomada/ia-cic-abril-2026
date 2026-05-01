from transformers import pipeline

# Task: Generación de Texto (Autocompletado) 
# Input: Texto fuente (Prompt)
# Output: Texto completado (Prompt extendido)

model = pipeline(
    "text-generation",
    model="distilgpt2"
)

# prompt = "En el futuro deseo que"
prompt = "In the future I wish that"

result = model(
    prompt,
    max_new_tokens=60,
    do_sample=True,
    temperature=0.8
)

print("-" * 80)
print("=" * 80)
print(result[0]["generated_text"])
print("=" * 80)