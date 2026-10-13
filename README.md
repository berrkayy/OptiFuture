# OptiFuture

AI-powered lifelong learning and career guidance platform. OptiFuture reads a user's CV, extracts their education and skills, and generates a personalized **3-month career roadmap**, a **mini project suggestion** and **matching free courses** from Turkish platforms such as BTK Akademi.

Finalist of the **TEKNOFEST KKTC Social Innovation Competition** and winner of the **TÜBİTAK Special Presentation Award (1st)**.

## Features

- **CV analysis (NLP):** Extracts education status, class, department, programming languages and tools from CV text using the OpenAI GPT-3.5 Turbo API.
- **Personalized roadmap:** Generates a month-by-month 3-month learning plan and a real-world mini project based on the user's profile and career goal.
- **Course matching:** Maps roadmap topics to a curated course list (`courses.json`) with fuzzy matching (`fuzzywuzzy`); unmatched topics fall back to GPT-based course suggestions from local free platforms.
- **Success stories:** Suggests an inspiring story related to the user's career goal.
- **Promotional website:** Multi-page, responsive site (home, features, about, contact) built with HTML and CSS.

## Tech Stack

Python · OpenAI API (GPT-3.5 Turbo) · fuzzywuzzy · python-dotenv · HTML · CSS

## Project Structure

```
OptiFuture/
├── backend/
│   ├── main.py          # CLI entry point
│   ├── rules.py         # CV extraction, roadmap generation, course matching
│   └── courses.json     # Curated course database
├── website/
│   ├── index.html
│   ├── features.html
│   ├── about.html
│   ├── contact.html
│   └── styles.css
├── .env.example
├── requirements.txt
└── LICENSE
```

## Getting Started

### Requirements

- Python 3.9+
- An [OpenAI API key](https://platform.openai.com/api-keys)

### Installation

```bash
git clone https://github.com/berrkayy/OptiFuture.git
cd OptiFuture
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the project root (see `.env.example`):

```
OPENAI_API_KEY=your_openai_api_key_here
```

### Usage

```bash
cd backend
python main.py
```

Enter the path to a plain-text CV (UTF-8), confirm the extracted information, then enter your career goal to receive your roadmap, project suggestion and course recommendations.

### Website

Open `website/index.html` in a browser.

## Roadmap

- Web interface for the career engine
- PDF CV support
- Larger course database and more platforms

## Authors

Developed by [Berkay Altunbağ](https://github.com/berrkayy) and the OptiFuture team.

## License

[MIT](LICENSE)
