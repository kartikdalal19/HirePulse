
# from groq import AsyncGroq
# from app.config import settings


# class GroqService:

#     def __init__(self):
#         if not settings.GROQ_API_KEY:
#             raise ValueError("GROQ_API_KEY is missing in .env")

#         if not settings.GROQ_MODEL:
#             raise ValueError("GROQ_MODEL is missing in .env")

#         self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)
#         self.model = settings.GROQ_MODEL

    
#     async def generate_text(
#         self,
#         prompt: str,
#         max_completion_tokens: int = 300
#     ) -> str:
#         response = await self.client.chat.completions.create(
#             model=self.model,
#             messages=[
#                 {
#                     "role": "system",
#                     "content": "You are an assistant for resume analysis."
#                 },
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ],
#             temperature=0.2,
#             max_completion_tokens=max_completion_tokens
#         )

#         content = response.choices[0].message.content

#         if not content:
#             raise RuntimeError("Groq returned an empty response")

#         return content.strip()


# groq_service = GroqService()


import asyncio
import time
from collections import deque

from groq import AsyncGroq, APIStatusError, APIConnectionError
from app.config import settings


class GroqService:

    REQUEST_LIMIT = 3
    WINDOW_SECONDS = 60
    MAX_RETRIES = 5

    def __init__(self):
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is missing in .env")

        if not settings.GROQ_MODEL:
            raise ValueError("GROQ_MODEL is missing in .env")

        # Disable SDK retries so every retry passes through our limiter.
        self.client = AsyncGroq(
            api_key=settings.GROQ_API_KEY,
            max_retries=0,
            timeout=60.0
        )

        self.model = settings.GROQ_MODEL

        # Shared rolling-window request limiter
        self.request_times = deque()
        self.rate_limit_lock = asyncio.Lock()

    async def wait_for_rate_limit(self):

        async with self.rate_limit_lock:

            while True:

                now = time.monotonic()

                # Remove requests outside the 60-second window
                while (
                    self.request_times
                    and now - self.request_times[0] >= self.WINDOW_SECONDS
                ):
                    self.request_times.popleft()

                # Allow request if limit has not been reached
                if len(self.request_times) < self.REQUEST_LIMIT:
                    self.request_times.append(now)
                    return

                # Wait until the oldest request exits the window
                wait_time = (
                    self.WINDOW_SECONDS
                    - (now - self.request_times[0])
                )

                print(
                    f"[Groq Rate Limiter] Limit reached. "
                    f"Waiting {wait_time:.2f} seconds..."
                )

                await asyncio.sleep(max(wait_time, 0.1))

    async def generate_text(
        self,
        prompt: str,
        max_completion_tokens: int = 300
    ) -> str:

        for attempt in range(self.MAX_RETRIES + 1):

            # Every attempt, including retries, passes through the limiter
            await self.wait_for_rate_limit()

            try:

                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an assistant for resume analysis."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.2,
                    max_completion_tokens=max_completion_tokens
                )

                content = response.choices[0].message.content

                if not content:
                    raise RuntimeError("Groq returned an empty response")

                return content.strip()

            except (APIStatusError, APIConnectionError) as exc:

                retryable = (
                    isinstance(exc, APIConnectionError)
                    or exc.status_code in (408, 409, 429)
                    or exc.status_code >= 500
                )

                if not retryable or attempt >= self.MAX_RETRIES:
                    raise

                # Respect Retry-After if the API supplies it
                retry_after = None

                if isinstance(exc, APIStatusError):
                    headers = exc.response.headers
                    retry_after = headers.get("retry-after")

                try:
                    retry_after = float(retry_after) if retry_after else None
                except (TypeError, ValueError):
                    retry_after = None

                backoff = min(2 ** attempt, 30)

                delay = max(backoff, retry_after or 0)

                print(
                    f"[Groq Retry] Attempt {attempt + 1} failed: {exc}. "
                    f"Retrying in {delay} seconds..."
                )

                await asyncio.sleep(delay)


groq_service = GroqService()
