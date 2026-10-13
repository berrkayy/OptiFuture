import openai
import os
import json
from dotenv import load_dotenv
from fuzzywuzzy import process

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Kurs verilerini JSON dosyasından yükle
with open("courses.json", "r", encoding="utf-8") as f:
    course_data = json.load(f)

# Başarı Hikayeleri Veri Tabanı
success_stories = {
    "veri bilimi": "Ahmet Yılmaz, Endüstri Mühendisliği mezunu, Python ve SQL öğrendikten sonra veri analizi projeleri geliştirdi ve şu anda XYZ Tech şirketinde Veri Bilimcisi olarak çalışıyor.",
    "yapay zeka": "Ayşe Demir, Bilgisayar Mühendisliği mezunu, yapay zeka üzerine Kaggle projeleri yaptı ve Google AI'da staj yaptı.",
    "web geliştirme": "Berkay Altunbağ, Elektrik Elektronik Mühendisliği mezunu, Frontend geliştirme üzerine çalıştı ve bir startupta yazılım geliştirici olarak kariyerine başladı.",
    "aviyonik sistem mühendisliği": "Burak Yılmaz, Kontrol ve Otomasyon Mühendisliği mezunu, ASELSAN'da staj yaptıktan sonra aviyonik sistem geliştirme mühendisi olarak çalışmaya başladı."
}

# CV'den Eğitim Bilgisi ve Yetenekleri Çek
def extract_info_from_cv(cv_text):
    prompt = f"""
Bu kişinin CV içeriğini analiz et:
{cv_text}

Şu bilgileri bana kısa ve net şekilde ver:
- Eğitim durumu (Öğrenci/Mezun)
- Kaçıncı sınıf
- Mezuniyet bölümü
- Bildiği programlama dilleri
- Bildiği araçlar

Format:
Eğitim Durumu: ...
Sınıf: ...
Bölüm: ...
Programlama Dilleri: ...
Araçlar: ...
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Sen bir bilgi çıkarıcısın."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=300
    )

    result = response.choices[0].message.content.strip()

    lines = result.split('\n')
    education_status = lines[0].split(':')[-1].strip()
    student_class = lines[1].split(':')[-1].strip()
    education = lines[2].split(':')[-1].strip()
    programming_skills = lines[3].split(':')[-1].strip()
    tools = lines[4].split(':')[-1].strip()

    return {
        "education_status": education_status,
        "student_class": student_class,
        "education": education,
        "programming_skills": programming_skills,
        "tools": tools
    }

# Başarı Hikayesi Öner
def suggest_success_story(goal):
    goal = goal.lower()
    for keyword in success_stories:
        if keyword in goal:
            return success_stories[keyword]
    return None

# GPT'den Yerli ve Maksimum 5 Kurs Öner
def ask_gpt_for_courses(topic):
    prompt = f"""
'{topic}' konusunda öğrenmek isteyen bir kullanıcı için maksimum 5 adet kurs öner. 
Sadece BTK Akademi, T3 Akademi veya Yetenek Kapısı gibi yerli ve ücretsiz platformlardan öner.

Format:
- Kurs Adı - Platform Adı

Kurs isimleri net ve gerçekçi olsun. Uydurma veya alakasız şeyler yazma.
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Sen bir kariyer danışmanısın."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=400
    )
    return response.choices[0].message.content.strip()

# Konuları Kurslarla Eşleştir
def match_courses(advice_text):
    matched_courses = []
    unmatched_topics = []

    for line in advice_text.split("\n"):
        clean_line = line.strip()
        if clean_line == "":
            continue
        best_match, score = process.extractOne(clean_line, course_data.keys())
        if score >= 80:
            course_info = course_data[best_match]
            matched_courses.append(
                f"- 📚 Kurs: {course_info['course_name']} ({course_info['platform']})\n🔗 Link: {course_info['link']}"
            )
        else:
            unmatched_topics.append(clean_line)

    if unmatched_topics:
        gpt_courses = ask_gpt_for_courses(", ".join(unmatched_topics))
        matched_courses.append(f"\nGPT'den gelen kurslar:\n{gpt_courses}")

    return matched_courses

# Kişisel Yol Haritası + Proje Önerisi Üret
def generate_advice_and_project(user_profile):
    prompt = f"""
    Kullanıcının bilgileri:
    - CV İçeriği: {user_profile.get('cv_content')}
    - Eğitim Durumu: {user_profile.get('education_status')}
    - Sınıf: {user_profile.get('student_class')}
    - Bölüm: {user_profile.get('education')}
    - Bildiği Programlama Dilleri: {user_profile.get('programming_skills')}
    - Bildiği Araçlar: {user_profile.get('tools')}
    - Hedef: {user_profile.get('goal')}

    Bu bilgilere göre:
    1. Kariyer hedefi doğrultusunda 3 aylık eğitim planı oluştur.
    - 5 ila 8 öğrenme konusu yaz.
    - Ay ay listele.
    - Bildiği konuları tekrar önerme.
    2. Hedefe uygun gerçek dünyaya dayalı bir mini proje öner.
    - Proje adı
    - Proje açıklaması
    - Kullanılacak araçlar
    - Beklenen çıktı

    Yanıtı çok açık ve düzenli ver.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Sen bir kariyer planlayıcı ve proje önericisin."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=1000
    )

    return response.choices[0].message.content.strip()