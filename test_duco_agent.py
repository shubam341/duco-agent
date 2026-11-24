"""
test_duco_agent.py
Comprehensive Verification & Test Suite for DuCO-Agent.
Runs automated end-to-end assertions against the Assessment Rubric:
1. Multi-Modal Ingestion & Code Inference
2. COB Order Determination (Subscriber vs Dependent Rules)
3. Medical Necessity & Clinical Pre-Auth Mandate Verification
4. Mathematical & Financial Accuracy (Fund Conservation, Deductibles, Coinsurance)
5. Output Visualizations & Pre-Auth Letters
"""

import os
import unittest
from duco_agent import DuCOAgent, AgentState
from insurance_api import MockInsuranceAPI
from multimodal_extractor import MultimodalExtractor

class TestDuCOAgent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.agent = DuCOAgent()
        cls.memory = cls.agent.run_full_pipeline()

    def test_01_agent_state_and_thought_logs(self):
        """Verify agentic autonomy, state transitions, and reflection blackboard."""
        self.assertEqual(self.agent.state, AgentState.COMPLETED)
        self.assertGreaterEqual(len(self.agent.thought_logs), 7)
        for log in self.agent.thought_logs:
            self.assertTrue(len(log.thought) > 10)
            self.assertTrue(len(log.action) > 5)
            self.assertTrue(len(log.observation) > 10)
            self.assertTrue(len(log.reflection) > 10)

    def test_02_multimodal_extraction(self):
        """Verify multi-modal extraction of all 4 input files."""
        inputs = self.memory["inputs"]
        # 1. Query
        self.assertIn("Aarav Sen", inputs["query"]["extracted_patients"])
        self.assertIn("SURGERY_COB_ANALYSIS", inputs["query"]["detected_intents"])
        
        # 2. Priya PT Invoice
        inv = inputs["pt_invoice"]
        self.assertEqual(inv["total_billed_amount"], 30000.0)
        cpt_codes = [c["cpt_code"] for c in inv["inferred_cpt_codes"]]
        self.assertIn("97161", cpt_codes)
        self.assertIn("97110", cpt_codes)
        icd_codes = [c["icd10_code"] for c in inv["inferred_icd10_codes"]]
        self.assertIn("M54.5", icd_codes)

        # 3. Aarav MRI Report
        mri = inputs["mri_report"]
        self.assertEqual(mri["findings"]["acl"]["status"], "COMPLETE_TEAR")
        self.assertEqual(mri["findings"]["medial_meniscus"]["status"], "COMPLEX_TEAR")

        # 4. Surgeon Estimate
        surg = inputs["surgeon_estimate"]
        self.assertEqual(surg["total_estimated_amount"], 450000.0)
        surg_cpts = [p["cpt_code"] for p in surg["itemized_procedures"]]
        self.assertIn("29888", surg_cpts)
        self.assertIn("29881", surg_cpts)

    def test_03_cob_order_determination(self):
        """Verify Subscriber / Employee Rule for COB primary vs secondary assignment."""
        cob_a = self.memory["cob_hierarchy"]["aarav"]
        cob_p = self.memory["cob_hierarchy"]["priya"]

        # For Aarav: Plan B is Primary, Plan A is Secondary
        self.assertEqual(cob_a["primary"]["insurer_id"], "INSURER_2")
        self.assertEqual(cob_a["secondary"]["insurer_id"], "INSURER_1")

        # For Priya: Plan A is Primary, Plan B is Secondary
        self.assertEqual(cob_p["primary"]["insurer_id"], "INSURER_1")
        self.assertEqual(cob_p["secondary"]["insurer_id"], "INSURER_2")

    def test_04_mathematical_financial_accuracy(self):
        """Verify claims calculations, deductible rollovers, and out-of-pocket optimization."""
        adj_a = self.memory["claims_adjudication"]["aarav"]["summary"]
        adj_p = self.memory["claims_adjudication"]["priya"]["summary"]

        # Aarav Surgery (INR 4,50,000)
        self.assertEqual(adj_a["total_billed"], 450000.0)
        self.assertEqual(adj_a["primary_paid"], 390000.0) # After OOP max
        self.assertEqual(adj_a["secondary_paid"], 60000.0) # COB pays remainder
        self.assertEqual(adj_a["total_insurance_paid"], 450000.0)
        self.assertEqual(adj_a["final_patient_out_of_pocket"], 0.0) # 100% coverage
        self.assertEqual(adj_a["dual_coverage_savings"], 60000.0)

        # Priya PT Sessions (INR 30,000)
        self.assertEqual(adj_p["total_billed"], 30000.0)
        self.assertEqual(adj_p["primary_paid"], 16000.0)
        self.assertEqual(adj_p["secondary_paid"], 9000.0)
        self.assertEqual(adj_p["total_insurance_paid"], 25000.0)
        self.assertEqual(adj_p["final_patient_out_of_pocket"], 5000.0) # Only cap excess
        self.assertEqual(adj_p["dual_coverage_savings"], 9000.0)

        # Total Family Savings: ₹60,000 + ₹9,000 = ₹69,000
        total_savings = adj_a["dual_coverage_savings"] + adj_p["dual_coverage_savings"]
        self.assertEqual(total_savings, 69000.0)

    def test_05_conservation_of_funds_validation(self):
        """Verify automated mathematical audit loop."""
        val = self.memory["validation_results"]
        self.assertTrue(val["all_passed"])
        for check in val["checks"]:
            self.assertTrue(check["passed"], f"Check failed: {check['check']}")

    def test_06_preauth_letters_and_audio_artifacts(self):
        """Verify clinical pre-auth documents and audio briefing assets."""
        letters = self.memory["preauth_letters"]
        self.assertIn("primary_hdfc_ergo", letters)
        self.assertIn("secondary_star_care", letters)
        self.assertIn("29888", letters["primary_hdfc_ergo"])
        self.assertIn("S83.511A", letters["primary_hdfc_ergo"])
        self.assertIn("Dr. Vikram Malhotra", letters["primary_hdfc_ergo"])
        self.assertIn("COB ENDORSEMENT", letters["secondary_star_care"])

        # Check files on disk
        self.assertTrue(os.path.exists("cost_flow_sankey.png"))
        self.assertTrue(os.path.exists("cost_flow_sankey.html"))
        self.assertTrue(os.path.exists("financial_waterfall.png"))
        self.assertTrue(os.path.exists("coverage_comparison.png"))
        self.assertTrue(os.path.exists("aarav_primary_preauth_hdfc.txt"))
        self.assertTrue(os.path.exists("aarav_secondary_prenotif_star.txt"))
        self.assertTrue(os.path.exists("patient_briefing_audio.wav"))
        self.assertTrue(os.path.exists("patient_briefing_transcript.txt"))

if __name__ == "__main__":
    unittest.main()
