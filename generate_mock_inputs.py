"""
generate_mock_inputs.py
Generates the 4 multi-modal input files required for the DuCO-Agent system:
1. priya_pt_invoice.png (scanned crumpled clinic invoice with handwritten notes)
2. aarav_mri_report.pdf (knee MRI radiology diagnostic report)
3. surgeon_estimate.jpg (surgeon's surgical cost estimate sheet)
4. user_query.txt (Aarav's voice-to-text transcription)
"""

import os
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def create_priya_pt_invoice():
    # Width and height for an A4-like image at ~150 DPI
    width, height = 1240, 1600
    img = Image.new("RGB", (width, height), color=(250, 249, 245))
    draw = ImageDraw.Draw(img)

    # Add slight paper aging/noise
    # Draw border
    draw.rectangle([(20, 20), (width - 20, height - 20)], outline=(210, 205, 195), width=2)

    # Header
    draw.rectangle([(40, 40), (width - 40, 160)], fill=(235, 242, 250))
    # Title
    try:
        # Use default fonts if truetype not found
        font_header = ImageFont.load_default()
    except Exception:
        font_header = None

    # Header text
    draw.text((60, 60), "REHABILITATION & SPINE WELLNESS CLINIC", fill=(20, 50, 90))
    draw.text((60, 85), "Advanced Musculoskeletal & Post-Operative Physiotherapy Care", fill=(70, 80, 95))
    draw.text((60, 110), "Plot 42, Hill Road, Bandra West, Mumbai - 400050 | Ph: +91 22 2640 8899 | Reg: MH-MUM-PT-2019-88", fill=(100, 110, 120))

    # Invoice Meta
    draw.line([(40, 180), (width - 40, 180)], fill=(180, 180, 180), width=2)
    draw.text((60, 200), "PATIENT NAME: Mrs. Priya Sen", fill=(30, 30, 30))
    draw.text((60, 225), "AGE/GENDER: 31 Y / Female", fill=(50, 50, 50))
    draw.text((60, 250), "ADDRESS: Flat 802, Marina Bay Towers, Worli, Mumbai", fill=(50, 50, 50))
    draw.text((60, 275), "DIAGNOSIS: Chronic Lumbosacral Strain / Low Back Pain", fill=(50, 50, 50))

    draw.text((700, 200), "INVOICE NO: RSWC/2026/INV-1142", fill=(30, 30, 30))
    draw.text((700, 225), "INVOICE DATE: 18-Nov-2026", fill=(50, 50, 50))
    draw.text((700, 250), "PAYMENT STATUS: PENDING / UNPAID", fill=(180, 30, 30))
    draw.text((700, 275), "TREATMENT CYCLE: Oct 14, 2026 - Nov 16, 2026", fill=(50, 50, 50))

    # Table Header
    table_top = 320
    draw.rectangle([(40, table_top), (width - 40, table_top + 40)], fill=(220, 225, 230))
    draw.text((50, table_top + 10), "Date", fill=(20, 20, 20))
    draw.text((180, table_top + 10), "Clinical Service Description", fill=(20, 20, 20))
    draw.text((750, table_top + 10), "Sessions", fill=(20, 20, 20))
    draw.text((880, table_top + 10), "Rate (INR)", fill=(20, 20, 20))
    draw.text((1050, table_top + 10), "Total (INR)", fill=(20, 20, 20))

    # Items
    items = [
        ("14-Oct-2026", "Initial Physical Therapy Comprehensive Evaluation & Functional Assessment", "1", "3,000", "3,000"),
        ("18-Oct-2026", "Therapeutic Exercise & Lumbar Core Stabilization Protocol", "1", "3,000", "3,000"),
        ("22-Oct-2026", "Therapeutic Exercise & Manual Spinal Mobilization", "1", "3,000", "3,000"),
        ("26-Oct-2026", "Therapeutic Exercise & Deep Heat Ultrasound Diathermy", "1", "3,000", "3,000"),
        ("30-Oct-2026", "Spinal Decompression & Targeted Neuromuscular Re-education", "1", "3,000", "3,000"),
        ("03-Nov-2026", "Therapeutic Exercise & Active Resistance Core Strengthening", "1", "3,000", "3,000"),
        ("06-Nov-2026", "Therapeutic Exercise & Myofascial Release Techniques", "1", "3,000", "3,000"),
        ("09-Nov-2026", "Therapeutic Exercise & Ergonomic Postural Re-training", "1", "3,000", "3,000"),
        ("12-Nov-2026", "Active Core Conditioning & Lumbar Stabilization Drills", "1", "3,000", "3,000"),
        ("16-Nov-2026", "Therapeutic Exercise & Final Functional Re-assessment", "1", "3,000", "3,000"),
    ]

    y = table_top + 45
    for idx, (dt, desc, qty, rate, amt) in enumerate(items):
        bg = (245, 247, 250) if idx % 2 == 1 else (255, 255, 255)
        draw.rectangle([(40, y), (width - 40, y + 36)], fill=bg)
        draw.text((50, y + 8), dt, fill=(40, 40, 40))
        draw.text((180, y + 8), desc, fill=(40, 40, 40))
        draw.text((780, y + 8), qty, fill=(40, 40, 40))
        draw.text((900, y + 8), rate, fill=(40, 40, 40))
        draw.text((1060, y + 8), amt, fill=(40, 40, 40))
        draw.line([(40, y + 36), (width - 40, y + 36)], fill=(230, 230, 230), width=1)
        y += 38

    # Summary box
    draw.rectangle([(700, y + 20), (width - 40, y + 140)], fill=(240, 245, 240), outline=(180, 200, 180), width=2)
    draw.text((720, y + 35), "Subtotal (10 Sessions):", fill=(50, 50, 50))
    draw.text((1040, y + 35), "INR 30,000", fill=(50, 50, 50))
    draw.text((720, y + 65), "Applicable GST (0% Healthcare):", fill=(80, 80, 80))
    draw.text((1040, y + 65), "INR 0.00", fill=(80, 80, 80))
    draw.text((720, y + 95), "TOTAL AMOUNT DUE:", fill=(180, 20, 20))
    draw.text((1040, y + 95), "INR 30,000", fill=(180, 20, 20))

    # Handwritten notes simulation in blue ink
    # "Pt completed 10 sessions of evaluation & therapeutic exercise for chronic lumbosacral strain."
    # "Clinic does not bill insurance directly. Patient to submit for insurance reimbursement under corporate policy."
    note_y = y + 180
    draw.rectangle([(50, note_y), (650, note_y + 260)], outline=(120, 140, 180), fill=(255, 255, 248), width=1)
    draw.text((70, note_y + 15), "[Billing Desk Clinical Memo / Notes]", fill=(100, 100, 100))
    draw.text((70, note_y + 45), "- Patient presented with persistent chronic low back ache (L4-L5/S1)", fill=(0, 35, 140))
    draw.text((70, note_y + 75), "- Services rendered: 1x Initial PT Evaluation (45 min) + 9x Therapeutic Exercise", fill=(0, 35, 140))
    draw.text((70, note_y + 105), "- Modalities: core muscle stabilization, spinal exercises, ultrasound", fill=(0, 35, 140))
    draw.text((70, note_y + 135), "- Note: Direct CPT/ICD codes not printed on standard OPD bills in clinic.", fill=(0, 35, 140))
    draw.text((70, note_y + 165), "- Please provide this memo to insurance desk for CPT 97161 / 97110 claim.", fill=(0, 35, 140))
    draw.text((70, note_y + 195), "- Certified: Treatment completed as advised by consulting orthopaedist.", fill=(0, 35, 140))
    draw.text((70, note_y + 225), "  Sd/- Dr. Anjali Mehta, PT, BPT, MIAP (Reg # PT-8721)", fill=(0, 20, 120))

    # Stamp
    draw.rectangle([(750, note_y + 50), (1050, note_y + 180)], outline=(200, 30, 30), width=3)
    draw.text((770, note_y + 70), "REHAB & SPINE CLINIC", fill=(200, 30, 30))
    draw.text((790, note_y + 100), "*** UNPAID ***", fill=(200, 30, 30))
    draw.text((765, note_y + 130), "PAYMENT RECEIPT PENDING", fill=(200, 30, 30))

    # Add simulated slight fold lines
    draw.line([(0, height * 0.35), (width, height * 0.35 + 15)], fill=(225, 220, 210), width=2)
    draw.line([(0, height * 0.70), (width, height * 0.70 - 10)], fill=(230, 225, 215), width=2)

    img.save("priya_pt_invoice.png", "PNG")
    print("Created priya_pt_invoice.png")

def create_aarav_mri_report():
    # Generate Aarav's MRI report as PDF using matplotlib's PdfPages
    pdf_path = "aarav_mri_report.pdf"
    fig = plt.figure(figsize=(8.5, 11), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')

    # Add background texture/frame
    rect = plt.Rectangle((0.03, 0.03), 0.94, 0.94, fill=False, edgecolor='#2c3e50', linewidth=1.5)
    ax.add_patch(rect)

    # Header
    ax.text(0.5, 0.94, "APEX ADVANCED IMAGING & DIAGNOSTIC CENTRE", ha='center', va='center', fontsize=14, weight='bold', color='#1a365d')
    ax.text(0.5, 0.915, "NABH & NABL ACCREDITED MRI & CT SUITE", ha='center', va='center', fontsize=9, color='#4a5568')
    ax.text(0.5, 0.895, "Dr. Annie Besant Road, Worli, Mumbai - 400018 | Tel: +91 22 6677 4400 | Email: reports@apeximaging.in", ha='center', va='center', fontsize=8, color='#718096')

    # Line separator
    ax.plot([0.05, 0.95], [0.875, 0.875], color='#cbd5e1', lw=1.5)

    # Demographics Box
    demo_box = plt.Rectangle((0.05, 0.75), 0.90, 0.11, fill=True, facecolor='#f8fafc', edgecolor='#cbd5e1', linewidth=1)
    ax.add_patch(demo_box)

    ax.text(0.07, 0.835, "Patient Name: AARAV SEN", fontsize=9.5, weight='bold', color='#0f172a')
    ax.text(0.07, 0.805, "Patient ID / UHID: APX-2026-90412", fontsize=8.5, color='#334155')
    ax.text(0.07, 0.775, "Age / Gender: 32 Years / Male", fontsize=8.5, color='#334155')
    ax.text(0.07, 0.755, "Referral Physician: Dr. Vikram Malhotra, MS (Ortho)", fontsize=8.5, color='#334155')

    ax.text(0.55, 0.835, "Study: MRI RIGHT KNEE JOINT (HIGH RESOLUTION 3T)", fontsize=9.5, weight='bold', color='#0f172a')
    ax.text(0.55, 0.805, "Date of Scan: 18-Nov-2026", fontsize=8.5, color='#334155')
    ax.text(0.55, 0.775, "Date of Report: 19-Nov-2026", fontsize=8.5, color='#334155')
    ax.text(0.55, 0.755, "Status: Final Verified Diagnostic Report", fontsize=8.5, weight='bold', color='#166534')

    # Clinical Indication
    y = 0.71
    ax.text(0.06, y, "CLINICAL HISTORY & INDICATION:", fontsize=9, weight='bold', color='#1e293b')
    y -= 0.025
    ax.text(0.06, y, "32-year-old male with acute twisting injury sustained while playing football 4 days ago.", fontsize=8.5, color='#334155')
    y -= 0.02
    ax.text(0.06, y, "Complaining of severe pain, immediate right knee swelling, and feeling of instability / 'giving way'.", fontsize=8.5, color='#334155')
    y -= 0.02
    ax.text(0.06, y, "Clinical examination revealed positive Lachman Test (Grade 3), positive anterior drawer, and medial joint-line tenderness.", fontsize=8.5, color='#334155')

    # Imaging Technique
    y -= 0.035
    ax.text(0.06, y, "IMAGING PROTOCOL:", fontsize=9, weight='bold', color='#1e293b')
    y -= 0.02
    ax.text(0.06, y, "Multiplanar multi-echo MRI performed on 3.0 Tesla Siemens Skyra MRI Scanner using dedicated 16-channel knee coil.", fontsize=8.5, color='#334155')
    y -= 0.02
    ax.text(0.06, y, "Sequences: Sagittal, Coronal, and Axial PD FS (Proton Density Fat Suppressed), T1W, T2W, and Coronal T2*", fontsize=8.5, color='#334155')

    # Detailed Findings
    y -= 0.035
    ax.text(0.06, y, "FINDINGS:", fontsize=9.5, weight='bold', color='#1e293b')
    
    findings = [
        ("ANTERIOR CRUCIATE LIGAMENT (ACL):", 
         "There is complete discontinuity and fiber disruption of the mid-substance fibers of the anterior cruciate ligament (ACL) with non-visualization of normal taut parallel low-signal fibers. Associated retraction and fluid signal hyperintensity on T2/PDFS noted. Empty notch sign is positive. Bone contusions noted in lateral femoral condyle and posterior lateral tibial plateau (classic pivot-shift mechanism bone marrow edema)."),
        ("MENISCI:",
         "Medial Meniscus: Demonstrates an extensive complex oblique tear involving the posterior horn and body, extending to both superior and inferior articular surfaces with meniscocapsular separation. Lateral Meniscus: Normal size, contour, and low signal intensity throughout anterior, body, and posterior horns. No tear identified."),
        ("POSTERIOR CRUCIATE LIGAMENT (PCL):",
         "The PCL is anatomically intact with normal curvature and signal characteristics."),
        ("COLLATERAL LIGAMENTS:",
         "Medial Collateral Ligament (MCL): Mild Grade 1 periligamentous edema without full-thickness discontinuity. Lateral Collateral Ligament (LCL) and posterolateral corner structures are intact."),
        ("EXTENSOR MECHANISM & ARTICULAR CARTILAGE:",
         "Quadriceps and patellar tendons are intact. Patellofemoral joint shows normal alignment. Mild focal chondral softening in medial compartment."),
        ("JOINT FLUID & SYNOVIUM:",
         "Moderate-to-large joint effusion with hemarthrosis. No intra-articular loose bodies or Baker's cyst.")
    ]

    for title, desc in findings:
        y -= 0.025
        ax.text(0.06, y, title, fontsize=8.5, weight='bold', color='#0f172a')
        # Split desc into multiple lines
        import textwrap
        lines = textwrap.wrap(desc, width=95)
        for line in lines:
            y -= 0.017
            ax.text(0.08, y, line, fontsize=8, color='#334155')

    # Impression Box
    y -= 0.03
    imp_box = plt.Rectangle((0.05, y - 0.105), 0.90, 0.11, fill=True, facecolor='#fef2f2', edgecolor='#f87171', linewidth=1)
    ax.add_patch(imp_box)

    ax.text(0.07, y - 0.015, "IMPRESSION & CLINICAL CORRELATION:", fontsize=9.5, weight='bold', color='#991b1b')
    ax.text(0.08, y - 0.038, "1. COMPLETE TEAR OF THE ANTERIOR CRUCIATE LIGAMENT (ACL) with classic pivot-shift osseous contusions.", fontsize=8.5, weight='bold', color='#7f1d1d')
    ax.text(0.08, y - 0.058, "2. HIGH-GRADE COMPLEX TEAR OF THE POSTERIOR HORN AND BODY OF MEDIAL MENISCUS.", fontsize=8.5, weight='bold', color='#7f1d1d')
    ax.text(0.08, y - 0.078, "3. MODERATE TRAUMATIC KNEE HEMARTHROSIS AND MILD GRADE-1 MCL SPRAIN.", fontsize=8.5, color='#7f1d1d')
    ax.text(0.08, y - 0.096, "RECOMMENDATION: Urgent Orthopaedic surgical consultation for Arthroscopic ACL Reconstruction + Meniscal Repair/Debridement.", fontsize=8, style='italic', color='#450a0a')

    # Signature Block
    y -= 0.13
    ax.text(0.1, y, "Radiological Technologist: K. Shinde, B.Sc RIT", fontsize=7.5, color='#64748b')
    ax.text(0.65, y, "Dr. Sunita Deshmukh, MD, DMRD", fontsize=8.5, weight='bold', color='#0f172a')
    ax.text(0.65, y - 0.016, "Consultant Musculoskeletal Radiologist", fontsize=8, color='#475569')
    ax.text(0.65, y - 0.032, "Maharashtra Medical Council Reg. # MMC/2008/04/1892", fontsize=7.5, color='#64748b')

    with PdfPages(pdf_path) as pdf:
        pdf.savefig(fig)
    plt.close(fig)
    print("Created aarav_mri_report.pdf")

def create_surgeon_estimate():
    # Width and height for surgical estimate image
    width, height = 1200, 1500
    img = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Outer border
    draw.rectangle([(15, 15), (width - 15, height - 15)], outline=(40, 70, 110), width=3)
    draw.rectangle([(22, 22), (width - 22, height - 22)], outline=(200, 215, 230), width=1)

    # Hospital Header
    draw.rectangle([(30, 30), (width - 30, 150)], fill=(240, 246, 255))
    draw.text((50, 45), "ORTHOCARE SPECIALTY SURGICAL HOSPITAL & ARTHROSCOPY CENTRE", fill=(20, 60, 120))
    draw.text((50, 75), "Centre of Excellence in Sports Medicine & Joint Reconstruction | NABH Accredited", fill=(60, 80, 100))
    draw.text((50, 100), "Senapati Bapat Marg, Lower Parel, Mumbai - 400013 | Tel: +91 22 4900 1100 | Reg: ROHINI-892100", fill=(100, 110, 130))

    # Document Title
    draw.rectangle([(40, 165), (width - 40, 205)], fill=(30, 60, 110))
    draw.text((420, 175), "SURGICAL PRE-AUTHORIZATION ESTIMATION SHEET", fill=(255, 255, 255))

    # Patient & Admission Details
    draw.rectangle([(40, 220), (width - 40, 330)], fill=(248, 250, 252), outline=(210, 220, 230))
    draw.text((60, 235), "PATIENT NAME: Aarav Sen", fill=(30, 30, 30))
    draw.text((60, 260), "AGE / GENDER: 32 Yrs / Male", fill=(60, 60, 60))
    draw.text((60, 285), "IP / REGISTRATION NO: OCSH-IP-2026-4412", fill=(60, 60, 60))
    draw.text((60, 305), "PRIMARY DIAGNOSIS: Acute Complete ACL Tear + Medial Meniscus Tear (Right Knee)", fill=(180, 40, 40))

    draw.text((680, 235), "OPERATING SURGEON: Dr. Vikram Malhotra", fill=(30, 30, 30))
    draw.text((680, 260), "QUALIFICATIONS: MS (Ortho), DNB, Fellowship Arthroscopy (USA)", fill=(60, 60, 60))
    draw.text((680, 285), "PROPOSED SURGERY DATE: 02-Dec-2026", fill=(60, 60, 60))
    draw.text((680, 305), "ESTIMATED HOSPITAL STAY: 2 Days (Inpatient OT Care)", fill=(60, 60, 60))

    # CPT Codes and Itemized Estimate Table
    table_top = 360
    draw.rectangle([(40, table_top), (width - 40, table_top + 45)], fill=(225, 235, 245))
    draw.text((60, table_top + 12), "Code / CPT", fill=(20, 40, 70))
    draw.text((220, table_top + 12), "Surgical Procedure / Clinical Service Description", fill=(20, 40, 70))
    draw.text((820, table_top + 12), "Dept / Category", fill=(20, 40, 70))
    draw.text((1020, table_top + 12), "Est. Cost (INR)", fill=(20, 40, 70))

    # Procedures list
    proc_items = [
        ("CPT 29888", "Arthroscopically aided anterior cruciate ligament (ACL) reconstruction", "Major OT / Surgeon", "3,50,000"),
        ("CPT 29881", "Arthroscopy, knee, surgical; with meniscectomy (medial meniscus repair/debridement)", "Surgical Arthroscopy", "1,00,000"),
    ]

    curr_y = table_top + 50
    for code, desc, cat, amt in proc_items:
        draw.rectangle([(40, curr_y), (width - 40, curr_y + 55)], fill=(255, 255, 255))
        draw.text((60, curr_y + 15), code, fill=(30, 30, 30))
        draw.text((220, curr_y + 15), desc, fill=(30, 30, 30))
        draw.text((820, curr_y + 15), cat, fill=(70, 70, 70))
        draw.text((1020, curr_y + 15), amt, fill=(20, 20, 20))
        draw.line([(40, curr_y + 55), (width - 40, curr_y + 55)], fill=(220, 220, 220), width=1)
        curr_y += 58

    # Itemized Inpatient Components Included
    draw.rectangle([(40, curr_y + 15), (width - 40, curr_y + 260)], fill=(250, 252, 255), outline=(210, 225, 240))
    draw.text((60, curr_y + 25), "INCLUDED INPATIENT CLINICAL COMPONENTS IN ESTIMATE:", fill=(30, 60, 100))
    components = [
        "1. Operation Theatre Charges & High-Definition Arthroscopic Tower Instrumentation Suite",
        "2. Anesthesia Fees & Pre-Operative Assessment (Regional Spinal / Epidural + Femoral Nerve Block)",
        "3. Quadrupled Hamstring Autograft Harvest & Bio-absorbable Interference Screw Fixation Implants",
        "4. Standard Semi-Private Room Nursing Care (2 Days / 1 Night Post-Op Observation)",
        "5. Post-Operative Knee Immobilizer Brace & Immediate Day-1 Inpatient Mobilization Physiotherapy",
        "6. Routine Intra-operative Medications, Consumables, and Surgical Disposables"
    ]
    comp_y = curr_y + 55
    for c in components:
        draw.text((80, comp_y), c, fill=(60, 70, 85))
        comp_y += 30

    # Total Summary Box
    sum_y = curr_y + 290
    draw.rectangle([(650, sum_y), (width - 40, sum_y + 110)], fill=(235, 245, 235), outline=(100, 160, 100), width=2)
    draw.text((670, sum_y + 20), "Subtotal Surgical Estimate:", fill=(50, 60, 50))
    draw.text((1000, sum_y + 20), "INR 4,50,000", fill=(50, 60, 50))
    draw.text((670, sum_y + 55), "TOTAL ESTIMATED EXPENSE:", fill=(160, 20, 20))
    draw.text((1000, sum_y + 55), "INR 4,50,000", fill=(160, 20, 20))
    draw.text((670, sum_y + 85), "(Four Lakh Fifty Thousand Rupees Only)", fill=(80, 80, 80))

    # Notes & Policyholder Advice
    notes_y = sum_y + 130
    draw.rectangle([(40, notes_y), (620, notes_y + 240)], fill=(255, 255, 245), outline=(220, 200, 150))
    draw.text((60, notes_y + 15), "PRE-AUTHORIZATION MANDATE & CLINICAL NOTE:", fill=(140, 80, 0))
    draw.text((60, notes_y + 40), "- CPT 29888 & 29881 are elective inpatient surgical procedures.", fill=(50, 50, 50))
    draw.text((60, notes_y + 65), "- Pre-authorization must be submitted >= 72 hours prior to admission.", fill=(50, 50, 50))
    draw.text((60, notes_y + 90), "- Dual Insurance: Insurer2 (Plan B) is Primary policy for Mr. Aarav Sen.", fill=(50, 50, 50))
    draw.text((60, notes_y + 115), "- Plan A is Secondary policy. Coordination of Benefits (COB) is advised.", fill=(50, 50, 50))
    draw.text((60, notes_y + 140), "- Clinical documents required: 3T MRI Report, Pre-Op Fitness, Govt ID.", fill=(50, 50, 50))
    draw.text((60, notes_y + 165), "- Failure to secure cashless pre-auth may lead to denial of direct billing.", fill=(150, 20, 20))

    # Doctor Stamp & Signature Box
    stamp_x = 750
    draw.rectangle([(stamp_x, notes_y + 30), (width - 60, notes_y + 210)], outline=(30, 60, 150), width=2)
    draw.text((stamp_x + 20, notes_y + 45), "DR. VIKRAM MALHOTRA", fill=(30, 60, 150))
    draw.text((stamp_x + 20, notes_y + 70), "MS (Ortho), DNB (Ortho)", fill=(30, 60, 150))
    draw.text((stamp_x + 20, notes_y + 95), "Consultant Arthroscopy & Joint Reconstruction", fill=(30, 60, 150))
    draw.text((stamp_x + 20, notes_y + 120), "Reg. No: MMC/2004/08/3120", fill=(30, 60, 150))
    draw.text((stamp_x + 20, notes_y + 155), "[Digitally Verified & Authorized Signature]", fill=(60, 120, 60))

    img.save("surgeon_estimate.jpg", "JPEG", quality=95)
    print("Created surgeon_estimate.jpg")

def create_user_query():
    query_text = (
        'Hi DuCO-Agent, I need to get my knee operated on soon, and Priya has some physical therapy '
        'bills lying around. We have Insurer1 (Plan A) and Insurer2 (Plan B). Can you help us figure '
        'out which plan pays first for my surgery and her bills? How much will we actually have to '
        'pay out of our own pocket? Also, we need the pre-auth letters generated for both insurers '
        'so we don\'t end up with a claim rejection. Please help!'
    )
    with open("user_query.txt", "w", encoding="utf-8") as f:
        f.write(query_text)
    print("Created user_query.txt")

if __name__ == "__main__":
    create_priya_pt_invoice()
    create_aarav_mri_report()
    create_surgeon_estimate()
    create_user_query()
    print("All 4 multi-modal input files generated successfully.")
