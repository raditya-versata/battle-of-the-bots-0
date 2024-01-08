# 🤖 Battle of the Bots Starter Kit 🚀

Welcome to the "Battle of the Bots Starter Kit" project! This repository is your starting point to dive into the world of AWS Serverless Applications with AWS SAM 🛠, AWS Lambda 🧙‍♂️, and Amazon API Gateway 🌉. Choose your favorite programming language - Node.js 🟢 or Python 🐍 - to build your bot and join the battle!

## 🚀 Getting Started

### Prerequisites

Some CS pre-requisites to get started are:

- Membership to the AD Group: [RAM-AWS-Dev-CentralSupport-csaielite-Admin](https://supportportal-df.atlassian.net/servicedesk/customer/portal/6/group/76/create/367)
  - This will get you access to our AWS Sandbox account.
- An API Key for our Ticket Cache API specifically for the Battle of the Bots (ping James Miller in GChat to make this for you).

Before you begin, make sure you have the following installed. **Note:** If you are using the pre-built environment, you should be good on these requirements.

- AWS CLI: [Installation Guide](https://aws.amazon.com/cli/)
- AWS SAM CLI: [Installation Guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
- AWS Credentials via Devfactory:
  - In the prebuilt environment, available via `devfactory-aws-keys`
  - Otherwise, follow [AWS CLI Access thru ADFS](https://trilogy-confluence.atlassian.net/wiki/spaces/ALIN/pages/363036197/AWS+CLI+access+thru+ADFS)
- Docker: [Installation Guide](https://docs.docker.com/get-docker/)
- Python 3.x: [Download Python](https://www.python.org/downloads/) (if using Python)
- Node.js: [Download Node.js](https://nodejs.org/) (if using Node.js)

### 📦 Installation

1. **Clone the Starter Kit**:
   ```bash
   git clone https://github.com/jamesmiller-trilogy/battle-of-the-bots-starter.git
   ```
2. **Enter the Arena**:
   ```bash
   cd battle-of-the-bots-starter
   ```

## 🏗 Project Structure

- `lambda/node`: Home of the Node.js Lambda starter function.
- `lambda/python`: Home of the Python Lambda starter function.
- `scripts`: Scripts that build environment variables for you, before testing and deployment.
- `templates`: Language specific blueprints for your AWS SAM setup.

### Lambda Details

Right now, the lambda functions are mostly a blank canvas for you to begin scripting your bot.

However, they both make calls to a special API to get ticket information from a special cache we have set up for you:

```node
    // Set our ticket cache API endpoint.
    const apiUrl = 'https://t2kc19w5te.execute-api.us-east-1.amazonaws.com/prod';

    // Making a fetch call to the API
    const response = await fetch(`${apiUrl}?ticketId=${ticketId}`, {
        headers: {
            'Authorization': `Bearer ${process.env.TICKET_TOKEN}`
        }
    });
```

## 🛠 Build and Deploy

Embark on your journey to deploying your bot, whether it's crafted in Node.js 🟢 or Python 🐍. Here's how to bring your creation to life in the AWS cloud.

### Initial Setup

1. **Choose Your Language**:
   Decide whether you're going to use Node.js or Python for your Lambda function.
   - For Node.js, copy the Node.js template:
     ```bash
     cp templates/node-template.yaml template.yaml
     ```
   - For Python, copy the Python template:
     ```bash
     cp templates/python-template.yaml template.yaml
     ```

2. **Python Build Step (Not Needed for NodeJS)**:
   Be sure to install the `requests` package in Python like so:

   ```bash
   pip install -r lambda/python/requirements.txt -t lambda/python/dependencies/
   ```

3. **Start Your Local API**:
   Use the `start-api.sh` script to set up your environment variables (for the first time) and to start running the local API with the demo functions.
   ```bash
   ./scripts/start-api.sh
   ```
   This script will guide you through setting up any necessary environment variables and kick off your local API for testing.

### Deploying to AWS

4. **Prepare for the Cloud**:
   Before deploying, ensure you have the necessary AWS credentials. This can be done either through the `devfactory-aws-keys` command or by following the AWS credential setup guide in the "Requirements" section.

5. **Deploy Your Bot**:
   Once you're ready to test your project in the cloud, use the `deploy.sh` script to deploy your bot to AWS.
   ```bash
   ./scripts/deploy.sh
   ```
   This script will package your Lambda function, upload it to AWS, and deploy your API Gateway, allowing your bot to interact with the world.

### 🚀 Launching Your Bot into the Cloud

When you feel your bot is ready for a real challenge, it's time to deploy it to the AWS cloud. Use the `deploy.sh` script to unleash its potential in the vast AWS arena.

```bash
./scripts/deploy.sh
```

This script will handle the complexities of deployment, ensuring your bot finds its place in the cloud, ready to respond and interact.

## 📚 Additional Resources

Check out these docs for more knowledge:

- [AWS SAM Developer Guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html)
- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
- [Amazon API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html)

---

May the code be with you on your journey to become the ultimate bot champion! 🏆🤖
