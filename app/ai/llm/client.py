import google.generativeai as genai
from app.ai.llm.root_prompts.loader import load_prompt


class GeminiClient:
    def __init__(
        self,
        model_name="gemini-3-flash-preview",
        fallback_name="gemini-2.5-flash",
        temperature: float = 0.6,
        max_output_tokens: int = 2021,
        root_prompt=load_prompt("questa.prompt"),
    ):
        self.model = genai.GenerativeModel(
            model_name,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_output_tokens,
            },
            system_instruction=root_prompt,
        )
        self.fallback = genai.GenerativeModel(
            fallback_name,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_output_tokens,
            },
            system_instruction=root_prompt,
        )

    async def generate(self, prompt: str):
        try:
            res = await self.model.generate_content_async(prompt)
            if not res or not res.text:
                raise RuntimeError("Empty response from gemini")
            return res.text.strip()
        
        except Exception:
            pass

        res = await self.fallback.generate_content_async(prompt)
        if not res.text:
            raise RuntimeError("Gemini failed totally")
        return res.text.strip()


aiClient = GeminiClient()
