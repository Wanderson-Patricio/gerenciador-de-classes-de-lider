const tokenInput = document.getElementById("apiToken");
const toggleBtn = document.getElementById("toggleToken");
const tokenForm = document.getElementById("tokenForm");
const statusMsg = document.getElementById("statusMessage");

// 1. Lógica para mostrar/esconder o token
toggleBtn.addEventListener("click", () => {
  if (tokenInput.type === "password") {
    tokenInput.type = "text";
  } else {
    tokenInput.type = "password";
  }
});

// 2. Lógica para salvar no localStorage
tokenForm.addEventListener("submit", (e) => {
  e.preventDefault(); // Impede o recarregamento da página

  const tokenValue = tokenInput.value;

  // Salvando na chave solicitada
  localStorage.setItem("x-api-token", tokenValue);

  // Feedback visual para o usuário
  statusMsg.textContent = "Token salvo com sucesso no navegador!";
  statusMsg.classList.remove("d-none", "alert-danger");
  statusMsg.classList.add("alert-success");

  // Opcional: Limpar o campo após salvar
  // tokenInput.value = '';
});
