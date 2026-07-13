document.getElementById('form-aumentar').addEventListener('submit', function(event) {
    event.preventDefault();

    const formulario = this;
    const url = formulario.action;
    const formData = new FormData(formulario);

    const cajaMensaje = document.getElementById('mensaje-js');

    fetch(url, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            cajaMensaje.style.display = 'block';
            cajaMensaje.style.backgroundColor = '#d4edda';
            cajaMensaje.style.color = '#155724';
            cajaMensaje.style.border = '1px solid #c3e6cb';
            cajaMensaje.textContent = `${data.message}. Nuevo stock: ${data.nuevo_stock}`;

            document.getElementById('nuevo_stock').value = '';

            setTimeout(() => {
                window.location.href = '/productos';
            }, 1500);

        } else {
            cajaMensaje.style.display = 'block';
            cajaMensaje.style.backgroundColor = '#f8d7da';
            cajaMensaje.style.color = '#721c24';
            cajaMensaje.style.border = '1px solid #f5c6cb';
            cajaMensaje.textContent = data.message;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        cajaMensaje.style.display = 'block';
        cajaMensaje.style.backgroundColor = '#f8d7da';
        cajaMensaje.style.color = '#721c24';
        cajaMensaje.textContent = 'Hubo un error de conexión con el servidor.';
    });
});