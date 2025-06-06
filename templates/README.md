# Proje Yönetimi Şablonları

Bu dizin, yapay zeka destekli proje yönetimi süreçlerinizi farklı projelerde yeniden kullanabilmeniz için genel şablonlar içermektedir. Her yeni proje için bu şablonları kopyalayarak ve proje özelindeki bilgileri doldurarak hızlıca bir başlangıç yapabilirsiniz.

## Şablonlar

1.  `generic_ai_project_manager_prompt_template.md`:
    *   Yapay zeka proje yöneticisi için temel talimatları ve görev tanımlarını içerir.
    *   Proje adı, dosya adları, faz başlıkları gibi alanlar yer tutucular (`[YER_TUTUCU]`) ile belirtilmiştir.

2.  `project_config_template.json`:
    *   Yeni projeler için `project_config.json` dosyasının şablonunu sağlar.
    *   Proje özelindeki dinamik bilgilerin merkezi olarak yönetilmesini kolaylaştırır.

3.  `problem_solution_log_template.md`:
    *   Proje sürecinde karşılaşılan sorunları, uygulanan çözümleri ve çıkarılan dersleri kayıt altına almak için standart bir format sunar.
    *   Deneyim kazanımı için önemli bir bilgi tabanı görevi görür.

4.  `ai_session_notes_template.md`:
    *   Yapay zeka oturum notları ve ilerleme takibi için genel bir yapıyı temsil eder.
    *   Oturum tarihi, proje durumu ve kritik başarılar gibi dinamik bilgileri girmek için yer tutucular içerir.

5.  `proje_analiz_raporu_template.md`:
    *   Proje başlangıcında veya belirli dönemlerde yapılacak analiz raporları için genel bir yapı sunar (SWOT analizi vb.).
    *   Proje özelindeki analiz bilgilerini girmek için yer tutucular içerir.

6.  `proje_calisma_plani_template.md`:
    *   Projenin detaylı çalışma planını, fazlarını, hedeflerini, adımlarını ve risk yönetimini tanımlamak için bir şablondur.
    *   Proje özelindeki çalışma planı bilgilerini girmek için yer tutucular içerir.

7.  `ai_todo_list_template.md`:
    *   Yapay zeka tarafından takip edilecek aktif görevleri ve alt görevleri listelemek için kullanılır. Otomasyon scriptleri tarafından okunur.

8.  `task_progress_template.md`:
    *   Görevlerin ilerleme durumlarını özetleyen, otomasyon scriptleri tarafından kullanılan bir tablo şablonudur.

9.  `uyari_raporu_template.md`:
    *   Otomatik görev tutarlılık kontrol scripti tarafından oluşturulan uyarı ve analiz raporlarının formatını tanımlar.

## Nasıl Kullanılır?

Yeni bir proje için bu şablonları kullanmak üzere aşağıdaki adımları izleyebilirsiniz:

1.  **`project_config.json` Dosyasını Hazırlayın:** `templates/project_config_template.json` dosyasını `projenizin_kök_dizini/project_config.json` olarak kopyalayın. Ardından, bu kopyaladığınız dosyadaki yer tutucuları kendi projenize özel bilgilerle doldurun. Bu dosya, diğer şablonlardan türetilecek proje belgeleri için temel yapılandırma bilgilerini sağlayacaktır.

2.  **Proje Belgelerini Otomatik Oluşturun (Yapay Zeka Asistanı ile):** Yapay zeka asistanınıza, hazırladığınız `project_config.json` dosyasını okuyarak, `templates` dizinindeki (`generic_ai_project_manager_prompt_template.md`, `problem_solution_log_template.md`, `ai_session_notes_template.md`, `proje_analiz_raporu_template.md`, `proje_calisma_plani_template.md`, `ai_todo_list_template.md`, `task_progress_template.md`, `uyari_raporu_template.md`) şablonları kullanarak ilgili proje belgelerini (örn. `project_docs/ai_prompt_for_your_project.md`, `project_docs/problem_solution_log_for_your_project.md`, `project_docs/proje_analiz_raporu.md`, `project_docs/proje_calisma_plani.md`, `project_docs/ai_session_notes.md`, `project_docs/ai_todo_list.md`, `project_docs/task_progress.md`, `project_docs/uyari_raporu.md`) projenizin `project_docs` dizini altına otomatik olarak oluşturmalısın. Bu dosyaları oluştururken, `project_config.json` dosyasındaki değerleri kullanarak yer tutucuları doldurmalısın.

3.  **Proje Yönetimini Başlatın:** Oluşturulan ve projenize özel hale getirilen belge dosyalarını (özellikle AI proje yöneticisi talimat dosyası) yapay zeka asistanınıza okutarak yeni proje yönetim sürecinizi başlatın. Yapay zeka, bu belgelere dayanarak projenizi yönetmeye ve ilerlemeyi raporlamaya başlayacaktır.

Bu yapı, projenizin özel gereksinimlerine göre kolayca uyarlanabilir ve yapay zeka tabanlı proje yönetimini farklı bağlamlarda etkin bir şekilde kullanmanızı sağlar. 