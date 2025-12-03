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
total_workers_registered = 0   # Count of workers registered today
total_companies_registered = 0
total_jobs_posted = 0
total_membership_fee = 0

#=============================================================================
# STARTUP FUNCTION
def load_previous_totals():
    """
    Loads cumulative totals from the previous report.txt file at startup.
    Reads the last saved values from the file(we are not using database till now) to continue tracking across sessions.

    :return: None (updates global variables directly)
    """
    global total_workers_registered, total_companies_registered, total_jobs_posted, total_membership_fee

    try:
        with open("report.txt" , 'r') as file:
            for line in file:
                line = line.strip() #read line by line

                if "Total number of Workers Registered: " in line:
                    total_workers_registered = int(line.split(':')[1].strip())

                elif "Total number of Companies Registered: " in line:
                    total_companies_registered = int(line.split(':')[1].strip())

                elif "Total number of Jobs posted: " in line:
                    total_jobs_posted = int(line.split(':')[1].strip())

                elif "Total Revenue Collected so far :" in line:
                    total_membership_fee = float(line.split('$')[1].strip())

        print(f"\nPrevious data loaded from report\n")

    except FileNotFoundError:
        print("\nNo previous report found. Starting fresh.\n")
    except:
        print("\nError loading report. Starting from 0.\n")



        #Extract total_workers_registered



#=============================================================================

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
            print("  Error: Phone number cannot be empty. \n")
            continue

        #Check if all characters are digits
        if not phone.isdigit():
            print("  Error: Phone number must contain only digits. \n")
            continue

        # Check if exactly 10 digits
        if len(phone) != 10:
                print(f"  Error: Phone number must be exactly 10 digits. You entered {len(phone)} digits.\n")
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
                print(f"  Value must be at least ${min_value}.\n")
                continue
            if value> max_value:
                print(f" Value must be at most ${max_value}.\n")
                continue
            return value

        except ValueError:
            #if conversion to the float fails
            print(" Error: Please enter a valid number. \n")



def validate_date(prompt):
    """
    Validates date input in MM/DD/YYYY format
    Ensures the date is today or in the future
    : param prompt: Message to display to the user
    return: A valid date string in MM/DD/YYYY format
    """

    while True:
        date_str = input(prompt).strip()

        #Check if empty
        if not date_str:
            print("  Error: Date cannot be empty.\n")
            continue

        try:
            #Try to parse the date
            date_obj = datetime.strptime(date_str, "%m/%d/%Y") #Parse string to time

            #Check if date is not in  the past
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            if date_obj < today:
                print("X Error: Date cannot be in the past. \n")
                continue
            return date_str

        except ValueError:
            print("  Error: Invalid date format. Please use MM/DD/YYYY (e.g., 12/25/2024). \n")









def register_worker():
    """
    Registers a new worker in the system.
    Collects worker information with validation and saves to file.
    Increments the global worker counter to satisy the procedural style of writing code
    """
    global total_workers_registered
    global total_membership_fee

    print("\n" + "="*70)
    print("WOKRER RESGISTRATION")

    #Get worker name with validation(not empty)
    while True:
        worker_name = input("Enter worker name: ").strip()
        if worker_name and len(worker_name) > 2:
            break
        print("  Error: Name must be at least 2 characters. \n")

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
        print("  Error: Skills cannot be empty . \n")

    #Prompt user for membership fee
    while True:
        decision = input("Do you want to may membership fee  now ?.. Enter 'Y' or 'N' : ").strip().upper()
        if not decision or (decision != 'Y' and decision!= 'N') :
            print("Enter Correctly")
            continue
        if decision == 'Y':
            total_membership_fee = total_membership_fee+100
            break
        else:  # decision == 'N'
            print("Worker registered without payment. Payment pending.")
            break





    # Display summary for confirmation
    print("\n" + "-"*70)
    print("WORKER REGISTRATION SUMMARY")
    print("-"*70)
    print(f"Name: {worker_name}")
    print(f"Phone: {worker_phone}")
    print(f"Expected wage: ${worker_wage:.2f}/hour")
    print(f"Skills: {worker_skills}")
    print(f"Membership fee: {'Paid' if decision == 'Y' else 'Unpaid'}")
    print("-"*70)

    #write to the file
    write_worker_to_file(worker_name, worker_phone, worker_wage, worker_skills)

    #Increment counter
    total_workers_registered += 1

    print(f"Worker registered successfully! Total workers so far: {total_workers_registered}\n")



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
        print("  Error:Company Name must be at least 2 characters. \n")

    # Get Business Type with validation
    while True:
        business_type = input("Enter business type (e.g., restaurant, retail, construction, cleaning): ").strip()
        if business_type and len(business_type)>2:
            break
        print("  Error: Business type must be valid one.\n")

    #Get Company Address
    while True:
        company_address = input("Enter the address of the company:  \n").strip()
        if not  company_address or  len(company_address)<5:
            print("  Address too short.\n")
            continue

        if not company_address[0].isdigit():
            print("  Address should start with a street number.\n")
            continue
        break





    #Get phone number with validation
    company_phone = validate_phone_number()


    #Display summary for confirmation
    print(f"\n  {'-'*70}")
    print("COMPANY REGISTRATION SUMMARY")
    print("-"*70)
    print(f"Company Name: {company_name} ")
    print(f"Company Type: {business_type}")
    print(f"Company Address: {company_address}")
    print(f"Company Phone: {company_phone}")
    print("-"*70)

    #Write company to the file
    write_company_to_file(company_name, business_type, company_address, company_phone )

    #Increment Counter
    total_companies_registered += 1

    print(f"✅ Company registered successfully! (Total Company Registered so far: {total_companies_registered}) \n ")

def write_company_to_file(company_name, company_type,company_address,company_phone):
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
        file.write(f"Company Address:{company_address} \n ")
        file.write(f"Company Phone:{company_phone} \n ")
        file.write("=" * 70)


def post_job():
    """
      Posts a new job opportunity in the system.
      Collects job details with validation and saves to file.
      Increments the global jobs counter.
    """
    global total_jobs_posted

    print(f"\n { '-'*70}")
    print("JOB POSTING")

    #Get job details with validation

    # Get company name (who is posting the job)
    while True:
        company_name = input("Enter company name posting this job: ").strip()
        if company_name and len(company_name) >2:
            break
        print(" Error: Company name must be at least 2 characters \n ")


    # Get job position/title
    while True:
        job_position = input(f"\nEnter job position (e.g., dishwasher, cashier, cleaner): ").strip()
        if job_position and len(job_position) > 3:
            break
        print("  Error: Job position must be at least 2 characters.\n")

    # Get required skills(soft and hard)
    while True:
        required_skills = input(
            "\nEnter skills required for this position (e.g., must know dishwashing, food prep experience): ").strip()
        if required_skills and len(required_skills) >2:
            break
        print("  Error: Required skills must be valid one.\n")

    # Get to be offered hourly pay rate with validation
    pay_rate = validate_positive_number(  # Helper function
        "\nEnter hourly pay rate($10 - $50): ",
        10.0,
        50.0
    )

    # Get hours offered with validation
    hours_offered_per_week = int(validate_positive_number(
        "\nEnter hours offered per week(1-80): ",
        1,
        80 ))


    total_pay_per_week = hours_offered_per_week* pay_rate



    # Get start_date with validation
    start_date = validate_date("\nEnter start date (MM/DD/YYYY): ")


    # Display summary for confirmation

    print(f"\n {'-'*70}")
    print("JOB POSTING SUMMARY")
    print(f"\n {'-' * 70}")
    print(f"Company: {company_name}")
    print(f"Position: {job_position}")
    print(f"Required Skills: {required_skills}")
    print(f"Pay Rate: {pay_rate}")
    print(f"Hours Offered/Week: {hours_offered_per_week}")
    print(f"Total Pay per week: ${total_pay_per_week}")
    print(f"Start Date: {start_date}")
    print(f"\n {'-' * 70}")

    #Write to the file
    write_job_to_file(company_name, job_position, required_skills, pay_rate, hours_offered_per_week,
                      total_pay_per_week, start_date)

    #Increment the counter
    total_jobs_posted += 1

    print(f"✅ Job posted successfully! (Total jobs posted so far: {total_jobs_posted})\n")


def write_job_to_file(company_name, job_position, required_skills, pay_rate, hours_offered_per_week,
                      total_pay_per_week, start_date):
    """
    Writes job posting information to the jobs.txt file.
    Appends data with timestamp for record-keeping.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("job_post.txt", "a") as file:
        file.write(f"\n{'-'*70}\n")
        file.write(f"Posted Timestamp: {timestamp}\n")
        file.write(f"Company: {company_name}\n")
        file.write(f"Job Position: {job_position}\n")
        file.write(f"Pay_Rate: {pay_rate}\n")
        file.write(f"Hours Offered Per Week: {hours_offered_per_week}\n")
        file.write(f"Total Pay per Week: {total_pay_per_week}\n")
        file.write(f"Start_date: {start_date}\n")
        file.write(f"\n{'-' * 70}\n")


def generate_daily_earnings_report():
    """
     Generates comprehensive daily earnings report at :59
    """

    print("###########generated daily report########### ")

    #timestamp
    #report is generated automatically at a given time, no options
    #display with cat

    write_report_to_file()


def write_report_to_file():
    """
    Writes cumulative report to report.txt (overwrites existing file).

    Generates a summary report containing total workers, companies, jobs,
    and revenue collected. Report reflects cumulative data across all
    program sessions since files persist between runs.
    """

    with open("report.txt" ,'w') as file:
        file.write(f"\n {'='*70}")
        file.write(f"           LOCALWORK CONNECT - DAILY REPORT\n")
        file.write(f"{'=' * 70}\n")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"Report Generated : {timestamp} \n")
        file.write(f"{'=' * 70}\n")

        # Activity Summary
        file.write(f"DAILY ACTIVITY SUMMARY\n")
        file.write(f"{'-' * 70}\n")
        file.write(f"Total number of Workers Registered: {total_workers_registered} \n")
        file.write(f"Total number of Companies Registered: {total_companies_registered} \n")
        file.write(f"Total number of Jobs posted: {total_jobs_posted} \n\n")

        #Revenue Breakdown
        file.write(f"REVENUE BREAKDOWN \n")
        file.write(f"{'=' * 70}\n")
        file.write(f"Total numbers of paid workers:{total_membership_fee/100}\n")
        file.write(f"Total Revenue Collected so far : ${total_membership_fee:.2f}\n\n")



def read_file_content(FileChoice:str):
    FileChoice = FileChoice.strip() + ".txt"
    print(FileChoice)
    if (FileChoice!= "companies.txt" and FileChoice!= "job_post.txt" and FileChoice!= "report.txt" and
            FileChoice!="workers.txt"):
        print("Sorry!, Such file doesnt exist.")
        return

    with open(FileChoice, 'r') as file:
        file_content = file.read()
        print(file_content)



# =============================================================================
# MAIN MENU (for testing)
# =============================================================================

def display_menu():
    """
     Display the main menu for the LocalWork Connect system
    """
    print("\n" + "="*70)
    print("LOCALWORK CONNECT - COMMUNITY EMPLOYMENT AGENCY")
    print("="*70)
    print("RW. Register Worker")
    print("RC. Register Company")
    print("PJ. Post Job")
    print("READ. Display the content of the files")
    print("E.  Exit")
    print("="*70)











def main():
    """
    Main Program loop
    """

    load_previous_totals() #load the global variable from the reports.txt file
    try:
        while True:
            display_menu()
            choice = input("Enter your choice: ").strip().upper()

            if choice == "RW":
                register_worker()
            elif choice == "RC":
                register_company()
            elif choice == "PJ":
                post_job()
            elif choice == "READ":
                FileChoice = input("Enter the exact name of the file you want to access, no need to include "
                                   ".txt:    ").lower()
                read_file_content(FileChoice)

            elif choice == "E":
                generate_daily_earnings_report()
                print(f"\n {'=' * 70}")
                print("DAILY SUMMARY")
                print("=" * 70)
                print(f"Workers Registered: {total_workers_registered}")
                print(f"Companies Registered: {total_companies_registered}")
                print(f"Jobs Posted: {total_jobs_posted}")
                print(f"Total Membership Collected: {total_membership_fee}")
                print("=" * 70)
                print("Thank you for using LocalWork Connect!")
                print("=" * 70 + "\n")
                break
            else:
                print(" Invalid Choice. Please enter from among these options:")
                print("RW. Register Worker")
                print("RC. Register Company")
                print("PJ. Post Job")
                print("E.  Exit")

    except KeyboardInterrupt:
    # ✅ User pressed Ctrl+C - save before exiting!
        print("\n\n" + "=" * 70)
        print(" PROGRAM INTERRUPTED")
        print("=" * 70)
        print("Saving data before exit...")
        generate_daily_earnings_report()
        print("Data saved successfully!")
        print("=" * 70 + "\n")


#Run the program
if __name__ == "__main__":
    main()





