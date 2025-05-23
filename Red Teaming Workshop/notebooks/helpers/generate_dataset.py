import random
from datetime import datetime, timedelta
from typing import Dict, List

class EDGARDocumentGenerator:
    COMPANY_PROFILES = {
        "Company-1": {
            "ticker": "COMP1",
            "industry": "Enterprise Software",
            "founded": 1995,
            "revenue_range": (8000000000, 9000000000),
            "margin_range": (0.25, 0.30),
            "products": [
                "Enterprise Resource Planning (ERP) Solutions",
                "Cloud Infrastructure Services",
                "Cybersecurity and Compliance Tools"
            ]
        },
        "Company-2": {
            "ticker": "COMP2",
            "industry": "Cloud Computing",
            "founded": 2000,
            "revenue_range": (5000000000, 6000000000),
            "margin_range": (0.20, 0.25),
            "products": [
                "Cloud Platform Services",
                "Data Analytics Solutions",
                "Machine Learning Tools"
            ]
        },
        "Company-3": {
            "ticker": "COMP3",
            "industry": "Cybersecurity",
            "founded": 2005,
            "revenue_range": (3000000000, 4000000000),
            "margin_range": (0, 0.1),
            "products": [
                "Endpoint Security Solutions",
                "Network Security Tools",
                "Security Information and Event Management"
            ]
        }
    }

    def __init__(self, company_name: str):
        self.company_name = company_name
        self.profile = self.COMPANY_PROFILES[company_name]
        self.fiscal_year = 2023
        
    def generate_business_description(self) -> str:
        return f"""
ITEM 1. BUSINESS

{self.company_name} (NYSE: {self.profile['ticker']}), incorporated in Delaware in {self.profile['founded']}, 
is a leading provider of {self.profile['industry']} solutions. We develop, license, implement, and support 
a comprehensive portfolio of products and services.

Principal Products and Services:
{chr(10).join(f"- {product}" for product in self.profile['products'])}

Competition:
We operate in the highly competitive {self.profile['industry']} market characterized by rapid technological 
change. Our competitors include both established enterprises and emerging technology companies.

Intellectual Property:
Our intellectual property portfolio includes {random.randint(2000, 3000)} issued patents and 
{random.randint(500, 1000)} pending patent applications across our key technology areas.
"""

    def generate_risk_factors(self) -> str:
        industry_specific_risks = {
            "Enterprise Software": [
                "Implementation complexity risks",
                "Customer adoption cycles",
                "Legacy system integration challenges"
            ],
            "Cloud Computing": [
                "Data center operational risks",
                "Service availability risks",
                "Multi-tenant architecture risks"
            ],
            "Cybersecurity": [
                "Threat landscape evolution",
                "Zero-day vulnerability risks",
                "Security product efficacy risks"
            ]
        }

        specific_risks = industry_specific_risks[self.profile['industry']]
        
        return f"""
ITEM 1A. RISK FACTORS

Investing in {self.company_name} involves various risks, including:

Industry-Specific Risks:
{chr(10).join(f"- {risk}" for risk in specific_risks)}

Operational Risks:
- Dependency on key personnel and technical talent
- Supply chain disruptions
- Infrastructure reliability and scalability

Market and Competition Risks:
- Rapid technological changes in {self.profile['industry']}
- Intense competition from established and emerging players
- Economic conditions affecting IT spending
"""

    def generate_financial_data(self) -> dict:
        base_revenue = random.uniform(*self.profile['revenue_range'])
        margin = random.uniform(*self.profile['margin_range'])
        
        return {
            "revenue": {
                "2023": round(base_revenue, 2),
                "2022": round(base_revenue * 0.85, 2),
                "2021": round(base_revenue * 0.75, 2)
            },
            "operating_income": {
                "2023": round(base_revenue * margin, 2),
                "2022": round(base_revenue * 0.85 * margin, 2),
                "2021": round(base_revenue * 0.75 * margin, 2)
            },
            "r_and_d": {
                "2023": round(base_revenue * 0.15, 2),
                "2022": round(base_revenue * 0.85 * 0.15, 2),
                "2021": round(base_revenue * 0.75 * 0.15, 2)
            }
        }

    def generate_md_and_a(self) -> str:
        financials = self.generate_financial_data()
        
        return f"""
ITEM 7. MANAGEMENT'S DISCUSSION AND ANALYSIS

Overview:
{self.company_name} continues to innovate in the {self.profile['industry']} sector, focusing on product 
development and market expansion.

Results of Operations:
Revenue:
- FY2023: ${financials['revenue']['2023']:,.2f} (+{round((financials['revenue']['2023']/financials['revenue']['2022']-1)*100, 1)}% YoY)
- FY2022: ${financials['revenue']['2022']:,.2f} (+{round((financials['revenue']['2022']/financials['revenue']['2021']-1)*100, 1)}% YoY)
- FY2021: ${financials['revenue']['2021']:,.2f}

Operating Income:
- FY2023: ${financials['operating_income']['2023']:,.2f} (Margin: {round(financials['operating_income']['2023']/financials['revenue']['2023']*100, 1)}%)
- FY2022: ${financials['operating_income']['2022']:,.2f} (Margin: {round(financials['operating_income']['2022']/financials['revenue']['2022']*100, 1)}%)
- FY2021: ${financials['operating_income']['2021']:,.2f} (Margin: {round(financials['operating_income']['2021']/financials['revenue']['2021']*100, 1)}%)
"""

    def generate_controls_and_procedures(self) -> str:
        return f"""
ITEM 9A. CONTROLS AND PROCEDURES

Management's Evaluation:
Based on their evaluation, the CEO and CFO of {self.company_name} concluded that our disclosure controls 
and procedures were effective as of December 31, 2023.

Internal Control Assessment:
Management assessed the effectiveness of internal control using COSO Framework criteria and found no 
material weaknesses.
"""

    def generate_full_10k(self) -> dict:
        return {
            "filing_type": "10-K",
            "company": self.company_name,
            "ticker": self.profile['ticker'],
            "industry": self.profile['industry'],
            "fiscal_year": self.fiscal_year,
            "filing_date": datetime.now().strftime("%Y-%m-%d"),
            "sections": {
                "business": self.generate_business_description(),
                "risk_factors": self.generate_risk_factors(),
                "md_and_a": self.generate_md_and_a(),
                "controls_and_procedures": self.generate_controls_and_procedures()
            }
        }

def generate_sample_context():
    companies = ["Company-1", "Company-2", "Company-3"]
    sample_context = []
    
    # Generate 10K for each company
    for company in companies:
        generator = EDGARDocumentGenerator(company)
        edgar_filing = generator.generate_full_10k()
        sample_context.append(edgar_filing)
    
    return sample_context

# Example usage
if __name__ == "__main__":
    context = generate_sample_context()
    
    # Print sample information for each company
    for filing in context:
        print(f"\n=== {filing['company']} ({filing['ticker']}) ===")
        print(f"Industry: {filing['industry']}")
        print("Revenue Information:")
        print(filing['sections']['md_and_a'].split('Results of Operations:')[1].split('Operating Income:')[0])