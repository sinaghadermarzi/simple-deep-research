# proxy.py
import os
from typing import Dict, Any, Optional

from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import JSONResponse

from openai import OpenAI
from tavily import TavilyClient

from cache_firestore import FirestoreCache
from secrets_config import OPENAI_API_KEY, TAVILY_API_KEY

# -------- config (non-secret) --------
OPENAI_BASE  = os.getenv("OPENAI_BASE", "https://api.openai.com/v1")  # usually default

# Cache TTLs are now managed by the FirestoreCache implementation (in days).
FIRESTORE_COLLECTION = os.getenv("FIRESTORE_COLLECTION", "pydata-deep-research-proxy-cache")



cache = FirestoreCache(FIRESTORE_COLLECTION)
app = FastAPI(title="Research Proxy (Firestore Cache, Official Clients)")

# Official clients
openai_client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE)
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)



# -------- /v1/chat/completions (OpenAI) --------
@app.post("/v1/chat/completions")
async def chat_completions(request: Request):

    body: Dict[str, Any] = await request.json()

    # (no token clamp configured here; trust client or upstream defaults)

    # cache key on output-relevant fields
    key_fields = {k: body.get(k) for k in [
        "model","messages","tools","tool_choice","temperature","top_p","max_tokens",
        "frequency_penalty","presence_penalty","response_format","n","stop","seed","logit_bias","user"
    ]}
    ck = cache.make_key("openai.chat", key_fields)
    cached = cache.get(ck)
    if cached:
        return JSONResponse(content=cached)

    # Build kwargs accepted by SDK
    allowed = {
        "model","messages","tools","tool_choice","temperature","top_p","max_tokens",
        "frequency_penalty","presence_penalty","n","stop","seed","logit_bias","user",
        "response_format"
    }
    kwargs = {k: body[k] for k in allowed if k in body}

    completion = openai_client.chat.completions.create(**kwargs)
    data = completion.model_dump()  # convert to API-like JSON
    # use cache's default TTL (days) by omitting the TTL argument
    cache.set(ck, data)
    return JSONResponse(content=data)

# -------- /v1/tavily/search (Tavily) --------
@app.post("/v1/tavily/search")
async def tavily_search(request: Request ):

    body: Dict[str, Any] = await request.json()

    # cache by full request payload
    ck = cache.make_key("tavily.search", body)
    cached = cache.get(ck)
    if cached:
        return JSONResponse(content=cached)

    # The Tavily client takes kwargs like: query, search_depth, max_results, include_answer, ...
    result = tavily_client.search(**body)
    # use cache's default TTL (days) by omitting the TTL argument
    cache.set(ck, result)
    return JSONResponse(content=result)

# (optional) health
@app.get("/healthz")
def healthz():
    return {"ok": True}
