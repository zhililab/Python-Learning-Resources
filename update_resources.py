#!/usr/bin/env python3
"""
Update README for Python-Learning-Resources repository.

This script fetches trending Python repositories from GitHub and regenerates
README.md with curated tutorials, best practices, and trending projects.

If unable to access the trending page or API, it falls back to a predefined
list of popular repositories.

Sources:
- Real Python docstrings article【156047168182090†L29-L33】
- Dataquest project ideas【904153524833764†L50-L67】
- DataCamp intro to Python【949811956147805†L52-L55】
- Python 100 Days【836895632859947†L307-L317】
- PEP 8 guidelines【615368974677617†L119-L176】
- DataCamp best practices【826886253017015†L146-L179】
- Top trending projects【836895632859947†L206-L217】【836895632859947†L223-L236】【836895632859947†L240-L251】
"""

import datetime
import requests
from bs4 import BeautifulSoup

FALLBACK_PROJECTS = [
    ("donnemartin/system-design-primer", "Learn how to design large-scale systems; includes Anki flashcards"),
    ("vinta/awesome-python", "An opinionated list of awesome Python frameworks, libraries and resources"),
    ("TheAlgorithms/Python", "All algorithms implemented in Python, a great resource for practice"),
    ("jackfrued/Python-100-Days", "Chinese course: Python — 100 days from beginner to master"),
    ("yt-dlp/yt-dlp", "A feature-rich command-line program to download audio/video"),
]

def fetch_trending_projects(limit=5):
    try:
        url = "https://github.com/trending/python?since=daily"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        entries = soup.find_all("article", class_="Box-row")
        projects = []
        for entry in entries[:limit]:
            h2 = entry.find("h2")
            repo = "".join(part.strip() for part in h2.text.split()) if h2 else ""
            repo = repo.replace(" / ", "/").replace(" ", "")
            p = entry.find("p")
            desc = p.text.strip() if p else "No description provided."
            projects.append((repo, desc))
        return projects
    except Exception:
        return FALLBACK_PROJECTS[:limit]

def generate_readme(projects):
    date_str = datetime.date.today().strftime("%Y-%m-%d")
    content = f"""# Python Learning Resources

Welcome!  This repository collects carefully curated resources to help you
learn and grow as a Python developer.  Whether you're new to the
language or looking to deepen your expertise, you'll find tutorials,
courses, best practice guidelines and inspiring open‑source projects
here.  The document is regenerated automatically on a daily basis to
keep the content fresh and relevant.

## Tutorials & Courses

* **Write Effective Docstrings** – Real Python's recent article shows how to document your
  functions and classes clearly and professionally using built‑in
  conventions【156047168182090†L29-L33】.
* **60+ Python Project Ideas** – Dataquest's guide encourages learning by
  building projects.  It suggests beginner projects such as an
  interactive word game, analyzing your Netflix data, predicting heart
  disease, exploring Hacker News posts, and analyzing eBay car sales
  data【904153524833764†L50-L67】.
* **Intro to Python for Data Science** – DataCamp's course provides an
  accessible introduction to Python and its data ecosystem【949811956147805†L52-L55】.
* **Python 100 Days** – A hands‑on Chinese course that takes you from
  beginner to advanced through 100 days of projects【836895632859947†L307-L317】.

If you prefer guided learning paths, [Real Python](https://realpython.com/)
and [Dataquest](https://www.dataquest.io/blog/python-projects-for-beginners/)
offer curated courses and project‑based learning.

## Best Practices

Writing clean, maintainable code is essential for any developer.  Here are
some key takeaways from the Python community’s style guides and
literature:

* **Follow PEP 8** – Use 4 spaces per indentation level and limit lines
  to around 79 characters to improve readability【615368974677617†L119-L176】.  Separate
  functions and classes with blank lines and group related code
  logically【615368974677617†L119-L176】.
* **Meaningful Names** – Choose descriptive variable, function and class
  names.  Avoid single‑letter names except for short loop variables.
* **Use Docstrings** – Document modules, classes and functions using
  triple‑quoted strings so that users understand the API and internal
  behavior【156047168182090†L29-L33】.
* **Keep Functions Small** – Each function should do one thing well.  If a
  function grows too long, consider breaking it into smaller helpers.
* **Leverage Linters and Formatters** – Tools like ``flake8``, ``pylint``
  and ``black`` help ensure stylistic consistency and catch common
  mistakes【826886253017015†L146-L179】.
* **Test Your Code** – Adopt a test‑driven workflow: write tests first,
  implement the functionality and then refactor.  Automated tests
  increase confidence when refactoring and deploying changes.
* **Readability Over Cleverness** – Clear and straightforward code is
  preferred over overly clever constructs.  Remember, code is read more
  often than it is written【615368974677617†L89-L97】.

For a comprehensive reference, consult the full PEP 8 document【615368974677617†L119-L176】.

## Trending Open‑Source Projects

The open‑source community produces a wealth of high‑quality projects.
Here are some of the Python repositories trending on GitHub today:

"""
    for name, desc in projects:
        content += f"* **{name}** – {desc}\n"
    content += """For further inspiration, check out established resources such as
**system‑design‑primer** for learning how to design large‑scale
systems【836895632859947†L206-L217】 and **awesome‑python**, a curated list of
libraries and frameworks【836895632859947†L223-L236】.  The **TheAlgorithms/Python**
repository implements many algorithms in Python and is updated
regularly【836895632859947†L240-L251】.
"""
    content += f"\n_Last updated: {date_str}_\n"
    return content

def main():
    projects = fetch_trending_projects()
    readme = generate_readme(projects)
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)
    print("README.md updated")

if __name__ == "__main__":
    main()
