from langchain.chat_models.openai import ChatOpenAI

class LLMModel:
    def __init__(self, openai_api_key: str, temperature: float ):
        self.openai_api_key = openai_api_key
        self.set_temperature = temperature
        self.model = "gpt-4o-2024-05-13"  # or "gpt-3.5-turbo"
        self.llm_model = self._create_llm_model()

    def _create_llm_model(self) -> ChatOpenAI:
        llm_model = ChatOpenAI(
            model=self.model,
            name="Agent for job applications",
            temperature=self.set_temperature,
            n=1,
            api_key=self.openai_api_key
        )
        return llm_model

    def get_llm_model(self) -> ChatOpenAI:
        return self.llm_model