# Family-Tree

This is REST API implemented in flask capable of keeping track of people and the connections between them.


## How to execute:
> export PYTHONPATH=$PYTHONPATH:PATH_TO_DOWNLOADED_PROJECT  
> source venv/bin/activate  
> python code/app.py  



## Project Details

Following are the traits of each person present in the hierarchy:
- First name
- Last name
- Phone number
- Email address
- Address
- Birth date

Following information is provided by the API.
- For a given person list all of their siblings
- For a given person list all of their parents
- For a given person list all their children
- For a given person list all of their grandparents
- For a given person list all of their cousins

## API Documentation:  

1. User API:
    - <b> /user/register </b> [POST]: This endpoint is used to register users for accessing the API.  
      <b> payload fields: </b> username, password
      <b> required </b>: username, password   
      Eg:- `{ "username": "jkhuttan", "password": "qwerty" }`

    - <b> /login </b> [POST]: This endpoint is used to login into the application. Returns back the JWT token, which is primarily used when doing DELETE operations.  
      <b> payload fields: </b> username, password  
      <b> required </b>: username, password  
      Eg:- `{ "username": "jkhuttan", "password": "qwerty" }`

    - <b> /user/\<string:username\> </b> [GET]: This endpoint returns the user id & username registered in the DB.
  
2. Family API:
    - <b> /family/register </b> [POST]: This endpoint is used to create a family in DB. Just provide the family name that you want to create, it autogenerates an ID for it & returns back.  
      <b> payload fields: </b> family_name (required)  
      Eg:- `{ "family_name": "Alphabet Family" }`  

    - <b> /family/\<int:family_id\> </b> [GET]: Based on the given family id, it returns back family id, family name & members of the family.  
  
3. Member API:
    - <b> /member </b> [POST]: This endpoint is used to create a family member.  
      <b> payload fields </b>: family_id, first_name, last_name, birth_date, phone_number, address, email_id.  
      <b> required: </b> family_id, first_name, last_name, birth_date.  
      <b> optional: </b> phone_number, address, email_id.  
      Eg:- `{
        "family_id": 1,
        "first_name": "Jitesh",
        "last_name": "Khuttan",
        "birth_date": "20-10-1996"
      }`

    - <b> /member </b> [GET]: This endpoint is used to search a member in database. Search can be made using - member id, first name or last name.
      If multiple parameters specified, search is performed in following priority: <b> memberid > firstname > lastname </b>   
      <b> query parameters: </b> ?memberid=1, ?firstname=Jitesh, ?lastname=Khuttan

    - <b> /member/additional-details </b> [POST]: This endpoint can be used to add address, phone number or email id for member. This can be called multiple times as well for same member, because all these three fields are multi-valued.  
      <b> payload fields </b>: member_id, address, phone_number, email_id  
      <b> required </b>: member_id  
      <b> optional </b>: address, phone_number, email  
      Eg:- `{
          "member_id": 1,
          "address": "Boston",
          "phone_number": "9465XXXXXX",
          "email": "A.a@gmail.com"
      }`

     - <b> /member/additional-details </b> [PUT]: This endpoint can be used to update address, phone number or email id for member.  
       <b> payload fields </b>: member_id, current_address, new_address, current_phone_number, new_phone_number, current_email, new_email  
       <b> required </b>: member_id, (current_address, new_address), (current_phone_number, new_phone_number), (current_email, new_email)  
       NOTE:- address, phone_number, email are optional, but required in pairs if one of them is mentioned.
       Eg:- `{
          "member_id": 1,
          "current_address": "Boston",
          "new_address": "New York"
      }`
    
4. Parent-Child API:
    - <b> /parent </b> [POST]: This endpoint is used to add parent-child relationships. You can basically tell, which member should act as a parent for which member. Member ids can always be retrived by calling GET /family/<family_id> API.  
       <b> payload fields </b>: parent_id, child_id  
       <b> required </b>: parent_id, child_id
       Eg:- `{
          "parent_id": 1,
          "child_id": 3
      }`

    - <b> /parent/\<int:member_id\> </b> [GET]: This endpoint is used to retrieve parents for given member_id.  
    - <b> /parent </b> [DELETE]: This endpoint is used to delete some parent-child relationship. You need to send in payload - parent_id, child_id for which relationship needs to be dropped.  
      <b> payload fields </b>: parent_id, child_id  
      <b> required </b>: parent_id, child_id  
    - <b> /children/\<int:member_id\> </b> [GET]: This endpoint is used to retrieve all the childs for given member_id. 
  
5. Sibling API:
    - <b> /sibling </b> [POST]: This endpoint is used to add sibling relationship between two members.  
      <b> payload fields </b>: sibling_id1, sibling_id2  
      <b> required </b>: sibling_id1, sibling_id2  
      NOTE:- sibling_id1 -> is ID of a member who is already part of family tree i.e. already has some parent.  
             sibling_id2 -> is not a part of family tree yet i.e. it is present in family as a member but not linked to anyone yet.    
      Eg:- `{
          "sibling_id1": 3,
          "sibling_id2": 4 
      }`

    - <b> /sibling/\<int:member_id\> </b> [GET]: This endpoint returns all the siblings for a given member id.  
    - <b> /sibling </b> [DELETE]: This endpoint is used to remove sibling relationship between two members having same parent.  
      <b> payload fields </b>: sibling_id1, sibling_id2  
      <b> required </b>: sibling_id1, sibling_id2  
      Eg:- `{
          "sibling_id1": 3,
          "sibling_id2": 4 
      }`
    
    
6. Grandparent API:
    - <b> /grandparent/\<int:member_id\> </b> [GET]: This API is used to retrieve all the grandparents for the given member id.
  
7. Cousin API:
    - <b> /cousin/\<int:member_id\> [GET]: This API is used to retrieve all the cousins for the given member id.
