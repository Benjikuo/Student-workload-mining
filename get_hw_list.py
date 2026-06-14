from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from dotenv import load_dotenv
import json
import time
import os
import re


def clean_text(text):
    return " ".join(text.split())


def parse_score(text):
    text = clean_text(text)

    if not text:
        return None

    match = re.search(r"\d+(\.\d+)?", text)

    if match:
        score = match.group(0)
        return float(score) if "." in score else int(score)

    return None


def parse_late_minutes(uploaded_text):
    if "遲(" not in uploaded_text:
        return 0

    start = uploaded_text.find("遲(") + len("遲(")
    end = uploaded_text.find(")", start)

    if end == -1:
        return 0

    late_text = uploaded_text[start:end].replace("-", "").strip()

    days = 0
    hours = 0
    minutes = 0

    if "日" in late_text:
        day_part, late_text = late_text.split("日", 1)
        if day_part.isdigit():
            days = int(day_part)

    if "時" in late_text:
        hour_part, late_text = late_text.split("時", 1)
        if hour_part.isdigit():
            hours = int(hour_part)

    if "分鐘" in late_text:
        minute_part = late_text.split("分鐘", 1)[0]
        if minute_part.isdigit():
            minutes = int(minute_part)

    return days * 24 * 60 + hours * 60 + minutes


# 1. get password
print("1. get pasword")
load_dotenv()
USER = os.getenv("YZU_ID")
PASSWORD = os.getenv("YZU_PASS")

# 2. go to login page
print("2. go to login page")
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 15)
driver.get("https://portalx.yzu.edu.tw/PortalSocialVB/Login.aspx")

# 3. login
print("3. login")
time.sleep(0.2)
account_input = driver.find_element(By.ID, "Txt_UserID")
password_input = driver.find_element(By.ID, "Txt_Password")
account_input.send_keys(USER)  # type: ignore
password_input.send_keys(PASSWORD)  # type: ignore
time.sleep(0.4)
password_input.send_keys(Keys.ENTER)

# 4. go to course page
print("4. go to course page")
driver.get("https://portalx.yzu.edu.tw/PortalSocialVB/FMain/PageMyList.aspx")

# 5. find the course for each semester
print("5. find the course for each semester\n\nChecking semesters:")
wait.until(EC.presence_of_element_located((By.ID, "divPageA")))
courses = []

semester_headers = driver.find_elements(By.CSS_SELECTOR, "#divPageA > div.divClassYS")
for semester_header in semester_headers:
    semester = semester_header.get_attribute("textContent").strip()  # type: ignore
    driver.execute_script("arguments[0].click();", semester_header)

    semester_course_box = semester_header.find_element(
        By.XPATH, "following-sibling::div[1]"
    )

    course_links = semester_course_box.find_elements(
        By.CSS_SELECTOR, "a[href*='FirstToPage.aspx?PageID=']"
    )

    course_count = 0
    for link in course_links:
        course_name = link.get_attribute("textContent").strip()  # type: ignore
        course_url = link.get_attribute("href")

        if course_name and course_url:
            courses.append(
                {
                    "semester": semester,
                    "course_name": course_name,
                    "course_url": course_url,
                }
            )

            course_count += 1

    print(semester, "\t", course_count, "courses")

print("\nNumber of courses found:", len(courses))

# 6. skip semesters
skip_input = input(
    "\n6. Enter the semesters you don't want to visit, separated by commas (e.g., 1151, 1142).\nYour input: "
)

skip_semesters = [
    semester.strip() for semester in skip_input.split(",") if semester.strip()
]

courses = [course for course in courses if course["semester"] not in skip_semesters]
print("\nNumber of courses will be visited:", len(courses))

# 7. visit each course
print("\n7. visit each course")

results = []

for course in courses:
    driver.get(course["course_url"])

    homework_tab = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[normalize-space(text())='作業']"))
    )
    homework_tab.click()

    table = wait.until(EC.presence_of_element_located((By.ID, "Table1")))

    rows = table.find_elements(By.XPATH, "./tbody/tr")

    homework_count = 0

    for row in rows:
        cells = row.find_elements(By.XPATH, "./td")

        if len(cells) < 10:
            continue

        no_text = clean_text(cells[0].text)

        if not no_text.isdigit():
            continue

        homework_count += 1

        subject_lines = [
            line.strip() for line in cells[2].text.splitlines() if line.strip()
        ]

        assignment_name = subject_lines[0] if subject_lines else ""

        due_at = clean_text(cells[4].text)

        uploaded_text = cells[5].text.strip()
        late_minutes = parse_late_minutes(uploaded_text)

        assignment_type = cells[7].text.strip()
        score = parse_score(cells[9].text)

        record = {
            "semester": course["semester"],
            "course_name": course["course_name"],
            "assignment_name": assignment_name,
            "due_at": due_at,
            "late_minutes": late_minutes,
            "assignment_type": assignment_type,
            "score": score,
        }

        results.append(record)

    print(
        f"{course['semester']} | {course['course_name']} | {homework_count} homeworks"
    )

# 8. save results as a JSON file
print("8. save results as a JSON file")
with open("homeworks.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

driver.quit()
