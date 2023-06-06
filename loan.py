import streamlit as st

class Customer():
    
    def __init__(self,
                 age: int,
                 income: float,
                 credit_score: int,
                 income_debt_ratio: float,
                 bankruptcy_within_last_two_years: bool,
                 has_outstanding_judgments_or_liens: bool,
                 employment_status: bool,
                 loan_amount: float,
                 loan_time_period: int):
        
        self.age = age # Deal breaker if less than 21 or above 70
        self.income = income
        self.credit_score = credit_score # Deal breaker if less than 580
        self.income_debt_ratio = income_debt_ratio
        self.bankruptcy_within_last_two_years = bankruptcy_within_last_two_years # Deal breaker if True
        self.has_outstanding_judgments_or_liens = has_outstanding_judgments_or_liens # Deal breaker if True
        self.employment_status = employment_status # Deal breaker if False
        self.loan_amount = loan_amount
        self.loan_time_period = loan_time_period


def calculate_loan(customer: Customer):
    # Deal breakers
    if customer.credit_score < 580 or customer.age < 21 or customer.age > 70 or customer.bankruptcy_within_last_two_years is True or customer.has_outstanding_judgments_or_liens is True or customer.employment_status is False:
        return False, None
    
    # Assigning weightage to parameters
    weightage_credit_score = 0.3
    weightage_income_debt_ratio = 0.2
    weightage_income = 0.15
    weightage_loan_amount = 0.2
    weightage_loan_time_period = 0.15
    
    # Calculating weighted scores
    weighted_credit_score = weightage_credit_score * customer.credit_score
    weighted_income_debt_ratio = weightage_income_debt_ratio * (1 - customer.income_debt_ratio)
    weighted_income = weightage_income * (customer.income / 10000)  # Scaling income weightage for better proportion
    weighted_loan_amount = weightage_loan_amount * (1 - customer.loan_amount / customer.income)
    weighted_loan_time_period = weightage_loan_time_period * (1 - customer.loan_time_period / 60)  # Assuming max loan time period is 60 months
    
    # Calculating total weighted score
    total_weighted_score = weighted_credit_score + weighted_income_debt_ratio + weighted_income + weighted_loan_amount + weighted_loan_time_period
    
    # Determining loan status based on the total weighted score
    if total_weighted_score >= 0.8:
        return True, 6
    elif total_weighted_score >= 0.6:
        return True, 8
    elif total_weighted_score >= 0.4:
        return True, 10
    else:
        return False, None

# Create the Streamlit app
def main():
    bg = """<div style='background-color:white; padding:13px'>
              <h1 style='color:black'>Financial Credit Scoring App</h1>
       </div>"""
    st.markdown(bg, unsafe_allow_html=True)
    left, right = st.columns((2,2))
    age = right.number_input('Age')
    employment_status = left.selectbox('Employed', ('Yes', 'No'))
    has_outstanding_judgments_or_liens = left.selectbox('Has outstanding judgements or liens', ('Yes', 'No'))
    bankruptcy_within_last_two_years = left.selectbox('Has bankruptcy within the last two years', ('Yes', 'No'))
    applicant_income = right.number_input('Applicant Income')
    loanAmount = right.number_input('Loan Amount')
    loan_amount_term = left.number_input('Loan Tenor (in months)')
    creditscore = right.number_input('Credit Score')
    income_to_debt_ratio = right.number_input('Income to Debt Ratio', 0.0, 1.0)
    button = st.button('Calculate')
    # if button is clicked
    if button:
        # make prediction
        result = calculate_loan(Customer(age, applicant_income, creditscore, income_to_debt_ratio, bankruptcy_within_last_two_years, has_outstanding_judgments_or_liens, employment_status, loanAmount, loan_amount_term))
        st.success(f'You are {result} for the loan')

# Run the app
if __name__ == "__main__":
    main()
