import requests
from collections import defaultdict
import csv
from datetime import datetime

# ======================
# Настройки
# ======================
BASE_URL = "http://127.0.0.1:8000/resumes"
HEADERS = {
    "Authorization": (
        "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNzU1MTc5NjQ3fQ."
        "n4c0F9LEqiUYrYT_QmgP-QLhX3dbMETMae95RSgY9To"
    )
}

skills_to_search = ["Python", "SQL", "Power BI"]
keywords_to_search = ["data analysis", "machine learning", "reporting"]

# ======================
# Функции
# ======================

def fetch_all_resumes():
    """Запрашивает все резюме с сервера через API."""
    try:
        response = requests.get(BASE_URL, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Ошибка запроса: {e}")
        return []

def collect_resumes(skills, keywords):
    """Собирает резюме с навыками и ключевыми словами."""
    combined = defaultdict(lambda: {"skills": set(), "keywords": set()})
    resumes = fetch_all_resumes()

    for resume in resumes:
        filename = resume.get("filename") or resume.get("id", "Без имени файла")
        parsed_data = resume.get("parsed_data", {})
        parsed_skills = parsed_data.get("skills", [])
        text = parsed_data.get("text", "").lower()

        # Нормализация навыков
        normalized_skills = []
        for s in parsed_skills:
            if isinstance(s, str):
                normalized_skills.append(s.lower())
            elif isinstance(s, dict):
                normalized_skills.append(s.get("skill", "").lower())
                if s.get("matched_alias"):
                    normalized_skills.append(s.get("matched_alias").lower())

        # Проверка навыков
        for skill in skills:
            if skill.lower() in normalized_skills:
                combined[filename]["skills"].add(skill)

        # Проверка ключевых слов
        for keyword in keywords:
            if keyword.lower() in text:
                combined[filename]["keywords"].add(keyword)

    return combined

def print_combined_resumes(combined_resumes):
    """Вывод найденных резюме."""
    if not combined_resumes:
        print("⚠ Резюме с такими навыками или ключевыми словами не найдены.\n")
        return

    print("\n📄 Найденные резюме:\n")
    for filename, data in combined_resumes.items():
        skills_list = ", ".join(sorted(data["skills"])) or "Нет"
        keywords_list = ", ".join(sorted(data["keywords"])) or "Нет"
        print(f"✅ {filename}:")
        print(f"   - Навыки: {skills_list}")
        print(f"   - Ключевые слова: {keywords_list}\n")

def export_to_csv(combined_resumes, filename=None):
    """Экспорт результатов в CSV."""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"resumes_{timestamp}.csv"

    with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Filename", "Skills", "Keywords"])
        for file, data in combined_resumes.items():
            writer.writerow([
                file,
                ", ".join(sorted(data["skills"])),
                ", ".join(sorted(data["keywords"]))
            ])

    print(f"\n💾 Результаты экспортированы в файл: {filename}")
    return filename  # возвращаем имя файла для последующего просмотра

def show_csv(filename):
    """Выводит содержимое CSV в консоль."""
    print(f"\n📊 Содержимое файла {filename}:\n")
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)

# ======================
# Основной запуск
# ======================
if __name__ == "__main__":
    combined_resumes = collect_resumes(skills_to_search, keywords_to_search)
    print_combined_resumes(combined_resumes)
    csv_file = export_to_csv(combined_resumes)
    show_csv(csv_file)
