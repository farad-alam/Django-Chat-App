
function appendMessage(message, sendByUserId, userId) {
    const chatbox = document.querySelector('.chatbox');

    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');

    const paragraph = document.createElement('p');
    const messageText = document.createTextNode(message.message);
    paragraph.appendChild(messageText);

    // const timeStamp = document.createElement('span');
    // timeStamp.textContent = ' ' + getMessageTimeStamp(); // Function to get the timestamp

    // paragraph.appendChild(document.createElement('br'));
    // paragraph.appendChild(timeStamp);

    messageDiv.appendChild(paragraph);
    console.log(parseInt(sendByUserId), userId)
    // Check if the message is sent to the user or sent by the user
    if (parseInt(sendByUserId) === userId) {
        messageDiv.classList.add('friend_msg');
    } else {
        messageDiv.classList.add('my_msg');
    }

    chatbox.appendChild(messageDiv);
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
        appendMessage(data, data.send_by_user_id, userId);
        
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

