from datetime import datetime
import time
import streamlit as st
import pandas as pd
import numpy as np
import json
import openai
from openai.embeddings_utils import get_embedding, cosine_similarity
import os


openai.api_type = "azure"
openai.api_base = "https://er-openai.openai.azure.com/" # os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_key = "257454561a2b4e5387bd934245661f1d" # os.getenv("AZURE_OPENAI_API_KEY")
openai.api_version = "2022-12-01"

with open('onboarding_short.json') as file:
    json1 = json.load(file)

# input excel file and get col names automatically
# Here’s the supporting Variables information for which the code will reference from the file : onboardingurl,firstname,lastname,ssn,dob,email,mobileNo,invalidssn,patriotActcontentbefore,patriotActContent,ITINnumber,usCitizenDefinition,emailincorrect,ssnInvalid,taxID,MNOVerbiage,UsCitizenDefinition1,UsCitizenDefinition2,UsCitizenDefinition3,UsCitizenDefinition4,LanlineUSNumber,EqualHousingLogo,InvalidSSN,NoUsCitizenfailuremsg,ssntext1,ssntext2,ssntext3,ssntext4,ssnInvalidmsg,CitizenYesOption,CitizenNoOption,MNOVerbiage,VoiceIP,UsCitizenDefinition1,UsCitizenDefinition2,UsCitizenDefinition3,UsCitizenDefinition4,emailerrormessage,blockedemail,IncorrectUSphoneformat,validmobileNo,validSSN,validTaxid,legalIDText,suffix,middlename,CIPConsentText,OTPurl,enterOTPphoneNumber,userid,password

prompt1=f"""Prompt: Build a Cucumber BDD Format code in Gherkin Language for Tallos App.

Here are the available objects to use in the code: """ + str(",".join(json1.keys())) + """

Access to variables will be in the format: “And type on '${{onboarding:firstname}}' the text '${{datos_outline_Onboarding:Onboardingdata.firstname.<row>}}’”

Here’s the supporting metadata information about the code of the task:
    Channel:Onboarding; EPIC ID:HZ-116; User Story ID:HZ-369; Subject:2.2.2 - Confirm OTP; Sprint/Code Drop:PI23.1.2.MVP0; Test Name:TC02_HZ-369_Valid OTP; Description:Valid OTP;

Name of the task: Valid OTP

The following steps are to be coded for the domain of onboarding:
Step 1 is input: Start an Application leading to an output of: Application is started;
Step 2 is input: Navigate to Register page leading to an output of: User navigates to the Register page;
Step 3 is input: Complete the personal information sections and navigate to the OTP screen leading to an output of: User navigates to the OTP page;
Step 4 is input: Enter Valid OTP received on the phone (OTP console in PRE) leading to an output of: User navigates to Set Banking credentials screen;

Include only the variables, available objects, and metadata mentioned above, and provide only the code.

Completion: 
"
@PI23.2.2-Onboard
@23.2.3_ON_WEB
Feature: Registry page in Onboarding validating Registry screen

Background:
Given access the web application 'https://onboarding.stg.mb.openbank.us/registration' And accept all cookies

  @Epic-HZ-116
  @UserStory-HZ-369
  Scenario Outline:  TC02_HZ-369_Valid OTP
    And validate element text '${{onboarding:pageHeading}}' is equal with text value 'Register'
    And click on '${{onboarding:login-page.UScitizen}}'
    And click on '${{onboarding:login-page.continue_btn}}'
    And wait '4' seconds
    And type on '${{onboarding:firstname}}' the text '${{datos_outline_Onboarding:Onboardingdata.firstname.<row>}}'
    And type on '${{onboarding:lastname}}' the text '${{datos_outline_Onboarding:Onboardingdata.lastname.<row>}}'
    And click on '${{onboarding:continue_button}}'
    And type on '${{onboarding:ssn}}' the ssn
    And type on '${{onboarding:dob}}' the text '${{datos_outline_Onboarding:Onboardingdata.dob.<row>}}'
    And click on '${{onboarding:registrationcheckbox}}'
    And click on '${{onboarding:registrationContinuebutton}}'
    And type on '${{onboarding:email}}' the text '${{datos_outline_Onboarding:Onboardingdata.email.<row>}}'
    And type on '${{onboarding:mobileNo}}' the text '${{datos_outline_Onboarding:Onboardingdata.mobileNo.<row>}}'
    And wait '5' seconds
    And click on TAB '${{onboarding:mobileNo}}'
    And click on '${{onboarding:continue_button}}'
    And validate element text '${{onboarding:VerificationCodeHeading}}' is equal with text value 'Verification Code'
    And type on '${{onboarding:enterOTPVerficationCode}}' the text '0P3N'
    And click on '${{onboarding:validateBtn}}'
    And click on '${{onboarding:continue_button}}'
    And validate element text '${{onboarding:congratsSuccMsg}}' is equal with text value 'Congrats!'
    And validate element text '${{onboarding:succMsg}}' is equal with text value 'We have successfully validated your Mobile Number'

    Examples:
      | row |
      | 0  |
"
"""

prompt12=f"""Prompt: Build a Cucumber BDD Format code in Gherkin Language for Tallos App.

Here are the available objects to use in the code: """ + str(",".join(json1.keys())) + """

Access to variables will be in the format: “And type on '${{onboarding:firstname}}' the text '${{datos_outline_Onboarding:Onboardingdata.firstname.<row>}}’”

Here’s the supporting metadata information about the code of the task:
    Channel:Onboarding; EPIC ID:HZ-116; User Story ID:HZ-369; Subject:2.2.2 - Confirm OTP; Sprint/Code Drop:PI23.1.2.MVP0; Test Name:TC02_HZ-369_Valid OTP; Description:Valid OTP;

Name of the task: Valid OTP

The following steps are to be coded for the domain of onboarding:
Step 1 is input: Start an Application leading to an output of: Application is started;
Step 2 is input: Navigate to Register page leading to an output of: User navigates to the Register page;
Step 3 is input: Complete the personal information sections and navigate to the OTP screen leading to an output of: User navigates to the OTP page;
Step 4 is input: Enter Valid OTP received on the phone (OTP console in PRE) leading to an output of: User navigates to Set Banking credentials screen;

Include only the variables, available objects, and metadata mentioned above, and provide only the code.

Completion: 

  @Epic-HZ-116
  @UserStory-HZ-369
  Scenario Outline:  TC02_HZ-369_Valid OTP
    And validate element text '${{onboarding:pageHeading}}' is equal with text value 'Register'
    And click on '${{onboarding:login-page.UScitizen}}'
    And click on '${{onboarding:login-page.continue_btn}}'
    And wait '4' seconds
    And type on '${{onboarding:firstname}}' the text '${{datos_outline_Onboarding:Onboardingdata.firstname.<row>}}'
    And type on '${{onboarding:lastname}}' the text '${{datos_outline_Onboarding:Onboardingdata.lastname.<row>}}'
    And click on '${{onboarding:continue_button}}'
    And type on '${{onboarding:ssn}}' the ssn
    And type on '${{onboarding:dob}}' the text '${{datos_outline_Onboarding:Onboardingdata.dob.<row>}}'
    And click on '${{onboarding:registrationcheckbox}}'
    And click on '${{onboarding:registrationContinuebutton}}'
    And type on '${{onboarding:email}}' the text '${{datos_outline_Onboarding:Onboardingdata.email.<row>}}'
    And type on '${{onboarding:mobileNo}}' the text '${{datos_outline_Onboarding:Onboardingdata.mobileNo.<row>}}'
    And wait '5' seconds
    And click on TAB '${{onboarding:mobileNo}}'
    And click on '${{onboarding:continue_button}}'
    And validate element text '${{onboarding:VerificationCodeHeading}}' is equal with text value 'Verification Code'
    And type on '${{onboarding:enterOTPVerficationCode}}' the text '0P3N'
    And click on '${{onboarding:validateBtn}}'
    And click on '${{onboarding:continue_button}}'
    And validate element text '${{onboarding:congratsSuccMsg}}' is equal with text value 'Congrats!'
    And validate element text '${{onboarding:succMsg}}' is equal with text value 'We have successfully validated your Mobile Number'

    Examples:
      | row |
      | 0  |
"""

prompt2=f"""Prompt: Build a Cucumber BDD Format code in Gherkin Language for Tallos App.

Here are the available objects to use in the code: """ + str(",".join(json1.keys())) + """

Access to variables will be in the format: “And type on '${{onboarding:firstname}}' the text '${{datos_outline_Onboarding:Onboardingdata.firstname.<row>}}’”

Here’s the supporting metadata information about the code of the task:
    Channel:HZ-413; EPIC ID:07.Onboarding\MVP0_23.1\MVP0_23.1.5\SIT; User Story ID:HZ-413_TC02_Account number and routing number is displayed in proper format on congratulations page; Subject:"Congratulations on your new account! Here are you account details” page is displayed with below information:
Adopt US format for account number
Include Routing number;

Name of the task: Account Creation

The following steps are to be coded for the domain of onboarding:
Step 1: Launch the onboarding process https://onboarding.stg.mb.openbank.us/registration: Application is launched;
Step 2: In the register screen, for the question, are you a US citizen, select the radio button, Yes, I am a US citizen. : The radio button, Yes, I am a US citizen, is selected.;
Step 3: Validate that continue button is enabled once the 'Yes, I am a US citizen' is selected.: Continue button is enabled;
Step 4: Click on continue button: User is navigated to register page - enter your legal first name;
Step 5: Enter the firstname of the User: User is able to enter firstname;
Step 6: Enter the firstname of the User: User is able to enter lastname;
Step 7: Click on continue button: User is navigated to register page - lets make sure its really you;
Step 8: Enter the SSN number: User is able to enter 9 digit SSN number;
Step 9: Enter the date of birth in US format(MM-DD-YYYY): User is able to enter DOB in US format(MM-DD-YYYY);
Step 10: Tick the check box for 'I understand that Santander may obtain information from my consumer report or a consumer reporting agency to verify the information I have provided to help determine if Santander should open an account for me': User is able to tick  the check box and continue button is enabled;
Step 11: Click on continue button: User is navigated to Register - Finally, we also need your contact info screen;
Step 12: Enter the primary email address and US phone number of the customer: User is able to enter the email address and the US phone number and continue button is enabled;
Step 13: Click on continue button: User is navigated to Verification code screen(Step 2 of 6);
Step 14: Enter the verification code/OTP sent to user's mobile number: User is able to enter OTP sent to user's mobile number;
Step 15: Click on validate button: OTP is validated and continue button is enabled;
Step 16: Click on continue button : User is navigated to Banking Credentials(Step 3 of 6) screen;
Step 17: Enter a username meeting the below conditions:
Must be between 8 and 20 characters
Can contain letters, numbers and any of the following special characters: , . : @ _
Spaces are not allowed: User is able to enter username meeting the conditions;
Step 18: Enter the password meeting the below conditions:
Must be between 8 and 20 characters
Not include 3 or more consecutive indentical characters
One upper case letter, one lower case letter and one number
One of the following special characters: - # $ % ‘ , ( ) * + . : | = ? @ / ] [ _ `{ } ! ; -
Is not your User ID or User ID spelled backwards: User is able to enter the password meeting the conditions and continue button is enabled;
Step 19: Click on continue button: User is navigated to Address Info(Step 4 of 6) screen;
Step 20: Validate that the page has below info about address:
Your residential address is the address where you normally reside, and it will be the one to which we still send your card and future communications.

Important: Foreign address or PO Box not available.: Information about address is provided to the User;
Step 21: Start typing the address in find your address tab: User is able to type in the address and select the right one from the options provided by google api.;
Step 22: Validate that there is an option to enter address manually: User is given an option to enter address manually;
Step 23: Validate that user is navigated to Residential address page once address is selected from options provided by google api: User is navigated to residential address page;
Step 24: Select the type of address as standard from the dropdown:
Standard
Military
Rural: User is able to select type of address as standard;
Step 25: Enter address line1, address line 2(optional), city, state and zipcode: User is able to enter address line1, address line 2(optional), city, state and zipcode and continue button is enabled;
Step 26: Click on continue button: User is navigated to Address Info(Step 4 of 6) screen with address summary;
Step 27: User has an option to edit the address or continue: User is able to edit the address or continue;
Step 28: Click on continue button: User is navigated to Employment and Income(Step 5 of 6) screen (KYC page);
Step 29: User is provided with question 'What is the nature of your professional or business activity?' with options as 
Employed
Self employed
Military on duty
Student -employed
Student  - unemployed
Retired
Unemployed
Never employed.
Select 'employed'  from the list.: User is able to click on employed radio button as employment status and User is provided the question 'What is your occupation?';
Step 30: Select account manager from the drop down for  'What is your occupation?': User is able to select account manager from the drop down;
Step 31: User is asked 'Tell us your level of annual gross income' and is able to enter gross income in digits: User is able to enter gross income;
Step 32: Click on enter button: User is provided with question 'What is your main Source of your Funds?' with options with check box:
Employment
Household income
Inheritance/Trust
Investment
Retirement
Social Security
Unemployment
;
Step 33: Select employment and Investment and click on select: User is provided with question 'Do you perform or have you performed in the last two years any important public function in the US or abroad or are you a direct family member or do you have a direct relationship with them?';
Step 34: Select no radio button: Continue button is enabled;
Step 35: User is navigated to Terms and Conditions(Step 6 of 6) screen with below information:
You almost have it! But before finalizing the process, we need you to review and agree to the following information: User is navigated to T & C page;
Step 36: Tick the check boxes with below information:

I have read and agree to the ESIGN Act Consent and I understand I won’t receive documents in the mail


I agree with the clauses contained in the following documents:
PDAA
Fee Schedule
Interest Rate Disclosure
Privacy Notice
Digital Banking Agreement: User is able to check the boxes and continue button is enabled;
Step 37: Click on continue button: User is navigated to Terms and Conditions(Step 6 of 6) page with below information:
In order to proceed with the opening of your account, please check the following information and review the tax certification clause.
Name, Surname, SSN number except last four digits masked;
Step 38: Check if user is able to unmask SSN: SSN is unmasked;
Step 39: Validate the information of the user: Name, surname and SSN are correct;
Step 40: User is provided with below information in the page:
By sumbitting the application, I confirm that the data above is correct and under penalties of perjury, I certify that:

Under penalties of perjury, I certify that:
The number shown above is my correct taxpayer identification number.

I am not subject to backup withholding because:
I am exempt from backup withholding, or
I have not been notified by the Internal Revenue Service (IRS) that I am subject to backup withholdingas a result of a failure to report all interest or dividends, or
The IRS has notified me that I am no longer subject to backup withholding;

I have been notified by the IRS that I am subject to backup withholding.
(If you select this option, the account will not be created)

I am a U.S. citizen or other U.S. person.
The FATCA code entered above, if any, indicating that I am exempt from FATCA reporting is correct.(This certification is not applicable to accounts opened in the United States): User is provided with the information ;
Step 41: In the second certification clause, select 'I am not subject to backup withholding' radio button: User is able to select 'I am not subject to backup withholding' radio button;
Step 42: Validate whether continue button is enabled: Continue button is enabled;
Step 43: Validate whether congratulations page is displayed with routing number and account number: Congratulations page is displayed with routing number and account number;

Include only the variables, available objects, and metadata mentioned above, and provide only the code.

Completion: 

  @Epic-HZ-137
  @UserStory-Hz-413
  Scenario Outline: HZ-413_TC02_Account number and routing number is displayed in proper format on congratulations page
    And validate element text '${{onboarding:pageHeading}}' is equal with text value 'Register'
    And click on '${{onboarding:login-page.UScitizen}}'
    And click on '${{onboarding:login-page.continue_btn}}'
    And type on '${{onboarding:firstname}}' the text '${{datos_outline_Onboarding:Onboardingdata.firstname.<row>}}'
    And type on '${{onboarding:lastname}}' the text '${{datos_outline_Onboarding:Onboardingdata.lastname.<row>}}'
    And click on '${{onboarding:continue_button}}'
    And type on '${{onboarding:ssn}}' the ssn
    And type on '${{onboarding:dob}}' the text '${{datos_outline_Onboarding:Onboardingdata.dob.<row>}}'
    And click on '${{onboarding:registrationcheckbox}}'
    And click on '${{onboarding:registrationContinuebutton}}'
    And type on '${{onboarding:email}}' the text '${{datos_outline_Onboarding:Onboardingdata.email.<row>}}'
    And type on '${{onboarding:mobileNo}}' the text '${{datos_outline_Onboarding:Onboardingdata.mobileNo.<row>}}'
    And click on TAB '${{onboarding:mobileNo}}'
    And click on '${{onboarding:continue_button}}'
    And validate element text '${{onboarding:VerificationCodeHeading}}' is equal with text value 'Verification Code'
    And click on '${{onboarding:requestNewOTP}}'
    And click on '${{onboarding:requestNewOTP}}'
    And launch the another url in new tab '${{datos_outline_Onboarding:Onboardingdata.OTPurl.<row>}}'
    And clear phone number in OTP screen
    And type on '${{onboarding:enterOTPphoneNumber}}' the phone number '${{datas:enterOTPphoneNumber}}'
    And click on '${{onboarding:searchOTP_btn}}'
    And copy the otp '${{onboarding:copyOTP}}' and paste it into verification page '${{onboarding:enterOTPVerficationCode}}'
    And click on '${{onboarding:validateBtn}}'
    And click on '${{onboarding:continue_button}}'
    And validate element text '${{onboarding:congratsSuccMsg}}' is equal with text value 'Congrats!'
    And validate element text '${{onboarding:succMsg}}' is equal with text value 'We have successfully validated your Mobile Number'
    And type on '${{onboarding:enterUserID}}' the userid
    And scroll to bottom of the page
    And type on '${{onboarding:enterPassword}}' the text '${{datos_outline_Onboarding:Onboardingdata.password.<row>}}'
    And click on '${{onboarding:continue_button}}'
    And wait '5' seconds
    And validate element text '${{onboarding:addressInfoHeading}}' is equal with text value 'Address Info'
    And type on '${{onboarding:enterAddressAuto}}' the text 'Alabama'
    And click on '${{onboarding:selectAutopopulateAddress}}'
    And wait '2' seconds
    And validate element text '${{onboarding:residentialAddressHeading}}' is equal with text value 'Residential address'
    And validate element text '${{onboarding:addressinform}}' is equal with text value '${{datos_outline_Onboarding:Onboardingdata.addressinform.<row>}}'
    And click on '${{onboarding:AddressType}}'
    And click on '${{onboarding:standardAddress}}'
    And type on '${{onboarding:addressLine1}}' the text '86 Dunn Drive'
    And click on '${{onboarding:selectAutopopulateAddressLine1}}'
    And type on '${{onboarding:addressLine2}}' the text 'Test'
    And wait '2' seconds
    And click on '${{onboarding:confirmButton}}'
    And wait '2' seconds
    And click on '${{onboarding:confirmButton}}'
    And validate element text '${{onboarding:confirmAddress}}' is equal with text value '86 Dunn Drive Test Fort Novosel AL, 36362'
    And click on '${{onboarding:continue_button}}'
    And wait '2' seconds
    And click on '${{onboarding:professionalType}}'
    And type on '${{onboarding:income}}' the text '2000'
    And click on '${{onboarding:enter_button}}'
    And click on '${{onboarding:sourceofFunds}}'
    And click on '${{onboarding:select_button}}'
    And click on '${{onboarding:No_radiobutton}}'
    And click on '${{onboarding:continue_button}}'
    And wait '2' seconds
    And click on '${{onboarding:checkbox1}}'
    And click on '${{onboarding:checkbox2}}'
    And validate element text '${{onboarding:PDAALink}}' is equal with text value 'PDAA'
    And validate element text '${{onboarding:FeeScheduleLink}}' is equal with text value 'Fee Schedule'
    And validate element text '${{onboarding:InterestRateDisclosureLink}}' is equal with text value 'Interest Rate Disclosure'
    And validate element text '${{onboarding:PrivacyNoticeLink}}' is equal with text value 'Privacy Notice'
    And wait '2' seconds
    And validate element text '${{onboarding:DigitalBankingAgreementLink}}' is equal with text value 'Digital Banking Agreement'
    And wait '5' seconds
    And click on '${{onboarding:continue_button}}'
    And click on '${{onboarding:radiobtn}}'
    And click on '${{onboarding:continue_button}}'
    And wait '4' seconds
    And validate element text '${{onboarding:accountCreateMsg}}' is equal with text value 'Congratulations on your new account!'
    And click on '${{onboarding:showAccountNumber}}'
    And wait '2' seconds

    Examples:
      | row |
      | 27  |

"""

prompt2_sum = """
Prompt: To build code for the Tallos app, the instructions are to create a Cucumber BDD Format code in the Gherkin Language. The available objects to use in the code are provided in a JSON format. Access to variables will be done through the format "And type on '${{onboarding:firstname}}' the text '${{datos_outline_Onboarding:Onboardingdata.firstname.<row>}}’”. The name of the task is "Account Creation" and the following steps need to be coded for the onboarding domain: Launch the onboarding process, select the "Yes, I am a US citizen" radio button, validate that the continue button is enabled, enter the user's first and last name, enter the user's SSN and DOB, tick the checkbox to allow Santander to obtain information from the consumer report, enter the primary email address and US phone number, enter the verification code/OTP sent to the user's mobile number, enter the username and password meeting specific conditions, validate the page has the address information, enter the user's address, select the type of address, enter the employment and income information, enter the routing number and account number in US format, and validate that the Congratulations page is displayed with the user's account details.

Completion: 
@Epic-HZ-137
  @UserStory-Hz-413
  Scenario Outline: HZ-413_TC02_Account number and routing number is displayed in proper format on congratulations page
    And validate element text '${{onboarding:pageHeading}}' is equal with text value 'Register'
    And click on '${{onboarding:login-page.UScitizen}}'
    And click on '${{onboarding:login-page.continue_btn}}'
    And type on '${{onboarding:firstname}}' the text '${{datos_outline_Onboarding:Onboardingdata.firstname.<row>}}'
    And type on '${{onboarding:lastname}}' the text '${{datos_outline_Onboarding:Onboardingdata.lastname.<row>}}'
    And click on '${{onboarding:continue_button}}'
    And type on '${{onboarding:ssn}}' the ssn
    And type on '${{onboarding:dob}}' the text '${{datos_outline_Onboarding:Onboardingdata.dob.<row>}}'
    And click on '${{onboarding:registrationcheckbox}}'
    And click on '${{onboarding:registrationContinuebutton}}'
    And type on '${{onboarding:email}}' the text '${{datos_outline_Onboarding:Onboardingdata.email.<row>}}'
    And type on '${{onboarding:mobileNo}}' the text '${{datos_outline_Onboarding:Onboardingdata.mobileNo.<row>}}'
    And click on TAB '${{onboarding:mobileNo}}'
    And click on '${{onboarding:continue_button}}'
    And validate element text '${{onboarding:VerificationCodeHeading}}' is equal with text value 'Verification Code'
    And click on '${{onboarding:requestNewOTP}}'
    And click on '${{onboarding:requestNewOTP}}'
    And launch the another url in new tab '${{datos_outline_Onboarding:Onboardingdata.OTPurl.<row>}}'
    And clear phone number in OTP screen
    And type on '${{onboarding:enterOTPphoneNumber}}' the phone number '${{datas:enterOTPphoneNumber}}'
    And click on '${{onboarding:searchOTP_btn}}'
    And copy the otp '${{onboarding:copyOTP}}' and paste it into verification page '${{onboarding:enterOTPVerficationCode}}'
    And click on '${{onboarding:validateBtn}}'
    And click on '${{onboarding:continue_button}}'
    And validate element text '${{onboarding:congratsSuccMsg}}' is equal with text value 'Congrats!'
    And validate element text '${{onboarding:succMsg}}' is equal with text value 'We have successfully validated your Mobile Number'
    And type on '${{onboarding:enterUserID}}' the userid
    And scroll to bottom of the page
    And type on '${{onboarding:enterPassword}}' the text '${{datos_outline_Onboarding:Onboardingdata.password.<row>}}'
    And click on '${{onboarding:continue_button}}'
    And wait '5' seconds
    And validate element text '${{onboarding:addressInfoHeading}}' is equal with text value 'Address Info'
    And type on '${{onboarding:enterAddressAuto}}' the text 'Alabama'
    And click on '${{onboarding:selectAutopopulateAddress}}'
    And wait '2' seconds
    And validate element text '${{onboarding:residentialAddressHeading}}' is equal with text value 'Residential address'
    And validate element text '${{onboarding:addressinform}}' is equal with text value '${{datos_outline_Onboarding:Onboardingdata.addressinform.<row>}}'
    And click on '${{onboarding:AddressType}}'
    And click on '${{onboarding:standardAddress}}'
    And type on '${{onboarding:addressLine1}}' the text '86 Dunn Drive'
    And click on '${{onboarding:selectAutopopulateAddressLine1}}'
    And type on '${{onboarding:addressLine2}}' the text 'Test'
    And wait '2' seconds
    And click on '${{onboarding:confirmButton}}'
    And wait '2' seconds
    And click on '${{onboarding:confirmButton}}'
    And validate element text '${{onboarding:confirmAddress}}' is equal with text value '86 Dunn Drive Test Fort Novosel AL, 36362'
    And click on '${{onboarding:continue_button}}'
    And wait '2' seconds
    And click on '${{onboarding:professionalType}}'
    And type on '${{onboarding:income}}' the text '2000'
    And click on '${{onboarding:enter_button}}'
    And click on '${{onboarding:sourceofFunds}}'
    And click on '${{onboarding:select_button}}'
    And click on '${{onboarding:No_radiobutton}}'
    And click on '${{onboarding:continue_button}}'
    And wait '2' seconds
    And click on '${{onboarding:checkbox1}}'
    And click on '${{onboarding:checkbox2}}'
    And validate element text '${{onboarding:PDAALink}}' is equal with text value 'PDAA'
    And validate element text '${{onboarding:FeeScheduleLink}}' is equal with text value 'Fee Schedule'
    And validate element text '${{onboarding:InterestRateDisclosureLink}}' is equal with text value 'Interest Rate Disclosure'
    And validate element text '${{onboarding:PrivacyNoticeLink}}' is equal with text value 'Privacy Notice'
    And wait '2' seconds
    And validate element text '${{onboarding:DigitalBankingAgreementLink}}' is equal with text value 'Digital Banking Agreement'
    And wait '5' seconds
    And click on '${{onboarding:continue_button}}'
    And click on '${{onboarding:radiobtn}}'
    And click on '${{onboarding:continue_button}}'
    And wait '4' seconds
    And validate element text '${{onboarding:accountCreateMsg}}' is equal with text value 'Congratulations on your new account!'
    And click on '${{onboarding:showAccountNumber}}'
    And wait '2' seconds

    Examples:
      | row |
      | 27  |
"""


def get_prompt(task_df, json_file):
    task_df=task_df.reset_index(drop=True)
    # find the index of the column "Step number (Design Steps)" - every col before this is metadata
    steps_idx = list(task_df.columns).index("Step number (Design Steps)")
    metadata_vals=task_df.loc[0].values[0:steps_idx]
    metadata_cols=task_df.columns[0:steps_idx]
    metadata_text="""Here’s the supporting metadata information about the code of the task:
    """
    for i in range(len(metadata_cols)):
        if metadata_vals[i] is not None:
            temp=metadata_cols[i]+":"+metadata_vals[i]+"; "
            metadata_text+=temp
    metadata_text+="\n\nName of the task: "+metadata_vals[-1]
    code_logic="\n".join(task_df['Step number (Design Steps)']+ ": "+task_df['Description (Design Steps)']+": "+task_df['Expected Result (Design Steps)']+";")
    
    prompt_header=f"""Prompt: Build a Cucumber BDD Format code in Gherkin Language for Tallos App.

Here are the available objects to use in the code: """ + str(",".join(json_file.keys())) + """

Access to variables will be in the format : “And type on '${{onboarding:firstname}}' the text '${{datos_outline_Onboarding:Onboardingdata.firstname.<row>}}’”

"""

    prompt=prompt_header+metadata_text+"\n\nThe following steps are to be coded for the domain of onboarding:\n"+code_logic + "\n\nInclude only the variables, available objects, and metadata mentioned above, and provide only the code.\n\nCompletion:"
    
    return prompt,code_logic

def inputs_to_prompts(input_excel_name, json_file):
    
    input_excel=pd.read_excel(input_excel_name)
    input_excel = input_excel.replace(np.nan, None)

    # get a list of the indices where each task starts (at Step 1) and add len(input_excel) so we have a stop idx
    task_starts = input_excel.index[input_excel['Step number (Design Steps)'] == 'Step 1'].tolist() + [len(input_excel)]
    prompts=[]
    code_logics=[]
    for i in range(len(task_starts) - 1):
        start = task_starts[i]
        end = task_starts[i+1]
        task_df = input_excel.iloc[start:end]
        prompt,code_logic = get_prompt(task_df, json_file)
        prompts.append(prompt)
        code_logics.append(code_logic)
    return prompts


st.title("GenAI powered Code Generation")
st.header("Excel and JSON File Upload")
uploaded_file = st.file_uploader('Upload the Excel file with your desired code steps')
uploaded_json = st.file_uploader('Upload the corresponding JSON file')
if (uploaded_file is not None) and (uploaded_json is not None):
    st.write('File upload success! Here is the Excel you uploaded:')
    st.write(pd.read_excel(uploaded_file))
    st.write('And here is the JSON you uploaded:')
    with open(uploaded_json.name) as file:
        uploaded_json = json.load(file)
    st.json(uploaded_json)
    #st.code(prompt2_sum)
    # print("uploaded_file",uploaded_file.name)
    # print(pd.read_excel(uploaded_file))

    # input_excel = pd.read_excel(uploaded_file)
    # input_excel = input_excel.replace(np.nan, None)
    
    # code logic to separate tasks
    # k=0
    # indexes=[]
    # global current_v
    # task_index={}
    # itera=0
    # for i,v in enumerate(input_excel["Channel"]):
    #     print(i,v)
    #     if k==0 and v!=None:
    #         current_v=v+str(itera)
    #         itera+=1
    #         task_index[current_v]=[]
    #         task_index[current_v].append(i)
    #         k+=1
    #     elif v==None:
    #         task_index[current_v].append(i)
    #         k+=1
    #     elif k!=0 and v!=None:
    #         current_v=v+str(itera)
    #         itera+=1
    #         task_index[current_v]=[]
    #         task_index[current_v].append(i)
    #         k=0

    # # for sake of demonstration, just look at the first task
    # task_df=input_excel.loc[task_index["Onboarding0"]]
    # # using this subset of task data, create the code steps
    # code_logic="\n".join(task_df['Step number (Design Steps)']+ " is input:"+task_df['Description (Design Steps)']+" leading to an output of :"+task_df['Expected Result (Design Steps)']+";")
    # # embed the code logic
    # code_logic_embed = get_embedding(code_logic, engine=EMBEDDING_MODEL)

    # # read in the embedded data generated from generate_embeddings.py
    # dataset = pd.read_pickle('./src/app/pdf-embeddings/all_docs_embeddings/embeddings.pkl')
    # # get similarity between new code logic and each existing one
    # dataset["similarity"] = dataset.text_embeddings.apply(lambda x: cosine_similarity(x, code_logic_embed))
    # # find the text that is most similar
    # most_relevant_texts = (dataset.sort_values("similarity", ascending=False).head(1))

    prompts=inputs_to_prompts(uploaded_file, uploaded_json)
    background = """
    @PI23.2.2-Onboard
    @23.2.3_ON_WEB
    Feature: Registry page in Onboarding validating Registry screen
    
    Background:
    Given access the web application 'https://onboarding.stg.mb.openbank.us/registration' And accept all cookies
    """
    st.subheader("Here is the background for your requested features:")
    st.code(background)
    # keep track of the responses from OpenAI (append everything after the background)
    responses = background
    for i, prompt in enumerate(prompts):
        #st.subheader("Here is the prompt:")
        #st.code(prompt)
        prompt_to_openai= prompt12+"\n\n"+prompt
        start_time=time.time()
        #Note: The openai-python library support for Azure OpenAI is in preview.

        response = openai.Completion.create(
                                            engine="text-davinci-003",
                                            prompt=prompt_to_openai,
                                            temperature=0,
                                            max_tokens=1500,
                                            top_p=0,
                                            frequency_penalty=0,
                                            presence_penalty=0,
                                            best_of=1,
                                            stop=None)
        end_time = time.time()
        duration = end_time - start_time
        print(duration)
        json_object = json.loads(str(response))
        # print("Generated CODE:\n",json_object['choices'][0]['text'])
        st.subheader(f"Here is a generated code by OpenAI for your requested task ({i+1} of {len(prompts)}):")
        st.code(json_object['choices'][0]['text'])
        responses += json_object['choices'][0]['text']+"\n\n"

    with open(f"responses/responses_{datetime.now()}.txt", "w") as text_file:
        text_file.write(responses)
