const form = document.getElementById("form");
const statusMsg = document.getElementById("statusMessage");

form.addEventListener("submit", (e) => {
  statusMsg.textContent =
    "Arquivo enviado com sucesso! Esperando processamento...";
  statusMsg.classList.remove("d-none", "alert-danger");
  statusMsg.classList.add("alert-success");
});
