function confirmarDelete(event, id_obra) {
    event.preventDefault(); // Prevenir la acción por defecto del enlace
    console.log("Eliminar ID:", id_obra); // Verifica el valor de ID en la consola
    Swal.fire({
        title: "¿Estás seguro que deseas eliminar?",
        text: "Estos cambios no se podrán revertir!",
        icon: "error",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Sí, eliminar!"
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire({
                title: "Eliminado!",
                text: "Empleado eliminado correctamente!",
                icon: "success"
            }).then(function () {
                // Redirigir a la URL de eliminación
                const deleteUrl = "/eliminar/" + id_obra + "/";
                console.log("Redirigiendo a:", deleteUrl); // Verifica la URL de redirección en la consola
                window.location.href = deleteUrl;
            });
        }
    });
}