"""
mock_insurance_data.py
Defines the policy parameters, fee schedules, member accounts, and clinical rule engines
for Insurer 1 (Plan A: Star Care Health) and Insurer 2 (Plan B: HDFC ERGO Care Shield).
"""

INSURERS_DATABASE = {
    "INSURER_1": {
        "insurer_id": "INSURER_1",
        "company_name": "Star Care Health Insurance Co. Ltd.",
        "tpa_name": "MediAssist Healthcare Services TPA",
        "plan_name": "Corporate Star Comprehensive Care Plan (Plan A)",
        "policy_number": "STAR-CORP-2026-88192A",
        "subscribers": {
            "Priya Sen": {
                "role": "PRIMARY_SUBSCRIBER",
                "employee_id": "EMP-PRIYA-771",
                "corporate_group": "FinTech Innovations Global Ltd.",
                "member_id": "STAR-PRI-01",
                "dob": "1995-04-12",
                "gender": "Female",
                "annual_sum_insured": 800000.0,
                "individual_deductible": 10000.0,
                "deductible_met": 5000.0,  # Priya already met 5,000 earlier this year
                "coinsurance_inpatient": 0.10,  # Insurer pays 90%, patient pays 10%
                "coinsurance_outpatient": 0.20, # Insurer pays 80%, patient pays 20%
                "copay_fixed": 0.0,
                "annual_oop_max": 50000.0,
                "oop_accumulated": 5000.0,
                "opd_pt_annual_cap": 25000.0,  # Max annual benefit for outpatient physiotherapy
                "opd_pt_accumulated": 0.0,
            },
            "Aarav Sen": {
                "role": "DEPENDENT_SPOUSE",
                "employee_id": "EMP-PRIYA-771-DEP01",
                "corporate_group": "FinTech Innovations Global Ltd.",
                "member_id": "STAR-AAR-02",
                "dob": "1994-08-25",
                "gender": "Male",
                "annual_sum_insured": 800000.0,
                "individual_deductible": 10000.0,
                "deductible_met": 0.0,  # Aarav hasn't used Plan A deductible yet
                "coinsurance_inpatient": 0.10,  # 90% covered
                "coinsurance_outpatient": 0.20,
                "copay_fixed": 0.0,
                "annual_oop_max": 50000.0,
                "oop_accumulated": 0.0,
                "opd_pt_annual_cap": 25000.0,
                "opd_pt_accumulated": 0.0,
            }
        },
        "cob_rules": {
            "model": "STANDARD_COB_NAIC_IRDAI",
            "coordination_formula": "LESSER_OF_NORMAL_BENEFIT_OR_PATIENT_REMAINDER",
            "allowable_expenses_ceiling": 1.0, # 100% of allowable expense
            "requires_secondary_pre_notification": True
        },
        "preauth_rules": {
            "inpatient_surgery_threshold": 50000.0,
            "mandatory_codes": ["29888", "29881", "27447"],
            "advance_notice_hours": 48,
            "required_documents": ["Radiology MRI Report", "Surgeon Detailed Estimate", "Clinical Notes"]
        },
        "fee_schedule": {
            "29888": {"description": "Arthroscopic ACL Reconstruction", "allowable_per_unit": 350000.0},
            "29881": {"description": "Arthroscopic Meniscectomy", "allowable_per_unit": 100000.0},
            "97161": {"description": "PT Evaluation Low/Mod Complexity", "allowable_per_unit": 3000.0},
            "97110": {"description": "PT Therapeutic Exercise (per unit)", "allowable_per_unit": 3000.0}
        }
    },
    "INSURER_2": {
        "insurer_id": "INSURER_2",
        "company_name": "HDFC ERGO General Insurance Co. Ltd.",
        "tpa_name": "Vidal Health Insurance TPA Pvt. Ltd.",
        "plan_name": "Care Shield Executive Corporate Group Plan (Plan B)",
        "policy_number": "HDFC-EXEC-2026-99014B",
        "subscribers": {
            "Aarav Sen": {
                "role": "PRIMARY_SUBSCRIBER",
                "employee_id": "EMP-AARAV-402",
                "corporate_group": "Apex Engineering & Architecture Ltd.",
                "member_id": "HDFC-AAR-01",
                "dob": "1994-08-25",
                "gender": "Male",
                "annual_sum_insured": 1000000.0,
                "individual_deductible": 15000.0,
                "deductible_met": 0.0,  # Aarav hasn't met deductible yet
                "coinsurance_inpatient": 0.15,  # Insurer pays 85%, patient pays 15%
                "coinsurance_outpatient": 0.30, # Insurer pays 70%, patient pays 30%
                "copay_fixed": 0.0,
                "annual_oop_max": 60000.0,
                "oop_accumulated": 0.0,
                "opd_pt_annual_cap": 25000.0,
                "opd_pt_accumulated": 0.0,
            },
            "Priya Sen": {
                "role": "DEPENDENT_SPOUSE",
                "employee_id": "EMP-AARAV-402-DEP01",
                "corporate_group": "Apex Engineering & Architecture Ltd.",
                "member_id": "HDFC-PRI-02",
                "dob": "1995-04-12",
                "gender": "Female",
                "annual_sum_insured": 1000000.0,
                "individual_deductible": 15000.0,
                "deductible_met": 0.0,
                "coinsurance_inpatient": 0.15,
                "coinsurance_outpatient": 0.30,
                "copay_fixed": 0.0,
                "annual_oop_max": 60000.0,
                "oop_accumulated": 0.0,
                "opd_pt_annual_cap": 25000.0,
                "opd_pt_accumulated": 0.0,
            }
        },
        "cob_rules": {
            "model": "STANDARD_COB_NAIC_IRDAI",
            "coordination_formula": "LESSER_OF_NORMAL_BENEFIT_OR_PATIENT_REMAINDER",
            "multiple_procedure_discount": False,
            "requires_secondary_pre_notification": True
        },
        "preauth_rules": {
            "inpatient_surgery_threshold": 40000.0,
            "mandatory_codes": ["29888", "29881", "27447", "29877"],
            "advance_notice_hours": 72,
            "required_documents": ["3T MRI Diagnostic Scan Report", "Hospital Pre-Auth Form", "Itemized Tariff Breakdown"]
        },
        "fee_schedule": {
            "29888": {"description": "Arthroscopic ACL Reconstruction", "allowable_per_unit": 350000.0},
            "29881": {"description": "Arthroscopic Meniscectomy", "allowable_per_unit": 100000.0},
            "97161": {"description": "PT Evaluation Low/Mod Complexity", "allowable_per_unit": 3000.0},
            "97110": {"description": "PT Therapeutic Exercise (per unit)", "allowable_per_unit": 3000.0}
        }
    }
}

CLINICAL_CODE_KNOWLEDGE = {
    "CPT": {
        "29888": {
            "description": "Arthroscopically aided anterior cruciate ligament (ACL) reconstruction / augmentation",
            "category": "Orthopaedic Inpatient Surgery",
            "standard_indication": "Complete rupture of anterior cruciate ligament with persistent mechanical knee laxity",
            "interqual_criteria": [
                "Full-thickness ACL tear documented on 1.5T/3T MRI",
                "Positive clinical laxity test (Grade II or III Lachman or pivot shift)",
                "Patient wishes to return to active lifestyle or work requiring stability"
            ]
        },
        "29881": {
            "description": "Arthroscopy, knee, surgical; with meniscectomy (medial or lateral, including debridement/repair)",
            "category": "Surgical Arthroscopy",
            "standard_indication": "Tear of meniscus with mechanical symptoms, joint-line tenderness, or locking",
            "interqual_criteria": [
                "MRI documented meniscal tear extending to articular surface",
                "Joint line tenderness or positive McMurray/Apley test",
                "Concomitant with ACL reconstruction when meniscocapsular stability is compromised"
            ]
        },
        "97161": {
            "description": "Physical therapy evaluation: low complexity, requiring history and examination addressing 1-2 elements",
            "category": "Outpatient Physical Medicine & Rehabilitation",
            "standard_indication": "Initial evaluation for musculoskeletal complaint (e.g. chronic lumbosacral strain)"
        },
        "97110": {
            "description": "Therapeutic procedure, 1 or more areas, each 15 minutes; therapeutic exercises",
            "category": "Physical Therapy / Therapeutic Exercise",
            "standard_indication": "Active exercise to develop lumbar core strength, stability, and range of motion"
        }
    },
    "ICD10": {
        "S83.511A": {
            "description": "Complete tear of anterior cruciate ligament of right knee, initial encounter",
            "clinical_synonyms": ["ACL rupture", "anterior cruciate ligament tear", "torn right ACL"]
        },
        "S83.241A": {
            "description": "Complex tear of medial meniscus, current injury, right knee, initial encounter",
            "clinical_synonyms": ["medial meniscus tear", "torn medial meniscus", "meniscal posterior horn tear"]
        },
        "M54.50": {
            "description": "Low back pain, unspecified",
            "clinical_synonyms": ["chronic low back pain", "lumbosacral pain", "lumbar backache"]
        },
        "M54.5": {
            "description": "Low back pain / Lumbago",
            "clinical_synonyms": ["chronic back pain", "lumbosacral strain", "mechanical back pain"]
        }
    }
}
