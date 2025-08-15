Resume Screener API Client

A Python-based tool for searching resumes via a local API, filtering them by specific skills and keywords, and exporting the results into a CSV file.
Designed for HR professionals, recruiters, and data analysts who need a quick way to screen candidate resumes.

FEATURES

Connects to a local resume parsing API using Bearer Token authentication.

Searches resumes for specific skills and keywords.

Outputs a clear console report with found matches.

Exports the results into a timestamped CSV file.

Works cross-platform (Windows, macOS, Linux).

PROJECT STRUCTURE
resume-screener/
│
├── search_by_skill.py # Main script
├── requirements.txt # Project dependencies
└── README.md # Project documentation

REQUIREMENTS

Python 3.8+

Installed packages listed in requirements.txt

Access to a local or remote API that returns resume data in JSON format

INSTALLATION

Clone this repository
git clone https://github.com/YOUR_USERNAME/resume-screener.git
cd resume-screener

Create a virtual environment
python -m venv .venv

Activate the virtual environment

Windows (PowerShell)
.venv\Scripts\activate

macOS/Linux
source .venv/bin/activate

Install dependencies
pip install -r requirements.txt

CONFIGURATION
Open search_by_skill.py and configure:

BASE_URL — the URL of your resume API (e.g. http://127.0.0.1:8000/resumes)

HEADERS — replace the token with your actual Bearer Token

skills_to_search — list of skills to filter resumes

keywords_to_search — list of keywords to match in resume text

Example:
skills_to_search = ["Python", "SQL", "Power BI"]
keywords_to_search = ["data analysis", "machine learning", "reporting"]

USAGE
Run the script:
python search_by_skill.py

Example output:
📄 Found resumes:

✅ resume_example.pdf:

Skills: Python



✅ resume_text_1.txt:

Skills: Power BI, Python, SQL



✅ resume_text_3.txt:

Skills: Python



💾 Results exported to file: resumes_20250814_162953.csv

OUTPUT
The CSV file will contain:

Filename	Skills	Keywords
resume_example.pdf	Python	
resume_text_1.txt	Power BI, Python, SQL	
resume_text_3.txt	Python	

LICENSE
This project is licensed under the MIT License — see the LICENSE file for details.

CONTRIBUTING
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

AUTHOR
Niko Vlasov — LinkedIn | GitHub