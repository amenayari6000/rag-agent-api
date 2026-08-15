import os
from dotenv import load_dotenv
from fastapi import FastAPI


from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel











load_dotenv()

app = FastAPI()


# Request format for /chat
class ChatRequest(BaseModel):
    question: str


# OpenAI model
openai_key = os.getenv("OPENAI_API_KEY")

if not openai_key:
    raise RuntimeError("OPENAI_API_KEY is missing")

llm = ChatOpenAI(
    api_key=openai_key,
    model="gpt-4o-mini",
    temperature=0
)


# Chat endpoint
@app.post("/chat")
def chat(request: ChatRequest):
    try:
        response = llm.invoke(request.question)

        return {
            "question": request.question,
            "response": response.content
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# Health check
@app.get("/health")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"message": "RAG API is running"}


def main():
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    if not openai_key or openai_key.startswith("your_"):
        raise RuntimeError("OPENAI_API_KEY is missing or still a placeholder value")
    if not anthropic_key or anthropic_key.startswith("your_"):
        raise RuntimeError("ANTHROPIC_API_KEY is missing or still a placeholder value")

    llm = ChatOpenAI(api_key=openai_key, model_name="gpt-4o-mini", temperature=0)
    response = llm.invoke("say 'setup complete!' in one word")
    print(f"Response from ChatOpenAI: {response}")

    llm_anthropic = ChatAnthropic(api_key=anthropic_key, model_name="claude-sonnet-4-5-20250929", temperature=0)
    response_anthropic = llm_anthropic.invoke("say 'setup complete!' in one word")
    print(f"Response from ChatAnthropic: {response_anthropic}")

    print("setup complete!")


if __name__ == "__main__":
    main()
