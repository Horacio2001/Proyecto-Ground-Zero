
    function confirmarEnvio() {
        let isFormFilled = true;
        const formFields = document.querySelectorAll('.formulario_contacto input, .formulario_contacto textarea');

        formFields.forEach(field => {
            if (field.value === '') {
                isFormFilled = false;
            }
        });

        if (!isFormFilled) {
            // Mostrar mensaje de error si no todos los campos están llenos
            Swal.fire({
                icon: 'error',
                title: 'Campos incompletos',
                text: 'Por favor, complete todos los campos antes de enviar.'
            });
            // Detener el envío del formulario
            return false;
        }

        // Mostrar confirmación antes de enviar el formulario
        Swal.fire({
            title: '¿Estás seguro?',
            text: '¿Deseas enviar el mensaje?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Sí, enviar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                // Aquí puedes hacer algo adicional si lo deseas antes de enviar el formulario
                // Por ejemplo, mostrar un mensaje de éxito
                Swal.fire({
                    title: 'Enviado!',
                    text: 'Tu mensaje ha sido enviado.',
                    icon: 'success'
                });

                // Finalmente, enviar el formulario
                document.querySelector('.formulario_contacto').submit();
            }
        });

        // Detener el envío del formulario por defecto
        return false;
    }







