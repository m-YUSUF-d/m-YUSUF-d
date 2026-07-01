import json
import random
import re

README_PATH = "README.md"
FACTS_PATH = "facts.json"

START_TAG = "<!-- DAILY_FACT_START -->"
END_TAG = "<!-- DAILY_FACT_END -->"


def load_facts():
    with open(FACTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_current_readme():
    with open(README_PATH, "r", encoding="utf-8") as f:
        return f.read()


def save_readme(content):
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)


def extract_current_fact(readme_text):
    pattern = f"{START_TAG}(.*?){END_TAG}"
    match = re.search(pattern, readme_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""


def choose_new_fact(facts, current_fact):
    # random seç, aynıysa tekrar dene
    if len(facts) == 0:
        return ""

    new_fact = current_fact

    attempts = 0
    while new_fact == current_fact and attempts < 20:
        new_fact = random.choice(facts)
        attempts += 1

    return new_fact


def update_readme(readme_text, new_fact):
    pattern = f"{START_TAG}(.*?){END_TAG}"

    replacement = f"{START_TAG}{new_fact}{END_TAG}"

    if re.search(pattern, readme_text, re.DOTALL):
        updated = re.sub(pattern, replacement, readme_text, flags=re.DOTALL)
    else:
        # tag yoksa ekle
        updated = readme_text + "\n\n" + replacement

    return updated


def main():
    facts = load_facts()
    readme = get_current_readme()

    current_fact = extract_current_fact(readme)
    new_fact = choose_new_fact(facts, current_fact)

    if new_fact == current_fact:
        print("No change needed.")
        return

    updated_readme = update_readme(readme, new_fact)

    save_readme(updated_readme)

    print("README updated successfully!")
    print("New fact:", new_fact)


if __name__ == "__main__":
    main()