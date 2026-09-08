"""
Pre-indexed fact datasets for Delhivery and India Macroeconomy starter datasets.
Provides grounded facts with exact page numbers, quotes, and contexts.
"""

from typing import List, Dict
from app.core.models import Fact, Evidence, FactContext, DocumentMetadata


def get_delhivery_documents() -> List[DocumentMetadata]:
    return [
        DocumentMetadata(
            id="delhivery-prospectus",
            filename="01-delhivery-prospectus-2022-excerpt.pdf",
            title="Delhivery IPO Prospectus (May 2022)",
            total_pages=100,
            dataset_group="delhivery",
            file_size_bytes=1597612,
            facts_count=8,
            indexed_at="2024-05-14"
        ),
        DocumentMetadata(
            id="delhivery-ar24",
            filename="02-delhivery-annual-report-fy24-excerpt.pdf",
            title="Delhivery Annual Report FY 2023-24",
            total_pages=100,
            dataset_group="delhivery",
            file_size_bytes=6679023,
            facts_count=12,
            indexed_at="2024-08-01"
        ),
        DocumentMetadata(
            id="delhivery-ep24",
            filename="03-delhivery-q4-fy24-earnings-presentation.pdf",
            title="Delhivery Q4 FY24 Earnings Presentation (May 2024)",
            total_pages=27,
            dataset_group="delhivery",
            file_size_bytes=1988328,
            facts_count=10,
            indexed_at="2024-05-17"
        )
    ]


def get_delhivery_facts() -> List[Fact]:
    facts = []

    # -------------------------------------------------------------
    # 1. Delhivery Prospectus Facts
    # -------------------------------------------------------------
    facts.append(Fact(
        id="del-pr-cin",
        entity="Delhivery Limited",
        attribute="Corporate Identity Number (CIN)",
        value="U63090DL2011PLC221234",
        category="Governance",
        context=FactContext(
            temporal_period="Pre-IPO (As of May 2022)",
            scope="Corporate Registry",
            accounting_or_source_note="Unlisted Public Company ('U' prefix)"
        ),
        evidence=Evidence(
            document_id="delhivery-prospectus",
            document_name="01-delhivery-prospectus-2022-excerpt.pdf",
            page_number=1,
            quote="CORPORATE IDENTITY NUMBER: U63090DL2011PLC221234",
            surrounding_context="DELHIVERY LIMITED | Corporate Identity Number: U63090DL2011PLC221234",
            section_title="Cover Page"
        ),
        confidence=0.99
    ))

    facts.append(Fact(
        id="del-pr-reg-addr",
        entity="Delhivery Limited",
        attribute="Registered Office Address",
        value="N24-N34, S24-S34, Air Cargo Logistics Centre-II, Opposite Gate 6 Cargo Terminal, Indira Gandhi International Airport, New Delhi 110037 Delhi, India",
        category="Governance",
        context=FactContext(
            scope="Statutory Registered Office",
            unit="Postal Address"
        ),
        evidence=Evidence(
            document_id="delhivery-prospectus",
            document_name="01-delhivery-prospectus-2022-excerpt.pdf",
            page_number=1,
            quote="REGISTERED OFFICE: N24-N34, S24-S34, Air Cargo Logistics Centre-II, Opposite Gate 6 Cargo Terminal, Indira Gandhi International Airport, New Delhi 110037 Delhi, India",
            surrounding_context="REGISTERED OFFICE: N24-N34, S24-S34, Air Cargo Logistics Centre-II",
            section_title="Cover Page"
        ),
        confidence=0.99
    ))

    facts.append(Fact(
        id="del-pr-corp-addr",
        entity="Delhivery Limited",
        attribute="Corporate Headquarters Postal PIN Code",
        value="Plot 5, Sector 44, Gurugram 122002 Haryana, India",
        category="Governance",
        context=FactContext(
            scope="Corporate Headquarters Address",
            unit="Postal Code"
        ),
        evidence=Evidence(
            document_id="delhivery-prospectus",
            document_name="01-delhivery-prospectus-2022-excerpt.pdf",
            page_number=1,
            quote="CORPORATE OFFICE: Plot 5, Sector 44, Gurugram 122002 Haryana, India",
            surrounding_context="CORPORATE OFFICE: Plot 5, Sector 44, Gurugram 122002 Haryana, India",
            section_title="Cover Page"
        ),
        confidence=0.99
    ))

    facts.append(Fact(
        id="del-pr-inc-date",
        entity="Delhivery Limited",
        attribute="Date of Incorporation",
        value="June 22, 2011",
        category="Governance",
        context=FactContext(
            temporal_period="Historical",
            scope="Original Incorporation as SSN Logistics"
        ),
        evidence=Evidence(
            document_id="delhivery-prospectus",
            document_name="01-delhivery-prospectus-2022-excerpt.pdf",
            page_number=30,
            quote="Our Company was incorporated as 'SSN Logistics Private Limited'... pursuant to a certificate of incorporation issued by the RoC on June 22, 2011.",
            surrounding_context="Brief History of our Company",
            section_title="Corporate History"
        ),
        confidence=0.99
    ))

    facts.append(Fact(
        id="del-pr-rev-fy21",
        entity="Delhivery Limited",
        attribute="Revenue from operations",
        value="₹36,465.27 million",
        normalized_value=3646.53,
        normalized_unit="INR_CR",
        category="Financial",
        context=FactContext(
            temporal_period="FY 2020-21 (Year ended March 31, 2021)",
            scope="Restated Consolidated",
            unit="INR Million"
        ),
        evidence=Evidence(
            document_id="delhivery-prospectus",
            document_name="01-delhivery-prospectus-2022-excerpt.pdf",
            page_number=17,
            quote="Revenue from contract with customers: For the year ended March 31, 2021: 36,465.27 (in ₹ million)",
            surrounding_context="Restated Summary Consolidated Profit and Loss Data",
            section_title="Summary Financial Statements"
        ),
        confidence=0.98
    ))

    # -------------------------------------------------------------
    # 2. Delhivery Annual Report FY24 Facts
    # -------------------------------------------------------------
    facts.append(Fact(
        id="del-ar-cin",
        entity="Delhivery Limited",
        attribute="Corporate Identity Number (CIN)",
        value="L63090DL2011PLC221234",
        category="Governance",
        context=FactContext(
            temporal_period="Post-IPO (FY 2023-24)",
            scope="Corporate Registry",
            accounting_or_source_note="Listed Public Company ('L' prefix)"
        ),
        evidence=Evidence(
            document_id="delhivery-ar24",
            document_name="02-delhivery-annual-report-fy24-excerpt.pdf",
            page_number=51,
            quote="Corporate Identity Number (CIN) of the Listed Entity: L63090DL2011PLC221234",
            surrounding_context="BRSR Section A: General Disclosures",
            section_title="Business Responsibility & Sustainability Report"
        ),
        confidence=0.99
    ))

    facts.append(Fact(
        id="del-ar-reg-addr",
        entity="Delhivery Limited",
        attribute="Registered Office Address",
        value="N24-N34, S24-S34, Air Cargo Logistics Centre-II, Opposite Gate 6 Cargo Terminal, IGI Airport, New Delhi 110037",
        category="Governance",
        context=FactContext(
            scope="Statutory Registered Office",
            unit="Postal Address"
        ),
        evidence=Evidence(
            document_id="delhivery-ar24",
            document_name="02-delhivery-annual-report-fy24-excerpt.pdf",
            page_number=51,
            quote="Registered office address: N24-N34, S24-S34, Air Cargo Logistics Centre-II, Opposite Gate 6 Cargo Terminal, IGI Airport, New Delhi 110037",
            surrounding_context="BRSR Section A: General Disclosures",
            section_title="Business Responsibility & Sustainability Report"
        ),
        confidence=0.99
    ))

    facts.append(Fact(
        id="del-ar-corp-addr",
        entity="Delhivery Limited",
        attribute="Corporate Headquarters Postal PIN Code",
        value="Plot No. 5, Sector 44, Gurugram, Haryana 122001",
        category="Governance",
        context=FactContext(
            scope="Corporate Headquarters Address",
            unit="Postal Code"
        ),
        evidence=Evidence(
            document_id="delhivery-ar24",
            document_name="02-delhivery-annual-report-fy24-excerpt.pdf",
            page_number=51,
            quote="Corporate address: Plot No. 5, Sector 44, Gurugram, Haryana 122001",
            surrounding_context="BRSR Section A: General Disclosures",
            section_title="Business Responsibility & Sustainability Report"
        ),
        confidence=0.99
    ))

    facts.append(Fact(
        id="del-ar-workforce",
        entity="Delhivery Limited",
        attribute="Workforce Strength",
        value="98,135 personnel",
        normalized_value=98135.0,
        normalized_unit="PERSONNEL",
        category="Operational",
        context=FactContext(
            temporal_period="As of March 31, 2024",
            scope="Total Workforce (includes permanent employees, contractual workers, and last-mile partner agents)",
            unit="Personnel Count",
            accounting_or_source_note="Annual Report 'Delhivery in Numbers' (Footnote 1, 5)"
        ),
        evidence=Evidence(
            document_id="delhivery-ar24",
            document_name="02-delhivery-annual-report-fy24-excerpt.pdf",
            page_number=2,
            quote="98,135(1,5) Workforce strength | (1) As of March 31, 2024 (5) Includes permanent employees, contractual workers and last mile deliver partner agents",
            surrounding_context="Delhivery In Numbers | 18,793 Pin codes covered",
            section_title="Delhivery In Numbers"
        ),
        confidence=0.99
    ))

    facts.append(Fact(
        id="del-ar-infra-sort",
        entity="Delhivery Limited",
        attribute="Automated Sort Centers and Gateways Count",
        value="29 automated sort centres and 111 gateways",
        category="Operational",
        context=FactContext(
            temporal_period="As of March 31, 2024",
            scope="All-India Infrastructure Network",
            unit="Facility Count"
        ),
        evidence=Evidence(
            document_id="delhivery-ar24",
            document_name="02-delhivery-annual-report-fy24-excerpt.pdf",
            page_number=22,
            quote="Your Company operated 29 fully and semi automated sortation centres and 111 gateways across India as of March 31, 2024.",
            surrounding_context="Rated Automated Sort Capacity of 7.1 million shipments per day",
            section_title="Directors' Report"
        ),
        confidence=0.99
    ))

    facts.append(Fact(
        id="del-ar-pin-codes",
        entity="Delhivery Limited",
        attribute="PIN Code Reach",
        value="18,793 PIN codes",
        normalized_value=18793.0,
        normalized_unit="COUNT",
        category="Operational",
        context=FactContext(
            temporal_period="As of March 31, 2024",
            scope="Pan-India Postal Coverage",
            unit="Postal Index Numbers"
        ),
        evidence=Evidence(
            document_id="delhivery-ar24",
            document_name="02-delhivery-annual-report-fy24-excerpt.pdf",
            page_number=2,
            quote="18,793(1) Pin codes covered | (1) As of March 31, 2024",
            surrounding_context="Delhivery In Numbers",
            section_title="Delhivery In Numbers"
        ),
        confidence=0.99
    ))

    facts.append(Fact(
        id="del-ar-rev-cons-fy24",
        entity="Delhivery Limited",
        attribute="Revenue from operations",
        value="₹81,415.38 million",
        normalized_value=8141.54,
        normalized_unit="INR_CR",
        category="Financial",
        context=FactContext(
            temporal_period="FY 2023-24 (Year ended March 31, 2024)",
            scope="Consolidated",
            unit="INR Million",
            accounting_or_source_note="Audited Financial Statements (Ind AS)"
        ),
        evidence=Evidence(
            document_id="delhivery-ar24",
            document_name="02-delhivery-annual-report-fy24-excerpt.pdf",
            page_number=22,
            quote="Revenue from Operations | Consolidated – FY ended March 31, 2024: 81,415.38",
            surrounding_context="Key highlights of the financial performance of your Company for the FY24",
            section_title="Directors' Report - Financial Performance"
        ),
        confidence=0.99
    ))

    facts.append(Fact(
        id="del-ar-rev-stan-fy24",
        entity="Delhivery Limited",
        attribute="Revenue from operations",
        value="₹74,540.82 million",
        normalized_value=7454.08,
        normalized_unit="INR_CR",
        category="Financial",
        context=FactContext(
            temporal_period="FY 2023-24 (Year ended March 31, 2024)",
            scope="Standalone",
            unit="INR Million",
            accounting_or_source_note="Audited Standalone Financial Statements"
        ),
        evidence=Evidence(
            document_id="delhivery-ar24",
            document_name="02-delhivery-annual-report-fy24-excerpt.pdf",
            page_number=22,
            quote="Revenue from Operations | Standalone – FY ended March 31, 2024: 74,540.82",
            surrounding_context="The revenue from operations on standalone basis for FY24 stood at ₹ 74,540.82 million",
            section_title="Directors' Report - Financial Performance"
        ),
        confidence=0.99
    ))

    # -------------------------------------------------------------
    # 3. Delhivery Q4 FY24 Earnings Presentation Facts
    # -------------------------------------------------------------
    facts.append(Fact(
        id="del-ep-team-size",
        entity="Delhivery Limited",
        attribute="Team Size",
        value="63,713 employees",
        normalized_value=63713.0,
        normalized_unit="PERSONNEL",
        category="Operational",
        context=FactContext(
            temporal_period="As of Q4 FY24 (March 31, 2024)",
            scope="Core Team (permanent employees and contractual workers, excluding partner agents)",
            unit="Personnel Count",
            accounting_or_source_note="Earnings Presentation Operating Metrics (Footnote 4, 5)"
        ),
        evidence=Evidence(
            document_id="delhivery-ep24",
            document_name="03-delhivery-q4-fy24-earnings-presentation.pdf",
            page_number=8,
            quote="Team size(4): 63,713 | Partner agents(5): 34,422",
            surrounding_context="(4) Includes permanent employees and contractual workers (excluding partner agents, daily wage manpower)",
            section_title="Key Operating Metrics Table"
        ),
        confidence=0.99
    ))

    facts.append(Fact(
        id="del-ep-infra-sort",
        entity="Delhivery Limited",
        attribute="Automated Sort Centers and Gateways Count",
        value="29 automated sort centers and 111 gateways",
        category="Operational",
        context=FactContext(
            temporal_period="As of end of Q4 FY24 (March 31, 2024)",
            scope="Operating Metrics Infrastructure",
            unit="Facility Count"
        ),
        evidence=Evidence(
            document_id="delhivery-ep24",
            document_name="03-delhivery-q4-fy24-earnings-presentation.pdf",
            page_number=8,
            quote="Gateways: 111 | Automated sort centers: 29",
            surrounding_context="Key operating metrics as of end of / for the period Q4 FY24",
            section_title="Key Operating Metrics Table"
        ),
        confidence=0.99
    ))

    facts.append(Fact(
        id="del-ep-pin-codes",
        entity="Delhivery Limited",
        attribute="PIN Code Reach",
        value="18,793 PIN codes",
        normalized_value=18793.0,
        normalized_unit="COUNT",
        category="Operational",
        context=FactContext(
            temporal_period="As of Q4 FY24 (March 31, 2024)",
            scope="Pin-code reach out of 19,300 per India Post",
            unit="Postal Index Numbers"
        ),
        evidence=Evidence(
            document_id="delhivery-ep24",
            document_name="03-delhivery-q4-fy24-earnings-presentation.pdf",
            page_number=8,
            quote="Pin-code reach(1) Q4 FY24: 18,793 | (1) Out of 19,300 Pin-codes as per India Post",
            surrounding_context="Key operating metrics as of end of / for the period",
            section_title="Key Operating Metrics Table"
        ),
        confidence=0.99
    ))

    facts.append(Fact(
        id="del-ep-rev-fy24",
        entity="Delhivery Limited",
        attribute="Revenue from services",
        value="₹8,142 Cr",
        normalized_value=8142.0,
        normalized_unit="INR_CR",
        category="Financial",
        context=FactContext(
            temporal_period="FY 2023-24 (Full Year)",
            scope="Consolidated Services",
            unit="INR Crore",
            accounting_or_source_note="Excludes revenue from traded goods"
        ),
        evidence=Evidence(
            document_id="delhivery-ep24",
            document_name="03-delhivery-q4-fy24-earnings-presentation.pdf",
            page_number=6,
            quote="₹8,142 Cr FY24 revenue from services | YoY: 12.7%",
            surrounding_context="India's largest integrated logistics platform - FY24 Performance Highlights",
            section_title="Executive Overview"
        ),
        confidence=0.99
    ))

    facts.append(Fact(
        id="del-ep-rev-q4fy24",
        entity="Delhivery Limited",
        attribute="Revenue from services",
        value="₹2,076 Cr",
        normalized_value=2076.0,
        normalized_unit="INR_CR",
        category="Financial",
        context=FactContext(
            temporal_period="Q4 FY24 (Three Months ended March 31, 2024)",
            scope="Consolidated Services (Quarterly)",
            unit="INR Crore"
        ),
        evidence=Evidence(
            document_id="delhivery-ep24",
            document_name="03-delhivery-q4-fy24-earnings-presentation.pdf",
            page_number=7,
            quote="₹2,076 Cr Q4 FY24 revenue from services | YoY: 11.6%",
            surrounding_context="Q4 FY24 Highlights",
            section_title="Quarterly Overview"
        ),
        confidence=0.99
    ))

    return facts


def get_macro_documents() -> List[DocumentMetadata]:
    return [
        DocumentMetadata(
            id="macro-survey25",
            filename="01-india-economic-survey-2024-25-excerpt.pdf",
            title="Economic Survey 2024-25 (Ministry of Finance)",
            total_pages=89,
            dataset_group="india-macroeconomy",
            file_size_bytes=3920928,
            facts_count=6,
            indexed_at="2025-01-31"
        ),
        DocumentMetadata(
            id="macro-rbi25",
            filename="02-rbi-annual-report-2024-25-excerpt.pdf",
            title="RBI Annual Report 2024-25",
            total_pages=100,
            dataset_group="india-macroeconomy",
            file_size_bytes=1507769,
            facts_count=6,
            indexed_at="2025-05-30"
        ),
        DocumentMetadata(
            id="macro-imf25",
            filename="03-imf-india-2025-article-iv-excerpt.pdf",
            title="IMF India 2025 Article IV Consultation",
            total_pages=95,
            dataset_group="india-macroeconomy",
            file_size_bytes=4305245,
            facts_count=6,
            indexed_at="2025-11-25"
        )
    ]


def get_macro_facts() -> List[Fact]:
    facts = []

    # 1. Economic Survey Facts
    facts.append(Fact(
        id="macro-es-gdp-fy25",
        entity="Indian Economy",
        attribute="Real GDP Growth Rate",
        value="6.4%",
        normalized_value=6.4,
        normalized_unit="PERCENT",
        category="Macroeconomic",
        context=FactContext(
            temporal_period="FY 2024-25 (FY25)",
            scope="National Economy",
            unit="Percentage",
            accounting_or_source_note="First Advance Estimates (MoSPI)"
        ),
        evidence=Evidence(
            document_id="macro-survey25",
            document_name="01-india-economic-survey-2024-25-excerpt.pdf",
            page_number=4,
            quote="As per the first advance estimates of national accounts, India’s real GDP is estimated to grow by 6.4 per cent in FY25.",
            surrounding_context="Chapter 1: State of the Economy: Getting Back into the Fast Lane",
            section_title="State of the Economy"
        ),
        confidence=0.99
    ))

    # 2. RBI Annual Report Facts
    facts.append(Fact(
        id="macro-rbi-gdp-fy25",
        entity="Indian Economy",
        attribute="Real GDP Growth Rate",
        value="6.5%",
        normalized_value=6.5,
        normalized_unit="PERCENT",
        category="Macroeconomic",
        context=FactContext(
            temporal_period="FY 2024-25 (FY25)",
            scope="National Economy",
            unit="Percentage",
            accounting_or_source_note="Second Advance / Provisional Estimates (NSO)"
        ),
        evidence=Evidence(
            document_id="macro-rbi25",
            document_name="02-rbi-annual-report-2024-25-excerpt.pdf",
            page_number=24,
            quote="Table II.2.1: Real GDP Growth | 2024-25: 6.5 per cent (Source: NSO)",
            surrounding_context="Economic Review - Consumption & Investment",
            section_title="Real GDP Growth Table"
        ),
        confidence=0.99
    ))

    facts.append(Fact(
        id="macro-rbi-gdp-fy24",
        entity="Indian Economy",
        attribute="Real GDP Growth Rate",
        value="9.2%",
        normalized_value=9.2,
        normalized_unit="PERCENT",
        category="Macroeconomic",
        context=FactContext(
            temporal_period="FY 2023-24 (2023-24)",
            scope="National Economy",
            unit="Percentage",
            accounting_or_source_note="Revised Estimates (NSO)"
        ),
        evidence=Evidence(
            document_id="macro-rbi25",
            document_name="02-rbi-annual-report-2024-25-excerpt.pdf",
            page_number=24,
            quote="Table II.2.1: Real GDP Growth | 2023-24: 9.2 per cent (Source: NSO)",
            surrounding_context="Economic Review - National Accounts",
            section_title="Real GDP Growth Table"
        ),
        confidence=0.99
    ))

    # 3. IMF Article IV Facts
    facts.append(Fact(
        id="macro-imf-gdp-fy25",
        entity="Indian Economy",
        attribute="Real GDP Growth Rate",
        value="6.5%",
        normalized_value=6.5,
        normalized_unit="PERCENT",
        category="Macroeconomic",
        context=FactContext(
            temporal_period="FY 2024-25 (FY2024/25)",
            scope="National Economy",
            unit="Percentage",
            accounting_or_source_note="IMF Staff Assessment basis updated NSO data"
        ),
        evidence=Evidence(
            document_id="macro-imf25",
            document_name="03-imf-india-2025-article-iv-excerpt.pdf",
            page_number=10,
            quote="Growth has been robust (Figure 2). India’s real GDP grew by 6.5 percent in FY2024/25.",
            surrounding_context="Staff Report for the 2025 Article IV Consultation",
            section_title="Recent Economic Developments"
        ),
        confidence=0.99
    ))

    facts.append(Fact(
        id="macro-imf-gdp-fy24",
        entity="Indian Economy",
        attribute="Real GDP Growth Rate",
        value="9.2%",
        normalized_value=9.2,
        normalized_unit="PERCENT",
        category="Macroeconomic",
        context=FactContext(
            temporal_period="FY 2023-24 (2023/24)",
            scope="National Economy",
            unit="Percentage",
            accounting_or_source_note="Table 1: Selected Social and Economic Indicators"
        ),
        evidence=Evidence(
            document_id="macro-imf25",
            document_name="03-imf-india-2025-article-iv-excerpt.pdf",
            page_number=5,
            quote="Table 1. India: Selected Social and Economic Indicators | Real GDP (at market prices) 2023/24: 9.2%",
            surrounding_context="Selected Economic Indicators Table",
            section_title="Executive Indicators"
        ),
        confidence=0.99
    ))

    return facts
