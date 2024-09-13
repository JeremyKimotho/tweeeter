const modal = new bootstrap.Modal(document.getElementById("modal"))
const form_textareas = document.querySelectorAll('.auto-expand');

console.log("I navbar.js was loaded in and is getting active ! ")

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

form_textareas.forEach(textarea => {
  textarea.addEventListener('input', function () {
        this.style.height = 'auto'; // Reset height
        this.style.height = `${this.scrollHeight}px`; // Set to scrollHeight
      }, true);
}, true);

// document.getElementById('pin-text-').addEventListener('click', function () {
  
//   var toastEl = document.getElementById('myToast');
//   var toast = new bootstrap.Toast(toastEl);
//   toast.show();
// });

// document