# AutoGrader System


Developed an intelligent Auto Grader platform featuring secure user authentication, which autonomously evaluates students' programming submissions against comprehensive predefined test cases. This innovative system streamlines the assessment process, ensuring consistent and objective grading of coding assignments while maintaining data integrity through robust login functionality.

Choice of Frameworks and Tools:

## FrontEnd:
* **Flask**: Lightweight and well-suited for building simple web applications with user interfaces. It's easy to use, making it a good choice for this project.
* **HTML/CSS**: Easy to generate templates for user interface.

## BackEnd:
* **Boto3**: Python library for interacting with AWS services. Used for Cognito and DynamoDB interaction.
* **AWS Cognito**: Manages user authentication and authorization for secure access.
* **AWS DynamoDB**: Store student grades
