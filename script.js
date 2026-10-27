const input = document.getElementById("messageInput");
const chatBox = document.getElementById("chatBox");
const typing = document.getElementById("typing");


// ==========================================
// ENTER KEY
// ==========================================

input.addEventListener("keypress", function(event) {

    if (event.key === "Enter") {
        sendMessage();
    }

});


// ==========================================
// GET CURRENT TIME
// ==========================================

function getTime() {

    return new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit"
    });

}


// ==========================================
// ADD MESSAGE
// ==========================================

function addMessage(
    message,
    type,
    intent = null,
    confidence = null
) {

    const messageDiv =
        document.createElement("div");

    messageDiv.className =
        "message " + type;


    // BOT AVATAR

    if (type === "bot") {

        const avatar =
            document.createElement("div");

        avatar.className = "avatar";

        avatar.innerText = "🧠";

        messageDiv.appendChild(avatar);
    }


    const content =
        document.createElement("div");

    content.className =
        "message-content";


    const bubble =
        document.createElement("div");

    bubble.className =
        "bubble";


    // MESSAGE TEXT

    bubble.innerText = message;


    // ======================================
    // ANN INFORMATION
    // ======================================

    if (
        type === "bot" &&
        intent !== null &&
        confidence !== null
    ) {

        const info =
            document.createElement("div");

        info.className =
            "confidence";

        info.innerText =
            "Intent: " +
            intent +
            " • Confidence: " +
            confidence +
            "%";


        const bar =
            document.createElement("div");

        bar.className =
            "confidence-bar";


        const fill =
            document.createElement("div");

        fill.className =
            "confidence-fill";

        fill.style.width =
            Math.min(confidence, 100) + "%";


        bar.appendChild(fill);

        info.appendChild(bar);

        bubble.appendChild(info);

    }


    content.appendChild(bubble);


    // TIME

    const time =
        document.createElement("div");

    time.className = "time";

    time.innerText =
        type === "bot"
            ? "NeuroBot • " + getTime()
            : "You • " + getTime();


    content.appendChild(time);

    messageDiv.appendChild(content);

    chatBox.appendChild(messageDiv);


    // SCROLL

    chatBox.scrollTop =
        chatBox.scrollHeight;
}


// ==========================================
// TYPING INDICATOR
// ==========================================

function showTyping() {

    typing.classList.remove("hidden");

    chatBox.scrollTop =
        chatBox.scrollHeight;
}


function hideTyping() {

    typing.classList.add("hidden");
}


// ==========================================
// SEND MESSAGE
// ==========================================

async function sendMessage() {

    const message =
        input.value.trim();


    if (!message) {
        return;
    }


    // USER MESSAGE

    addMessage(
        message,
        "user"
    );


    input.value = "";


    // TYPING

    showTyping();


    try {

        const response =
            await fetch(
                "/chat",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({
                            message: message
                        })
                }
            );


        if (!response.ok) {
            throw new Error(
                "Server error"
            );
        }


        const data =
            await response.json();


        hideTyping();


        // BOT RESPONSE

        addMessage(

            data.response,

            "bot",

            data.intent,

            data.confidence

        );

    }


    catch (error) {

        console.error(error);

        hideTyping();


        addMessage(

            "Sorry, I couldn't connect to the NeuroBot server. Please make sure Flask is running.",

            "bot"

        );

    }

}


// ==========================================
// QUICK QUESTIONS
// ==========================================

function quickMessage(message) {

    input.value = message;

    sendMessage();

}