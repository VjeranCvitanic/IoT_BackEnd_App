const axios = require('axios');

axios.get('http://127.0.0.1:8000/location1/room1')
  .then(response => {
    console.log(response.data); // Print the response data
  })
  .catch(error => {
    console.error('Error:', error); // Print any errors that occurred
  });
