/**
 * Chat widget that renders LLM responses in the browser.
 */

async function sendMessage(userMessage) {
  const response = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: userMessage }),
  });
  const data = await response.json();

  // Render the assistant's response
  const chatContainer = document.getElementById("chat-messages");
  const messageDiv = document.createElement("div");
  messageDiv.className = "assistant-message";
  messageDiv.innerHTML = data.response;
  chatContainer.appendChild(messageDiv);

  // Also update the summary sidebar
  document.getElementById("conversation-summary").innerHTML = data.summary;
}

function renderMarkdown(text) {
  // Simple markdown rendering
  const html = text
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.*?)\*/g, "<em>$1</em>")
    .replace(/`(.*?)`/g, "<code>$1</code>");
  return html;
}
