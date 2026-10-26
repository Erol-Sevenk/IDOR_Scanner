# API BOLA Scanner - Mimari Tasarım

```mermaid
flowchart TD
    A[OpenAPI Reader] --> D[Endpoint Listesi]
    B[HAR Reader] --> D
    D --> E[ID Parametresi Çıkarımı]
    E --> F[Oturum Yöneticisi - Hafta 3-4]
    F --> G[İstek Mutasyon Motoru - Hafta 5-6]
    G --> H[Analiz Motoru - Hafta 7-8]
    H --> I[Raporlama - Hafta 9]
