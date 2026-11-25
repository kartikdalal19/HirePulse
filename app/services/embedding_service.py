
import httpx

from app.config import settings


class EmbeddingService:

    def __init__(self):
        self.account_id = settings.CLOUDFLARE_ACCOUNT_ID
        self.api_token = settings.CLOUDFLARE_API_TOKEN
        self.model = settings.CLOUDFLARE_EMBEDDING_MODEL

        if not self.account_id:
            raise ValueError("CLOUDFLARE_ACCOUNT_ID is missing")

        if not self.api_token:
            raise ValueError("CLOUDFLARE_API_TOKEN is missing")

        if not self.model:
            raise ValueError("CLOUDFLARE_EMBEDDING_MODEL is missing")

        self.url = (
            f"https://api.cloudflare.com/client/v4/accounts/"
            f"{self.account_id}/ai/run/{self.model}"
        )

    async def generate_embeddings(self, texts: list[str]) -> list[list[float]]:

        if not texts:
            return []

        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "text": texts
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                self.url,
                headers=headers,
                json=payload
            )

            response.raise_for_status()
            result = response.json()

        if not result.get("success"):
            raise RuntimeError(
                f"Cloudflare API error: {result.get('errors')}"
            )

        embeddings = result.get("result", {}).get("data", [])

        if len(embeddings) != len(texts):
            raise RuntimeError("Unexpected number of embeddings returned")

        return embeddings


embedding_service = EmbeddingService()
