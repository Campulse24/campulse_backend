from sqlmodel import Session, select
from app.db.session import engine, create_db_and_tables
from app.models.models import Opportunity, Tutor, OpportunityCategory

def create_initial_data():
    create_db_and_tables()
    with Session(engine) as session:
        # Check if data exists
        if session.exec(select(Opportunity)).first():
            print("Data already exists.")
            return

        # Opportunities
        opportunities = [
            Opportunity(
                title="Frontend Developer Intern",
                summary="Remote internship for React developers.",
                category=OpportunityCategory.GIG,
                link="https://example.com/job1"
            ),
            Opportunity(
                title="NNPC Scholarship 2025",
                summary="Full tuition scholarship for engineering students.",
                category=OpportunityCategory.SCHOLARSHIP,
                link="https://example.com/scholarship1"
            ),
            Opportunity(
                title="Math Tutor Needed",
                summary="Help a high school student with Calculus.",
                category=OpportunityCategory.TUTOR,
                link="https://example.com/tutor1"
            ),
             Opportunity(
                title="50% Off Jumia Books",
                summary="Back to school promo.",
                category=OpportunityCategory.DEAL,
                link="https://example.com/deal1"
            ),
        ]
        
        for opp in opportunities:
            session.add(opp)

        # Tutors
        tutors = [
            Tutor(
                name="David Okeke",
                course="MTH 101",
                price_range="N2000/hr",
                rating=4.5,
                whatsapp_contact="+2348012345678"
            ),
            Tutor(
                name="Sarah Musa",
                course="CHM 102",
                price_range="N1500/hr",
                rating=4.8,
                whatsapp_contact="+2348098765432"
            ),
        ]
        
        for tutor in tutors:
            session.add(tutor)
            
        session.commit()
        print("Initial data created.")

if __name__ == "__main__":
    create_initial_data()
