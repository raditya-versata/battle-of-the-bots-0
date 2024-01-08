exports.handler = async (event) => {
  try {
      // Read the ticketId from the URL query parameters
      const ticketId = event.queryStringParameters.ticketId;

      if (!ticketId) {
          return {
              statusCode: 400,
              body: JSON.stringify({ message: 'Missing ticketId parameter' }),
          };
      }

      // Set our ticket cache API endpoint.
      const apiUrl = 'https://t2kc19w5te.execute-api.us-east-1.amazonaws.com/prod';

      // Making a fetch call to the API
      const response = await fetch(`${apiUrl}?ticketId=${ticketId}`, {
          headers: {
              'Authorization': `Bearer ${process.env.TICKET_TOKEN}`
          }
      });
      
      // Parsing the JSON response
      const data = await response.json();

      const { id, subject } = data.ticket;
      const { name, email } = data.users[0];

      // This is where you make the magic happen. 
      // Call an AI model, process the ticket data, etc.
      // Then, build your response!
      
      const aiResponse = 
          `Dear ${name},\n\n` +
          `Beep boop. I am a robot.\n\n` +
          `This is regarding ticket #${id}.\n\n` + 
          `I can see this request is regarding ${subject}\n\n` +
          `We will get back to you at ${email} as soon as possible.\n\n` +
          `Best regards,\n\n` + 
          `L2 Support Bot`;

      // Returning the JSON response
      return {
          statusCode: 200,
          body: JSON.stringify({ aiResponse }),
      };

  } catch (error) {
      console.error('Error:', error);

      return {
          statusCode: 500,
          body: JSON.stringify({ message: 'Internal Server Error' }),
      };
  }
};