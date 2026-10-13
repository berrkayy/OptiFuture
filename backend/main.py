from rules import generate_advice_and_project, extract_info_from_cv, suggest_success_story, match_courses

print("OptiFuture AI'ye Hoş Geldin! 🚀 Bilgilerini yükleyerek sana özel bir kariyer rehberi oluşturacağım.\n")

cv_path = input("CV dosya yolunu gir (örnek: /Users/ahmetkaganorun/Desktop/cv.txt): ").strip()

try:
    with open(cv_path, "r", encoding="utf-8") as file:
        cv_content = file.read()
except FileNotFoundError:
    print("Hata: Belirttiğin dosya bulunamadı. Lütfen doğru bir dosya yolu gir.")
    exit()

print("\nCV verileri başarıyla alındı! Şimdi bilgilerini çıkarıyorum...\n")

extracted_info = extract_info_from_cv(cv_content)

print(f"""
Tespit edilen bilgiler:
- Eğitim Durumu: {extracted_info.get('education_status')}
- Sınıf: {extracted_info.get('student_class')}
- Bölüm: {extracted_info.get('education')}
- Bildiği Programlama Dilleri: {extracted_info.get('programming_skills')}
- Bildiği Araçlar: {extracted_info.get('tools')}
""")

onay = input("Bu bilgiler doğru mu? (Evet/Hayır): ").strip().lower()

if onay != "evet":
    extracted_info['education_status'] = input("Lütfen Eğitim Durumu (Öğrenci/Mezun) gir: ").strip()
    extracted_info['student_class'] = input("Kaçıncı sınıftasın? (1/2/3/4): ").strip()
    extracted_info['education'] = input("Bölümün nedir?: ").strip()
    extracted_info['programming_skills'] = input("Bildiğin programlama dilleri: ").strip()
    extracted_info['tools'] = input("Kullandığın araçlar (Excel, AutoCAD gibi): ").strip()

while True:
    goal = input("\nKariyer hedefin nedir?: ").strip()

    user_profile = {
        "cv_content": cv_content,
        "education_status": extracted_info.get('education_status'),
        "student_class": extracted_info.get('student_class'),
        "education": extracted_info.get('education'),
        "programming_skills": extracted_info.get('programming_skills'),
        "tools": extracted_info.get('tools'),
        "goal": goal
    }

    response = generate_advice_and_project(user_profile)
    print("\n--- Sana Özel OptiFuture Yol Haritası ve Proje Önerisi ---\n")
    print(response)

    matched_courses = match_courses(response)
    print("\n--- Önerilen Kurslar ---\n")
    for course in matched_courses:
        print(course)

    success_story = suggest_success_story(goal)
    if success_story:
        print("\n--- Sana İlham Verecek Bir Başarı Hikayesi ---\n")
        print(success_story)

    tekrar = input("\nHedefini değiştirmek ister misin? (Evet/Hayır): ").strip().lower()
    if tekrar != "evet":
        print("\nBaşarılar dileriz! 🚀")
        break