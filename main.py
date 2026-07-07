import re

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class RequestBody(BaseModel):
    text: str


class Invoice(BaseModel):
    vendor: str
    amount: float
    currency: str
    date: str


@app.post("/extract", response_model=Invoice)
def extract(data: RequestBody):

    text = data.text

    vendor = ""
    amount = 0.0
    currency = ""
    date = ""

    # Date
    m = re.search(r"\b(2026-\d{2}-\d{2})\b", text)
    if m:
        date = m.group(1)

    # Currency
    m = re.search(r"\b(USD|EUR|GBP)\b", text, re.I)
    if m:
        currency = m.group(1).upper()

    # Amount
    m = re.search(r"(?:USD|EUR|GBP)\s*([0-9]+(?:\.[0-9]+)?)", text, re.I)
    if m:
        amount = float(m.group(1))
    else:
        m = re.search(r"([0-9]+(?:\.[0-9]+)?)", text)
        if m:
            amount = float(m.group(1))

    # Vendor
    m = re.search(r"([A-Za-z0-9\-]+(?:\s+[A-Za-z0-9&.\-]+){0,5})", text)
    if m:
        vendor = m.group(1).strip()

    return Invoice(
        vendor=vendor,
        amount=amount,
        currency=currency,
        date=date,
    )