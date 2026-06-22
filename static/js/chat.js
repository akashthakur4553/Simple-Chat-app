// Chat client logic for FastAPI WebSocket chat
// Handles connection, sending messages, and rendering incoming messages with avatar emoji.

const ws = new WebSocket(`ws://localhost:8000/ws`);
let myInfo = { ip: null, emoji: null };

ws.addEventListener('open', () => {
  console.log('WebSocket connection opened');
});

ws.addEventListener('message', (event) => {
  const payload = JSON.parse(event.data);
  const messagesDiv = document.getElementById('messages');
  // Handle initialization payload
  if (payload.type === 'init') {
    myInfo = { ip: payload.ip, emoji: payload.emoji, name: payload.name };
    updateActiveUsers([myInfo]);
    return;
  }
  // Handle presence updates
  if (payload.type === 'presence') {
    updateActiveUsers(payload.users);
    return;
  }
  // Regular chat message
  const bubble = document.createElement('div');
  bubble.className = 'message-bubble';
  if (payload.ip === myInfo.ip) {
    bubble.classList.add('self');
  }
  const emojiSpan = document.createElement('span');
  emojiSpan.className = 'emoji';
  emojiSpan.textContent = payload.emoji || '❓';
  const textSpan = document.createElement('span');
  textSpan.className = 'text';
  textSpan.textContent = `${payload.message}`;
  bubble.appendChild(emojiSpan);
  bubble.appendChild(textSpan);
  messagesDiv.appendChild(bubble);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
});

// Helper to update active users UI
function updateActiveUsers(users) {
  const container = document.getElementById('active-users');
  container.innerHTML = '';
  // Header indicating online users
  const header = document.createElement('div');
  header.className = 'online-header';
  header.textContent = 'These are the online:';
  container.appendChild(header);
  users.forEach(u => {
    const span = document.createElement('span');
    span.className = 'active-user';
    // Show emoji and assigned name instead of IP
    span.textContent = `${u.emoji} ${u.name || 'Anonymous'}`;
    container.appendChild(span);
  });
}

ws.addEventListener('error', (err) => {
  console.error('WebSocket error', err);
});

ws.addEventListener('close', () => {
  console.log('WebSocket connection closed');
});

window.addEventListener('beforeunload', () => {
  if (ws.readyState === WebSocket.OPEN) {
    ws.close();
  }
});

// Form handling
const form = document.getElementById('input-form');
const messageInput = document.getElementById('message');

form.addEventListener('submit', (e) => {
  e.preventDefault();
  const text = messageInput.value.trim();
  if (text === '') return;
  ws.send(JSON.stringify({ data: text }));
  messageInput.value = '';
});
