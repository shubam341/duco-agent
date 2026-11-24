"""
insurance_api.py
Mock Insurance API client providing programmatic interfaces for querying member policies,
checking pre-authorizations, running claim adjudications, and executing COB rules.
"""

from typing import Dict, Any, List, Optional
from mock_insurance_data import INSURERS_DATABASE, CLINICAL_CODE_KNOWLEDGE

class MockInsuranceAPI:
    def __init__(self):
        self.db = INSURERS_DATABASE
        self.knowledge = CLINICAL_CODE_KNOWLEDGE

    def get_policy(self, insurer_id: str) -> Dict[str, Any]:
        """Fetch general policy specifications for an insurer."""
        if insurer_id not in self.db:
            raise ValueError(f"Unknown insurer ID: {insurer_id}")
        return self.db[insurer_id]

    def get_member_eligibility(self, insurer_id: str, member_name: str) -> Dict[str, Any]:
        """Verify member enrollment, coverage tier, subscriber role, and accumulator status."""
        policy = self.get_policy(insurer_id)
        subscribers = policy.get("subscribers", {})
        if member_name not in subscribers:
            raise ValueError(f"Member '{member_name}' not found under policy {policy['policy_number']}")
        
        member_data = subscribers[member_name].copy()
        member_data["insurer_id"] = insurer_id
        member_data["policy_number"] = policy["policy_number"]
        member_data["company_name"] = policy["company_name"]
        member_data["tpa_name"] = policy["tpa_name"]
        member_data["plan_name"] = policy["plan_name"]
        return member_data

    def check_preauth_mandate(self, insurer_id: str, cpt_codes: List[str], total_amount: float) -> Dict[str, Any]:
        """Check whether pre-authorization is mandatory for given CPT codes and total cost."""
        policy = self.get_policy(insurer_id)
        rules = policy["preauth_rules"]
        
        mandatory_for_codes = any(code in rules["mandatory_codes"] for code in cpt_codes)
        exceeds_threshold = total_amount >= rules["inpatient_surgery_threshold"]
        is_required = mandatory_for_codes or exceeds_threshold
        
        return {
            "is_required": is_required,
            "mandatory_codes_triggered": [c for c in cpt_codes if c in rules["mandatory_codes"]],
            "cost_threshold_exceeded": exceeds_threshold,
            "advance_notice_hours": rules["advance_notice_hours"],
            "required_documents": rules["required_documents"],
            "tpa_desk": policy["tpa_name"],
            "company_name": policy["company_name"]
        }

    def verify_clinical_necessity(self, cpt_code: str, clinical_findings: Dict[str, Any]) -> Dict[str, Any]:
        """Validate medical necessity of a CPT code against clinical documentation."""
        if cpt_code not in self.knowledge["CPT"]:
            return {"valid": False, "reason": f"Unknown CPT code {cpt_code}"}
        
        code_meta = self.knowledge["CPT"][cpt_code]
        criteria = code_meta.get("interqual_criteria", [])
        
        # Check matching clinical evidence
        matched_criteria = []
        if cpt_code == "29888":  # ACL reconstruction
            if clinical_findings.get("acl_tear") in ["complete", "high_grade", "full_thickness"]:
                matched_criteria.append("Full-thickness ACL tear documented on MRI")
            if clinical_findings.get("instability") or clinical_findings.get("positive_lachman"):
                matched_criteria.append("Clinical laxity (Lachman 3+ / positive drawer)")
            if clinical_findings.get("active_functional_demand"):
                matched_criteria.append("Active patient requiring stability for athletic/work activities")
        elif cpt_code == "29881":  # Meniscectomy
            if clinical_findings.get("meniscus_tear"):
                matched_criteria.append("MRI documented meniscal tear extending to articular surface")
            if clinical_findings.get("joint_line_tenderness"):
                matched_criteria.append("Joint line tenderness or mechanical symptoms")
            if clinical_findings.get("concomitant_acl"):
                matched_criteria.append("Concomitant with ACL reconstruction")
        elif cpt_code in ["97161", "97110"]:
            if clinical_findings.get("musculoskeletal_pain"):
                matched_criteria.append("Documented musculoskeletal complaint / functional deficit")
            if clinical_findings.get("active_pt_protocol"):
                matched_criteria.append("Prescribed therapeutic exercise regimen")
        
        is_approved = len(matched_criteria) >= 2 or (cpt_code in ["97161", "97110"] and len(matched_criteria) >= 1)
        return {
            "cpt_code": cpt_code,
            "description": code_meta["description"],
            "is_medically_necessary": is_approved,
            "matched_criteria": matched_criteria,
            "required_criteria": criteria,
            "status": "APPROVED" if is_approved else "PENDING_ADDITIONAL_INFO"
        }

    def adjudicate_claim(
        self,
        insurer_id: str,
        patient_name: str,
        service_type: str, # "INPATIENT_SURGERY" or "OUTPATIENT_PT"
        line_items: List[Dict[str, Any]],
        is_primary: bool,
        primary_eob: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Adjudicate a claim according to NAIC & Indian corporate COB rules.
        Handles deductibles, coinsurance, caps, and secondary coordination.
        """
        member = self.get_member_eligibility(insurer_id, patient_name)
        policy = self.get_policy(insurer_id)
        
        billed_total = sum(item["billed_amount"] for item in line_items)
        
        # Step 1: Calculate Allowable Expense
        allowable_items = []
        for item in line_items:
            code = item.get("cpt_code")
            billed = item["billed_amount"]
            units = item.get("units", 1)
            # Lookup fee schedule
            fee_info = policy.get("fee_schedule", {}).get(code, {})
            rate_per_unit = fee_info.get("allowable_per_unit", billed / max(units, 1))
            calculated_allowable = rate_per_unit * units
            allowable = min(billed, calculated_allowable)
            allowable_items.append({
                "cpt_code": code,
                "description": item.get("description", ""),
                "units": units,
                "billed": billed,
                "allowable": allowable
            })
            
        total_allowable = sum(i["allowable"] for i in allowable_items)
        contractual_discount = billed_total - total_allowable

        # Apply specific rules (e.g. Outpatient PT Cap)
        cap_exceeded = 0.0
        if service_type == "OUTPATIENT_PT":
            pt_cap = member.get("opd_pt_annual_cap", 25000.0)
            if total_allowable > pt_cap:
                cap_exceeded = total_allowable - pt_cap
                total_allowable = pt_cap

        if is_primary:
            # PRIMARY CLAIM ADJUDICATION
            # Deductible
            indiv_deductible = member["individual_deductible"]
            deductible_already_met = member["deductible_met"]
            deductible_remaining = max(0.0, indiv_deductible - deductible_already_met)
            
            deductible_applied = min(total_allowable, deductible_remaining)
            amount_after_deductible = total_allowable - deductible_applied
            
            # Coinsurance
            coinsurance_rate = member["coinsurance_inpatient"] if service_type == "INPATIENT_SURGERY" else member["coinsurance_outpatient"]
            patient_coinsurance_amount = amount_after_deductible * coinsurance_rate
            insurer_paid_rate = 1.0 - coinsurance_rate
            insurer_payment = amount_after_deductible * insurer_paid_rate
            
            # OOP Maximum Check
            patient_total_copay = deductible_applied + patient_coinsurance_amount
            oop_max = member["annual_oop_max"]
            oop_accumulated = member["oop_accumulated"]
            oop_remaining = max(0.0, oop_max - oop_accumulated)
            
            if patient_total_copay > oop_remaining:
                excess_oop = patient_total_copay - oop_remaining
                patient_total_copay = oop_remaining
                insurer_payment += excess_oop
                oop_adjustment = excess_oop
            else:
                oop_adjustment = 0.0

            # Patient total responsibility for primary
            patient_balance = (billed_total - insurer_payment)
            
            return {
                "adjudication_tier": "PRIMARY",
                "insurer_id": insurer_id,
                "company_name": policy["company_name"],
                "policy_number": policy["policy_number"],
                "patient_name": patient_name,
                "billed_total": billed_total,
                "contractual_discount": contractual_discount,
                "total_allowable": total_allowable,
                "cap_exceeded_disallowed": cap_exceeded,
                "deductible_applied": deductible_applied,
                "patient_coinsurance": patient_coinsurance_amount,
                "oop_adjustment": oop_adjustment,
                "insurer_payment": insurer_payment,
                "patient_remainder_balance": patient_balance,
                "patient_net_cost_after_primary": patient_balance,
                "line_items": allowable_items
            }

        else:
            # SECONDARY CLAIM ADJUDICATION (COB)
            if not primary_eob:
                raise ValueError("Secondary adjudication requires Primary Explanation of Benefits (EOB)")

            # What would secondary have paid if it had been primary?
            indiv_deductible = member["individual_deductible"]
            deductible_already_met = member["deductible_met"]
            deductible_remaining = max(0.0, indiv_deductible - deductible_already_met)
            
            # Standard COB Deductible Credit: Primary expenses / deductible applied satisfy secondary deductible
            primary_deductible_applied = primary_eob.get("deductible_applied", 0.0)
            secondary_deductible_credited = min(primary_deductible_applied, deductible_remaining)
            effective_secondary_deductible = max(0.0, deductible_remaining - secondary_deductible_credited)
            
            deductible_applied_hypo = min(total_allowable, effective_secondary_deductible)
            amount_after_deductible = total_allowable - deductible_applied_hypo
            
            coinsurance_rate = member["coinsurance_inpatient"] if service_type == "INPATIENT_SURGERY" else member["coinsurance_outpatient"]
            hypothetical_secondary_normal_payment = amount_after_deductible * (1.0 - coinsurance_rate)

            # In Standard COB (NAIC Model):
            # Secondary pays the LESSER of:
            # 1. Normal Secondary Benefit (what it would pay with deductible credit)
            # 2. Patient Remainder Balance after Primary Payment
            # 3. Total Allowable Expense minus Primary Payment (allowable unpaid)
            primary_paid = primary_eob["insurer_payment"]
            patient_liability_after_primary = primary_eob["patient_remainder_balance"]
            allowable_unpaid = max(0.0, total_allowable - primary_paid)
            
            secondary_payment = min(
                hypothetical_secondary_normal_payment,
                patient_liability_after_primary,
                allowable_unpaid if allowable_unpaid > 0 else patient_liability_after_primary
            )

            total_insurance_paid = primary_paid + secondary_payment
            final_patient_oop = max(0.0, billed_total - total_insurance_paid)

            return {
                "adjudication_tier": "SECONDARY",
                "insurer_id": insurer_id,
                "company_name": policy["company_name"],
                "policy_number": policy["policy_number"],
                "patient_name": patient_name,
                "billed_total": billed_total,
                "contractual_discount": contractual_discount,
                "total_allowable": total_allowable,
                "primary_paid": primary_paid,
                "hypothetical_normal_secondary_benefit": hypothetical_secondary_normal_payment,
                "secondary_payment": secondary_payment,
                "secondary_deductible_credited": secondary_deductible_credited,
                "total_combined_reimbursement": total_insurance_paid,
                "final_patient_out_of_pocket": final_patient_oop,
                "savings_from_dual_coverage": primary_eob["patient_remainder_balance"] - final_patient_oop,
                "line_items": allowable_items
            }
