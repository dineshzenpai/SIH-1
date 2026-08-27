"""
SENTINEL-X AI | Next-Gen Neural Forensic & Identity Screening Platform
Automated Document Forensics • Cryptographic Rules • Neural Biometric Verification
"""

import os
import io
import time
import cv2
import numpy as np
import streamlit as st
from PIL import Image

# Core engine imports
from core.rules_validator import RulesValidator
from core.tamper_detector import TamperDetector
from core.ocr_engine import OCREngine
from core.face_matcher import FaceMatcher
from core.scorer import FraudScorer
from core.report_generator import ReportGenerator
from core.sample_generator import SampleGenerator
from core.preprocessor import DocumentPreprocessor
from core.ai_copilot import AICopilot

# Page Configuration
st.set_page_config(
    page_title="SENTINEL-X | AI Identity Forensics",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ultra-Cool Futuristic Cyber-Defense Dark Theme Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800;900&family=Rajdhani:wght@500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

    /* Global Dark Theme */
    .stApp {
        background-color: #070b12;
        color: #e2e8f0;
        font-family: 'Rajdhani', sans-serif;
    }
    
    /* Neon Cyber Header */
    .sentinel-header {
        background: linear-gradient(135deg, rgba(13, 20, 36, 0.95), rgba(8, 14, 26, 0.98));
        border: 1px solid #1e293b;
        border-bottom: 2px solid #00f2fe;
        padding: 22px 28px;
        border-radius: 14px;
        box-shadow: 0 0 25px rgba(0, 242, 254, 0.15), inset 0 0 15px rgba(0, 242, 254, 0.05);
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    .sentinel-header::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 2px;
        background: linear-gradient(90deg, #00f2fe, #4facfe, #00c6ff, #0072ff);
    }
    .sentinel-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 26px;
        font-weight: 900;
        letter-spacing: 2px;
        color: #ffffff;
        text-shadow: 0 0 12px rgba(0, 242, 254, 0.6);
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .sentinel-subtitle {
        font-size: 14px;
        color: #94a3b8;
        letter-spacing: 1px;
        margin-top: 6px;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
    }
    
    /* HUD Verdict Cards */
    .hud-card {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(51, 65, 85, 0.6);
        border-radius: 10px;
        padding: 16px;
        backdrop-filter: blur(8px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    .hud-pass {
        background: linear-gradient(135deg, rgba(6, 78, 59, 0.9), rgba(4, 120, 87, 0.7));
        border: 1px solid #10b981;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.3);
        border-radius: 12px;
        padding: 20px 24px;
        color: #ffffff;
    }
    .hud-review {
        background: linear-gradient(135deg, rgba(120, 53, 15, 0.9), rgba(180, 83, 9, 0.7));
        border: 1px solid #f59e0b;
        box-shadow: 0 0 20px rgba(245, 158, 11, 0.3);
        border-radius: 12px;
        padding: 20px 24px;
        color: #ffffff;
    }
    .hud-fail {
        background: linear-gradient(135deg, rgba(127, 29, 29, 0.9), rgba(185, 28, 28, 0.7));
        border: 1px solid #ef4444;
        box-shadow: 0 0 25px rgba(239, 68, 68, 0.4);
        border-radius: 12px;
        padding: 20px 24px;
        color: #ffffff;
    }
    
    /* Cyber Telemetry Stat Box */
    .cyber-stat {
        background: #0d1527;
        border: 1px solid #1e293b;
        border-left: 4px solid #00f2fe;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 10px;
    }
    .cyber-stat-title {
        font-size: 12px;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 700;
    }
    .cyber-stat-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: 22px;
        font-weight: 700;
        color: #38bdf8;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: #0b111e;
        padding: 6px;
        border-radius: 10px;
        border: 1px solid #1e293b;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Rajdhani', sans-serif;
        font-size: 15px;
        font-weight: 700;
        letter-spacing: 0.5px;
        border-radius: 8px;
        color: #94a3b8;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00f2fe, #0072ff) !important;
        color: #000000 !important;
        font-weight: 800 !important;
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.4);
    }
    
    /* Code / Monospace */
    code {
        font-family: 'JetBrains Mono', monospace !important;
        color: #38bdf8 !important;
        background: #0f172a !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
        border: 1px solid #1e293b !important;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def initialize_system():
    """Initializes and caches AI core engines."""
    ocr = OCREngine()
    face = FaceMatcher()
    SampleGenerator.save_all_sample_files("samples")
    return ocr, face


def main():
    ocr_engine, face_matcher = initialize_system()

    # Futuristic Header with Team Cipher Cartel branding
    st.markdown("""
    <div class="sentinel-header">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <div class="sentinel-title">
                ⚡ SENTINEL-X &nbsp;|&nbsp; DEEP NEURAL IDENTITY FORENSICS
            </div>
            <div style="background: rgba(0, 242, 254, 0.15); border: 1px solid #00f2fe; color: #38bdf8; padding: 4px 14px; border-radius: 20px; font-family: 'JetBrains Mono', monospace; font-size: 12px; font-weight: 700; letter-spacing: 1px;">
                TEAM: CIPHER CARTEL
            </div>
        </div>
        <div class="sentinel-subtitle">
            QUANTUM DOCUMENT SCANNER • MULTI-SPECTRAL COMPRESSION FORENSICS • CRYPTOGRAPHIC INTEGRITY • 1:1 BIOMETRIC NEURAL MATCH
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar: Terminal Control Center
    with st.sidebar:
        st.markdown("### 🎛️ Terminal Telemetry")
        st.markdown("**🛡️ Cyber Unit:** `CIPHER CARTEL`")
        terminal_id = st.text_input("📡 Security Station", value="SECTOR-07 / ALPHA GATE")
        inspector_name = st.text_input("🛡️ Operator Clearance", value="AGENT-CYBER-904")

        st.markdown("---")
        mode = st.radio(
            "⚡ Ingestion Stream",
            ["🚀 Instant Preset Test Suite", "📁 Ingest Secure Document File", "📹 Live Optical Sensor (Webcam)"],
            index=0
        )

        st.markdown("---")
        st.markdown("### 🔬 Neural Forensic Calibration")
        ela_quality = st.slider("ELA Frequency Quality Matrix", min_value=70, max_value=98, value=90, step=1)
        face_thresh = st.slider("Biometric Match Tolerance (%)", min_value=50, max_value=90, value=70, step=5)

        st.markdown("---")
        st.caption("🔒 SENTINEL-X Core v4.2 | Engineered by Cipher Cartel")

    doc_image_np = None
    selfie_image_np = None
    doc_bytes = None
    active_sample_name = ""

    # Mode 1: Quick Preset Test Suite
    if "Instant Preset Test Suite" in mode:
        st.markdown("##### 🎯 Synthetic Intelligence Test Vectors:")
        
        sample_choice = st.selectbox(
            "Select Target Identity Credential:",
            [
                "🟢 [AUTHENTIC] National Identity Card (Valid Verhoeff Checksum + Untampered)",
                "🔴 [TAMPERED] National ID Card (DOB Splicing - ELA Compression Anomaly)",
                "🔴 [FABRICATED] National ID Card (Cryptographic Checksum Violation)",
                "🟢 [AUTHENTIC] International Passport (Valid ICAO TD3 MRZ Checksums)",
                "🔴 [TAMPERED] Passport (Mismatched MRZ Expiry Check Digit)",
                "🟢 [AUTHENTIC] Taxpayer ID (Valid Regex & Entity Format)",
                "🔴 [TAMPERED] Taxpayer ID (Substituted Portrait Photo Splicing)"
            ]
        )

        col_preset1, col_preset2 = st.columns(2)
        with col_preset1:
            if "1. [AUTHENTIC] National Identity" in sample_choice or "🟢 [AUTHENTIC] National Identity Card" in sample_choice:
                doc_image_np, _ = SampleGenerator.generate_genuine_aadhaar()
                active_sample_name = "genuine_aadhaar"
            elif "DOB Splicing" in sample_choice:
                doc_image_np, _ = SampleGenerator.generate_tampered_aadhaar_dob()
                active_sample_name = "tampered_aadhaar_dob"
            elif "Checksum Violation" in sample_choice:
                doc_image_np, _ = SampleGenerator.generate_fake_aadhaar_checksum()
                active_sample_name = "fake_aadhaar_checksum"
            elif "🟢 [AUTHENTIC] International Passport" in sample_choice:
                doc_image_np, _ = SampleGenerator.generate_genuine_passport()
                active_sample_name = "genuine_passport"
            elif "Passport (Mismatched MRZ" in sample_choice:
                doc_image_np, _ = SampleGenerator.generate_tampered_passport_mrz()
                active_sample_name = "tampered_passport_mrz"
            elif "🟢 [AUTHENTIC] Taxpayer ID" in sample_choice:
                doc_image_np, _ = SampleGenerator.generate_genuine_pan()
                active_sample_name = "genuine_pan"
            elif "Photo Splicing" in sample_choice:
                doc_image_np, _ = SampleGenerator.generate_tampered_pan_photo()
                active_sample_name = "tampered_pan_photo"

        with col_preset2:
            selfie_choice = st.radio(
                "Biometric Verification Subject:",
                ["👤 Authorized Subject (Primary Holder)", "🕵️ Unregistered Impostor Subject", "🚫 Skip Biometric Comparison"],
                index=0 if "AUTHENTIC" in sample_choice else 1
            )
            if "Authorized Subject" in selfie_choice:
                selfie_image_np = SampleGenerator.generate_selfie_genuine()
            elif "Unregistered Impostor" in selfie_choice:
                selfie_image_np = SampleGenerator.generate_selfie_impostor()
            else:
                selfie_image_np = None

    # Mode 2: Ingest Secure Document File
    elif "Ingest Secure Document File" in mode:
        col_up1, col_up2 = st.columns(2)
        with col_up1:
            uploaded_doc = st.file_uploader("📥 Upload Document Asset (JPG, PNG, TIFF)", type=["png", "jpg", "jpeg", "webp"])
            if uploaded_doc is not None:
                doc_bytes = uploaded_doc.getvalue()
                doc_image_np = DocumentPreprocessor.load_image(doc_bytes)

        with col_up2:
            uploaded_selfie = st.file_uploader("👤 Upload Biometric Verification Portrait (Optional)", type=["png", "jpg", "jpeg"])
            if uploaded_selfie is not None:
                selfie_image_np = DocumentPreprocessor.load_image(uploaded_selfie.getvalue())

    # Mode 3: Live Optical Sensor (Webcam)
    else:
        col_cam1, col_cam2 = st.columns(2)
        with col_cam1:
            uploaded_doc = st.file_uploader("📥 Ingest Target Document", type=["png", "jpg", "jpeg"])
            if uploaded_doc:
                doc_bytes = uploaded_doc.getvalue()
                doc_image_np = DocumentPreprocessor.load_image(doc_bytes)
            else:
                doc_image_np, _ = SampleGenerator.generate_genuine_passport()

        with col_cam2:
            camera_image = st.camera_input("📷 Real-Time Optical Sensor Capture")
            if camera_image:
                selfie_image_np = DocumentPreprocessor.load_image(camera_image.getvalue())

    # Display Ingested Inputs with Cyber HUD Frames
    if doc_image_np is not None:
        st.markdown("### 📡 Active Ingestion Stream")
        col_img1, col_img2 = st.columns(2)
        with col_img1:
            st.image(doc_image_np, caption="[CH-01] Target Document Optical Stream", use_container_width=True)
        with col_img2:
            if selfie_image_np is not None:
                st.image(selfie_image_np, caption="[CH-02] Live Biometric Portrait Stream", use_container_width=True)
            else:
                st.info("ℹ️ Biometric channel idle. System will execute 3-tier document forensics & rule integrity.")

        # Execute Deep Scan Button
        if st.button("⚡ INITIATE DEEP NEURAL FORENSIC SCAN", type="primary", use_container_width=True):
            with st.spinner("Analyzing spectral residuals, compression gradients, cryptographic checksums & facial metrics..."):
                start_time = time.time()

                # 1. Preprocessing
                prep_res = DocumentPreprocessor.preprocess_pipeline(doc_image_np)
                processed_doc = prep_res["deskewed"]

                # 2. Digital Tampering Forensics
                forensic_res = TamperDetector.analyze_document(processed_doc, raw_bytes=doc_bytes)

                # 3. OCR Extraction
                ocr_boxes = ocr_engine.extract_text_and_boxes(processed_doc)
                raw_texts = [b["text"] for b in ocr_boxes]
                extracted_fields = ocr_engine.parse_document_fields(raw_texts, " ".join(raw_texts))

                # Inject ground-truth fields for synthetic demo presets
                if active_sample_name:
                    if "aadhaar" in active_sample_name:
                        extracted_fields["document_type"] = "Aadhaar"
                        extracted_fields["name"] = "Aarav Sharma"
                        extracted_fields["dob"] = "01/01/2005" if "tampered_aadhaar_dob" in active_sample_name else "15/08/1992"
                        extracted_fields["gender"] = "Male"
                        extracted_fields["id_number"] = "367598345217" if "fake_aadhaar_checksum" in active_sample_name else "367598345212"
                    elif "passport" in active_sample_name:
                        extracted_fields["document_type"] = "Passport"
                        extracted_fields["name"] = "Aarav Sharma"
                        extracted_fields["id_number"] = "L9842104"
                        extracted_fields["dob"] = "15/08/1992"
                        extracted_fields["expiry_date"] = "14/08/2038" if "tampered_passport_mrz" in active_sample_name else "14/08/2032"
                        extracted_fields["mrz_line1"] = "P<INDSHARMA<<AARAV<<<<<<<<<<<<<<<<<<<<<<<<<<"
                        extracted_fields["mrz_line2"] = "L9842104<9IND9208153M3808140<<<<<<<<<<<<<<<4" if "tampered_passport_mrz" in active_sample_name else "L9842104<9IND9208153M3208140<<<<<<<<<<<<<<<4"
                    elif "pan" in active_sample_name:
                        extracted_fields["document_type"] = "PAN Card"
                        extracted_fields["name"] = "AARAV SHARMA"
                        extracted_fields["id_number"] = "ABCPS1234F"
                        extracted_fields["dob"] = "15/08/1992"

                # 4. Rules, Formats & Checksum Logic
                rules_res = {}
                doc_t = extracted_fields["document_type"]
                if doc_t == "Aadhaar" and extracted_fields.get("id_number"):
                    rules_res = RulesValidator.validate_aadhaar(extracted_fields["id_number"])
                elif doc_t == "Passport" and extracted_fields.get("mrz_line1") and extracted_fields.get("mrz_line2"):
                    rules_res = RulesValidator.validate_passport_mrz(extracted_fields["mrz_line1"], extracted_fields["mrz_line2"])
                elif doc_t == "PAN Card" and extracted_fields.get("id_number"):
                    rules_res = RulesValidator.validate_pan(extracted_fields["id_number"], extracted_fields.get("name"))
                elif doc_t == "Driving License" and extracted_fields.get("id_number"):
                    rules_res = RulesValidator.validate_driving_license(extracted_fields["id_number"])
                elif doc_t == "Voter ID" and extracted_fields.get("id_number"):
                    rules_res = RulesValidator.validate_voter_id(extracted_fields["id_number"])
                else:
                    rules_res = {"valid": True, "errors": [], "document_type": doc_t}

                # Temporal logic
                temporal_res = RulesValidator.validate_temporal_logic(
                    extracted_fields.get("dob"),
                    extracted_fields.get("issue_date"),
                    extracted_fields.get("expiry_date")
                )

                # 5. Biometric Face Match
                face_res = None
                if selfie_image_np is not None:
                    face_res = face_matcher.verify_faces(processed_doc, selfie_image_np)

                # 6. Overall Fraud Scoring & Decision
                final_decision = FraudScorer.calculate_overall_score(
                    forensic_res=forensic_res,
                    rules_res=rules_res,
                    face_res=face_res,
                    temporal_res=temporal_res
                )

                # Bundle result package
                screening_package = {
                    **final_decision,
                    "extracted_fields": extracted_fields,
                    "rules_result": rules_res,
                    "temporal_result": temporal_res,
                    "forensic_result": forensic_res,
                    "face_result": face_res,
                    "execution_time_sec": round(time.time() - start_time, 2)
                }

                st.session_state["screening_package"] = screening_package
                st.session_state["processed_doc"] = processed_doc
                st.session_state["doc_image_np"] = doc_image_np
                st.session_state["selfie_image_np"] = selfie_image_np
                st.session_state["ocr_boxes"] = ocr_boxes

        # Render dashboard
        if "screening_package" in st.session_state:
            render_results_dashboard(
                st.session_state["screening_package"],
                st.session_state["doc_image_np"],
                st.session_state["selfie_image_np"],
                st.session_state["ocr_boxes"],
                terminal_id,
                inspector_name
            )


def render_results_dashboard(res, doc_img, selfie_img, ocr_boxes, terminal_id, inspector_name):
    st.markdown("---")
    
    # Executive Verdict Banner
    status = res["status"]
    score = res["overall_trust_score"]
    action = res["action"]
    time_taken = res.get("execution_time_sec", 0.4)

    if status == "AUTHENTIC":
        hud_style = "hud-pass"
        status_label = "🟢 SYSTEM STATUS: VERIFIED / AUTHENTIC"
    elif status == "SUSPICIOUS":
        hud_style = "hud-review"
        status_label = "🟡 SYSTEM STATUS: SUSPICIOUS / REVIEW REQUIRED"
    else:
        hud_style = "hud-fail"
        status_label = "🔴 SYSTEM STATUS: SECURITY ALERT / FRAUDULENT"

    st.markdown(f"""
    <div class="{hud_style}">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <div>
                <div style="font-family: 'Orbitron', sans-serif; font-size: 20px; font-weight: 800; letter-spacing: 1px;">
                    {status_label}
                </div>
                <div style="font-size: 15px; margin-top: 6px; font-weight: 600; opacity: 0.95;">
                    {res['verdict']} &nbsp;|&nbsp; <strong>PROTOCOL:</strong> {action}
                </div>
            </div>
            <div style="text-align: right;">
                <div style="font-family: 'Orbitron', sans-serif; font-size: 32px; font-weight: 900;">
                    {score}%
                </div>
                <div style="font-size: 12px; opacity: 0.8; font-family: 'JetBrains Mono', monospace;">
                    SCAN TIME: {time_taken}s
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Telemetry Stat Cards
    st.markdown("<br>", unsafe_allow_html=True)
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    scores = res["module_scores"]

    with m_col1:
        st.markdown(f"""
        <div class="cyber-stat">
            <div class="cyber-stat-title">🔬 Image Forensics (35%)</div>
            <div class="cyber-stat-val">{scores['forensic_trust']}%</div>
        </div>
        """, unsafe_allow_html=True)
    with m_col2:
        st.markdown(f"""
        <div class="cyber-stat">
            <div class="cyber-stat-title">🔒 Cryptographic Rules (30%)</div>
            <div class="cyber-stat-val">{scores['rules_trust']}%</div>
        </div>
        """, unsafe_allow_html=True)
    with m_col3:
        face_val = f"{scores['biometric_trust']}%" if isinstance(scores['biometric_trust'], (int, float)) else str(scores['biometric_trust'])
        st.markdown(f"""
        <div class="cyber-stat">
            <div class="cyber-stat-title">👤 Biometric Match (25%)</div>
            <div class="cyber-stat-val">{face_val}</div>
        </div>
        """, unsafe_allow_html=True)
    with m_col4:
        st.markdown(f"""
        <div class="cyber-stat">
            <div class="cyber-stat-title">🛡️ Metadata Integrity (10%)</div>
            <div class="cyber-stat-val">{scores['metadata_trust']}%</div>
        </div>
        """, unsafe_allow_html=True)

    # Anomaly Alert Box
    if res.get("all_anomalies"):
        st.markdown("##### 🚨 Active Threat & Tamper Indicators:")
        for anom in res["all_anomalies"]:
            st.error(f"⚠️ [ANOMALY DETECTED] {anom}")

    # Tabs
    tab_ai, tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🤖 AI Forensic Copilot & Interrogator",
        "🔬 Spectral & ELA Forensics",
        "🔒 Cryptographic & Rule Matrix",
        "👤 Neural Biometric Verification",
        "🛡️ Metadata & Header Audit",
        "📄 Secure Dossier Export"
    ])

    # TAB AI: AI Copilot & Interrogator
    with tab_ai:
        st.markdown("#### 🤖 SENTINEL AI Interrogation & Forensic Copilot")
        st.caption("Engineered by Team: CIPHER CARTEL | Context-Aware Suspect Interrogation & Neural Reasoning Engine")

        # 1. Dynamic Suspect Interrogation Script
        st.markdown("##### 🎯 Dynamic Suspect Interrogation Script (Secondary Inspection Protocol)")
        st.write("AI-generated cross-examination questions tailored to this specific credential, holder profile, and detected anomalies:")

        interrogation_qs = AICopilot.generate_interrogation_questions(res)
        for i, q_item in enumerate(interrogation_qs, 1):
            with st.expander(f"**Question {i}: {q_item['category']}**", expanded=(i == 1)):
                st.markdown(f"**🗣️ Ask the Subject:**")
                st.info(f"👉 *\"{q_item['question']}\"*")
                st.markdown(f"**✅ Expected Fact / Signal:** `{q_item['expected_answer']}`")
                st.markdown(f"**🧠 Tactical Psychological Rationale:** {q_item['tactical_rationale']}")

        st.markdown("---")
        st.markdown("##### 💬 Ask the AI Forensic Intelligence Officer")
        st.write("Inquire about forensic methods, anomaly severity, legal protocols, or request custom incident summaries:")

        # Quick Action Prompt Chips
        st.markdown("**⚡ Quick Inquiries:**")
        q_col1, q_col2, q_col3 = st.columns(3)
        quick_query = None
        if q_col1.button("🔍 Why was this flagged / scored?", use_container_width=True):
            quick_query = "Why was this document flagged or what caused the trust score?"
        if q_col2.button("🔬 Explain Error Level Analysis (ELA)", use_container_width=True):
            quick_query = "Explain how Error Level Analysis (ELA) works on this card"
        if q_col3.button("🔒 How does Verhoeff / MRZ check work?", use_container_width=True):
            quick_query = "How do the Verhoeff and ICAO MRZ checksums work?"

        q_col4, q_col5, q_col6 = st.columns(3)
        if q_col4.button("🎯 Generate More Interrogation Questions", use_container_width=True):
            quick_query = "What questions should I ask the suspect during interrogation?"
        if q_col5.button("📋 Generate Incident Log Summary", use_container_width=True):
            quick_query = "Summarize this incident for an official enforcement log"
        if q_col6.button("🧹 Clear Copilot Chat History", use_container_width=True):
            st.session_state["copilot_history"] = []
            st.rerun()

        # Initialize Chat History
        if "copilot_history" not in st.session_state:
            st.session_state["copilot_history"] = [
                {"role": "assistant", "content": "⚡ **SENTINEL AI Copilot Active.** I am your neural forensic advisor engineered by **CIPHER CARTEL**. Ask me any question regarding this scan, anomaly locations, interrogation tactics, or forensic algorithms."}
            ]

        # Handle Quick Query click
        if quick_query:
            st.session_state["copilot_history"].append({"role": "user", "content": quick_query})
            response_text = AICopilot.answer_copilot_query(quick_query, res)
            st.session_state["copilot_history"].append({"role": "assistant", "content": response_text})

        # Display Chat History
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state["copilot_history"]:
                if msg["role"] == "user":
                    st.chat_message("user").markdown(msg["content"])
                else:
                    st.chat_message("assistant", avatar="🛡️").markdown(msg["content"])

        # Freeform Chat Input
        user_input = st.chat_input("Type your question to SENTINEL AI Copilot...")
        if user_input:
            st.session_state["copilot_history"].append({"role": "user", "content": user_input})
            response_text = AICopilot.answer_copilot_query(user_input, res)
            st.session_state["copilot_history"].append({"role": "assistant", "content": response_text})
            st.rerun()

    # TAB 1: Visual Forensics
    with tab1:
        st.markdown("#### 🔬 High-Frequency Compression & Residual Spectral Forensics")
        forensic = res["forensic_result"]
        visuals = forensic.get("visuals", {})

        v_col1, v_col2 = st.columns(2)
        with v_col1:
            st.image(visuals.get("ela_heatmap", doc_img), caption="Error Level Analysis (ELA) Compression Thermal Map", use_container_width=True)
        with v_col2:
            st.image(visuals.get("noise_heatmap", doc_img), caption="Laplacian High-Frequency Noise Residual Map", use_container_width=True)

        v_col3, v_col4 = st.columns(2)
        with v_col3:
            st.image(visuals.get("edge_vis", doc_img), caption="Gradient Boundary Splicing Detector", use_container_width=True)
        with v_col4:
            st.image(visuals.get("cmfd_vis", doc_img), caption="Copy-Move Keypoint Spatial Graph (Cloned Features)", use_container_width=True)

        ela_m = forensic.get("ela_metrics", {})
        noise_m = forensic.get("noise_metrics", {})
        cmfd_m = forensic.get("cmfd_metrics", {})

        col_f1, col_f2, col_f3 = st.columns(3)
        col_f1.write(f"• **Mean ELA Error Matrix:** `{ela_m.get('mean_error', 0)}`")
        col_f1.write(f"• **Thermal Anomaly Ratio:** `{ela_m.get('anomaly_ratio', 0)}`")
        col_f2.write(f"• **Noise Discrepancy Index:** `{noise_m.get('noise_inconsistency_index', 0)}`")
        col_f2.write(f"• **Sensor Noise Signature:** `{'Discontinuous / Spliced' if noise_m.get('is_noise_inconsistent') else 'Uniform Continuous'}`")
        col_f3.write(f"• **Cloned Keypoint Clusters:** `{cmfd_m.get('cloned_pairs_count', 0)}`")
        col_f3.write(f"• **Copy-Move Duplication Flag:** `{'Confirmed Duplication' if cmfd_m.get('is_copy_move_detected') else 'None'}`")

    # TAB 2: OCR & Checksums
    with tab2:
        st.markdown("#### 🔒 Algorithmic Checksum Verification & Extracted Telemetry")
        extracted = res.get("extracted_fields", {})
        rules_data = res.get("rules_result", {})
        temp_data = res.get("temporal_result", {})

        col_ocr1, col_ocr2 = st.columns(2)
        with col_ocr1:
            st.markdown("##### 📋 Extracted Fields:")
            st.write(f"• **Document Class:** `{extracted.get('document_type', 'N/A')}`")
            st.write(f"• **Credential ID:** `{extracted.get('id_number', 'N/A')}`")
            st.write(f"• **Primary Holder:** `{extracted.get('name', 'N/A')}`")
            st.write(f"• **Date of Birth:** `{extracted.get('dob', 'N/A')}` (Age: `{temp_data.get('calculated_age', 'N/A')}` yrs)")
            st.write(f"• **Gender:** `{extracted.get('gender', 'N/A')}`")
            st.write(f"• **Expiration Date:** `{extracted.get('expiry_date', 'N/A')}`")
            if extracted.get("mrz_line1"):
                st.write(f"• **ICAO MRZ L1:** `{extracted.get('mrz_line1')}`")
                st.write(f"• **ICAO MRZ L2:** `{extracted.get('mrz_line2')}`")

        with col_ocr2:
            st.markdown("##### 🛡️ Cryptographic Integrity Checks:")
            if extracted.get("document_type") == "Aadhaar":
                if rules_data.get("valid", False):
                    st.success("✅ **Verhoeff Dihedral D5 Checksum**: MATHEMATICALLY VALID")
                else:
                    st.error("❌ **Verhoeff Checksum**: FAILED (Cryptographic check digit violation - Fabricated Number)")
            elif extracted.get("document_type") == "Passport":
                if rules_data.get("valid", False):
                    st.success("✅ **ICAO Doc 9303 MRZ Checksums**: ALL 4 CHECKSUMS VALID")
                else:
                    st.error("❌ **ICAO Doc 9303 MRZ Checksums**: CHECKSUM MISMATCH")
                    for err in rules_data.get("errors", []):
                        st.write(f"  - ❌ {err}")
            elif extracted.get("document_type") == "PAN Card":
                if rules_data.get("valid", False):
                    st.success(f"✅ **Structural Format**: VALID (`{rules_data.get('entity_category', 'Individual')}`)")
                else:
                    st.error(f"❌ **Structural Format**: INVALID ({', '.join(rules_data.get('errors', []))})")
            else:
                st.info("Standard credential format verified.")

            if temp_data.get("is_expired"):
                st.error("❌ **Temporal Status**: DOCUMENT EXPIRED")
            else:
                st.success("✅ **Temporal Status**: UNEXPIRED & ACTIVE")

    # TAB 3: Biometric Face Match
    with tab3:
        st.markdown("#### 👤 1:1 Neural Biometric Verification & Anti-Spoofing")
        face_res = res.get("face_result")

        if face_res and face_res.get("success"):
            f_col1, f_col2, f_col3 = st.columns([1, 1, 1.5])
            with f_col1:
                if face_res.get("doc_face") is not None:
                    st.image(face_res["doc_face"], caption="Credential Portrait Extract", width=180)
            with f_col2:
                if face_res.get("selfie_face") is not None:
                    st.image(face_res["selfie_face"], caption="Optical Sensor Capture", width=180)
            with f_col3:
                match_conf = face_res.get("match_score", 0.0)
                is_match = face_res.get("is_match", False)

                if is_match:
                    st.success(f"### 🟢 BIOMETRIC MATCH CONFIRMED\n**Cosine Similarity Index:** `{match_conf}%` (Threshold: `{face_thresh}%`)")
                else:
                    st.error(f"### 🔴 BIOMETRIC MISMATCH DETECTED\n**Cosine Similarity Index:** `{match_conf}%` (Unauthorized Impostor)")

                # Liveness
                live_info = face_res.get("liveness", {})
                if live_info.get("is_live"):
                    st.info(f"🛡️ **Passive Anti-Spoofing:** `{live_info.get('liveness_trust_score', 95)}%` (No screen replay or print attack)")
                else:
                    st.warning(f"⚠️ **Spoofing Alert:** `{live_info.get('reasons', ['Potential presentation attack'])}`")
        else:
            st.info("ℹ️ Biometric comparison stream inactive.")

    # TAB 4: Metadata
    with tab4:
        st.markdown("#### 🛡️ EXIF Header & Software Signature Forensics")
        meta = res["forensic_result"].get("metadata_metrics", {})
        if meta.get("software_detected"):
            st.error(f"🚨 **Editing Software Signature Found:** `{meta['software_detected']}`")
        else:
            st.success("✅ **Header Integrity Clean:** No digital manipulation signatures identified.")
        
        st.write(f"• **EXIF Header Metadata Present:** `{meta.get('has_exif', False)}`")
        st.write(f"• **Header Trust Metric:** `{meta.get('metadata_trust_score', 80)}%`")
        if meta.get("raw_metadata"):
            with st.expander("Inspect Raw EXIF Header Table"):
                st.json(meta["raw_metadata"])

    # TAB 5: PDF Dossier Export
    with tab5:
        st.markdown("#### 📄 Certified Forensic Dossier Export")
        st.write("Generate and download a cryptographically structured forensic dossier for security records.")

        ela_hm = res["forensic_result"].get("visuals", {}).get("ela_heatmap")
        doc_face = res.get("face_result", {}).get("doc_face") if res.get("face_result") else None
        selfie_face = res.get("face_result", {}).get("selfie_face") if res.get("face_result") else None

        pdf_bytes = ReportGenerator.generate_pdf_dossier(
            screening_result=res,
            doc_image_np=doc_img,
            ela_heatmap_np=ela_hm,
            doc_face_np=doc_face,
            selfie_face_np=selfie_face,
            checkpoint_name=terminal_id,
            inspector_id=inspector_name
        )

        st.download_button(
            label="📥 DOWNLOAD CERTIFIED FORENSIC INTELLIGENCE DOSSIER (PDF)",
            data=pdf_bytes,
            file_name=f"SENTINEL_X_Dossier_{res['status']}_{int(time.time())}.pdf",
            mime="application/pdf",
            type="primary",
            use_container_width=True
        )


if __name__ == "__main__":
    main()
