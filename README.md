# Crypto Query Assistant

Crypto Query Assistant is a FastAPI-based service that handles cryptocurrency-related queries using Together AI’s API, providing real-time cryptocurrency data and language translation capabilities. The assistant can answer questions about various supported cryptocurrencies and also handle queries in multiple languages, leveraging language detection to offer localized responses.

## Project Overview

This project is designed to respond to natural language prompts about cryptocurrencies, such as querying current prices or trends. It integrates several APIs and tools to deliver these responses dynamically. The project is still a work in progress, with active development focused on enhancing context management across multiple, unrelated queries.

### Current Functionality

- **Cryptocurrency Price Fetching:** The assistant fetches live prices of supported cryptocurrencies using a `CryptoService` class.
- **Language Detection and Translation:** Integrates `langdetect` for detecting non-English prompts and translates them to English using Together AI’s language model, enabling multi-language support.
- **Together AI Integration:** Utilizes Together AI’s language model API to generate responses based on user prompts and context.
- **Context Management:** Tracks conversation history to provide contextual responses. This is currently limited in handling unrelated queries sequentially.

## Tools & Technologies Used

- **FastAPI:** Serves as the backend framework for creating API endpoints.
- **Together AI API:** Provides the core language model for answering queries and performing translations.
- **Langdetect:** Detects the language of incoming prompts, enabling support for non-English languages.
- **Python `requests` and `httpx`:** Used for making asynchronous API requests to Together AI and other external services.

## Known Issues

### Context Management Limitations

The current implementation of context tracking in `AIAgent` does not effectively handle sequential, unrelated queries. For example:

- When the assistant is asked about "bitcoin price," it responds with the cryptocurrency data as expected.
- However, if subsequently asked about a general query like "What is the capital of Italy?" (in Italian), the assistant may respond with the translated query and still include context from the previous cryptocurrency question.
- This can lead to combined responses when two unrelated questions are asked back-to-back, such as mixing cryptocurrency data with general knowledge questions.

### Future Improvements

- **Enhanced Context Isolation:** Implement a more granular context-tracking mechanism that recognizes topic boundaries between unrelated questions.
- **Improved Response Formatting:** Ensure that only relevant responses are returned based on the current prompt, avoiding residual information from previous prompts.
- **Performance Optimization:** Address occasional delays in Together AI API response times when integrated with FastAPI.

## Getting Started

### Prerequisites

- Python 3.8+
- Together AI API Key
- FastAPI and related dependencies



1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/crypto-query-assistant.git
   cd crypto-query-assistant
