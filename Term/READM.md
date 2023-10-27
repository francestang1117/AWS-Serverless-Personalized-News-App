# Introduction
This project a news sentimental analysis system powered by AWS cloud services that send users email notification based on their specified preferences. The application processes user inputs such as keywords, language, and sortBy from a React frontend. These input trigger AWS Lambda Functions through an API Gateway that retrieve news articles using the News API and analyze them with AWS Comprehend for sentiment analysis. The collected data, including the sentiment results, are stored in a DynamoDB table named NEWS, which in turn triggers SNS to send emails to users. The frontend React application is hosted on an EC2 instance and all services, excluding an S3 bucket created manually for storing Lambda function zip files, React news zip file and layer zip file, are provisioned through AWS CloudFormation. This application not only fetches news based on the user's specific inputs, but it also analyses the sentiment of the content or the title of the news articles. This sentiment analysis gives users an immediate understanding of the overall tone of the news article - whether it is positive, negative, or neutral. This information can be valuable to users as it offers a quick glimpse into the general sentiment surrounding their topics of interest, potentially saving them reading time and helping them to prioritize which articles to read in depth.
# Enhanced performance targets
An additional performance target would be:
1. Sentiment Analysis Accuracy: The sentiment analysis performed by AWS Comprehend should be highly accurate, correctly interpreting the sentiment conveyed in the news article content or title. Achieving a high level of accuracy in sentiment scores will significantly increase the value of the news alerts for users.
2. Response Time: The system should respond promptly to user requests, ideally within a few seconds. We will set up AWS CloudWatch to monitor the latency of our API Gateway and Lambda functions to ensure this target is consistently met.
3. Monitoring and Visualization: All the KPIs (like response time, availability, scalability, email delivery rate, and sentiment analysis accuracy) will be continuously monitored and visualized using AWS CloudWatch. This will provide us with a real-time overview of our system's performance.
4. AWS Quicksight Integration: We can connect Quicksight to our DynamoDB tables and create visualizations for:
    * Trends in Sentiment: Plot sentiment scores over time to identify trends in how the sentiment (positive, negative, or neutral) is evolving for specific topics.
    * Volume of News: Visualize the volume of news related to user-specified keywords over time. This can highlight when there is a spike in news articles for a specific topic, indicating potentially significant events.
    * Keyword Frequency: Show the frequency of user-specified keywords in the news content, which can help users to better understand their prominence in the news landscape.
# Cloud Service Selection
1. **AWS API Gateway**: This service was chosen to handle incoming requests from the client. API Gateway provides robust, secure, and scalable infrastructure to manage all the API calls. It is tightly integrated with other AWS services, simplifying the system architecture.<br>
**Alternative**: Google Cloud Endpoints, which is Google Cloud's equivalent to API Gateway, was considered. However, AWS API Gateway was chosen due to the project's preference for the AWS ecosystem and its seamless integration with other AWS services, such as Lambda and DynamoDB, which isn't as smooth in the case of Google Cloud Endpoints.
2. **AWS Lambda**: Lambda is a serverless compute service that was selected to handle all the backend logic, including fetching news from the News API, conducting sentiment analysis with AWS Comprehend, and managing data with DynamoDB.
   <br>**Alternative**: Azure Functions is a similar serverless compute service from Microsoft's Azure. It was not chosen due to the project's preference for AWS and the seamless integration provided within the AWS ecosystem.
3. **AWS Comprehend**: We chose Comprehend for sentiment analysis because it offers highly accurate natural language processing capabilities right out of the box and integrates seamlessly with other AWS services.
<br>**Alternative**: Google's Natural Language API, but this was not chosen because it does not integrate as smoothly with the other AWS services being used in this project.
4. **AWS DynamoDB**: DynamoDB was chosen as our database solution because of its seamless scalability, high availability, and integration with other AWS services.
<br>**Alternative**: Google's Firebase, which also provides a NoSQL database. However, the choice to use DynamoDB was made due to its tighter integration with AWS services and superior scalability.
5. **AWS SNS**: SNS was used for email notifications due to its reliability, scalability, and the ease with which it can be set up and used within the AWS ecosystem.
<br>**Alternative**: Google Pub/Sub, another publish-subscribe service, was considered. However, AWS SNS was chosen for its native integration with AWS services, its straightforward setup, and the flexibility it offers in terms of messaging protocols (including email), which isn't as convenient in Google Pub/Sub.
6. **AWS CloudFormation**: This service was used to manage and provision our AWS services and resources. This choice was made for its deep integration with AWS, the ability to handle dependencies, and automate the provisioning of resources.
<br>**Alternative**: Terraform, which also provides infrastructure as code capabilities, but it requires additional setup and doesn't have the same level of AWS service integration.
7. **AWS EC2**: I used EC2 to host our React frontend application because of its scalability, security, and deep integration with AWS services.
<br>**Alternative**: Google Cloud Compute Engine, but EC2 was chosen for its better integration with the rest of our AWS-based architecture.
8. **AWS S3**: S3 bucket is to store the zip files of the react app, lambda functions and their layers.
# Programming Languages used
**Python** was used to write the AWS Lambda functions due to its simplicity, readability, and extensive support for various libraries, including AWS SDKs.
The front-end, built with **React**, used JavaScript. React, a JavaScript library, was chosen because of its efficiency, flexibility, and strong community support.



