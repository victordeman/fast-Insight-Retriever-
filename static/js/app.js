document.getElementById('query-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const input = document.getElementById('query-input');
    const query = input.value;
    const chatWindow = document.getElementById('chat-window');

    if (!query) return;

    // Add User Message
    chatWindow.innerHTML += `
        <div class="flex justify-end">
            <div class="bg-slate-800 text-white p-3 rounded-lg rounded-tr-none max-w-xs md:max-w-md shadow-sm mb-4">
                ${query}
            </div>
        </div>
    `;
    input.value = '';
    chatWindow.scrollTop = chatWindow.scrollHeight;

    // Show Loading
    const loadingId = 'loading-' + Date.now();
    chatWindow.innerHTML += `
        <div id="${loadingId}" class="flex start animate-pulse">
            <div class="bg-gray-200 p-3 rounded-lg max-w-xs text-gray-500">
                Thinking...
            </div>
        </div>
    `;
    chatWindow.scrollTop = chatWindow.scrollHeight;

    try {
        const response = await fetch('/api/query', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query })
        });
        const data = await response.json();

        // Remove Loading
        document.getElementById(loadingId).remove();

        // Add Bot Response
        chatWindow.innerHTML += `
            <div class="flex start">
                <div class="bg-blue-100 p-3 rounded-lg rounded-tl-none max-w-xs md:max-w-md text-slate-800 shadow-sm mb-4">
                    ${data.answer}
                </div>
            </div>
        `;
    } catch (error) {
        document.getElementById(loadingId).innerText = "Error fetching response.";
    }
    chatWindow.scrollTop = chatWindow.scrollHeight;
});
