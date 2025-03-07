# Open-Ended Vocabulary Quiz

An AI-powered interactive language learning tool that generates customized vocabulary quizzes and provides intelligent feedback on your answers.

## Overview

This application creates language-specific vocabulary quizzes where you fill in missing words in sentences. Unlike traditional multiple-choice quizzes, this tool accepts any answer and evaluates its appropriateness compared to the original word, providing nuanced feedback on your word choice.

## Features

- **Custom Quiz Generation**: Specify language, difficulty level, and number of questions
- **Open-Ended Answers**: Supply your own words rather than selecting from predefined choices
- **AI-Powered Evaluation**: Get detailed feedback on why your answer was appropriate or not
- **Multi-Language Support**: Works with any language (including right-to-left languages like Arabic)
- **Two Interfaces**: Command-line and web-based Streamlit interface

## Requirements

- Python 3.8+
- Azure OpenAI API access
- Required Python packages (install via `pip install -r requirements.txt`):
  - streamlit
  - langchain
  - langchain_openai
  - python-dotenv

## Setup

1. Clone this repository
2. Create a `.env` file in the project root with the following variables:
   ```
   AZURE_OPENAI_ENDPOINT=your_azure_endpoint
   AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
   AZURE_OPENAI_API_KEY=your_api_key
   ```
3. Install required packages: `pip install -r requirements.txt`

## Usage

### Command Line Interface

Run the quiz from the command line:

```
python main.py
```

You'll be prompted for:
- Target language
- Difficulty level
- Number of questions

The app will then:
1. Generate quiz sentences with blanks based on your parameters
2. Present each question one by one, allowing you to type your answer
3. Collect all your responses
4. Evaluate each answer compared to the original word
5. Provide detailed feedback on your vocabulary choices

### Streamlit Web Interface

Run the Streamlit app for a more user-friendly interface:

```
streamlit run app.py
```

The web interface provides:
1. Initial setup screen for quiz parameters
2. Interactive question-by-question interface
3. Results page with detailed feedback

## How It Works

1. **Quiz Generation**: The app prompts an AI model to create sentences with blanks based on your specified language and level
2. **Question Presentation**: Each question is presented as a sentence with a blank space
3. **Answer Collection**: You provide your own word to fill the blank
4. **Answer Evaluation**: The AI evaluates your answer against the original word, considering context, grammar, semantics, and appropriateness
5. **Feedback Display**: You receive detailed feedback on each answer

## Right-to-Left Language Support

The application automatically detects right-to-left scripts (like Arabic, Hebrew, etc.) and adjusts the display accordingly to ensure proper text rendering.

## Example Output

For a sentence like "Me gusta _____ todos los días." (I like _____ every day):

- Original answer: "leer" (to read)
- User answer: "nadar" (to swim)
- AI feedback: *"The student's answer 'nadar' (to swim) is appropriate in this context, as it fits the structure of the sentence 'Me gusta _____ todos los días' (I like _____ every day) just like the original word 'leer' (to read). Both activities can be done daily and express a routine or habit that someone might enjoy."*

## Project Structure

- `app.py`: Streamlit web interface
- `main.py`: Core logic and Azure OpenAI integration
- `prompts/`: Directory containing prompt templates
  - `generate_sentences/`: Templates for generating quiz questions
  - `evaluate_answer/`: Templates for evaluating user answers
- `app_architecture.md`: Technical documentation of app architecture

## License

[MIT License]

## Acknowledgments

This project uses Azure OpenAI services and was built with Streamlit and LangChain.