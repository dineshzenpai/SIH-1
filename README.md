# ⚡ SENTINEL-X AI | Deep Neural Identity & Document Forensic Intelligence Platform
*Engineered by Team: **CIPHER CARTEL***

An automated, multi-tiered AI screening and digital forensics intelligence system designed for high-throughput border checkpoints, airport immigration gates, and high-security identity verification terminals. 

SENTINEL-X screens identity documents (Passports, Aadhaar, PAN cards, Driving Licenses, National IDs) through a 4-tier neural forensic pipeline and computes a certified **Document Trust Score (0–100%)** with real-time visual compression heatmaps, copy-move graph analyzers, and printable court-admissible forensic dossiers.

---

## 🏛️ System Architecture

```
                               ┌──────────────────────────────────────────────────────────┐
                               │               Input: Document Asset + Live Biometric     │
                               └────────────────────────────┬─────────────────────────────┘
                                                            │
                 ┌──────────────────────────┬───────────────┴──────────────┬─────────────────────────┐
                 │                          │                              │                         │
                 ▼                          ▼                              ▼                         ▼
   ┌──────────────────────────┐┌──────────────────────────┐┌───────────────────────────┐┌──────────────────────────┐
   │        TIER 1            ││        TIER 2            ││          TIER 3           ││          TIER 4          │
   │  Preprocessing & OCR     ││  Cryptographic Integrity ││ Digital Tamper Forensics  ││ 1:1 Neural Face Match    │
   ├──────────────────────────┤├──────────────────────────┤├───────────────────────────┤├──────────────────────────┤
   │ • Deskew & Rectification ││ • Format Regex Check     ││ • Error Level Anal. (ELA) ││ • Optical Portrait Crop  │
   │ • LAB-space CLAHE Filter ││ • Verhoeff Checksum (UID)││ • Noise Residual Map      ││ • Live Camera Alignment  │
   │ • Multi-Engine OCR       ││ • ICAO Doc 9303 MRZ      ││ • Copy-Move Keypoint Det. ││ • Cosine Embedding Dist. │
   │ • Bounding Box Telemetry ││ • Chronological Logic    ││ • Edge Splicing Boundary  ││ • Passive Anti-Spoofing  │
   │ • Entity Field Parser    ││ • Cross-Field Coherence  ││ • EXIF / Software Tag Det.││ • Liveness Verification  │
   └─────────────┬────────────┘└────────────┬─────────────┘└─────────────┬─────────────┘└────────────┬─────────────┘
                 │                          │                              │                         │
                 └──────────────────────────┼──────────────────────────────┴─────────────────────────┘
                                            │
                                            ▼
                       ┌──────────────────────────────────────────┐
                       │          FRAUD DECISION ENGINE           │
                       │ Weighted Composite Trust Score (0-100%)  │
                       │ Status: AUTHENTIC / SUSPICIOUS / FRAUD   │
                       └────────────────────┬─────────────────────┘
                                            │
                                            ▼
                       ┌──────────────────────────────────────────┐
                       │    OPERATOR COMMAND HUD & PDF DOSSIER    │
                       │  • Interactive Visual Thermal Heatmaps   │
                       │  • Field-by-Field Discrepancy Breakdown  │
                       │  • Biometric Verification Card           │
                       │  • Downloadable Certified PDF Dossier    │
                       └──────────────────────────────────────────┘
```

---

## 🔬 Core Forensic Capabilities

### 1. Tier 1: Preprocessing & OCR Telemetry
- **Automatic Deskewing & Geometric Rectification**: Standardizes tilted cards using Hough line transform and minimum bounding area geometry.
- **Illumination Equalization**: LAB-space CLAHE (Contrast Limited Adaptive Histogram Equalization) balances flash glares and harsh shadows.
- **Multi-Engine OCR**: High-accuracy text bounding boxes, confidence metrics, and structured field extraction.

### 2. Tier 2: Cryptographic Checksums & Logical Validation
- **Verhoeff Checksum Algorithm**: Validates the 12th check digit of 12-digit UID numbers using the mathematical Dihedral Group $D_5$ multiplication table to detect swapped or fabricated numbers.
- **ICAO Doc 9303 MRZ Checksums**: Calculates and validates check digits for Passport Number, Date of Birth, Expiry Date, and composite check digit (7-3-1 weighting).
- **PAN Card Validation**: Structural `[A-Z]{5}[0-9]{4}[A-Z]` regex validation, 4th character entity type (`P` = Individual), and 5th character surname match.
- **Temporal & Coherence Logic**: Age plausibility ($\ge 18$), Issue Date $<$ Expiry Date, and expiration checks.

### 3. Tier 3: Digital Image Forensics & Tampering Detection
- **Error Level Analysis (ELA)**: Resaves at calibrated JPEG quality and computes difference matrix to expose spliced text or modified photos as bright thermal hotspots.
- **Noise Residual Analysis**: Laplacian high-pass filter detects mismatched sensor noise across copy-pasted document regions.
- **Copy-Move Forgery Detection (CMFD)**: ORB keypoint matching flags duplicated stamps, forged signatures, or cloned numbers.
- **EXIF & Metadata Audit**: Identifies editing software footprints (Photoshop, GIMP, Canva, PicsArt).

### 4. Tier 4: Biometric Face Matching & Passive Liveness
- **Automated ID Face Crop**: Detects portrait frame from the ID document.
- **Biometric 1:1 Embedding Matching**: Feature vector extraction with Cosine Similarity confidence score.
- **Passive Anti-Spoofing / Presentation Attack Detection**: 2D FFT frequency analysis detects moiré screen replay attacks and printed paper reflections.

---

## 📊 Decision Classification Matrix

$$\text{Unified Trust Score} = 0.35 \times S_{\text{Forensics}} + 0.30 \times S_{\text{Rules/OCR}} + 0.25 \times S_{\text{FaceMatch}} + 0.10 \times S_{\text{Metadata}}$$

| Trust Score | Status Classification | Protocol Action |
| :--- | :--- | :--- |
| **85 – 100%** | **🟢 AUTHENTIC** | Grant Instant Clearance |
| **60 – 84%** | **🟡 SUSPICIOUS** | Refer to Secondary Manual Inspection |
| **0 – 59%** | **🔴 FRAUDULENT** | Security Alert / Deny Entry & Investigate |

---

## 🚀 Quickstart Guide

### 1. Launch the Cyber-Defense Dashboard
Double-click `run_app.bat` or run:
```powershell
.venv_python\python.exe -m streamlit run app.py
```

### 2. Execute Automated Unit Tests
```powershell
.venv_python\python.exe -m unittest discover -s tests -p "test_*.py" -v
```

---

## 💻 Interactive Inspection Workflow

1. **Select Preset 1 (`[AUTHENTIC] National Identity Card`)** $\rightarrow$ Click **Initiate Deep Scan**.
   - Note the **96%+ Green Trust Score**, passed Verhoeff check, clean ELA thermal map, and confirmed Biometric Face Match.
2. **Select Preset 2 (`[TAMPERED] National ID Card (DOB Splicing)`)** $\rightarrow$ Click **Initiate Deep Scan**.
   - **Error Level Analysis (ELA)** immediately highlights the spliced DOB text in bright red/yellow thermal hotspot due to compression discrepancy.
3. **Select Preset 3 (`[FABRICATED] National ID Card (Checksum Violation)`)** $\rightarrow$ Click **Initiate Deep Scan**.
   - The mathematical **Dihedral $D_5$ algorithm** catches the fabricated number instantly.
4. **Select Preset 5 (`[TAMPERED] Passport (Mismatched MRZ)`)** $\rightarrow$ Click **Initiate Deep Scan**.
   - Identifies the failed **ICAO Doc 9303 7-3-1 check digit** on the modified expiry date.
5. **Switch Biometric Subject to Unregistered Impostor** $\rightarrow$ Triggers immediate biometric face mismatch rejection and passive presentation attack detection.
6. **Click "Download Certified Forensic Intelligence Dossier (PDF)"** $\rightarrow$ Generates the printable defense-grade dossier on the fly.
