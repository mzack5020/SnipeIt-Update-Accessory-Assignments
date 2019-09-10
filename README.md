# SnipeIt Update Accessory Assignments
Python script to create SQL file for manually updating accessory assignments.

# Configuration
## Expectations
1) config.json
   - accessoriesFile: Filename for the file containing the "Item Name" to "Customer Name" assignments. NOTE: This is a relative path.
   - accessoriesUrl: URL for the API of your instance of SnipeIt. It should be <your SnipeIt Url>/api/v1/accessories.
   - apiToken: API token retrieved from the UI of your SnipeIt instance.
   - updatedAccessoriesName: Filename that will be used for the creation of the .sql file
  
2) Input File - (accessoriesFile in config.json)
   - This file should be simple. The python script is expecting a "Item Name", "Customer Name" mapping in the form of a .csv. 
   - I haven't tested it with extra fields in there but my expectation is that it should still work. In my case, I was working from an export from another inventory system called Wasp. I simply changed the fields in the export to Item Name and Customer Name and it worked just fine. 

3) Accessory Notes
   - This script will NOT create new accessories. If it cannot find an accessory by the name presented in the Input File, it will simply skip over it and print out an error message to the console.
   - This script will also de-dup any SQL lines that insert the exact same record. 

# Installation
This python script was written in Python 2.7. I'm not familiar with writing requirements.txt or setup.py installation scripts yet so to get it to run in your local environment, I recommend using pyenv virtualenv to install Python 2.7. Then, I would look at the imports in the update_accessory_assignments.py file, and manually install them. All of them shouldn't require a pip installation except for PyInquirer (I think). 

# Disclaimer
This script was written very quickly as an ad hoc fix for a local environment I was working in. I understand that it is most likely not the most efficient or pretty chunk of code, but it worked for the purposes of creating the .sql script I needed to update the database correctly.
