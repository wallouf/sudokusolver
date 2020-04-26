# sudokusolver

* Description
* Design
* Lib used
* Notes

## Description

Sudoku solver is a little project to help me resolve my sudoku. I was bored to not having the solution of my sudoku. So i end up doing this to prepare the solution before doing my sudoku.

It help me to re-do a little project with Python, Web and AWS technologies.

So in the end, what you have is:
 - A web with Bootstrap
 - A login management with AWS Cognito
 - An upload page where you can push your sudoku picture and after a processing done by AWS Lambda - Restful API call the image you've uploaded with the right numbers filled.
 - The back-end use AWS lambda, AWS Api gateway and Python

## Design

Overview of the solution:
![AWS Sudoku Solver - By Wallouf](https://github.com/wallouf/help/GITHUB-WALLOUF-AWS_Sudoku_Solver.jpeg)


## Lib used

### Web:
* Bootstrap 4.4
* Jquery 3.4.1
* Popper 1.16
* AWS Cognito SDK

### AWS:
* API Gateway
* AWS Lambda & AWS Lambda Layer
* AWS S3 static hosting
* AWS IAM, AWS Cognito
* AWS S3 for layers

### Python:
* For the image recognition, i follow the help of this github: https://github.com/abidrahmank/OpenCV2-Python

Lib used:
* Numpy
* OpenCV
* Pillow
* Pytesseract

## Notes
Help for the parts i've got problems:

### CORS:
When i first re-use API Gateway and Lambda for this project, i've got the CORS bad return.
To solve this problem do not forget two important part on the "Server" side AWS:
* On your api gateway ressource, use the option to "enable CORS", and after do not forget to "redeploy"
* On your lambda code, do not forget to return in your response the CORS flag. This is the part where is was really stuck:

This is a non-working example:
`
return {
        'statusCode': 200,
        'body': json.dumps("TEST")
    }
`
This is a working example:
`
return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps("TEST")
    }
`

### Numbers recognition:
You can see in the image processing multiple try to be sure of the number detected.
At first i was using only one Knearest call but that didn't work for numbers like: 7 <-> 1 and 8 <-> 3

SO i order to improve that, i use multiple blur type and multiple Knearest call and get the max result

## To do

### AWS
* Set up a AWS CloudFormation in order to automate deployment
* Set up a CI with 5 image to test new code
* Set up a CD with AWS to deploy code in the lambda after a new commit or merge in the master branch with github

### Front-end
* Add "Download result" option
* Show side by side orignal and result images

### Back-end
* Clean sudoku python code
* Clean X & Y processing. Too much complicated to retrieve pos X and pos Y from case or square
* Clean list usage to get values