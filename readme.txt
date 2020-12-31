Welcome to the Restaurant Staffing Web Application

Reference : 
https://www.youtube.com/watch?v=F5mRW0jo-U4&t=10616s
https://github.com/CoreyMSchafer/code_snippets/tree/master/Django_Blog/06-User-Registration-Form/django_project/blog/static/blog


Before running the application, please go to restaurant-app/settings.py, and:
	Change the value of 'EMAIL_HOST_USER' from  '***@gmail.com' to 'your_gmail_id@gmail.com'
	and the value of 'EMAIL_HOST_PASSWORD' from '****' to 'password_of_your_gmail_id'
	(enter your actual gmail id and the password for that id)
	
Even after changing these settings, there is a chance that the application does not send out the mail. 
If that happens, please go to the google account(associated with the gmail id entered above) and switch on the setting - 'less secure access'. Please see https://hotter.io/docs/email-accounts/secure-app-gmail/ for details on how to enable this setting.


Steps for of the application

Steps :

1. Create an overall admin to monitor the status of everything in the application. This user has no restricted rights whatsoever 
Lets say user - "admin"  

2. Creat 2 restaurant administrators - ra1,ra2

3. Create 5 hiring managers - hm1, hm2, hm3, hm4, hm5 

4. Log in with your overall "admin": 
   Create 2 Restaurants : Restaurant1 , Restaurant2 
   Create 5 Locations : loc1, loc2, loc3, loc4, loc5 
  
5. Login with ra1:
	Create Location for his restaurant and assign hiring managers for the same. 
	Create Job Posting for his newly create restaurant and location 

6. Login with ra2 
	Create Location for his restaurant and assign hiring managers for the same. 
	Create Job Posting for his newly create restaurant and location
	
7. Open your hiring managers and check for the job Posting 

8. Create applicants 
	Submit applications to the job postings 
	
9. Go back to the hiring managers to check the job postings and then approve/reject them. 

10. Check for the email in the applicant's email address.  

