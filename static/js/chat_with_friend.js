
function appendMessage(message, sendByUserId, userId) {
    const chatbox = document.querySelector('.chatbox');

    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');

    const paragraph = document.createElement('p');
    const messageText = document.createTextNode(message.message_text);
    paragraph.appendChild(messageText);

    // Add timestamp
    const timestampSpan = document.createElement('span');
    const sendTime = new Date(message.send_time_str);
    const formattedTime = sendTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    timestampSpan.textContent = formattedTime;
    paragraph.appendChild(document.createElement('br'));
    paragraph.appendChild(timestampSpan);
    
    messageDiv.appendChild(paragraph);
    // console.log(parseInt(sendByUserId), userId)
    // Check if the message is sent to the user or sent by the user
    if (sendByUserId === userId) {
        messageDiv.classList.add('friend_msg');
    } else {
        messageDiv.classList.add('my_msg');
    }

    chatbox.appendChild(messageDiv);
}

function appendMessages(messages, sendByUserId, userId) {
    const chatbox = document.querySelector('.chatbox');

    messages.forEach(message => {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');

        const paragraph = document.createElement('p');
        const messageText = document.createTextNode(message.message_text);
        paragraph.appendChild(messageText);

        messageDiv.appendChild(paragraph);

        // Add timestamp
        const timestampSpan = document.createElement('span');
        const sendTime = new Date(message.send_time_str);
        const formattedTime = sendTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        timestampSpan.textContent = formattedTime;
        paragraph.appendChild(document.createElement('br'));
        paragraph.appendChild(timestampSpan);

        if (parseInt(message.send_by_id) === userId) {
            messageDiv.classList.add('friend_msg');
        } else {
            messageDiv.classList.add('my_msg');
        }

        chatbox.appendChild(messageDiv);
    });
}

document.addEventListener('DOMContentLoaded', function() {

    console.log("Yes Connected")

    const userId = JSON.parse(document.getElementById('user_id').textContent);

    console.log(userId)
    const chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/single-chat/'
        + userId
        + '/'
    );

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        console.log(data)

        if (Array.isArray(data.message)) {
            appendMessages(data.message, data.send_by_user_id, userId);
        } else {
            appendMessage(data, data.send_by_id, userId);
        }
        
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    document.querySelector('#chat-message-input').focus();
    document.querySelector('#chat-message-input').onkeyup = function(e) {
        if (e.key === 'Enter') {  // enter, return
            document.querySelector('#chat-message-submit').click();
        }
    };

    document.querySelector('#chat-message-submit').onclick = function(e) {
        const messageInputDom = document.querySelector('#chat-message-input');
        const message = messageInputDom.value;
        chatSocket.send(JSON.stringify({
            'message': message
        }));
        messageInputDom.value = '';
    };

  });

