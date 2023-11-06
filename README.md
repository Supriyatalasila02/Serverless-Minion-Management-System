# Serverless-Minion-Management-System


#### AWS Serverless:
###### Without the need of managing infrastructure, applications and services can be created and run using serverless architecture. Although the application continues to operate on servers, AWS handles all server administration. To run our apps, databases, and storage systems, we longer need to maintain servers. Serverless computing is event driven, the implementation and management of servers is different from the traditional architectures in enterprise environments also AWS Serverless is cost effective.
#### AWS Services Used:
#### 1. DynamoDB:
Amazon DynamoDB is a NoSQL database engine which stands out with its ability to support tables of any size. It is a serverless, Key-value NoSQL database which is designed to run high performance applications at any scale.
#### 2. AWS Lambda:
AWS Lambda is a serverless, even driven computing service that lets us run code virtually for any kind of application without the need of managing servers. There are mainly three components –function which is the actual code that performs the required task, Configuration to specify the execution of the function and an Event source to trigger the function. While configuring the lambda function, we specify which runtime environment is needed to run our code.
#### 3. AWS API Gateway:
Amazon API Gateway is a fully managed service that helps developers to create, publish, monitor, maintain and secure APIs at any scale. Using Amazon API Gateway, we will be able to create both RESTful APIs and WebSocket APIs that enable apps with real-time two-way communication. 
#### 4. IAM Role:
An IAM Role is an IAM identity that can be created in our account that has specific permissions.We can use roles to grant access to users, applications, services that usually don’t have access to our AWS resources.
#### 5. CloudWatch:
Amazon CloudWatch is a monitoring and observability service that collects the data in the form of logs, events and metrics. Any anomalous behavior in our environments can be detected using CloudWatch, also we can visualize logs and metrics side by side to troubleshoot issues, take required action and keep smooth running of our applications.


The Client sends a Post Request. This request goes to GruMinion API (API Gateway) and forwarded to the attached RequestMinion (Lambda function). The Lambda function fetches the data from MinionTable (DynamoDB) and the Response is sent back to the API Gateway which in-turn forwards the response to the client. Exception Handling is used in the Lambda function to catch if any error occurs, and these errors are logged in to CloudWatch.
#### Step1: Create Table in DynamoDB (Minion)
The Partition key (MinionID) is a string, and it is a mandatory field. We are using the Default settings for the remaining. The details of the Minions are stored in Minion Table and the partition key is the unique identifier of the minion and the sample data in the table contains “MinionID” – M1, M2, M3, M4, M5, M6, M7, M8, M9. 
Alongside, for each Minion we have maintained details of “EyeColor”, HairColor, Name, Occupation for the data present. We have a key called “IsSummoned” to maintain the Flag status of the Minion which is initially set to False.
#### Step2: Create New role (DynamoDbCloudWatchRole)
Create a new role in IAM Console. This Role will be attached to the Lambda Function (RequestMinion) to access DynamoDB Tables. This Role will have the “CompleteDynamoDbAccessPolicy” which is an Inline Policy. This policy is created in the next step. Also, attach AWS Managed “CloudWatchLogsFullAccess” Policy which is used for accessing CloudWatch.
#### Step3: Create new Customer Inline Policy (“CompleteDynamoDbAccessPolicy”)
#### Step4: Create Lambda Function (RequestMinion)
Create a Lambda function with python3.9 environment. The Role created in Step2 is attached to this Lambda function. This role is required to access the DynamoDB Tables and CloudWatch. This Lambda function logs errors to CloudWatch, used for debugging. This Lambda function will be integrated with AWS API Gateway in the next step.
After the Minion is Summoned through POST API call, the “IsSummoned” flag status is set to True and if the user tries to invoke the same Minion again, the details cannot be retrieved and a custom Message “Minion with id {MinionId} is already summoned”.
If the User tries to retrieve details of the Minion with invalid MinionID, a custom message “Minion with id {'MinionId'} not found” is sent back as response.
#### Step5: Create API (GruMinion)
Create API in AWS API Gateway service. Choose REST API and fill all the necessary details. Create a Resource(/summon) in the API and create a Post Method in the resource. Select Lambda Function in the integration type. Paste the RequestMinion Lambda function’s ARN in the Lambda function field. This will attach our Lambda function to the method created in Resource.
