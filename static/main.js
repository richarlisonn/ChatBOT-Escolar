document.getElementById('chat_form').addEventListener('submit', async function(event) {
  event.preventDefault();

  const input = document.getElementById('mensagem');
  const message = input.value.trim();

  if (message === "") {
      console.log("Campo de entrada vazio");
      return;
  }

  const chatContainer = document.getElementById('chat_container');
  
  // Mensagem do usuário
  const userMessage = document.createElement('div');
  userMessage.textContent = message;
  userMessage.classList.add('user-message');
  chatContainer.appendChild(userMessage);

  // Limpa o campo de entrada
  input.value = '';
  input.focus();

  // Adiciona o símbolo de carregamento
  const loadingMessage = document.createElement('div');
  loadingMessage.classList.add('loading-message');
  chatContainer.appendChild(loadingMessage);

  // Inicia a animação de carregamento
  let dots = 0;
  const loadingInterval = setInterval(() => {
      loadingMessage.textContent = ".".repeat(dots);
      dots = (dots + 1) % 4; // Faz os pontos variar de 0 a 3
  }, 500); // Altera a cada 500 ms

  // Envia a mensagem para o backend
  const response = await fetch("/", {
      method: 'POST',
      headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: new URLSearchParams({
          'prompt': message
      })
  });

  // Para a animação de carregamento
  clearInterval(loadingInterval);
  chatContainer.removeChild(loadingMessage);

  // Obtém a resposta da API
  const data = await response.json();

  // Adiciona a resposta do ChatGPT no chat
  const botMessage = document.createElement('div');
  botMessage.textContent = data.response;
  botMessage.classList.add('bot-message');
  chatContainer.appendChild(botMessage);

  // Desloca o scroll para o final
  chatContainer.scrollTop = chatContainer.scrollHeight;
});