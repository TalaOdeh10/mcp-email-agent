const form = document.getElementById("chat-form");

const input = document.getElementById("message-input");

const sendButton = document.getElementById("send-button");

const messages = document.getElementById("messages");

const newChatButton = document.getElementById("new-chat");

const suggestions = document.querySelectorAll(".suggestion");


// ========================================
// Send message
// ========================================

form.addEventListener("submit", async function (event) {

    event.preventDefault();


    const message = input.value.trim();


    if (!message) {
        return;
    }


    // Remove welcome screen

    const welcome = document.querySelector(".welcome");

    if (welcome) {
        welcome.remove();
    }


    // Show user message

    addMessage(
        message,
        "user"
    );


    // Clear input

    input.value = "";


    // Disable input while waiting

    setLoading(true);


    // Show loading animation

    const loadingMessage = addLoadingMessage();


    try {

        const response = await fetch(
            "http://127.0.0.1:8000/chat",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    message: message
                })
            }
        );


        // Check HTTP status

        if (!response.ok) {

            throw new Error(
                `Server returned ${response.status}`
            );

        }


        const data = await response.json();


        // Remove loading

        loadingMessage.remove();


        // Show AI response

        addMessage(
            data.response,
            "assistant"
        );


    } catch (error) {

        console.error(error);


        // Remove loading

        loadingMessage.remove();


        // Show error

        addMessage(
            "I couldn't connect to the AI agent. Make sure the FastAPI server is running.",
            "assistant"
        );

    }


    // Enable input again

    setLoading(false);


    input.focus();

});


// ========================================
// Add normal message
// ========================================

function addMessage(text, sender) {

    const messageElement =
        document.createElement("div");

    messageElement.classList.add(
        "message",
        sender
    );


    const bubble =
        document.createElement("div");

    bubble.classList.add("bubble");

    bubble.textContent = text;


    messageElement.appendChild(bubble);

    messages.appendChild(messageElement);


    scrollToBottom();


    return messageElement;
}


// ========================================
// Loading animation
// ========================================

function addLoadingMessage() {

    const messageElement =
        document.createElement("div");

    messageElement.classList.add(
        "message",
        "assistant"
    );


    const bubble =
        document.createElement("div");

    bubble.classList.add("bubble");


    bubble.innerHTML = `
        <div class="loading">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;


    messageElement.appendChild(bubble);

    messages.appendChild(messageElement);


    scrollToBottom();


    return messageElement;
}


// ========================================
// Loading state
// ========================================

function setLoading(isLoading) {

    input.disabled = isLoading;

    sendButton.disabled = isLoading;


    if (isLoading) {

        sendButton.textContent = "Sending...";

    } else {

        sendButton.textContent = "Send";

    }

}


// ========================================
// Scroll chat down
// ========================================

function scrollToBottom() {

    messages.scrollTop =
        messages.scrollHeight;

}


// ========================================
// Suggestion buttons
// ========================================

suggestions.forEach(function (button) {

    button.addEventListener(
        "click",
        function () {

            input.value =
                button.textContent;

            input.focus();

        }
    );

});


// ========================================
// New chat
// ========================================

newChatButton.addEventListener(
    "click",
    function () {

        messages.innerHTML = "";


        addMessage(
            "Hi! What would you like me to help you with?",
            "assistant"
        );


        input.value = "";

        input.focus();

    }
);