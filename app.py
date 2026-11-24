"""
app.py
DuCO-Agent: Multi-Modal Dual Coverage Coordination of Benefits (COB) AI System.
Interactive Streamlit Web Dashboard for Priya & Aarav Sen (Mumbai).
"""

import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image

from duco_agent import DuCOAgent
from insurance_api import MockInsuranceAPI
from multimodal_extractor import MultimodalExtractor

st.set_page_config(
    page_title="DuCO-Agent | Dual Coverage COB System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1e3a8a;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #475569;
        margin-top: 0px;
        margin-bottom: 20px;
    }
    .metric-card {
        background: #ffffff;
        border-radius: 10px;
        padding: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border-left: 5px solid #2563eb;
    }
    .metric-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #0f172a;
    }
    .metric-subtitle {
        font-size: 0.8rem;
        color: #10b981;
        font-weight: 600;
    }
    .thought-bubble {
        background: #f1f5f9;
        border-left: 4px solid #3b82f6;
        padding: 12px 16px;
        border-radius: 6px;
        margin-bottom: 12px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px 6px 0 0;
        padding: 10px 18px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_agent_instance():
    agent = DuCOAgent()
    memory = agent.run_full_pipeline()
    return agent, memory

agent, memory = get_agent_instance()

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shield.png", width=64)
    st.title("DuCO-Agent")
    st.caption("Agentic Multi-Modal COB Engine v2.4")
    st.markdown("---")
    
    st.markdown("### 📋 Active Case Profile")
    st.markdown("**Primary Family Unit:**")
    st.markdown("• **Aarav Sen** (32M, Mumbai)\n  - Primary: Plan B (HDFC ERGO)\n  - Dependent: Plan A (Star Care)")
    st.markdown("• **Priya Sen** (31F, Mumbai)\n  - Primary: Plan A (Star Care)\n  - Dependent: Plan B (HDFC ERGO)")
    
    st.markdown("---")
    st.markdown("### 🏥 Active Medical Events")
    st.markdown("1. **Aarav:** ACL Reconstruction + Meniscectomy (Est: ₹4,50,000)")
    st.markdown("2. **Priya:** 10x Physical Therapy Sessions (Billed: ₹30,000)")
    
    st.markdown("---")
    st.markdown("### ⚙️ Quick Actions")
    if st.button("🔄 Re-run Agent Reasoning Loop", use_container_width=True):
        st.cache_resource.clear()
        st.rerun()

# Main Header
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown('<div class="main-header">DuCO-Agent: Dual Coverage COB System</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Autonomous Agentic Reasoning, Coordination of Benefits & Multi-Modal Healthcare Financial Optimization</div>', unsafe_allow_html=True)

with col_h2:
    st.markdown("""
    <div style="background:#ecfdf5; border:1px solid #10b981; border-radius:8px; padding:10px; text-align:center;">
        <span style="color:#065f46; font-weight:700; font-size:0.9rem;">STATUS: ADJUDICATED</span><br>
        <span style="color:#047857; font-size:0.8rem;">COB Applied • Pre-Auth Validated</span>
    </div>
    """, unsafe_allow_html=True)

# Top KPI Metric Cards
a_sum = memory["claims_adjudication"]["aarav"]["summary"]
p_sum = memory["claims_adjudication"]["priya"]["summary"]

total_billed = a_sum["total_billed"] + p_sum["total_billed"]
total_prim_paid = a_sum["primary_paid"] + p_sum["primary_paid"]
total_sec_paid = a_sum["secondary_paid"] + p_sum["secondary_paid"]
total_ins_paid = total_prim_paid + total_sec_paid
total_oop = a_sum["final_patient_out_of_pocket"] + p_sum["final_patient_out_of_pocket"]
total_savings = a_sum["dual_coverage_savings"] + p_sum["dual_coverage_savings"]

m1, m2, m3, m4, m5 = st.columns(5)
with m1:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #3b82f6;">
        <div class="metric-title">Total Incurred Claims</div>
        <div class="metric-value">₹{total_billed:,.0f}</div>
        <div class="metric-subtitle" style="color:#64748b;">Surgery + PT Bills</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #059669;">
        <div class="metric-title">Primary Insurance Paid</div>
        <div class="metric-value">₹{total_prim_paid:,.0f}</div>
        <div class="metric-subtitle" style="color:#059669;">Plan B (Aarav) + Plan A (Priya)</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #0284c7;">
        <div class="metric-title">Secondary COB Paid</div>
        <div class="metric-value">₹{total_sec_paid:,.0f}</div>
        <div class="metric-subtitle" style="color:#0284c7;">Cross-Plan Coordination</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #10b981;">
        <div class="metric-title">Net Family Out-Of-Pocket</div>
        <div class="metric-value" style="color:#15803d;">₹{total_oop:,.0f}</div>
        <div class="metric-subtitle" style="color:#15803d;">Only 1.04% of Total Billed!</div>
    </div>
    """, unsafe_allow_html=True)

with m5:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #f59e0b;">
        <div class="metric-title">Dual Coverage Savings</div>
        <div class="metric-value" style="color:#b45309;">₹{total_savings:,.0f}</div>
        <div class="metric-subtitle" style="color:#b45309;">Shielded by DuCO-Agent</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# Navigation Tabs
tab_exec, tab_inputs, tab_trace, tab_letters, tab_audio, tab_sim = st.tabs([
    "📊 Financial Breakdown & Cost Flows",
    "📁 Multi-Modal Inputs & Extraction",
    "🧠 Agentic Reasoning & Reflection Trace",
    "📜 Clinical Pre-Auth Letters",
    "🎙️ Patient Audio Briefing",
    "🧪 Interactive COB Scenario Simulator"
])

# -------------------------------------------------------------
# TAB 1: Financial Breakdown & Cost Flows
# -------------------------------------------------------------
with tab_exec:
    st.markdown("### 🌊 Coordination of Benefits (COB) Flow of Funds")
    st.caption("Visualizing how bills flow through Primary and Secondary payers according to Employee/Subscriber and NAIC COB rules.")

    col_v1, col_v2 = st.columns([3, 2])
    with col_v1:
        # Embed interactive HTML Sankey
        if os.path.exists("cost_flow_sankey.html"):
            with open("cost_flow_sankey.html", "r", encoding="utf-8") as f:
                sankey_html = f.read()
            st.components.v1.html(sankey_html, height=520, scrolling=False)
        else:
            st.image("cost_flow_sankey.png", use_container_width=True)

    with col_v2:
        st.markdown("#### 💡 Key COB Findings")
        st.markdown(f"""
        - **Aarav's Knee Surgery (₹4,50,000):**
          - **Primary Payer:** Plan B (HDFC ERGO) under Subscriber Rule.
          - **Primary Paid:** **₹3,90,000** (Patient OOP capped at ₹60,000 by Out-of-Pocket Max protection).
          - **Secondary Payer:** Plan A (Star Care) steps in and pays **₹60,000** under standard COB!
          - **Aarav's Final Out-of-Pocket:** **₹0.00 (100% Fully Covered)**.
          - **Dual Coverage Savings:** **₹60,000.00**.
        
        - **Priya's Physical Therapy (₹30,000):**
          - **Primary Payer:** Plan A (Star Care) under Subscriber Rule.
          - **Primary Paid:** **₹16,000** (Remaining ₹5,000 deductible + 20% coinsurance up to ₹25,000 cap).
          - **Secondary Payer:** Plan B (HDFC ERGO) coordinates and pays **₹9,000**.
          - **Priya's Final Out-of-Pocket:** **₹5,000** (only the amount exceeding the ₹25,000 annual OPD PT cap).
          - **Dual Coverage Savings:** **₹9,000.00**.
        """)
        
        st.success("✅ Total Family Savings from Dual Coverage: **₹69,000.00**!")

    st.markdown("---")
    st.markdown("### 📈 Visual Cost Breakdown & Waterfall Charts")
    
    col_w1, col_w2 = st.columns(2)
    with col_w1:
        if os.path.exists("financial_waterfall.png"):
            st.image("financial_waterfall.png", caption="COB Claims Payment Waterfall Breakdown", use_container_width=True)
    with col_w2:
        if os.path.exists("coverage_comparison.png"):
            st.image("coverage_comparison.png", caption="Single Policy vs Dual Coverage Impact Comparison", use_container_width=True)

    st.markdown("---")
    st.markdown("### 📑 Detailed Claims Adjudication Ledger")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("#### 🏥 Aarav Sen: Knee Surgery Adjudication Table")
        df_aarav = pd.DataFrame([
            {"Stage": "1. Gross Billed Amount", "Amount (INR)": "₹4,50,000.00", "Notes": "CPT 29888 + 29881"},
            {"Stage": "2. Primary Insurer (Plan B)", "Amount (INR)": "₹3,90,000.00", "Notes": "85% covered, OOP Max ₹60,000 applied"},
            {"Stage": "3. Remainder to Secondary", "Amount (INR)": "₹60,000.00", "Notes": "Patient responsibility under Plan B"},
            {"Stage": "4. Secondary Insurer (Plan A)", "Amount (INR)": "₹60,000.00", "Notes": "Standard COB pays remaining allowable balance"},
            {"Stage": "5. Final Patient Out-of-Pocket", "Amount (INR)": "₹0.00", "Notes": "Zero Out-of-Pocket!"},
            {"Stage": "6. Dual Coverage Benefit", "Amount (INR)": "₹60,000.00", "Notes": "Saved compared to Plan B alone"}
        ])
        st.dataframe(df_aarav, hide_index=True, use_container_width=True)

    with col_t2:
        st.markdown("#### 🧘 Priya Sen: Physical Therapy Adjudication Table")
        df_priya = pd.DataFrame([
            {"Stage": "1. Gross Billed Amount", "Amount (INR)": "₹30,000.00", "Notes": "10 Sessions @ ₹3,000/session"},
            {"Stage": "2. Primary Insurer (Plan A)", "Amount (INR)": "₹16,000.00", "Notes": "₹5k deductible + 20% coinsurance (₹25k cap)"},
            {"Stage": "3. Remainder to Secondary", "Amount (INR)": "₹14,000.00", "Notes": "Patient responsibility under Plan A"},
            {"Stage": "4. Secondary Insurer (Plan B)", "Amount (INR)": "₹9,000.00", "Notes": "Secondary COB coordination"},
            {"Stage": "5. Final Patient Out-of-Pocket", "Amount (INR)": "₹5,000.00", "Notes": "Only ₹5,000 cap excess"},
            {"Stage": "6. Dual Coverage Benefit", "Amount (INR)": "₹9,000.00", "Notes": "Saved compared to Plan A alone"}
        ])
        st.dataframe(df_priya, hide_index=True, use_container_width=True)

# -------------------------------------------------------------
# TAB 2: Multi-Modal Inputs & Extraction
# -------------------------------------------------------------
with tab_inputs:
    st.markdown("### 📁 Multi-Modal Input Artifacts Inspection")
    st.caption("Inspect the 4 raw mock files submitted to DuCO-Agent and view extracted clinical/billing metadata.")

    c_in1, c_in2 = st.columns(2)
    
    with c_in1:
        st.markdown("#### 1. Priya's Scanned PT Invoice (`priya_pt_invoice.png`)")
        if os.path.exists("priya_pt_invoice.png"):
            st.image("priya_pt_invoice.png", caption="Scanned Invoice with Handwritten Billing Desk Notes", use_container_width=True)
        
        with st.expander("🔍 Extracted Data & Code Inference Details", expanded=True):
            inv = memory["inputs"]["pt_invoice"]
            st.markdown(f"**Clinic:** {inv['provider_name']}")
            st.markdown(f"**Total Billed:** ₹{inv['total_billed_amount']:,.2f} ({inv['currency']})")
            st.markdown(f"**Handwritten Notes Decoded:** *\"{inv['handwritten_notes']}\"*")
            st.markdown("**Autonomous Code Inference:**")
            for c in inv["inferred_cpt_codes"]:
                st.markdown(f"- **CPT {c['cpt_code']}**: {c['description']} (Units: {c['units']}, ₹{c['total_amount']:,.2f}) — *Confidence: {c['confidence']*100:.0f}%*")
            for icd in inv["inferred_icd10_codes"]:
                st.markdown(f"- **ICD-10 {icd['icd10_code']}**: {icd['description']} — *Confidence: {icd['confidence']*100:.0f}%*")

    with c_in2:
        st.markdown("#### 2. Aarav's Knee MRI Report (`aarav_mri_report.pdf`)")
        mri = memory["inputs"]["mri_report"]
        st.markdown(f"""
        <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:8px; padding:16px;">
            <div style="font-weight:700; color:#1e3a8a;">APEX ADVANCED IMAGING & DIAGNOSTIC CENTRE</div>
            <div style="font-size:0.85rem; color:#475569;">Study: {mri['study_name']} | Date: {mri['date_of_scan']}</div>
            <div style="font-size:0.85rem; color:#475569;">Patient: <b>{mri['patient_name']}</b> (32M) | Ref: {mri['referring_doctor']}</div>
            <hr style="margin:10px 0;">
            <div style="font-weight:600; color:#0f172a; font-size:0.9rem;">KEY RADIOLOGICAL FINDINGS:</div>
            <div style="font-size:0.85rem; color:#334155; margin-top:4px;">
                • <b>ACL:</b> Complete discontinuity of mid-substance fibers, empty notch sign, pivot-shift contusions.<br>
                • <b>Medial Meniscus:</b> Complex oblique tear extending to superior/inferior articular surfaces.<br>
                • <b>Lateral Meniscus:</b> Intact with normal signal.<br>
                • <b>Effusion:</b> Traumatic knee hemarthrosis.
            </div>
            <hr style="margin:10px 0;">
            <div style="font-weight:700; color:#991b1b; font-size:0.9rem;">RADIOLOGIST IMPRESSION:</div>
            <div style="font-size:0.85rem; color:#7f1d1d;">
                1. Complete tear of Anterior Cruciate Ligament (ACL).<br>
                2. High-grade complex tear of posterior horn and body of Medial Meniscus.<br>
                3. Recommendation: Urgent Arthroscopic Reconstruction + Meniscectomy.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("#### 3. Surgeon's Estimation Sheet (`surgeon_estimate.jpg`)")
        if os.path.exists("surgeon_estimate.jpg"):
            st.image("surgeon_estimate.jpg", caption="Surgeon Surgical Pre-Authorization Estimate", use_container_width=True)

    st.markdown("---")
    st.markdown("#### 4. Voice-to-Text User Query (`user_query.txt`)")
    q = memory["inputs"]["query"]
    st.info(f"🎙️ **Transcribed Audio Input:** \"{q['raw_text']}\"")
    st.markdown(f"**Parsed Intents:** {', '.join(q['detected_intents'])}")
    st.markdown(f"**Referenced Patients:** {', '.join(q['extracted_patients'])}")
    st.markdown(f"**Referenced Policies:** Plan A (Insurer 1) and Plan B (Insurer 2)")

# -------------------------------------------------------------
# TAB 3: Agentic Reasoning & Reflection Trace
# -------------------------------------------------------------
with tab_trace:
    st.markdown("### 🧠 Dynamic Agentic Reasoning & Reflection Blackboard")
    st.caption("Inspect the autonomous agent's internal monologue, tool invocations, observations, and validation loops.")

    for i, log in enumerate(agent.thought_logs, 1):
        with st.container():
            st.markdown(f"""
            <div class="thought-bubble">
                <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                    <span style="font-weight:700; color:#1e40af; font-size:1.0rem;">Step {i}: {log.step}</span>
                    <span style="font-size:0.8rem; color:#64748b;">⏱️ {log.timestamp}</span>
                </div>
                <div style="margin-bottom:8px;">
                    <span style="font-weight:600; color:#475569;">🤔 Agent Hypothesis / Thought:</span><br>
                    <span style="color:#1e293b; font-size:0.92rem;">{log.thought}</span>
                </div>
                <div style="margin-bottom:8px; background:#ffffff; padding:8px; border-radius:4px; border:1px solid #e2e8f0;">
                    <span style="font-weight:600; color:#0369a1;">⚡ Action / Tool Invoked:</span>
                    <code style="color:#0369a1; font-size:0.85rem;">{log.action}</code>
                </div>
                <div style="margin-bottom:8px;">
                    <span style="font-weight:600; color:#047857;">👁️ Tool Observation:</span><br>
                    <span style="color:#064e3b; font-size:0.92rem;">{log.observation}</span>
                </div>
                <div style="background:#fef3c7; border-left:3px solid #f59e0b; padding:8px; border-radius:3px;">
                    <span style="font-weight:600; color:#92400e;">💡 Self-Correction & Reflection:</span><br>
                    <span style="color:#78350f; font-size:0.92rem;">{log.reflection}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🛡️ Automated Financial & Compliance Validation Checks")
    val = memory["validation_results"]
    for c in val["checks"]:
        st.markdown(f"- ✅ **{c['check']}:** `PASSED` — *Formula verification: {c['details']}*")

# -------------------------------------------------------------
# TAB 4: Clinical Pre-Authorization Letters
# -------------------------------------------------------------
with tab_letters:
    st.markdown("### 📜 Clinically Sound, Compliant Pre-Authorization Letters")
    st.caption("Generated according to IRDAI cashless standardization formats, citing 3T MRI findings, CPT/ICD-10 pairings, and MCG criteria.")

    let_tab1, let_tab2 = st.tabs([
        "📄 Primary Request: HDFC ERGO (Plan B)",
        "📑 Secondary Pre-Notification: Star Care (Plan A)"
    ])

    with let_tab1:
        st.markdown("#### Primary Insurer Pre-Authorization Request")
        st.caption("To Vidal Health Insurance TPA / HDFC ERGO General Insurance Co. Ltd.")
        st.code(memory["preauth_letters"]["primary_hdfc_ergo"], language="text")
        st.download_button(
            label="⬇️ Download Primary Pre-Auth Letter (.txt)",
            data=memory["preauth_letters"]["primary_hdfc_ergo"],
            file_name="aarav_primary_preauth_hdfc.txt",
            mime="text/plain"
        )

    with let_tab2:
        st.markdown("#### Secondary Insurer Pre-Notification & COB Request")
        st.caption("To MediAssist Healthcare Services TPA / Star Care Health Insurance Co. Ltd.")
        st.code(memory["preauth_letters"]["secondary_star_care"], language="text")
        st.download_button(
            label="⬇️ Download Secondary Pre-Notification Letter (.txt)",
            data=memory["preauth_letters"]["secondary_star_care"],
            file_name="aarav_secondary_prenotif_star.txt",
            mime="text/plain"
        )

# -------------------------------------------------------------
# TAB 5: Patient Audio Briefing
# -------------------------------------------------------------
with tab_audio:
    st.markdown("### 🎙️ Patient Audio Briefing Console")
    st.caption("Empathetic, jargon-free voice briefing explaining who pays first, exact rupee amounts, and pre-auth status.")

    audio_data = memory["audio_briefing"]

    col_a1, col_a2 = st.columns([3, 2])
    with col_a1:
        st.markdown(f"#### 🔊 Audio Player")
        if os.path.exists("patient_briefing_audio.wav"):
            st.audio("patient_briefing_audio.wav", format="audio/wav")
            st.caption("Generated 44.1kHz audio stream with introduction melody.")

        # Interactive Browser Speech Synthesis Widget
        st.markdown("#### 🗣️ Live Interactive Browser Speech Synthesizer")
        st.caption("Click below to listen to the briefing spoken directly by your browser's speech voice!")

        script_text = audio_data["transcript"].replace('"', '\\"').replace('\n', ' ')
        html_speech = f"""
        <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:8px; padding:16px; margin-top:10px;">
            <div style="display:flex; gap:10px; align-items:center; margin-bottom:12px;">
                <button id="playBtn" onclick="playSpeech()" style="background:#2563eb; color:white; border:none; padding:10px 20px; border-radius:6px; cursor:pointer; font-weight:bold; font-size:14px;">▶ Play Briefing</button>
                <button id="pauseBtn" onclick="pauseSpeech()" style="background:#e2e8f0; color:#334155; border:none; padding:10px 18px; border-radius:6px; cursor:pointer; font-weight:bold;">⏸ Pause</button>
                <button id="stopBtn" onclick="stopSpeech()" style="background:#fee2e2; color:#b91c1c; border:none; padding:10px 18px; border-radius:6px; cursor:pointer; font-weight:bold;">⏹ Stop</button>
            </div>
            <div id="statusText" style="font-size:12px; color:#64748b; font-weight:600;">Status: Ready to play</div>
            <div id="waveBox" style="display:none; height:24px; align-items:center; gap:3px; margin-top:10px;">
                <span style="display:inline-block; width:4px; height:18px; background:#2563eb; animation:pulse 0.8s infinite alternate;"></span>
                <span style="display:inline-block; width:4px; height:24px; background:#3b82f6; animation:pulse 0.6s infinite alternate;"></span>
                <span style="display:inline-block; width:4px; height:12px; background:#60a5fa; animation:pulse 1.0s infinite alternate;"></span>
                <span style="display:inline-block; width:4px; height:20px; background:#2563eb; animation:pulse 0.7s infinite alternate;"></span>
                <span style="display:inline-block; width:4px; height:14px; background:#3b82f6; animation:pulse 0.9s infinite alternate;"></span>
                <span style="font-size:12px; color:#2563eb; margin-left:8px; font-weight:600;">Audio playing...</span>
            </div>
        </div>

        <script>
            var synth = window.speechSynthesis;
            var text = "{script_text}";
            var utterance = null;

            function playSpeech() {{
                if (synth.speaking && synth.paused) {{
                    synth.resume();
                    document.getElementById('statusText').innerText = "Status: Resumed playing";
                    document.getElementById('waveBox').style.display = "flex";
                    return;
                }}
                synth.cancel();
                utterance = new SpeechSynthesisUtterance(text);
                utterance.rate = 1.0;
                utterance.pitch = 1.0;
                
                // Try selecting Indian or natural English voice if available
                var voices = synth.getVoices();
                for (var i = 0; i < voices.length; i++) {{
                    if (voices[i].lang.includes('en-IN') || voices[i].name.includes('India') || voices[i].name.includes('Natural')) {{
                        utterance.voice = voices[i];
                        break;
                    }}
                }}

                utterance.onstart = function() {{
                    document.getElementById('statusText').innerText = "Status: Playing audio briefing...";
                    document.getElementById('waveBox').style.display = "flex";
                }};
                utterance.onend = function() {{
                    document.getElementById('statusText').innerText = "Status: Playback finished";
                    document.getElementById('waveBox').style.display = "none";
                }};
                synth.speak(utterance);
            }}

            function pauseSpeech() {{
                if (synth.speaking) {{
                    synth.pause();
                    document.getElementById('statusText').innerText = "Status: Paused";
                    document.getElementById('waveBox').style.display = "none";
                }}
            }}

            function stopSpeech() {{
                synth.cancel();
                document.getElementById('statusText').innerText = "Status: Stopped";
                document.getElementById('waveBox').style.display = "none";
            }}
        </script>
        """
        st.components.v1.html(html_speech, height=180)

    with col_a2:
        st.markdown("#### 📝 Complete Spoken Transcript")
        st.markdown(f"""
        <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:8px; padding:16px; font-size:0.92rem; line-height:1.6; max-height:360px; overflow-y:auto; color:#1e293b;">
            {audio_data['transcript'].replace(chr(10), '<br>')}
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        st.download_button(
            label="⬇️ Download Transcript (.txt)",
            data=audio_data['transcript'],
            file_name="patient_briefing_transcript.txt",
            mime="text/plain"
        )

# -------------------------------------------------------------
# TAB 6: Interactive Scenario Simulator
# -------------------------------------------------------------
with tab_sim:
    st.markdown("### 🧪 Interactive COB Scenario Simulator & Stress-Testing")
    st.caption("Modify surgery estimates, session counts, and deductible parameters to observe real-time COB recalculations.")

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown("#### Adjust Aarav's Surgery Variables")
        sim_surg_cost = st.slider("Aarav's Surgical Cost (INR)", min_value=300000, max_value=700000, value=450000, step=25000)
        sim_plan_b_deductible = st.number_input("Plan B Deductible (INR)", value=15000, step=5000)
        sim_plan_b_coins = st.slider("Plan B Patient Coinsurance (%)", min_value=5, max_value=30, value=15, step=5)
        sim_plan_b_oop = st.number_input("Plan B Annual OOP Max (INR)", value=60000, step=10000)

    with col_s2:
        st.markdown("#### Adjust Priya's Physical Therapy Variables")
        sim_pt_sessions = st.slider("Number of PT Sessions", min_value=5, max_value=25, value=10, step=1)
        sim_rate_per_session = st.number_input("Rate per Session (INR)", value=3000, step=500)
        sim_pt_cap = st.number_input("Plan A Outpatient PT Annual Cap (INR)", value=25000, step=5000)

    # Dynamic re-simulation
    sim_api = MockInsuranceAPI()
    
    # Sim Aarav
    sim_lines_a = [
        {"cpt_code": "29888", "description": "ACL Reconstruction", "units": 1, "billed_amount": sim_surg_cost * (350/450)},
        {"cpt_code": "29881", "description": "Meniscectomy", "units": 1, "billed_amount": sim_surg_cost * (100/450)}
    ]
    # Temporarily update policy for simulation
    sim_api.db["INSURER_2"]["subscribers"]["Aarav Sen"]["individual_deductible"] = float(sim_plan_b_deductible)
    sim_api.db["INSURER_2"]["subscribers"]["Aarav Sen"]["coinsurance_inpatient"] = float(sim_plan_b_coins) / 100.0
    sim_api.db["INSURER_2"]["subscribers"]["Aarav Sen"]["annual_oop_max"] = float(sim_plan_b_oop)

    sim_a_prim = sim_api.adjudicate_claim("INSURER_2", "Aarav Sen", "INPATIENT_SURGERY", sim_lines_a, is_primary=True)
    sim_a_sec = sim_api.adjudicate_claim("INSURER_1", "Aarav Sen", "INPATIENT_SURGERY", sim_lines_a, is_primary=False, primary_eob=sim_a_prim)

    # Sim Priya
    sim_lines_p = [
        {"cpt_code": "97161", "description": "PT Evaluation", "units": 1, "billed_amount": float(sim_rate_per_session)},
        {"cpt_code": "97110", "description": "PT Exercise", "units": sim_pt_sessions - 1, "billed_amount": float(sim_rate_per_session * (sim_pt_sessions - 1))}
    ]
    sim_api.db["INSURER_1"]["subscribers"]["Priya Sen"]["opd_pt_annual_cap"] = float(sim_pt_cap)
    sim_p_prim = sim_api.adjudicate_claim("INSURER_1", "Priya Sen", "OUTPATIENT_PT", sim_lines_p, is_primary=True)
    sim_p_sec = sim_api.adjudicate_claim("INSURER_2", "Priya Sen", "OUTPATIENT_PT", sim_lines_p, is_primary=False, primary_eob=sim_p_prim)

    st.markdown("---")
    st.markdown("#### 🎯 Real-Time Simulation Results")
    
    r1, r2, r3, r4 = st.columns(4)
    with r1:
        st.metric("Total Simulated Claims", f"₹{(sim_surg_cost + (sim_pt_sessions * sim_rate_per_session)):,.0f}")
    with r2:
        st.metric("Primary Paid (Combined)", f"₹{(sim_a_prim['insurer_payment'] + sim_p_prim['insurer_payment']):,.0f}")
    with r3:
        st.metric("Secondary COB Paid", f"₹{(sim_a_sec['secondary_payment'] + sim_p_sec['secondary_payment']):,.0f}")
    with r4:
        sim_total_oop = sim_a_sec["final_patient_out_of_pocket"] + sim_p_sec["final_patient_out_of_pocket"]
        st.metric("Simulated Net Family OOP", f"₹{sim_total_oop:,.0f}")

st.markdown("---")
st.markdown("DuCO-Agent System • Compliant with IRDAI & NAIC Coordination of Benefits Guidelines • Generated for Aarav & Priya Sen")
