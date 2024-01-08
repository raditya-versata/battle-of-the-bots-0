#!/bin/bash

# Path to the .env file
ENV_FILE=".env"

# Check if .env file exists
if [ -f "$ENV_FILE" ]; then
  # Load environment variables from .env file
  export $(cat $ENV_FILE | xargs)
else
  # Prompt the user for input and create the .env file
  echo "No .env file detected. Let's create one."

  # Prompt for AGENT_NAME
  read -p "Enter your AGENT_NAME (like JamesMiller): " AGENT_NAME
  echo "AGENT_NAME=${AGENT_NAME}" > $ENV_FILE

  # Prompt for TICKET_TOKEN
  read -p "Enter your TICKET_TOKEN (like botdev.xxxx...): " TICKET_TOKEN
  echo "TICKET_TOKEN=${TICKET_TOKEN}" >> $ENV_FILE

  # Export the newly entered variables
  export AGENT_NAME TICKET_TOKEN
fi

# Deploy with SAM using environment variables
sam build
sam deploy --guided --profile=saml --parameter-overrides AgentName=$AGENT_NAME TicketToken=$TICKET_TOKEN