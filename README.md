<div align="center">

# 🦺 Smart Glass — Construction Site (Device)
### 건설 현장 안전관리 스마트글래스 — 디바이스 펌웨어

<p>
  <img src="https://img.shields.io/badge/Project-2022_한이음_ICT_멘토링-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/Award-전국_600팀_중_장려상-orange?style=flat-square" />
  <img src="https://img.shields.io/badge/Award-정보처리학회_우수논문상-orange?style=flat-square" />
  <img src="https://img.shields.io/badge/Role-Team_Lead-red?style=flat-square" />
</p>

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Raspberry_Pi-A22846?style=for-the-badge&logo=raspberry-pi&logoColor=white" />
  <img src="https://img.shields.io/badge/AWS_S3-569A31?style=for-the-badge&logo=amazon-aws&logoColor=white" />
  <img src="https://img.shields.io/badge/Google_Assistant-4285F4?style=for-the-badge&logo=google-assistant&logoColor=white" />
  <img src="https://img.shields.io/badge/Android-3DDC84?style=for-the-badge&logo=android&logoColor=white" />
</p>

</div>

---

## 🏗 Why this project

건설 현장의 안전 점검은 여전히 종이 체크리스트와 수기 보고에 의존합니다. 작업자가 위험 상황을 발견해도 사진을 찍고 사무실에 보고하는 데 시간이 걸리고, 그 사이 사고가 일어납니다.

본 프로젝트는 **현장 작업자가 손을 떼지 않고 사고를 즉시 보고하도록** 설계된 안전관리 스마트글래스의 디바이스 측 코드를 담고 있습니다.

> 결과: 현장 점검 흐름 약 **40% 개선**, 한이음 전국 600팀 중 **장려상**, 한국정보처리학회 **우수논문상** 수상.

---

## 📷 Device Architecture

```
┌──────────────────────────────────────┐
│   Smart Glass (Raspberry Pi)         │
│                                      │
│   ▣ PiCamera 2592×1944               │
│   ▣ Microphone (PyAudio, 5s clip)    │
│   ▣ Hardware Switch (GPIO 14)        │
│   ▣ Curses-based local display       │
│                                      │
│   trigger ──► capture + record ──┐   │
└──────────────────────────────────│───┘
                                   ▼
                       ┌────────────────────┐
                       │  AWS S3 (boto3)    │
                       │  upload .jpg/.wav  │
                       └─────────┬──────────┘
                                 ▼
                       ┌────────────────────┐
                       │  Django Backend +  │
                       │  Android Viewer    │
                       └────────────────────┘
```

작업자가 위험을 발견하고 글래스의 스위치를 누르면 → 즉시 고해상도 사진 + 5초 음성 클립이 캡처되고 → AWS S3로 업로드 → 관제 앱에서 실시간 확인.

---

## 🧩 Components in this repo

| File | Role |
|---|---|
| `main.py` | 메인 루프 — 스위치 감지 / 캡처 / S3 업로드 |
| `camerascan.py` | 이미지 캡처 및 해상도 제어 |
| `recording.py` | PyAudio 기반 5초 현장 음성 녹음 |
| `display.py` | curses 기반 로컬 상태 표시 |
| `Hardware_Image.jpg` | 실제 디바이스 사진 |

---

## 🛠 Tech Stack

- **Hardware**: Raspberry Pi / PiCamera / Microphone / Tactile Switch
- **Software**: Python / picamera / pyaudio / RPi.GPIO / boto3 (AWS SDK)
- **Cloud**: AWS S3 (이미지 / 음성 저장), Backend Django REST
- **Companion**: Android viewer + Google Assistant 연동

---

## 🔗 Related Repositories

| | |
|---|---|
| 🦺 **Device firmware** *(this repo)* | [smartglass](https://github.com/SmartGlassAtConstructionSite/smartglass) |
| 🖥 Backend (Django REST) | [backend](https://github.com/SmartGlassAtConstructionSite/backend) |

---

## 🏆 Awards

- 🥉 **2022 한이음 ICT 멘토링 장려상** — 과학기술정보통신부 / KCC정보통신 (전국 600팀)
- 🏅 **2022 한국정보처리학회 ACK 우수논문상**

---

## 👥 Team

강현구,김성민,이민영,최혜린,최태훈

---

<div align="center">

*Bringing on-site safety reporting from minutes to seconds.*

</div>
