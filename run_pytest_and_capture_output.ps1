# Bu betiği projenin kök dizininde çalıştırmanız önerilir.
# cd C:\source\dual-modal-research

# PowerShell oturumunun varsayılan çıktı kodlamasını UTF-8 olarak ayarla.
# Bu, Türkçe karakterler ve diğer Unicode karakterlerin doğru görüntülenmesini sağlar.
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Conda'nın hata raporlama istemini kalıcı olarak devre dışı bırak.
# Bu, 'conda activate' sırasında ortaya çıkabilecek '[y/N]:' gibi etkileşimli istemleri önler.
# Bu komut yalnızca bir kez çalıştırılmalıdır; sonrasında raporlama ayarı kaydedilir.
# Eğer daha önce manuel olarak devre dışı bıraktıysanız bu satırı silebilirsiniz.
conda config --set report_errors false

# Conda ortamını etkinleştirme.
# Bu komutun Conda Prompt içinde doğru çalışacağı varsayılır.
conda activate dual-modal-research

# Pytest'i çalıştır ve tüm çıktıyı (standart çıktı ve hata çıktısı) dosyaya kaydet.
# -Encoding utf8 parametresi, dosya yazılırken UTF-8 kodlamasını kullanır.
pytest 2>&1 | Out-File -FilePath logs/pytest_output_for_ai.txt -Encoding utf8

Write-Host "Pytest çıktısı logs/pytest_output_for_ai.txt dosyasına başarıyla kaydedildi."