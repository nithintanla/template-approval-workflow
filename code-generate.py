from fastapi import FastAPI, Request
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import uvicorn

# Load pre-trained model and tokenizer (use a code-specific model if available)
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

app = FastAPI()

@app.post("/generate-code")
async def generate_code(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    if not prompt:
        return {"error": "Please provide a prompt."}
    
    # Encode prompt and generate code
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(input_ids, max_length=100, num_return_sequences=1, do_sample=True)
    generated_code = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {"generated_code": generated_code}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
