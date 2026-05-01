from transformers import pipeline

# Task: Resumir un texto (summarization)
# Input: Texto a resumir
# Output: Texto resumido

model = pipeline(
    "text-generation", 
    model="facebook/bart-large-cnn"
)

prompt = """
he Hugging Face Hub is a platform with over 2M models, 
500k datasets, and 1M demo apps (Spaces), 
all open source and publicly available, 
in an online platform where people can easily collaborate and build ML together. 

The Hub works as a central place where anyone can explore, experiment, 
collaborate, and build technology with Machine Learning. 

Are you ready to join the path towards open source Machine Learning? 🤗
"""

result = model(
    prompt,
    max_length=50, 
    min_length=15, 
    do_sample=False
)

print("-" * 80)
print("=" * 80)
print(result[0]["summary_text"])
print("=" * 80)