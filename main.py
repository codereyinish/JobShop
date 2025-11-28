"""
================================================================================
Company: LocalWork Connect - Community Employment Agency
================================================================================


COMPANY DESCRIPTION:
LocalWork Connect is a community-based employment agency that serves as a bridge
between immigrant workers seeking minimum-wage cash jobs and local businesses
needing short-term labor. The agency specializes in connecting day laborers with
opportunities in restaurants, retail stores, cleaning services, and construction
sites. Workers pay a small commission fee to the agency when successfully placed
in a job, and employers can post available positions through the agency or
authorized agents.



WHY I CHOSE THIS COMPANY:
I chose to create a data management system for an informal employment agency
that connects immigrant workers seeking minimum-wage cash jobs with local
employers posting short-term gigs. Having observed how disorganized this sector
is in real life, I recognized both a business opportunity and a chance to help
an underserved community. This project builds on my previous database coursework
where I explored similar concepts using Oracle APEX, making the transition to
a Python-based system intuitive and meaningful.

PROGRAM PURPOSE:
This program digitizes the daily operations of the employment agency by allowing
staff to register workers, post available job opportunities, record successful
placements, calculate agency commission, and generate comprehensive daily reports.
The system brings structure and efficiency to a sector that traditionally relies
on word-of-mouth and informal record-keeping.

PROGRAM DESIGN APPROACH:
This project functions as a "calculator-style" system where each operation
(worker registration, job posting, commission calculation) works independently
with manual data entry. The focus is on implementing robust input validation
(type checks, constraint checks, format checks) in the application layer before
data storage. This approach mirrors industry best practice where validation
happens early to catch errors fast and provide user-friendly feedback.

PROGRAM PURPOSE:
This system digitizes the agency's daily operations by allowing staff to register
workers, register employer companies, post job opportunities, record successful
placements, calculate agency commission earnings, and generate comprehensive
daily reports. The program brings structure and efficiency to a sector that
traditionally relies on word-of-mouth and informal record-keeping.

FUTURE VISION:
While this version stores data in text files, the validation logic and modular
structure are designed to transition smoothly into a web application using
FastAPI and PostgreSQL. The current Python validation (Layer 1) will remain
identical, with database constraints (Layer 2) added as a safety net for data
integrity - demonstrating the "defense-in-depth" validation strategy used in
production systems.

================================================================================
Author: Manish Bista
Course: COM-250-B01
Date: Fall 2025
================================================================================
"""



# =============================================================================
# IMPORTS
# =============================================================================
from datetime import datetime

# =============================================================================
# GLOBAL VARIABLES
# =============================================================================
total_workers_registered = 0      # Count of workers registered today
total_companies_registered = 0
total_jobs_posted = 0


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_phone_number():
    """
    Validate phone number input -- must be exactly 10 digits
    Uses a while loop to keep asking until the valid input is provided
    :return:
        str: A valid 10-digit number
    """
    while True:
        phone = input("Enter phone number (10 digits): ").strip()

        #Check if empty
        if not phone:
            print("❌ Error: Phone number cannot be empty. \n")
            continue

        #Check if all characters are digits
        if not phone.isdigit():
            print("❌ Error: Phone number must contain only digits. \n")
            continue

        # Check if exactly 10 digits
        if len(phone) != 10:
                print(f"❌ Error: Phone number must be exactly 10 digits. You entered {len(phone)} digits.\n")
                continue

        # If all checks pass, return the valid phone number
        return phone

def validate_positive_number(prompt, min_value, max_value):
    """
     Validates numeric input within a specified range
     Uses a while loop to keep asking until valid input is provided

     Parameters:
        :param prompt(str): Message to display to the user
        :param min_value(float):Minimum acceptable value
        :param max_value(float): Maximum acceptable value

    :Returns:
        float: A valid number within the specified range
    """

    while True:
        try:
            value = float(input(prompt))

            #Check if within the range:
            if value<min_value:
                print(f"❌ Value must be at least ${min_value}.\n")
                continue
            if value> max_value:
                print(f"❌Value must be at most ${max_value}.\n")
                continue
            return value

        except ValueError:
            #if conversion to the float fails
            print("❌Error: Please enter a valid number. \n")






def register_worker():
    """
    Registers a new worker in the system.
    Collects worker information with validation and saves to file.
    Increments the global worker counter to satisy the procedural style of writing code
    """
    global total_workers_registered

    print("\n" + "="*70)
    print("WOKRER RESGISTRATION")

    #Get worker name with validation(not empty)
    while True:
        worker_name = input("Enter worker name: ").strip()
        if worker_name and len(worker_name) >= 2:
            break
        print("❌ Error: Name must be at least 2 characters. \n")

    #Get phone number(using validation function)
    worker_phone = validate_phone_number()

    #Get hourly wage expectation with valiadation
    worker_wage = validate_positive_number(         #Helper function
        "Enter expected hourly wage($10 - $50): ",  #Parameter 1
        10.0,                                       #Parameter 2
        50.0                                        #Parameter 3
    )

    while True:
        worker_skills = input("Enter worker skills (e.g. cleaning , construction , cashier...").strip()
        if worker_skills:
            break
        print("❌ Error: Skills cannot be empty . \n")

    # Display summary for confirmation
    print("\n" + "-"*70)
    print("WORKER REGISTRATION SUMMARY")
    print("-"*70)
    print(f"Name: {worker_name}")
    print(f"Phone: {worker_phone}")
    print(f"Expected wage: ${worker_wage:.2f}/hour")
    print(f"Skills: {worker_skills}")
    print("-"*70)

    #write to the file
    write_worker_to_file(worker_name, worker_phone, worker_wage, worker_skills)

    #Increment counter
    total_workers_registered += 1

    print("✅Worker registered successfully! (Total workers so far: {total_worker_registered}) \n ")



def write_worker_to_file(name, phone , wage, skills):
    """
    Writes worker information to the workers.txt file
    Appends data with timestamp for record-keeping
    :param name: Worker's full name
    :param phone: Worker's phone number
    :param wage: Expected hourly wage
    :param skills: Worker's skills
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("workers.txt", "a") as file:
        file.write(f"\n{'='*70}\n")
        file.write(f"Name: {name}\n")
        file.write(f"Phone: {phone }\n")
        file.write(f"Expected Wage: ${wage:.2f}/hour\n")
        file.write(f"Skills: {skills}\n")
        file.write(f"{'='*70}\n")





def register_company():
    """
        Registers a new employer/company in the system.
        Collects company information with validation and saves to file.
        Increments the global company counter.
    """

    global total_companies_registered
    print("\n" + "'-''*70")
    print("Company Registration")
    print("-"*70)

    # Get company name with validation
    while True:
        company_name = input("Enter the name of the company: ").strip()
        if company_name and len(company_name)>2:
            break
        print("❌ Error:Company Name must be at least 2 characters. \n")

    # Get Business Type with validation
    while True:
        business_type = input("Enter business type (e.g., restaurant, retail, construction, cleaning): ").strip()
        if business_type and len(business_type)>2:
            break
        print("❌ Error: Business type must be valid one.\n")

    #Get phone number with validation
    company_phone = validate_phone_number()


    #Display summary for confirmation
    print(f"\n  {'-'*70}")
    print("COMPANY REGISTRATION SUMMARY")
    print("-"*70)
    print(f"Company Name: {company_name} ")
    print(f"Company Type: {business_type}")
    print(f"Company Phone: {company_phone}")
    print("-"*70)

    #Write company to the file
    write_company_to_file(company_name, business_type, company_phone)

    #Increment Counter
    total_companies_registered += 1

    print(f"✅ Company registered successfully! (Total Company Registered so far: {total_companies_registered}) \n ")

def write_company_to_file(company_name, company_type, company_phone):
    """
    Writes company information to the companies.txt file.
    Appends data with timestamp for record-keeping.

    :param company_name: Name of the company/business
    :param business_type: Type of business
    :param contact_person: Name of contact person
    :param phone: Company phone number
    """

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("companies.txt", "a") as file:
        file.write(f"\n{'=' * 70}\n")
        file.write(f"Registration Time: {timestamp} \n")
        file.write(f"Company Name: {company_name}\n")
        file.write(f"Company Type: {company_type}\n")
        file.write(f"Company_Phone:{company_phone} \n ")
        file.write("=" * 70)


