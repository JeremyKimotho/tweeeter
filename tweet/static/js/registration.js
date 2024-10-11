const modal = new bootstrap.Modal(document.getElementById("signup-modal"))

htmx.on("htmx:afterSwap", (e) => {
  // Response targeting #dialog => show the modal
  if (e.detail.target.id == "dialog") {
    modal.show();
    console.log("Target locked");
  }
});

htmx.on("htmx:beforeSwap", (e) => {
  // Empty response targeting #dialog => hide the modal
  if (e.detail.target.id == "dialog" && !e.detail.xhr.response) {
    modal.hide();
    e.detail.shouldSwap = false;
    console.log("hidden");
    url = document.getElementById("modal-return").getAttribute('data-url');
    window.location.href=url;
    // console.log(url);
  }
});

htmx.on("hidden.bs.modal", () => {
  document.getElementById("dialog").innerHTML = "";
});