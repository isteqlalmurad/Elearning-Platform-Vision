const postLinks = document.querySelectorAll('.post-link');
const postContentDiv = document.querySelector('#post-content');
var modal = document.getElementById("myModal");


// keep post current post Id global in the function, needs to be changed latter it can interfere with different users (will assign it to user session)
let currentPostId = null;

async function checkAndUnlockLink(link, postId) {
    let energyPoint = await fetchEnergyPoints();
    let requiredEnergyPoint = (postId - 1) * 3;

    if (postId == 1 || energyPoint >= requiredEnergyPoint) {
        link.innerHTML = link.innerHTML.replace("🔒 ", "");
    } else {
        link.innerHTML = "🔒 " + link.innerHTML;
    }
}


postLinks.forEach(link => {
    let postId = link.dataset.id;

    checkAndUnlockLink(link, postId);

    link.addEventListener('click', async function (e) {
        e.preventDefault();

        let energyPoint = await fetchEnergyPoints();
        currentPostId = this.dataset.id;
        const requiredEnergyPoint = (currentPostId - 1) * 3;

        if (currentPostId == 1) {
            loadPostContent(currentPostId);
        } else if (energyPoint >= requiredEnergyPoint) {
            loadPostContent(currentPostId);
        } else {
            alert("Content is locked! Earn more energy points to unlock this lesson.");
            return;
        }
    });
});



function loadPostContent(PostId) {
    currentPostId = PostId;  // Update the global variable
    fetch(`/blog/api/posts/${currentPostId}/`)
        .then(response => response.json())
        .then(data => {
            let mainContent = `
                <pre><h2>${data.title}</h2>
                <pre>${data.content}</pre>`; //pre is used to keep the original formating of the database without changes to keep spaces and new lines intact 

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

        // don't show the the move next btn at first
        var moveNextButton = document.getElementById('move_next')
        moveNextButton.style.display = 'none';
        fetchEnergyPoints().then(energyPoint => {

            console.log("Energy Points in Next lesson btn:", energyPoint);
            console.log("this post ID  in Next lesson btn::", currentPostId);

            requiredEnergyPoint = (currentPostId) * 3;

            if (energyPoint > requiredEnergyPoint) {
                // var moveNextButton = document.getElementById('move_next')
                moveNextButton.style.display = 'block';
            }

        });


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
//  Event delegation for modal close functionality 
document.body.addEventListener('click', function (event) {
    if (event.target.classList.contains('close')) {

        modal.style.display = "none";
        clearSession();
    }
});


//  Event delegation for check question event listener /
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
        /////////////////////////////////////////////////////////////////////////////////////////////////////////////
        fetchEnergyPoints().then(energyPoint => {

            // debuging checks 
            console.log("Energy Points: aa", energyPoint);
            console.log("this post ID: aa", currentPostId);
            console.log(typeof currentPostId);

            // currentPostId = parseInt(currentPostId, 10);


            requiredEnergyPoint = parseInt(currentPostId) * 3;

            if (energyPoint >= requiredEnergyPoint) {

                var moveNextButton = document.getElementById('move_next')
                moveNextButton.style.display = 'block';
            }

        });

    }
});

/////////////////////////////////////////////////////////////////////////link to move to the next lesson
document.getElementById("move_next").addEventListener("click", myFunction);


function myFunction() {
    console.log("move_next clicked");
    let nextId = parseInt(currentPostId) + 1; // Ensure the currentPostId is an integer

    // This will simulate the energy point checking and content loading as done by the sidebar link click
    fetchEnergyPoints().then(energyPoint => {

        const requiredEnergyPoint = (nextId - 1) * 3;

        if (energyPoint >= requiredEnergyPoint) {

            const nextLink = document.querySelector(`.post-link[data-id="${nextId}"]`);
            if (nextLink) {
                nextLink.innerHTML = nextLink.innerHTML.replace("🔒 ", "");
            }
            loadPostContent(nextId);

            fetch('progress/generate_progress_report/')
                .then(response => response.json())
                .then(data => {
                    console.log(data.message);
                    // Once the data has been fetched and processed, clear the session
                });

        }
    });
    setTimeout(() => {
        clearSession();
    }, 5000);
    modal.style.display = "none";


}




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

                // utterance.voice = voices[1];

                // // Set the rate of speech (1.0 is the default, range is 0.1 to 10)
                // utterance.rate = 1.0;

                // // Set the pitch (1.0 is the default, range is 0 to 2)
                // utterance.pitch = 1.0;

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
document.getElementById('gpt-display').style.transform = 'translateX(100%)';
let initialMessageShown = false;

document.getElementById('botFace').addEventListener('click', function () {
    var display = document.getElementById('gpt-display');
    var botFace = this;

    if (display.style.transform == 'translateX(0%)' || display.style.transform == '') {
        // Hide the gpt-display
        display.style.transform = 'translateX(100%)';

        // Move botFace back to its original position (right 10px)
        botFace.style.transform = 'translateX(0)';
        // this.innerHTML = 'Show'; // Change the button text to "Show"

    } else {
        // Show the gpt-display
        display.style.transform = 'translateX(0%)';

        // Move botFace to the left by the width of gpt-display plus some padding for separation
        var botFaceMoveAmount = '-' + (display.clientWidth + 20) + 'px'; // +20 for some space between them
        botFace.style.transform = 'translateX(' + botFaceMoveAmount + ')';


        // intianl welcoming message by vision bot, Only shows the initial message if it hasn't been shown yet
        if (!initialMessageShown) {
            setTimeout(function () {
                var aiMessage = document.createElement('p');
                aiMessage.classList.add('ai-message'); // Add a class to style AI messages differently
                aiMessage.innerHTML = 'سلام نام من ویژن هست استاد انګلسی شما چطور میتوانم کمک تان کنم..؟';

                // append the message to "Conv-Container"
                document.getElementById("Conv-Container").appendChild(aiMessage);

                // Mark that the initial message has been shown
                initialMessageShown = true;
            }, 1000); // 1000 milliseconds (or 1 second) delayi in showing the message 
        }
    }
});





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