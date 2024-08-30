const comment_modal = new bootstrap.Modal(document.getElementById("comment-modal"));
const quote_modal = new bootstrap.Modal(document.getElementById("quote-modal"));

console.log("I homepage.js was loaded in and is getting active ! ")

htmx.on("htmx:afterSwap", (e) => {
  // Response targeting #comment => show the modal
  if (e.detail.target.id == "comment") {
    comment_modal.show()
  } else if (e.detail.target.id == "quote") {
    quote_modal.show()
  }
})

htmx.on("htmx:beforeSwap", (e) => {
  // Empty response targeting #comment => hide the modal
  if (e.detail.target.id == "comment" && !e.detail.xhr.response) {
    comment_modal.hide()
    e.detail.shouldSwap = false
  } else if (e.detail.target.id == "quote" && !e.detail.xhr.response) {
    quote_modal.hide()
    e.detail.shouldSwap = false
  }
})

htmx.on("hidden.bs.modal", () => {
  document.getElementById("comment").innerHTML = ""
  document.getElementById("quote").innerHTML = ""
})

let like_toggle = true;
let bookmark_toggle = true;
let repost_toggle = false;
var isDropdownVisible = false;

$('#comment_button').click(function() {
    var commentUrl = $(this).data('url');
    var postID = $(this).data('id');
    $.ajax({
        url: commentUrl,
        method: 'GET',
        success: function(response) {
            $('#post-comments-{{ postID }}').text(response.content);
        },
        error: function(xhr, status, error) {
            console.log("An error occurred: " + error);
        }
    });
});

// $('#toggleButton').click(function() {
//     if (isDropdownVisible) {
//         hideDropdown();
//     } else {
//         showDropdown();
//     }
//     isDropdownVisible = !isDropdownVisible; // Toggle the state
// });

// function showDropdown() {
//     $('#dropdownContent').slideDown();
// }

// function hideDropdown() {
//     $('#dropdownContent').slideUp();
// }

$('#repost_button').click(function() {
    if (repost_toggle) {
        var repostUrl = $(this).data('t-url');
        var repostText = "Unrepost";
    } else {
        var repostUrl = $(this).data('f-url');
        var repostText = "Repost";
    }
    repost_toggle = !repost_toggle;  // Switch the toggle flag

    $.ajax({
        url: repostUrl,
        method: 'GET',
        success: function(response) {
            $("#post-repost-dd").text(repostText)
            $('#post-reposts').text(response.total);
        },
        error: function(xhr, status, error) {
            console.log("An error occurred: " + error);
        }
    });

    hideDropdown();
    isDropdownVisible = false;
}); 



// $(document).click(function(event) {
//         if (!$(event.target).closest('.dropdown').length) {
//             if (isDropdownVisible) {
//                 hideDropdown();
//                 isDropdownVisible = false;
//             }
//         }
//     });



