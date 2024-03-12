// Add an event listener for the chatbot button
$("#openChatbotButton").click(function () {
  // Toggle the visibility of the chatbot window when the button is clicked
  $(".chat_window").toggle();
});

// Define a Message class constructor
function Message(arg) {
  this.text = arg.text;
  this.message_side = arg.message_side;
}

// Define the draw method for Message objects
Message.prototype.draw = function () {
  var $message = $($(".message_template").clone().html());
  $message.addClass(this.message_side).find(".text").html(this.text);
  $(".messages").append($message);
  // Add animation to show the message
  setTimeout(function () {
    $message.addClass("appeared");
  }, 0);
};

// Initialize chat interface when the page is loaded
$(function () {
  // Initialize message side for user messages
  var message_side = "right";

  // Function to get the message text from input field
  function getMessageText() {
    return $(".message_input").val();
  }

  // Function to send a message
  function sendMessage(text) {
    // If the message is empty, do nothing
    if (text.trim() === "") {
      return;
    }
    // Clear the input field after sending the message
    $(".message_input").val("");

    // Get reference to the messages container
    var $messages = $(".messages");

    // Create a new Message object for the user's message and draw it
    var userMessage = new Message({
      text: text,
      message_side: message_side,
    });
    userMessage.draw();

    // Send an asynchronous request to get the chatbot's response
    $.get("/get", { msg: text }).done(function (data) {
      // Create a new Message object for the chatbot's response and draw it
      var botMessage = new Message({
        text: data,
        message_side: "left",
      });
      botMessage.draw();
      // Scroll to the bottom of the messages container
      $messages.animate({ scrollTop: $messages.prop("scrollHeight") }, 300);
    });

    // Scroll to the bottom of the messages container
    $messages.animate({ scrollTop: $messages.prop("scrollHeight") }, 300);
  }

  // Event listener for clicking the send button
  $(".send_message").click(function (e) {
    sendMessage(getMessageText());
  });

  // Event listener for pressing Enter key in the input field
  $(".message_input").keyup(function (e) {
    if (e.which === 13) {
      sendMessage(getMessageText());
    }
  });

  // Display initial message from the chatbot
  var initialMessage = new Message({
    text: "How can I help you today?",
    message_side: "left",
  });
  initialMessage.draw();
});
