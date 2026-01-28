const ws = new WebSocket(`ws://${location.hostname}:8765`);
const messages = document.getElementById("messages");
const form = document.getElementById("chatForm");
const input = document.getElementById("messageInput");
const toggle = document.getElementById("themeToggle");

ws.onmessage = (e) => {
    const div = document.createElement("div");
    div.className = "message";
    div.textContent = e.data;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
};

form.onsubmit = (e) => {
    e.preventDefault();
    if (input.value.trim()) {
        ws.send(input.value);
        input.value = "";
    }
};

toggle.onclick = () => {
    document.body.classList.toggle("dark");
};
