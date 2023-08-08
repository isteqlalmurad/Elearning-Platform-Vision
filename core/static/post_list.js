
const postLinks = document.querySelectorAll('.post-link');
const postContentDiv = document.querySelector('#post-content');

postLinks.forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        
        const postId = this.dataset.id;
        fetch(`/blog/api/posts/${postId}/`)
            .then(response => response.json())
            .then(data => {

                let mainContent = `<h2>${data.title}</h2>
                                   <pre>${data.content}<pre>`;
                // this funciton is created to send the post content to back-end django server 
                fetch('api/divcontent/?content=' + encodeURIComponent(mainContent))

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

                let footerContent = `<p>Author: ${data.author.username}</p>
                                     <p>Date: ${data.date_posted}</p>`;

                let completeContent = mainContent + videoContent + footerContent;

                postContentDiv.innerHTML = completeContent;
            });
    });
});


document.getElementById("send-button").addEventListener("click", function(){
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
            speakButton.addEventListener('click', function() {
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

document.getElementById("message-input").addEventListener("keypress", function(event){
    if(event.key === 'Enter'){
        document.getElementById("send-button").click();
    }
});

//to keep the link highlited in the left-side bar for the lessons tiltle 

$(document).ready(function() {
    $('#sidebar ul li a').click(function() {
        $('#sidebar ul li a').removeClass('selected');
        $(this).addClass('selected');
    });
});






