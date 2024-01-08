#!/bin/bash

# Path to the .env file
ENV_FILE=".env"
JSON_ENV_FILE="env.json"

# Convert .env to JSON format for SAM
convert_env_to_json() {
    # Extract AgentName from the .env file
    local agent_name=$(grep -oP '^AGENT_NAME=\K.*' "$ENV_FILE")

    # Construct the Lambda function name
    local lambda_function_name="${agent_name}-AiResponseLambdaFunction"

    # Start JSON file with Lambda function name
    echo "{\"${lambda_function_name}\": {" > $JSON_ENV_FILE

    # Add environment variables to JSON, skipping the AgentName
    grep -v '^AGENT_NAME=' "$ENV_FILE" | while IFS='=' read -r key value
    do
        echo "  \"${key}\": \"${value}\"," >> $JSON_ENV_FILE
    done

    # Remove the last comma and close the JSON object
    sed -i '$ s/,$//' $JSON_ENV_FILE
    echo "}}" >> $JSON_ENV_FILE
}

# Check if .env file exists
if [ -f "$ENV_FILE" ]; then
  # Load environment variables from .env file
  export $(cat $ENV_FILE | xargs)
else
  # Prompt the user for input and create the .env file
  echo "No .env file detected. Let's create one."

  # Prompt for AGENT_NAME
  read -p "Enter your AGENT_NAME: " AGENT_NAME
  echo "AGENT_NAME=${AGENT_NAME}" > $ENV_FILE

  # Prompt for TICKET_TOKEN
  read -p "Enter your TICKET_TOKEN: " TICKET_TOKEN
  echo "TICKET_TOKEN=${TICKET_TOKEN}" >> $ENV_FILE

  # Export the newly entered variables
  export AGENT_NAME TICKET_TOKEN
fi

# Convert .env to JSON format
convert_env_to_json

# Start local API using SAM with environment variables
sam build
sam local start-api --env-vars $JSON_ENV_FILE
