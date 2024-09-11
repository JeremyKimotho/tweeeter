const modal = new bootstrap.Modal(document.getElementById("modal"))
var comment_reply_text_info = document.getElementById("comment-modal-reply-info-div")

console.log("I navbar.js was loaded in and is getting active ! ")
comment_reply_text_info.style.display = "none";

htmx.on("htmx:afterSwap", (e) => {
  // Response targeting #dialog => show the modal
  if (e.detail.target.id == "dialog") {
    modal.show()

    const textareas = document.querySelectorAll('.auto-expand');

    console.log("Loading in listeners " + textareas.length)

    textareas.forEach(textarea => {
      textarea.addEventListener('input', function () {
        this.style.height = 'auto'; // Reset height
        this.style.height = `${this.scrollHeight}px`; // Set to scrollHeight
      });
    });
    
    console.log("Show the modal run")
  }
})

htmx.on("htmx:beforeSwap", (e) => {
  // Empty response targeting #dialog => hide the modal
  if (e.detail.target.id == "dialog" && !e.detail.xhr.response) {
    modal.hide()
    e.detail.shouldSwap = false
    console.log("Hide the modal run")
  }
})

htmx.on("hidden.bs.modal", () => {
  document.getElementById("dialog").innerHTML = ""
    console.log("Form clear run")
})
