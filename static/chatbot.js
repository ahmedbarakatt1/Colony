document.addEventListener('DOMContentLoaded', function () {
    const messagesDiv = document.getElementById('chatbot-messages');
    const inputField = document.getElementById('chatbot-input');
    const sendButton = document.getElementById('chatbot-send');

    sendButton.addEventListener('click', () => {
        const userMessage = inputField.value.trim();
        if (!userMessage) return; // Ignore empty input

        // Display user's message
        const userMessageDiv = document.createElement('div');
        userMessageDiv.className = 'chatbot-message user';
        userMessageDiv.textContent = userMessage;
        messagesDiv.appendChild(userMessageDiv);

        // Clear input field
        inputField.value = '';

        // Send message to the chatbot backend
        fetch('/chatbot', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: userMessage })
        })
        .then(response => response.json())
        .then(data => {
            // Display bot's response
            const botMessageDiv = document.createElement('div');
            botMessageDiv.className = 'chatbot-message bot';
            botMessageDiv.textContent = data.response;
            messagesDiv.appendChild(botMessageDiv);

            // Scroll to the bottom of the messages container
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        })
        .catch(() => {
            // Display an error message if the backend fails
            const botMessageDiv = document.createElement('div');
            botMessageDiv.className = 'chatbot-message bot';
            botMessageDiv.textContent = "An error occurred. Please try again.";
            messagesDiv.appendChild(botMessageDiv);
        });
    });
});
