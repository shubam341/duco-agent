"""
generate_visualizations.py
Generates aesthetic, publication-grade visual cost flow diagrams and waterfall charts
for DuCO-Agent's Dual Coverage Coordination of Benefits (COB) output.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

def generate_waterfall_charts():
    """Generate high-resolution waterfall charts for Aarav and Priya."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), dpi=150)
    fig.patch.set_facecolor('#f8fafc')

    # 1. Aarav's Surgery Waterfall
    categories_aarav = [
        'Total Billed\n(CPT 29888+29881)',
        'Deductible\n(Plan B)',
        'Plan B Paid\n(85% + OOP Cap)',
        'Bal. to Sec.\n(Plan A)',
        'Plan A Paid\n(Secondary COB)',
        'Final Patient\nOut-of-Pocket'
    ]
    values_aarav = [450000, -15000, -375000, 60000, -60000, 0]
    
    # Cumulative calculation for waterfall bars
    cumulative_a = [0, 450000, 435000, 60000, 60000, 0]
    bar_heights_a = [450000, 15000, 375000, 60000, 60000, 0]
    colors_a = ['#1e40af', '#e11d48', '#059669', '#d97706', '#0284c7', '#16a34a']

    ax1.set_facecolor('#ffffff')
    bars1 = ax1.bar(
        range(len(categories_aarav)),
        [450000, 15000, 375000, 60000, 60000, 0],
        bottom=[0, 435000, 60000, 0, 0, 0],
        color=colors_a,
        edgecolor='#1e293b',
        linewidth=1.2,
        width=0.55
    )

    # Values labels
    labels_a = ['₹4,50,000', '-₹15,000', '-₹3,75,000\n(Total Paid: ₹3.9L)', '₹60,000', '-₹60,000\n(Plan A Pays)', '₹0.00\n(100% Covered!)']
    for idx, (bar, label) in enumerate(zip(bars1, labels_a)):
        y = bar.get_y() + bar.get_height() / 2
        if idx == 5:
            ax1.text(idx, 15000, label, ha='center', va='bottom', fontsize=9.5, weight='bold', color='#15803d')
        else:
            ax1.text(idx, y, label, ha='center', va='center', fontsize=8.5, weight='bold', color='white' if idx in [0, 1, 2, 4] else '#1e293b')

    ax1.set_title('AARAV SEN: ACL Knee Surgery (₹4,50,000)\nDual Coverage COB Cost Flow', fontsize=12, weight='bold', color='#0f172a', pad=15)
    ax1.set_xticks(range(len(categories_aarav)))
    ax1.set_xticklabels(categories_aarav, fontsize=8.5, color='#334155')
    ax1.set_ylabel('Amount in INR (₹)', fontsize=10, weight='bold', color='#1e293b')
    ax1.grid(axis='y', linestyle='--', alpha=0.4)
    ax1.set_ylim(0, 500000)

    # 2. Priya's PT Sessions Waterfall
    categories_priya = [
        'Total Billed\n(10 PT Sessions)',
        'Plan A Paid\n(Primary Payer)',
        'Bal. to Sec.\n(Plan B)',
        'Plan B Paid\n(Secondary COB)',
        'Cap Disallowance\n(>₹25k Cap)',
        'Final Patient\nOut-of-Pocket'
    ]
    ax2.set_facecolor('#ffffff')
    bars2 = ax2.bar(
        range(len(categories_priya)),
        [30000, 16000, 14000, 9000, 5000, 5000],
        bottom=[0, 14000, 0, 5000, 0, 0],
        color=['#4338ca', '#059669', '#d97706', '#0284c7', '#dc2626', '#e11d48'],
        edgecolor='#1e293b',
        linewidth=1.2,
        width=0.55
    )

    labels_p = ['₹30,000', '-₹16,000\n(Plan A)', '₹14,000', '-₹9,000\n(Plan B)', '-₹5,000', '₹5,000\n(Net Patient OOP)']
    for idx, (bar, label) in enumerate(zip(bars2, labels_p)):
        y = bar.get_y() + bar.get_height() / 2
        ax2.text(idx, y, label, ha='center', va='center', fontsize=8.5, weight='bold', color='white' if idx in [0, 1, 3, 4, 5] else '#1e293b')

    ax2.set_title('PRIYA SEN: Outpatient Physical Therapy (₹30,000)\nDual Coverage COB Cost Flow', fontsize=12, weight='bold', color='#0f172a', pad=15)
    ax2.set_xticks(range(len(categories_priya)))
    ax2.set_xticklabels(categories_priya, fontsize=8.5, color='#334155')
    ax2.set_ylabel('Amount in INR (₹)', fontsize=10, weight='bold', color='#1e293b')
    ax2.grid(axis='y', linestyle='--', alpha=0.4)
    ax2.set_ylim(0, 35000)

    plt.tight_layout(pad=3.0)
    out_path = "financial_waterfall.png"
    plt.savefig(out_path, bbox_inches='tight')
    plt.close(fig)
    print(f"Generated {out_path}")

def generate_dual_vs_single_comparison():
    """Generate side-by-side comparison chart: Single Policy vs Dual Coverage COB."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=150)
    fig.patch.set_facecolor('#f8fafc')

    # Aarav
    scenarios_a = ['Single Coverage\n(Plan B Only)', 'Dual Coverage COB\n(Plan B + Plan A)']
    ins_paid_a = [390000, 450000]
    oop_a = [60000, 0]

    width = 0.45
    p1 = ax1.bar(scenarios_a, ins_paid_a, width, label='Insurance Paid', color='#059669', edgecolor='#1e293b')
    p2 = ax1.bar(scenarios_a, oop_a, width, bottom=ins_paid_a, label='Patient Out-of-Pocket', color='#e11d48', edgecolor='#1e293b')

    ax1.set_facecolor('#ffffff')
    ax1.set_title('Aarav: Knee Surgery Out-of-Pocket Impact\n(₹60,000 Saved via Dual COB!)', fontsize=11, weight='bold', color='#0f172a')
    ax1.set_ylabel('INR (₹)', fontsize=10, weight='bold')
    ax1.legend(loc='upper right', frameon=True)
    ax1.set_ylim(0, 520000)
    ax1.grid(axis='y', linestyle='--', alpha=0.3)

    # Annotate values
    ax1.text(0, 390000 / 2, '₹3,90,000', ha='center', va='center', color='white', weight='bold')
    ax1.text(0, 390000 + 30000, '₹60,000 OOP', ha='center', va='center', color='white', weight='bold')
    ax1.text(1, 450000 / 2, '₹4,50,000\n(100% Paid by COB!)', ha='center', va='center', color='white', weight='bold')
    ax1.text(1, 460000, '₹0.00 OOP!', ha='center', va='bottom', color='#16a34a', weight='bold', fontsize=11)

    # Priya
    scenarios_p = ['Single Coverage\n(Plan A Only)', 'Dual Coverage COB\n(Plan A + Plan B)']
    ins_paid_p = [16000, 25000]
    oop_p = [14000, 5000]

    p3 = ax2.bar(scenarios_p, ins_paid_p, width, label='Insurance Paid', color='#059669', edgecolor='#1e293b')
    p4 = ax2.bar(scenarios_p, oop_p, width, bottom=ins_paid_p, label='Patient Out-of-Pocket', color='#e11d48', edgecolor='#1e293b')

    ax2.set_facecolor('#ffffff')
    ax2.set_title('Priya: Physical Therapy Out-of-Pocket Impact\n(₹9,000 Saved via Dual COB!)', fontsize=11, weight='bold', color='#0f172a')
    ax2.set_ylabel('INR (₹)', fontsize=10, weight='bold')
    ax2.legend(loc='upper right', frameon=True)
    ax2.set_ylim(0, 35000)
    ax2.grid(axis='y', linestyle='--', alpha=0.3)

    ax2.text(0, 8000, '₹16,000', ha='center', va='center', color='white', weight='bold')
    ax2.text(0, 23000, '₹14,000 OOP', ha='center', va='center', color='white', weight='bold')
    ax2.text(1, 12500, '₹25,000\n(COB Paid)', ha='center', va='center', color='white', weight='bold')
    ax2.text(1, 27500, '₹5,000 OOP', ha='center', va='center', color='white', weight='bold')

    plt.tight_layout(pad=3.0)
    out_path = "coverage_comparison.png"
    plt.savefig(out_path, bbox_inches='tight')
    plt.close(fig)
    print(f"Generated {out_path}")

def generate_sankey_diagram():
    """Generate high-resolution Sankey diagram of the coordination of benefits flow."""
    # Nodes:
    # 0: Total Medical Claims (₹4,80,000)
    # 1: Aarav ACL Surgery (₹4,50,000)
    # 2: Priya PT Sessions (₹30,000)
    # 3: Primary: Plan B (HDFC ERGO)
    # 4: Primary: Plan A (Star Care)
    # 5: Aarav Remainder to Secondary
    # 6: Priya Remainder to Secondary
    # 7: Secondary: Plan A (Star Care COB)
    # 8: Secondary: Plan B (HDFC ERGO COB)
    # 9: Total Insurance Reimbursed (₹4,75,000)
    # 10: Final Patient Out-of-Pocket (₹5,000)

    label = [
        "Total Medical Claims\n₹4,80,000",          # 0
        "Aarav Surgery (CPT 29888/29881)\n₹4,50,000",# 1
        "Priya PT Sessions (CPT 97161/97110)\n₹30,000",# 2
        "Primary Payer: Plan B (HDFC ERGO)",       # 3
        "Primary Payer: Plan A (Star Care)",       # 4
        "Aarav Remainder (₹60,000)",               # 5
        "Priya Remainder (₹14,000)",               # 6
        "Secondary: Plan A (Star Care COB)",       # 7
        "Secondary: Plan B (HDFC ERGO COB)",       # 8
        "Total Insurance Paid\n₹4,75,000 (99.0%)", # 9
        "Patient Out-of-Pocket\n₹5,000 (1.0%)"     # 10
    ]

    source = [
        0, 0,       # Total Claims -> Aarav, Priya
        1, 1,       # Aarav -> Primary Plan B, Aarav Remainder
        2, 2,       # Priya -> Primary Plan A, Priya Remainder
        3,          # Primary Plan B -> Total Insurance Paid
        4,          # Primary Plan A -> Total Insurance Paid
        5,          # Aarav Remainder -> Secondary Plan A
        6, 6,       # Priya Remainder -> Secondary Plan B, Patient OOP (cap excess)
        7,          # Secondary Plan A -> Total Insurance Paid
        8           # Secondary Plan B -> Total Insurance Paid
    ]

    target = [
        1, 2,
        3, 5,
        4, 6,
        9,
        9,
        7,
        8, 10,
        9,
        9
    ]

    value = [
        450000, 30000,
        390000, 60000,
        16000, 14000,
        390000,
        16000,
        60000,
        9000, 5000,
        60000,
        9000
    ]

    color_node = [
        '#1e3a8a', '#2563eb', '#4f46e5',
        '#059669', '#0d9488',
        '#d97706', '#ea580c',
        '#0284c7', '#0891b2',
        '#16a34a', '#dc2626'
    ]

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=18,
            thickness=22,
            line=dict(color="#0f172a", width=0.8),
            label=label,
            color=color_node
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            color='rgba(148, 163, 184, 0.45)'
        )
    )])

    fig.update_layout(
        title_text="DuCO-Agent: End-to-End Dual Coverage Coordination of Benefits (COB) Flow",
        font_size=11,
        font_family="Arial",
        width=1100,
        height=620,
        paper_bgcolor="#f8fafc",
        plot_bgcolor="#ffffff"
    )

    # Save as HTML interactive
    fig.write_html("cost_flow_sankey.html")
    print("Generated cost_flow_sankey.html")

    # Also render with matplotlib for static png
    fig_static, ax = plt.subplots(figsize=(14, 7), dpi=150)
    fig_static.patch.set_facecolor('#f8fafc')
    ax.axis('off')

    # Draw visual flow representation in matplotlib
    ax.text(0.5, 0.94, 'DUAL COVERAGE COORDINATION OF BENEFITS (COB) ARCHITECTURE', ha='center', fontsize=14, weight='bold', color='#1e3a8a')
    ax.text(0.5, 0.90, 'Comprehensive Fund Allocation & Out-of-Pocket Optimization for Sen Family', ha='center', fontsize=10, color='#475569')

    # Draw Boxes
    boxes = [
        # (x, y, w, h, title, subtitle, color)
        (0.04, 0.52, 0.24, 0.30, 'Total Incurred Claims\nINR 4,80,000', '1. Aarav Surgery: ₹4,50,000\n2. Priya PT: ₹30,000', '#1e40af'),
        (0.36, 0.64, 0.28, 0.20, 'PRIMARY ADJUDICATION\nPaid: INR 4,06,000', '• Aarav (Plan B): ₹3,90,000\n• Priya (Plan A): ₹16,000', '#059669'),
        (0.36, 0.38, 0.28, 0.20, 'SECONDARY ADJUDICATION\nCOB Paid: INR 69,000', '• Aarav (Plan A): ₹60,000\n• Priya (Plan B): ₹9,000', '#0284c7'),
        (0.72, 0.58, 0.24, 0.24, 'TOTAL REIMBURSEMENT\nINR 4,75,000 (99.0%)', 'Combined Insurer 1 & 2\n(Full Financial Shield)', '#16a34a'),
        (0.72, 0.26, 0.24, 0.24, 'PATIENT OUT-OF-POCKET\nINR 5,000 (1.0%)', 'Aarav Surgery: ₹0.00\nPriya PT: ₹5,000 (Cap excess)', '#dc2626')
    ]

    for x, y, w, h, title, sub, col in boxes:
        rect = plt.Rectangle((x, y), w, h, facecolor='#ffffff', edgecolor=col, linewidth=2, transform=ax.transAxes)
        ax.add_patch(rect)
        # Header banner inside box
        banner = plt.Rectangle((x, y + h - 0.08), w, 0.08, facecolor=col, edgecolor=col, transform=ax.transAxes)
        ax.add_patch(banner)
        ax.text(x + w/2, y + h - 0.04, title, ha='center', va='center', fontsize=9.5, weight='bold', color='white', transform=ax.transAxes)
        ax.text(x + 0.02, y + (h - 0.08)/2, sub, ha='left', va='center', fontsize=8.5, color='#334155', transform=ax.transAxes)

    # Arrows
    arrow_props = dict(facecolor='#64748b', edgecolor='#475569', width=2, headwidth=8, shrink=0.05)
    ax.annotate('', xy=(0.35, 0.74), xytext=(0.28, 0.67), arrowprops=arrow_props, transform=ax.transAxes)
    ax.annotate('', xy=(0.35, 0.48), xytext=(0.28, 0.67), arrowprops=arrow_props, transform=ax.transAxes)
    ax.annotate('', xy=(0.71, 0.70), xytext=(0.64, 0.74), arrowprops=arrow_props, transform=ax.transAxes)
    ax.annotate('', xy=(0.71, 0.70), xytext=(0.64, 0.48), arrowprops=arrow_props, transform=ax.transAxes)
    ax.annotate('', xy=(0.71, 0.38), xytext=(0.64, 0.48), arrowprops=arrow_props, transform=ax.transAxes)

    # Bottom summary pill
    pill = plt.Rectangle((0.15, 0.06), 0.70, 0.12, facecolor='#ecfdf5', edgecolor='#10b981', linewidth=1.5, transform=ax.transAxes)
    ax.add_patch(pill)
    ax.text(0.5, 0.12, 'DUAL COVERAGE NET SAVINGS: INR 69,000.00', ha='center', va='center', fontsize=11, weight='bold', color='#065f46', transform=ax.transAxes)
    ax.text(0.5, 0.08, 'Without COB, Sen family would have paid ₹74,000 out-of-pocket. Dual COB lowers total family liability to ₹5,000!', ha='center', va='center', fontsize=8.5, color='#047857', transform=ax.transAxes)

    plt.savefig("cost_flow_sankey.png", bbox_inches='tight')
    plt.close(fig_static)
    print("Generated cost_flow_sankey.png")

if __name__ == "__main__":
    generate_waterfall_charts()
    generate_dual_vs_single_comparison()
    generate_sankey_diagram()
    print("All visualizations created successfully.")
