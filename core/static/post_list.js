const postLinks = document.querySelectorAll('.post-link');
const postContentDiv = document.querySelector('#post-content');
var modal = document.getElementById("myModal");

// post generation or population the main stuff
postLinks.forEach(link => {
    // Putting a lock icon before each lesson 
    link.innerHTML = "🔒 " + link.innerHTML;
    link.addEventListener('click', function (e) {
        e.preventDefault();

        fetchEnergyPoints().then(energyPoint => {
            const postId = this.dataset.id;
            const requiredEnergyPoint = (postId - 1) * 3;

            if (energyPoint < requiredEnergyPoint) {
                alert("Content is locked! Earn more energy points to unlock this lesson.");
                return;
            } else {
                this.innerHTML = this.innerHTML.replace("🔒 ", "");
                loadPostContent(postId);
            }
        });
    });
});

function loadPostContent(postId) {
    fetch(`/blog/api/posts/${postId}/`)
        .then(response => response.json())
        .then(data => {
            let mainContent = `
                <pre><h2>${data.title}</h2>
                <pre>${data.content}</pre>`;

            // Fetch function to send the post content (lesson) to back-end django server 
            function showContent(mainContent) {
                fetch('api/divcontent/?content=' + encodeURIComponent(mainContent))
                    .then(response => response.json())
                    .then(data => {
                        console.log(data);  // Log the response data
                    });
            }
            showContent(mainContent);

            let videoContent = '';
            if (data.youtube_video_id) {
                videoContent = `<iframe width="560" height="315" src="https://www.youtube.com/embed/${data.youtube_video_id}" frameborder="0" allowfullscreen></iframe>`;
            }

            let nextLesson = `<button id="nextLesson" class="custom-btn">NextLesson</button> <br>`;
            let completeContent = mainContent + videoContent + nextLesson;
            postContentDiv.innerHTML = completeContent;
        });
}

// Event delegation for the nextLesson button
postContentDiv.addEventListener('click', function (event) {
    if (event.target.id === 'nextLesson') {
        var modal = document.getElementById("myModal");
        modal.style.display = "block";

        fetch('progress/exercise/?answer=' + encodeURIComponent('go!'))
            .then(response => response.json())
            .then(data => {
                console.log(data);
                document.getElementById("gpt-asked-question").innerText = data.response;
            })
            .catch(error => {
                console.error("Error fetching data:", error);
            });
    }
});

// Modal close functionality
// 😊 Event delegation for modal close functionality 😊
document.body.addEventListener('click', function (event) {
    if (event.target.classList.contains('close')) {

        modal.style.display = "none";
        clearSession();
    }
});


// 😊 Event delegation for check question event listener 😊
document.body.addEventListener('click', function (event) {
    if (event.target.id === 'check_question') {
        console.log("Button clicked! 😃");
        var answer = document.getElementById('moadl_answer').value;
        document.getElementById('moadl_answer').value = '';

        fetch('progress/exercise/?answer=' + encodeURIComponent(answer))
            .then(response => response.json())
            .then(data => {
                document.getElementById("gpt-asked-question").innerText = data.response;
                console.log(data);
            });
    }
});


// Function to call backend Django for clearing the session
function clearSession() {
    fetch('progress/clear_session/')
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
        });
}



//interaction with vison bot
document.getElementById("send-button").addEventListener("click", function () {
    var message = document.getElementById("message-input").value;
    var conversationArea = document.getElementById("Conv-Container"); // use a single container for the whole conversation

    // Create a paragraph for the user's message and append it to the conversation area
    var userMessage = document.createElement('p');
    userMessage.classList.add('user-message'); // Add a class to style user messages differently
    userMessage.innerHTML = message;
    conversationArea.appendChild(userMessage);
    // empty the vision-bot input field after sending message
    document.getElementById("message-input").value = '';

    fetch('api/chat/?message=' + message)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            var aiMessage = document.createElement('p');
            aiMessage.classList.add('ai-message'); // Add a class to style AI messages differently
            var responseText = data.response.replace(/\./g, '.<br>').replace(/\:/g, ':<br>');
            aiMessage.innerHTML = responseText;

            // Create a new button element
            var speakButton = document.createElement('button');
            speakButton.innerText = 'Speak';

            // Add an event listener to the button that triggers the speech synthesis API
            speakButton.addEventListener('click', function () {
                // Creating a new SpeechSynthesisUtterance instance
                var utterance = new SpeechSynthesisUtterance(responseText.replace(/<br>/g, ' '));
                // Set the voice, rate, and pitch

                // Trigger the browser's speech synthesis API
                window.speechSynthesis.speak(utterance);
            });

            // Add the AI's message and the speak button to the conversation area
            conversationArea.appendChild(aiMessage);
            conversationArea.appendChild(speakButton);

        }).catch(error => console.error('Error:', error));;
});



// this function is used to create "enter" keypress listener so enter will work instead of clicking

document.getElementById("message-input").addEventListener("keypress", function (event) {
    if (event.key === 'Enter') {
        document.getElementById("send-button").click();
    }
});

//to keep the link highlited in the left-side bar for the lessons tiltle 

$(document).ready(function () {
    $('#sidebar ul li a').click(function () {
        $('#sidebar ul li a').removeClass('selected');
        $(this).addClass('selected');
    });
});

// colapsable vision-bot

// gpt-displlay collaped onload 
document.getElementById('gpt-display').style.transform = 'translateX(100%)';

// Flag to check if the initial message has been shown
let initialMessageShown = false;

document.getElementById('botFace').addEventListener('click', function () {
    var display = document.getElementById('gpt-display');

    // Check if the display is visible or hidden based on transform value
    if (display.style.transform == 'translateX(0%)' || display.style.transform == '') {
        // Hide the display using translateX
        display.style.transform = 'translateX(100%)';
        this.innerHTML = 'Show'; // Change the button text to "Show"
    } else {
        // Show the display using translateX
        display.style.transform = 'translateX(0%)';
        this.innerHTML = 'Hide'; // Change the button text back to "Hide"

        // Only show the initial message if it hasn't been shown yet
        if (!initialMessageShown) {
            setTimeout(function () {
                var aiMessage = document.createElement('p');
                aiMessage.classList.add('ai-message'); // Add a class to style AI messages differently
                aiMessage.innerHTML = 'سلام نام من ویژن هست استاد انګلسی شما چطور میتوانم کمک تان کنم..؟';

                // append the message to "Conv-Container"
                document.getElementById("Conv-Container").appendChild(aiMessage);

                // Mark that the initial message has been shown
                initialMessageShown = true;
            }, 1000); // 1000 milliseconds (or 1 second) delay
        }
    }
});


// toggle for nav bar for future use inshallah

// document.addEventListener("DOMContentLoaded", function () {

//     // Reference the menu toggle and the nav-menu
//     var menuToggle = document.querySelector(".menu-toggle");
//     var navMenu = document.querySelector(".nav-menu");

//     // Add a click event listener
//     menuToggle.addEventListener("click", function () {
//         if (navMenu.classList.contains("active")) {
//             navMenu.classList.remove("active");
//         } else {
//             navMenu.classList.add("active");
//         }
//     });

// });

// fetch the enrgyPoints function 
async function fetchEnergyPoints() {
    try {
        const response = await fetch('progress/get_energy_points/');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log("Energy Points:", data.energyPoint);
        return data.energyPoint;
    } catch (error) {
        console.error('There was a problem fetching the energy points:', error);
    }
}

// Fetch and update the energy points on page load
document.addEventListener("DOMContentLoaded", async function () {
    const energyPoints = await fetchEnergyPoints();
    document.getElementById("energyPointsValue").innerText = energyPoints;
})