from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup

app = FastAPI(title="Marketing Agent OS Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CompanyRequest(BaseModel):
    company_url: str

@app.get("/")
def root():
    return {"message": "Backend is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/test")
def test():
    return {
        "success": True,
        "message": "Frontend and backend connection is working"
    }

@app.post("/api/analyze")
def analyze_company(request: CompanyRequest):
    url = request.company_url.strip()

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    try:
        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; MarketingAgentOS/1.0)"
            },
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string.strip() if soup.title and soup.title.string else "No title found"

        meta_description_tag = soup.find("meta", attrs={"name": "description"})
        meta_description = (
            meta_description_tag.get("content", "").strip()
            if meta_description_tag and meta_description_tag.get("content")
            else "No meta description found"
        )

        h1_tag = soup.find("h1")
        h1_text = h1_tag.get_text(strip=True) if h1_tag else "No H1 found"

        heading_tags = soup.find_all(["h2", "h3"])
        headings = []
        for tag in heading_tags:
            text = tag.get_text(strip=True)
            if text and text not in headings:
                headings.append(text)
            if len(headings) >= 5:
                break

        paragraph_tags = soup.find_all("p")
        paragraphs = []
        for tag in paragraph_tags:
            text = tag.get_text(" ", strip=True)
            if len(text) > 50 and text not in paragraphs:
                paragraphs.append(text)
            if len(paragraphs) >= 3:
                break

        cta_candidates = []
        for tag in soup.find_all(["a", "button"]):
            text = tag.get_text(" ", strip=True)
            if text and len(text) <= 40:
                lowered = text.lower()
                if any(
                    phrase in lowered
                    for phrase in [
                        "start",
                        "book",
                        "demo",
                        "trial",
                        "contact",
                        "get started",
                        "sign up",
                        "talk to sales",
                    ]
                ):
                    if text not in cta_candidates:
                        cta_candidates.append(text)
            if len(cta_candidates) >= 5:
                break

        company_name_guess = url.replace("https://", "").replace("http://", "").split(".")[0].title()

        return {
            "success": True,
            "company_url": url,
            "company_name_guess": company_name_guess,
            "page_title": title,
            "meta_description": meta_description,
            "h1": h1_text,
            "headings": headings,
            "paragraphs": paragraphs,
            "cta_candidates": cta_candidates,
            "summary": f"Fetched homepage research for {company_name_guess}.",
            "next_step": "Generate positioning and outreach copy next"
        }

    except requests.RequestException as e:
        return {
            "success": False,
            "company_url": url,
            "company_name_guess": "Unknown",
            "page_title": "Unavailable",
            "meta_description": "Unavailable",
            "h1": "Unavailable",
            "headings": [],
            "paragraphs": [],
            "cta_candidates": [],
            "summary": f"Failed to fetch the website: {str(e)}",
            "next_step": "Check the URL and try again"
        }