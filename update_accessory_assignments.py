import csv
import HTMLParser
import itertools
import json
import requests
import urllib3

from PyInquirer import prompt, Separator

# Hide SSL Warnings in Output
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Template for Prompt
userSelectionTemplate = {
    'message': 'Please select a user that will act as the assigner for these accessories (User ID - Name - Username):',
    'name': 'assignedToUser',
    'type': 'list'
}

# Used in sorting list of users
def extract_name(json):
    return json['name']

def main():
    print 'Reading in config file...'
    with open('config.json') as config_file:
        config = json.load(config_file)
        filename = config['accessoriesFile']
        apiToken = config['apiToken']
        usersUrl = config['usersUrl']
        accessoriesUrl = config['accessoriesUrl']
        updatedAccessoriesName = config['updatedAccessoriesName']
    print 'Config file read successfully'

    # Headers for Authentication
    headers = {
        'accept': 'application/json',
        'authorization': 'Bearer ' + apiToken,
        'content-type': 'application/json'
    }

    # Ensure we get all manufacturers for de-dup checking
    queryParams = {
        "limit": "1000000"
    }

    # List of users
    choiceListForUsers = []

    # Look up userId by username
    print 'Querying SnipeIT for available users...'
    response = requests.get(usersUrl, headers=headers, params=queryParams, verify=False)
    users = response.json().get('rows')
    print 'Response Status: ' + str(requests.get(usersUrl, headers=headers, params=queryParams, verify=False))

    # Load Accessories
    print 'Loading Accessories'
    response = requests.get(accessoriesUrl, headers=headers, params=queryParams, verify=False)
    accessories = response.json().get('rows')
    print 'Loading Accessories Complete'

    if users:
        users.sort(key=extract_name, reverse=False)
        for row in users:
            choiceListForUsers.append({'name': str(row['id']) + ' - ' + HTMLParser.HTMLParser().unescape(row['name']).encode('utf-8') + ' - ' + HTMLParser.HTMLParser().unescape(row['username']).encode('utf-8')})
        print 'Query completed.'
        userSelectionTemplate['choices'] = choiceListForUsers

        # Prompt user to select assignedTo user
        selection = prompt(userSelectionTemplate)

        assignedToUser = selection['assignedToUser']
        fields = assignedToUser.split('-')
        userId = fields[0].strip()

        with open(filename) as accessories_file, open(updatedAccessoriesName, 'w+') as updated_accessories_file:
            accessoriesCsv = csv.DictReader(accessories_file, skipinitialspace=True)

            accessoryId = None
            assignedTo = None

            foundAccessory = False
            foundUser = False

            assignedAccessories = []

            for accessoryRow in accessoriesCsv:
                # Grab Accessory's Id from Accessory's List
                for accessory in accessories:
                    if accessory['name'].strip() == accessoryRow['Item Name'].strip():
                        accessoryId = accessory['id']

                # Grab Assigned To User's Id from List
                for user in users:
                    if user['name'].strip() == accessoryRow['Customer Name']:
                        assignedTo = user['id']

                if accessoryId and assignedTo:
                    if [str(accessoryId), str(assignedTo)] not in assignedAccessories:
                        updated_accessories_file.write('INSERT INTO accessories_users (USER_ID, ACCESSORY_ID, ASSIGNED_TO, CREATED_AT) VALUES (%s, %s, %s, CURRENT_TIMESTAMP);\n' % (userId, accessoryId, assignedTo))
                        assignedAccessories.append([str(accessoryId), str(assignedTo)])
                
            print str(assignedAccessories)
    else:
        print 'Response was either invalid or empty from server'

if __name__ == '__main__':
    main()

print 'DONE'